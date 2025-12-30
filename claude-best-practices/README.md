# Claude Best Practices

> 深入理解 Claude Code 和 SuperClaude 的最佳实践集合

这个文件夹包含了系统化的学习和参考材料，帮助你更好地掌握 AI 辅助编程。

---

## 快速导航

### 我想配置项目 → [01-setup/](01-setup/)
**任务**：把 Claude Code 配置好，让项目对 AI 友友

| 文件 | 说明 | 关键收益 |
|------|------|---------|
| [PROJECT_INDEX 使用指南](01-setup/project-index-usage.md) | 创建项目索引 | 94% token 节省 |
| [CLAUDE.md 最佳实践](01-setup/claude-md-best-practices.md) | 配置 AI 行为 | 定义团队和工作流 |
| [Skills 系统完全指南](01-setup/skills-system-guide.md) | 理解技能系统 | 扩展 AI 能力 |

---

### 我想理解系统 → [02-understand/](02-understand/)
**任务**：理解 Claude Code 如何工作

| 文件 | 说明 | 关键内容 |
|------|------|---------|
| [子代理系统架构](02-understand/subagent-system.md) | 理解子代理机制 | 专业化与委托 |
| [SuperClaude 架构](02-understand/superclaude-architecture.md) | 理解整体架构 | 命令系统和 MCP |
| [AI 工程核心原则](02-understand/ai-engineering-principles.md) | 理解工程原则 | ROI、Token 优化 |

---

### 我想创建/开发 → [03-create/](03-create/)
**任务**：创建自定义能力，扩展 Claude Code 功能

| 文件 | 说明 | 输出 |
|------|------|------|
| [Skill 设计最佳实践](03-create/skill-design-best-practices.md) | 设计自定义 Skill | 新的 .claude/commands/ |
| [Document Skills 使用指南](03-create/document-skills-guide.md) | 使用文档技能 | docx, pptx, pdf 等 |

---

### 我想深入学习 → [04-deep-dive/](04-deep-dive/)
**任务**：深入理解特定命令和功能的内部原理

| 文件 | 说明 | 深度 |
|------|------|------|
| [/sc:pm 深度解析](04-deep-dive/sc-pm-explained.md) | /sc:pm 完全解析 | 工作流、记忆系统 |
| [/sc:index-repo 深度分析](04-deep-dive/index-repo-analysis.md) | /sc:index-repo 分析 | Prompt 拆解 |
| [Context7 MCP 完全指南](04-deep-dive/context7-mcp-guide.md) | 获取最新库文档 | 工具详解、最佳实践 |
| [100+ 学习 prompts](04-deep-dive/learning-prompts-collection.md) | 实践练习集合 | 8个主题，100+ prompts |

---

### 我想掌握 Serena → [serena-mcp/](serena-mcp/)
**任务**：深入理解 Serena AI 项目内存系统

| 文件 | 说明 | 关键收益 |
|------|------|---------|
| [README.md](serena-mcp/README.md) | Serena 概览和导航 | 快速开始指南 |
| [01-architecture-overview.md](serena-mcp/01-architecture-overview.md) | 架构概览 | 系统组件详解 |
| [02-configuration-guide.md](serena-mcp/02-configuration-guide.md) | 配置完全指南 | project.yml 参考 |
| [03-memory-system-design.md](serena-mcp/03-memory-system-design.md) | 内存系统设计 | 记忆组织策略 |
| [04-cross-machine-sync.md](serena-mcp/04-cross-machine-sync.md) | 跨机器协作 | Git 共享策略 |
| [05-advanced-patterns.md](serena-mcp/05-advanced-patterns.md) | 高级模式技巧 | MCP 工具集成 |

---

## 文件夹结构

```
claude-best-practices/
├── README.md                      # 本文件
│
├── 01-setup/                      # 【我要配置项目】
│   ├── project-index-usage.md
│   ├── claude-md-best-practices.md
│   └── skills-system-guide.md
│
├── 02-understand/                 # 【我要理解系统】
│   ├── subagent-system.md
│   ├── superclaude-architecture.md
│   └── ai-engineering-principles.md
│
├── 03-create/                     # 【我要创建/开发】
│   ├── skill-design-best-practices.md
│   └── document-skills-guide.md
│
├── 04-deep-dive/                  # 【我要深入学习】
│   ├── sc-pm-explained.md
│   ├── index-repo-analysis.md
│   ├── context7-mcp-guide.md
│   └── learning-prompts-collection.md
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

### Day 11-14: 掌握 Serena
1. [Serena 架构概览](serena-mcp/01-architecture-overview.md) - 理解系统架构
2. [Serena 配置指南](serena-mcp/02-configuration-guide.md) - 配置 project.yml
3. [内存系统设计](serena-mcp/03-memory-system-design.md) - 组织项目记忆

### Day 15+: 深入学习
1. [/sc:pm 深度解析](04-deep-dive/sc-pm-explained.md) - 项目管理代理
2. [/sc:index-repo 分析](04-deep-dive/index-repo-analysis.md) - Prompt Engineering 深度分析
3. [Serena 高级模式](serena-mcp/05-advanced-patterns.md) - MCP 工具集成
4. [学习 prompts 实践](04-deep-dive/learning-prompts-collection.md) - 100+ 实践 prompts

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
