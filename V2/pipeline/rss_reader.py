"""
pipeline/rss_reader.py — RSS 数据源采集模块

支持从任意 RSS 源采集内容，配置文件见 pipeline/rss_sources.yaml。

用法:
    # 作为模块被 pipeline.py 导入
    from pipeline.rss_reader import collect_rss
    items = collect_rss(limit=10)

    # 独立运行（调试）
    python3 -m pipeline.rss_reader
    python3 -m pipeline.rss_reader --limit 5
"""

from __future__ import annotations

import html
import logging
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx
import yaml

logger = logging.getLogger(__name__)

# RSS 配置文件与 pipeline.py 共享同一份
RSS_CONFIG = Path(__file__).parent / "rss_sources.yaml"

# ── 解析用正则 ────────────────────────────────────────────────────────────

# RSS 2.0 条目块
ITEM_RE = re.compile(r"<item[^>]*>(.*?)</item>", re.DOTALL)
# Atom 条目块
ENTRY_RE = re.compile(r"<entry[^>]*>(.*?)</entry>", re.DOTALL)

# 标题（兼容 CDATA 与 type 属性）
TITLE_RE = re.compile(
    r"<title[^>]*>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>",
    re.DOTALL,
)
# Atom 首选 rel="alternate" 的链接
LINK_ALT_RE = re.compile(
    r"""<link[^>]*?rel=["']alternate["'][^>]*?href=["']([^"']+)["']""",
    re.DOTALL,
)
# Atom 任意 href 属性链接
LINK_ATTR_RE = re.compile(r"""<link[^>]*?href=["']([^"']+)["']""", re.DOTALL)
# RSS 2.0 文本形式链接
LINK_TEXT_RE = re.compile(r"<link[^>]*>\s*(.*?)\s*</link>", re.DOTALL)


def _strip_tags(text: str) -> str:
    """反转义 HTML 实体并去除文本中的 HTML 标签。"""
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", "", text)
    return text.strip()


def _parse_feed_entries(feed_text: str) -> list[tuple[str, str]]:
    """解析 RSS 2.0（<item>）与 Atom（<entry>）两种格式，返回 (title, link) 列表。"""
    blocks = ITEM_RE.findall(feed_text)
    blocks += ENTRY_RE.findall(feed_text)

    entries: list[tuple[str, str]] = []
    for block in blocks:
        title_match = TITLE_RE.search(block)
        if not title_match:
            continue
        title = _strip_tags(title_match.group(1))
        if not title:
            continue

        link = ""
        alt_match = LINK_ALT_RE.search(block)
        attr_match = LINK_ATTR_RE.search(block)
        text_match = LINK_TEXT_RE.search(block)
        if alt_match:
            link = alt_match.group(1)
        elif attr_match:
            link = attr_match.group(1)
        elif text_match:
            link = text_match.group(1)
        link = _strip_tags(link)
        if not link:
            continue

        entries.append((title, link))

    return entries


def collect_rss(limit: int = 10) -> list[dict[str, Any]]:
    """
    从配置的 RSS 源采集内容。

    Args:
        limit: 每个源的最大采集数量

    Returns:
        原始数据列表，每条包含 id/title/source/source_url/... 字段
    """
    if not RSS_CONFIG.exists():
        logger.warning("RSS 配置文件不存在: %s", RSS_CONFIG)
        return []

    with open(RSS_CONFIG, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    sources = [s for s in config.get("sources", []) if s.get("enabled", True)]
    results: list[dict[str, Any]] = []
    global_count = 0

    with httpx.Client(timeout=10.0) as client:
        for source in sources:
            try:
                resp = client.get(source["url"])
                resp.raise_for_status()
                feed_text = resp.text

                entries = _parse_feed_entries(feed_text)

                source_count = 0
                for title, link in entries:
                    if source_count >= limit:
                        break

                    now = datetime.now(timezone.utc).isoformat()
                    global_count += 1
                    source_count += 1
                    results.append({
                        "id": f"rss-{datetime.now().strftime('%Y%m%d')}-{global_count:03d}",
                        "title": title,
                        "source": f"rss:{source['name']}",
                        "source_url": link,
                        "author": source.get("name", "unknown"),
                        "published_at": now,
                        "raw_description": "",
                        "category": source.get("category", "general"),
                        "collected_at": now,
                    })

                logger.info("RSS [%s] 采集: %d 条", source["name"], source_count)

            except httpx.HTTPError as e:
                logger.warning("RSS 源 [%s] 获取失败: %s", source["name"], e)

    logger.info("RSS 采集完成: 共 %d 条", len(results))
    return results


# ── 独立调试入口 ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    import json

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    parser = argparse.ArgumentParser(description="RSS 数据源采集调试入口")
    parser.add_argument("--limit", type=int, default=10, help="每个源的最大采集条数")
    parser.add_argument("--output", type=str, default="", help="保存到 JSON 文件（可选）")
    args = parser.parse_args()

    items = collect_rss(limit=args.limit)
    print(f"\n采集到 {len(items)} 条 RSS 条目")
    for i, item in enumerate(items[:5], 1):
        print(f"  {i}. [{item['source']}] {item['title'][:60]}")
    if len(items) > 5:
        print(f"  ... 还有 {len(items) - 5} 条")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        print(f"\n已保存到: {args.output}")
