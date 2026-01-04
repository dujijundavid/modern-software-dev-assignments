# Claude Best Practices

> 深入理解 Claude Code 和 SuperClaude 的最佳实践集合

这个文件夹包含了系统化的学习和参考材料，帮助你更好地掌握 AI 辅助编程。

---

## 新增/更新（人工维护，最近 5 条）
- 2026-01-05 `KNOWLEDGE_INDEX.md`：同步文件计数、日期与节省率说明
- 2026-01-05 `01-setup/claude-code-architecture.md`：新增受众说明与下一步阅读
- 2026-01-05 `02-understand/superclaude-architecture.md`：补充编排/路由视角与互链
- 2026-01-05 `05-learning_mode_design/commands-vs-skills.md`：命令 vs Skills 决策对比
- 2026-01-05 `04-deep-dive/prompt-layer-design.md`：4 层 Prompt 设计框架收录

---

## 快速导航

### 我想配置项目 → [01-setup/](01-setup/)
| 文件 | 适用场景 + 关键输出 |
|------|--------------------|
| [PROJECT_INDEX 使用指南](01-setup/project-index-usage.md) | 初次为项目建索引，拿到 94% token 节省的创建/更新流程 |
| [CLAUDE.md 最佳实践](01-setup/claude-md-best-practices.md) | 需要统一 AI 行为时，产出团队化 CLAUDE.md 模板与校验清单 |
| [Skills 系统完全指南](01-setup/skills-system-guide.md) | 扩展/安装 Skills 前阅读，明确目录结构、触发机制与发布方式 |
| [Claude Code 架构指南](01-setup/claude-code-architecture.md) | 想速览四层体系（Skills/Commands/Subagents/Super Claude），拿到职责边界与调用链 |

---

### 我想理解系统 → [02-understand/](02-understand/)
| 文件 | 适用场景 + 关键输出 |
|------|--------------------|
| [子代理系统架构](02-understand/subagent-system.md) | 需要设计/挑选子代理时，拿到并行与角色分离的设计框架 |
| [SuperClaude 架构](02-understand/superclaude-architecture.md) | 想理解路由/编排层工作方式，获得命令体系与子代理调度视图 |
| [AI 工程核心原则](02-understand/ai-engineering-principles.md) | 做决策前量化 ROI/Token，附典型节省算例 |
| [TDD SubAgents 第一性原理](02-understand/tdd-first-principles.md) | 推行 TDD 协作时，得到 TestAgent/CodeAgent 分离的理由与交接格式 |

---

### 我想创建/开发 → [03-create/](03-create/)
| 文件 | 适用场景 + 关键输出 |
|------|--------------------|
| [Skill 设计最佳实践](03-create/skill-design-best-practices.md) | 要发布/分享技能时，拿到命名、结构、校验清单与打包指引 |
| [Document Skills 使用指南](03-create/document-skills-guide.md) | 处理 docx/pptx/pdf/xlsx 等文档时，快速获取调用示例与限制 |

---

### 我想深入学习 → [04-deep-dive/](04-deep-dive/)
| 文件 | 适用场景 + 关键输出 |
|------|--------------------|
| [/sc:pm 深度解析](04-deep-dive/sc-pm-explained.md) | 使用/二次开发 PM Agent 时，拿到路由、记忆与校验流程 |
| [/sc:index-repo 深度分析](04-deep-dive/index-repo-analysis.md) | 优化索引/Prompt 时，看到 prompt 拆解与 token 策略 |
| [Context7 MCP 完全指南](04-deep-dive/context7-mcp-guide.md) | 需要最新库文档检索时，掌握 Context7 工具用法与坑位 |
| [100+ 学习 prompts](04-deep-dive/learning-prompts-collection.md) | 练习/教学时，直接套用 8 主题 100+ Prompt |
| [Prompt 4 层设计](04-deep-dive/prompt-layer-design.md) | 设计高稳定度 Prompt 时，套用 Persona/Process/Output/Validation 模型 |

---

### 我想设计学习模式 → [05-learning_mode_design/](05-learning_mode_design/)
| 文件 | 适用场景 + 关键输出 |
|------|--------------------|
| [Commands vs Skills 对比](05-learning_mode_design/commands-vs-skills.md) | 需要在命令/Skill 间做决策时，快速对比触发、共享、版本与命名策略 |

---

### 我想分析需求/策略 → [06-analysis-tools/](06-analysis-tools/)
| 文件 | 适用场景 + 关键输出 |
|------|--------------------|
| [sc-brainstorm-guide.md](06-analysis-tools/sc-brainstorm-guide.md) | 需求挖掘时，使用 `/sc:brainstorm` 的问诊流程与输出模板 |
| [business-panel-guide.md](06-analysis-tools/business-panel-guide.md) | 商业/战略分析时，调用多专家 Panel 的提纲与校验表 |
| [目录总览](06-analysis-tools/README.md) | 想知道工具全景时，一眼看到可用命令与入门链接 |

---

### 我想掌握 Serena → [serena-mcp/](serena-mcp/)
| 文件 | 适用场景 + 关键输出 |
|------|--------------------|
| [README.md](serena-mcp/README.md) | 需要快速了解 Serena 时的 10 分钟上手 |
| [01-architecture-overview.md](serena-mcp/01-architecture-overview.md) | 评估组件/边界时的架构总览 |
| [02-configuration-guide.md](serena-mcp/02-configuration-guide.md) | 配置 project.yml、启动 server 时的参数参考 |
| [03-memory-system-design.md](serena-mcp/03-memory-system-design.md) | 设计记忆命名空间与持久化策略的模板 |
| [04-cross-machine-sync.md](serena-mcp/04-cross-machine-sync.md) | 多设备/多人协作时的 Git 同步与忽略策略 |
| [05-advanced-patterns.md](serena-mcp/05-advanced-patterns.md) | 需要高级 MCP 集成/模式时的案例与步骤 |

---

## 文件夹结构

```
claude-best-practices/
├── README.md                      # 本文件
│
├── 01-setup/                      # 【我要配置项目】
│   ├── project-index-usage.md
│   ├── claude-md-best-practices.md
│   ├── claude-code-architecture.md
│   └── skills-system-guide.md
│
├── 02-understand/                 # 【我要理解系统】
│   ├── subagent-system.md
│   ├── superclaude-architecture.md
│   ├── ai-engineering-principles.md
│   └── tdd-first-principles.md
│
├── 03-create/                     # 【我要创建/开发】
│   ├── skill-design-best-practices.md
│   └── document-skills-guide.md
│
├── 04-deep-dive/                  # 【我要深入学习】
│   ├── sc-pm-explained.md
│   ├── index-repo-analysis.md
│   ├── context7-mcp-guide.md
│   ├── prompt-layer-design.md
│   └── learning-prompts-collection.md
│
├── 05-learning_mode_design/       # 【我要设计学习模式】
│   └── commands-vs-skills.md
│
├── 06-analysis-tools/             # 【我要分析需求/策略】
│   ├── sc-brainstorm-guide.md
│   ├── business-panel-guide.md
│   └── README.md
│
└── serena-mcp/                    # 【Serena MCP 系统】
    ├── README.md
    ├── 01-architecture-overview.md
    ├── 02-configuration-guide.md
    ├── 03-memory-system-design.md
    ├── 04-cross-machine-sync.md
    └── 05-advanced-patterns.md
```

---

## 学习路径

### Day 1-3: 配置项目
1. [PROJECT_INDEX 使用指南](01-setup/project-index-usage.md) - 94% token 节省
2. [CLAUDE.md 最佳实践](01-setup/claude-md-best-practices.md) - 定义 AI 行为
3. [Skills 系统指南](01-setup/skills-system-guide.md) - 扩展 AI 能力

### Day 4-7: 理解系统
1. [子代理系统](02-understand/subagent-system.md) - 专业化与委托
2. [SuperClaude 架构](02-understand/superclaude-architecture.md) - 整体架构
3. [AI 工程原则](02-understand/ai-engineering-principles.md) - ROI 和 Token 优化

### Day 8-10: 创建能力
1. [Skill 设计最佳实践](03-create/skill-design-best-practices.md) - 创建自定义技能
2. [Document Skills 指南](03-create/document-skills-guide.md) - 使用文档技能

### Day 11-14: 掌握分析工具
1. [/sc:brainstorm 需求发现](06-analysis-tools/sc-brainstorm-guide.md) - 交互式需求发现
2. [/sc:business-panel 商业分析](06-analysis-tools/business-panel-guide.md) - 多专家分析系统

### Day 15+: 深入学习
1. [/sc:pm 深度解析](04-deep-dive/sc-pm-explained.md) - 项目管理代理
2. [/sc:index-repo 分析](04-deep-dive/index-repo-analysis.md) - Prompt Engineering 深度分析
3. [Serena 高级模式](serena-mcp/05-advanced-patterns.md) - MCP 工具集成
4. [学习 prompts 实践](04-deep-dive/learning-prompts-collection.md) - 100+ 实践 prompts

### Day 16+: 掌握 Serena（可选）
1. [Serena 架构概览](serena-mcp/01-architecture-overview.md) - 理解系统架构
2. [Serena 配置指南](serena-mcp/02-configuration-guide.md) - 配置 project.yml
3. [内存系统设计](serena-mcp/03-memory-system-design.md) - 组织项目记忆

---

## 核心概念速查

### Prompt Engineering 4 层模型

| 层级 | 内容 | 验证方法 |
|------|------|----------|
| Layer 1 | Persona: "你是一个..." | AI 是否表现出预期行为？ |
| Layer 2 | Process: Phase 1 → 2 → 3 | AI 是否按步骤执行？ |
| Layer 3 | Output: {field} 模板 | 输出是否符合模板？ |
| Layer 4 | Validation: [ ] 检查清单 | AI 是否检查输出？ |

### Token 效率策略

| 策略 | 效果 | 适用场景 |
|------|------|----------|
| 创建索引 | 94% 节省 | 大型项目 |
| 分模块索引 | 按需加载 | 模块化项目 |
| 增量更新 | 减少重建 | 频繁变更 |
| 压缩冗余 | 减少噪音 | 文档多的项目 |

### Claude Code 三个核心

| 核心 | 说明 | 关键文件 |
|------|------|----------|
| **配置** | 行为指南 | CLAUDE.md |
| **索引** | 结构指南 | PROJECT_INDEX.json |
| **命令** | 交互接口 | .claude/commands/ |

### Serena 四大组件

| 组件 | 说明 | 关键文件 |
|------|------|----------|
| **配置系统** | 项目级配置 | .serena/project.yml |
| **内存系统** | 持久化知识 | .serena/memories/ |
| **MCP 工具** | 读写接口 | MCP server tools |
| **Git 同步** | 跨设备协作 | .serena/.gitignore |

---

## 实战检查清单

### 写 Prompt 前
- [ ] 目标明确：AI 知道"成功是什么样"？
- [ ] 受众清晰：最终用户是谁？
- [ ] 约束条件：有哪些限制？

### 写 Prompt 时
- [ ] Layer 1: Persona 定义清晰
- [ ] Layer 2: 执行步骤合理
- [ ] Layer 3: 输出模板完整
- [ ] Layer 4: 验证机制完善

### 写 Prompt 后
- [ ] 测试输出是否稳定
- [ ] Token 使用是否高效
- [ ] 边界情况是否处理
- [ ] 错误处理是否完善

### 配置 Serena 时
- [ ] project.yml 配置正确
- [ ] .serena/.gitignore 只排除 /cache
- [ ] memories/ 目录有组织结构
- [ ] Git 追踪配置文件

---

## 推荐资源

### 官方资源
- [Claude Code 文档](https://docs.anthropic.com/claude-code)
- [Claude Agent SDK](https://docs.anthropic.com/claude-agent-sdk)
- [MCP 协议规范](https://modelcontextprotocol.io)

### 社区资源
- [SuperClaude GitHub](https://github.com/superclaude)
- [Claude Code Discord](https://discord.gg/claude-code)
- [Prompt Engineering Guide](https://www.promptingguide.ai)

### 本项目资源
- [CLAUDE.md](../CLAUDE.md) - 项目配置
- [PROJECT_INDEX.json](../PROJECT_INDEX.json) - 项目索引
- [.claude/commands/](../.claude/commands/) - 自定义命令
- [.serena/](../.serena/) - Serena 配置和记忆

---

## 贡献指南

这个集合是动态更新的，欢迎：
1. **报告问题**：发现错误或不清晰的地方
2. **建议改进**：有更好的组织方式
3. **分享经验**：你的学习心得和技巧
4. **贡献内容**：新的主题或示例

---

**开始你的 AI Engineering 之旅！**
