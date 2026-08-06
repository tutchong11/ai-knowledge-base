import logging
from typing import Optional, TypedDict

import requests


logger = logging.getLogger(__name__)


class RepoInfo(TypedDict):
    """GitHub 仓库基本信息。"""

    full_name: str
    stars: int
    forks: int
    description: Optional[str]


def get_repo_info(owner: str, repo: str, token: Optional[str] = None) -> Optional[RepoInfo]:
    """从 GitHub API 获取指定仓库的基本信息。

    Args:
        owner: 仓库所有者。
        repo: 仓库名称。
        token: GitHub Personal Access Token，提供后可提升 API 速率限制。

    Returns:
        RepoInfo 字典，包含 stars、forks、description；请求失败时返回 None。

    Raises:
        ValueError: owner 或 repo 为空时抛出。
    """
    if not owner or not repo:
        raise ValueError("owner 和 repo 不能为空")

    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        logger.error("请求 GitHub API 失败: %s/%s, 错误: %s", owner, repo, e)
        return None

    data = resp.json()

    return {
        "full_name": data.get("full_name", f"{owner}/{repo}"),
        "stars": data.get("stargazers_count", 0),
        "forks": data.get("forks_count", 0),
        "description": data.get("description"),
    }
