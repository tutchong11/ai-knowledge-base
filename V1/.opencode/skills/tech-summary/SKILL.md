---
name: tech-summary
description: 当需要对采集的技术内容进行深度分析总结时使用此技能
allowed-tools: Read, Grep, Glob, WebFetch
---

# 技术深度分析总结技能

## 使用场景

当需要对已采集的技术内容进行深度分析、价值评估与趋势洞察时使用此技能。

## 执行步骤

1. **读取最新采集文件**：读取 `knowledge/raw/` 目录下最新的采集文件。
2. **逐条深度分析**：对每条内容进行分析，包含：
   - 摘要（不超过 50 字）
   - 技术亮点 2-3 个（用事实说话）
   - 评分 1-10（附理由）
   - 标签建议
3. **趋势发现**：归纳共同主题与新概念。
4. **输出分析结果 JSON**：将分析结果写入结构化 JSON 文件。

## 评分标准

| 评分 | 含义     |
| ---- | -------- |
| 9-10 | 改变格局 |
| 7-8  | 直接有帮助 |
| 5-6  | 值得了解 |
| 1-4  | 可略过   |

## 注意事项

- 摘要使用中文，技术术语保留英文原文。
- 技术亮点必须基于事实，不编造数据。
- 约束：15 个项目中 9-10 分不超过 2 个。
- 评分需附理由。

## 输出格式

```json
{
  "source": "github-trending",
  "skill": "tech-summary",
  "analyzed_at": "YYYY-MM-DDTHH:MM:SSZ",
  "trends": ["共同主题", "新概念"],
  "items": [
    {
      "name": "项目名",
      "url": "https://github.com/owner/repo",
      "summary": "不超过 50 字的中文摘要",
      "tech_highlights": ["亮点1", "亮点2", "亮点3"],
      "relevance_score": 8,
      "score_reason": "评分理由",
      "tags": ["tag1", "tag2"]
    }
  ]
}
```
