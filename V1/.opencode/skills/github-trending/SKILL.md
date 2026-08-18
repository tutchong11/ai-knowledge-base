---
name: github-trending
description: 当需要采集 GitHub 热门开源项目时使用此技能
allowed-tools: Read, Grep, Glob, WebFetch
---

# GitHub Trending 采集技能

## 使用场景

当需要采集 GitHub 热门开源项目、追踪技术社区动态、为知识库补充项目数据时使用此技能。

## 执行步骤

1. **搜索热门仓库**：通过 GitHub API 搜索当前热门开源仓库。
2. **提取信息**：提取每个仓库的名称、描述、Star 数、语言、Topics 等关键信息。
3. **过滤**：仅保留 AI / LLM / Agent 相关项目，排除 Awesome 列表等聚合类仓库。
4. **去重**：与 `knowledge/raw/` 及 `knowledge/articles/` 中已有记录比对，去除重复项目。
5. **撰写中文摘要**：按公式「项目名 + 做什么 + 为什么值得关注」撰写中文摘要。
6. **排序取 Top15**：按 Star 数与相关度排序，取前 15 个项目。
7. **输出 JSON**：将结果写入 `knowledge/raw/github-trending-YYYY-MM-DD.json`。

## 注意事项

- 使用 GitHub API 时注意速率限制，必要时使用 Token。
- 摘要使用中文，技术术语保留英文原文。
- 不编造不存在的项目或数据。

## 输出格式

```json
{
  "source": "github-trending",
  "skill": "github-trending",
  "collected_at": "YYYY-MM-DDTHH:MM:SSZ",
  "items": [
    {
      "name": "项目名",
      "url": "https://github.com/owner/repo",
      "summary": "一句话中文摘要",
      "stars": 0,
      "language": "Python",
      "topics": ["topic1", "topic2"]
    }
  ]
}
```
