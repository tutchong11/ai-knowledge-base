# AGENTS.md — AI 知识库助手项目规范

## 项目概述
个人 AI 知识库助手系统（v0.1）。每天自动抓取 GitHub Trending 日榜 Top 25，
由 Agent 判断 AI 相关性并深度分析，输出结构化 JSON + Obsidian 兼容 Markdown 双格式。
定位为"能学到什么"，而非新闻简报。

## 技术栈
- 语言: Python 3.12
- AI 编排: OpenCode + 国产大模型（DeepSeek/Qwen/GLM/Kimi）
- 工作流: LangGraph（第 3 周引入）
- 部署: OpenClaw（第 4 周引入）
- 阅读: Obsidian（Markdown 含 YAML Frontmatter + 双链支持）
- 依赖管理: pip + requirements.txt
- 版本控制: Git

## 编码规范
- 遵循 PEP 8 规范
- 变量命名: snake_case
- 类名: PascalCase
- 所有函数必须有 docstring（Google 风格）
- 禁止裸 print()，使用 logging 或写入文件
- 禁止 import *
- 文件编码统一 UTF-8

## 项目结构

ai-knowledge-base/
├── AGENTS.md                  — 项目规范（本文件）
├── opencode.json              — OpenCode 配置
├── .opencode/
│   ├── agents/                — Agent 角色定义文件
│   │   ├── collector.md
│   │   ├── analyzer.md
│   │   └── organizer.md
│   └── skills/                — 可复用技能包
│       ├── github-trending/SKILL.md
│       └── tech-summary/SKILL.md
├── knowledge/
│   ├── raw/                   — 原始采集数据（JSON）
│   └── articles/              — 结构化知识条目（JSON + Markdown）
├── pipeline/                  — 自动化流水线（Week 2）
├── workflows/                 — LangGraph 工作流（Week 3）
└── openclaw/                  — OpenClaw 部署配置（Week 4）

## 内容规范
- 摘要语言: 中文
- 摘要长度: 不超过 100 字
- 技术术语保留英文原文（如 LangGraph、Agent、Token）
- 分析定位: 关注"能学到什么"，不做新闻简报
- 采集策略: 全语言不预筛，由 Agent 判断 AI 相关性
- Tags 为自由标签数组（如 LLM、RAG、Agent、Infra）

## 分析维度

每条知识条目需覆盖以下 5 个分析维度：

| 维度       | 说明                               |
| ---------- | ---------------------------------- |
| problem    | 项目解决的问题                     |
| tech_points| 核心技术点                         |
| use_cases  | 适用场景                           |
| ai_connection | 与 AI 的关联                    |
| takeaway   | 一句话 Takeaway（有收获感）        |

## 知识条目格式

### JSON 格式（存储在 `knowledge/articles/`）

```json
{
  "id": "2026-03-01-openclaw",
  "name": "OpenClaw",
  "owner": "openclaw",
  "url": "https://github.com/openclaw/openclaw",
  "source": "github-trending",
  "language": "Python",
  "stars": 1234,
  "date": "2026-03-01",
  "aliases": ["OpenClaw"],
  "ai_relevant": true,
  "tags": ["agent", "runtime", "open-source"],
  "problem": "AI Agent 缺少统一的运行环境和多平台部署方案",
  "tech_points": ["多 Agent 路由", "50+ 平台支持", "插件化架构"],
  "use_cases": ["企业内部 Agent 部署", "跨平台 AI 应用发布"],
  "ai_connection": "直接为 AI Agent 提供运行时基础设施",
  "takeaway": "OpenClaw 提供开箱即用的 Agent 运行时，降低 Agent 应用的生产部署门槛"
}
```

### Markdown 格式（YAML Frontmatter，兼容 Obsidian）

```markdown
---
id: "2026-03-01-openclaw"
tags: [agent, runtime, open-source]
aliases: [OpenClaw]
source: "github-trending"
url: "https://github.com/openclaw/openclaw"
language: "Python"
stars: 1234
date: "2026-03-01"
---

# OpenClaw

**一句话 Takeaway**: OpenClaw 提供开箱即用的 Agent 运行时，降低 Agent 应用的生产部署门槛

## 解决的问题
AI Agent 缺少统一的运行环境和多平台部署方案

## 核心技术点
- 多 Agent 路由
- 50+ 平台支持
- 插件化架构

## 适用场景
- 企业内部 Agent 部署
- 跨平台 AI 应用发布

## 与 AI 的关联
直接为 AI Agent 提供运行时基础设施

## 相关链接
- [[OpenClaw]] — 项目主页
```

**必填字段**：id, name, url, source, date, tags, ai_relevant
**ai_relevant**：Agent 判断该项目是否与 AI 相关（true/false），不相关的条目可跳过深度分析

## Agent 角色概览

| 角色       | 文件                          | 职责                                   |
| ---------- | ----------------------------- | -------------------------------------- |
| 采集 Agent | .opencode/agents/collector.md | 从 GitHub Trending 抓取 Top 25 日榜    |
| 分析 Agent | .opencode/agents/analyzer.md  | 判断 AI 相关性，5 维度深度分析          |
| 整理 Agent | .opencode/agents/organizer.md | 生成 JSON + Markdown 双输出，校验入库  |

## 边界与验收

### 硬性约束
- 全流程 ≤ 5 分钟
- 单日 Markdown 总大小 ≤ 200KB
- 每天固定 25 条（Top 25），不做增量/流式更新

### 数据源
- v0.1 仅 GitHub Trending（全语言，不预筛）
- 数据层预留多源扩展能力，后续支持 Hacker News 等

### 验收标准
| 等级 | 标准                                                                 |
| ---- | -------------------------------------------------------------------- |
| 及格 | 每天自动抓取 25 条 → Agent 分析 → 输出 JSON + Markdown，全程无人介入 |
| 良好 | tags 准确、takeaway 有信息量，无需人工修改                           |
| 优秀 | 多数据源扩展，80%+ 入库来自自动抓取                                  |

### 验证方式
- **自动化校验**: 每次运行后检查文件存在、JSON 合法、字段齐全、数量 = 25、tags 非空
- **人工抽检**: 每周随机 5 条，评估 takeaway 是否"有收获感"
- **Obsidian 验收**: 新版本部署时确认 tags 面板、双链、文件列表正常

## 不做什么（v0.1）

- 不做代码搜索引擎（不索引源码、不分析代码质量）
- 不做个性化推荐（无用户系统、无推荐算法）
- 不做实时/增量抓取（每天一批 digest）
- 不做多数据源（v0.1 仅 GitHub Trending）
- 不做项目对比/评测（条目独立，不横向比较）
- 不做 UI / 前端（纯 pipeline，本地 Obsidian 阅读）

## 红线（绝对禁止）

- 不编造不存在的项目或数据
- 不在日志中输出 API Key 或敏感信息
- 不执行 rm -rf 等危险命令
- 不修改 AGENTS.md 本身（除非明确要求）
