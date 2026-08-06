# AI 知识库 · 项目愿景 v0.1

## 要做什么
- 每天抓取 GitHub Trending 日榜 top 25（全语言，不预筛，由 Agent 判断 AI 相关性）
- 用 Agent 分析内容
  - 维度：解决的问题 / 核心技术点 / 适用场景 / 与 AI 的关联 / 一句话 Takeaway
  - 定位：关注"能学到什么"，而非新闻简报
- 输出知识条目：JSON（结构化存储）+ Markdown（人类阅读）双输出
  - Markdown 含 YAML Frontmatter，兼容 Obsidian（tags / aliases / 双链）
  - JSON 字段：id / name / owner / url / source / language / stars / date / aliases
  - 分析字段：ai_relevant / tags / problem / tech_points / use_cases / ai_connection / takeaway
  - tags 为自由标签数组（如 LLM、RAG、Agent、Infra）；aliases 支持 Obsidian [[双链]]

## 不做什么
- 不做代码搜索引擎（不索引源码、不分析代码质量）
- 不做个性化推荐（无用户系统、无推荐算法）
- 不做实时/增量抓取（每天一批 digest，不做流式更新）
- v0.1 不做多数据源（仅 GitHub Trending，但数据层预留多源扩展能力）
- 不做项目对比/评测（条目独立，不横向比较）
- 不做 UI / 前端（纯 pipeline，本地 Obsidian 内阅读）



## 边界 & 验收
- 及格：每天自动抓取 25 条 → Agent 分析 → 输出 JSON + Markdown，全程无人介入
- 良好：tags 准确、takeaway 有信息量，无需人工修改
- 优秀：多数据源扩展，80%+ 入库来自自动抓取
- 硬性约束：全流程 ≤ 5 分钟，单日 Markdown ≤ 200KB



## 怎么验证
- 自动化：每次运行后脚本校验（文件存在、JSON 合法、字段齐全、数量 = 25、tags 非空）
- 人工抽检：每周随机 5 条，评估 takeaway 是否"有收获感"
- Obsidian 验收：新版本部署时确认 tags 面板、双链、文件列表正常
