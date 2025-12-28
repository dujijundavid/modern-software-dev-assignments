# Claude Best Practices

> 深入理解 Claude Code 和 SuperClaude 的最佳实践集合

这个文件夹包含了系统化的学习和参考材料，帮助你更好地掌握 AI 辅助编程。

---

## 文件夹结构

```
claude-best-practices/
├── prompt-engineering/          # Prompt Engineering 深度解析
│   ├── 01-index-repo-analysis.md    # /sc:index-repo 命令分析
│   └── 02-ai-engineering-principles.md # AI 工程核心原则
│
├── project-patterns/            # 项目模式和实践
│   ├── 01-project-index-usage.md     # PROJECT_INDEX 使用指南
│   ├── 02-subagent-system.md         # 子代理系统架构
│   ├── 03-claude-md-best-practices.md # CLAUDE.md 最佳实践
│   ├── 04-skill-design-best-practices.md # MCP/Subagent Skill 设计
│   └── 05-skills-system-guide.md     # Skills 系统完全指南 ⭐ NEW
│
└── learning-prompts/            # 学习 Prompts 集合
    ├── README.md                    # 100+ 学习 prompts
    ├── sc-pm-explained.md           # /sc:pm 深度解析
    └── superclaude-architecture-analysis.md # SuperClaude 架构分析
```

---

## 快速开始

### 1. 理解 PROJECT_INDEX

**阅读**: [project-patterns/01-project-index-usage.md](project-patterns/01-project-index-usage.md)

**学习目标**：
- 为什么需要 PROJECT_INDEX？
- Claude Code 如何使用索引？
- 如何维护和更新索引？

**关键洞察**：
```
无索引：58,000 tokens/会话
有索引：3,000 tokens/会话
节省：94%
```

---

### 2. 学习 Prompt Engineering

**阅读**: [prompt-engineering/01-index-repo-analysis.md](prompt-engineering/01-index-repo-analysis.md)

**学习目标**：
- 4 层 Prompt 设计模式
- 并行执行触发技巧
- 验证驱动的 Prompt 设计
- Token 效率优化

**核心框架**：
```
Layer 1: Persona (角色认知)
   ↓
Layer 2: Process (执行流程)
   ↓
Layer 3: Output (输出模板)
   ↓
Layer 4: Validation (质量验证)
```

---

### 3. 理解子代理系统

**阅读**: [project-patterns/02-subagent-system.md](project-patterns/02-subagent-system.md)

**学习目标**：
- 主代理与子代理的关系
- 何时使用哪个子代理
- 子代理协作模式
- 如何定义新子代理

**核心概念**：
```
主代理 (编排者)
    ↓
专业化子代理 (执行者)
    ├─ fastapi-expert
    ├─ python-testing-expert
    └─ code-reviewer (必须)
```

---

### 4. 掌握 AI 工程原则

**阅读**: [prompt-engineering/02-ai-engineering-principles.md](prompt-engineering/02-ai-engineering-principles.md)

**学习目标**：
- 认知负载理论
- Token 效率数学
- 分层设计方法
- ROI 量化策略

**核心公式**：
```
Sessions_BreakEven = Token_Creation / (Token_Full - Token_Index)
```

---

### 5. 理解 CLAUDE.md 最佳实践

**阅读**: [project-patterns/03-claude-md-best-practices.md](project-patterns/03-claude-md-best-practices.md)

**学习目标**：
- CLAUDE.md 应该包含哪些部分？
- 如何组织信息结构？
- 如何定义 AI 团队角色？
- 如何与 PROJECT_INDEX.json 配合？

**核心框架**：
```
CLAUDE.md 三大功能
├── 行为指南 (Behavior Guide) - AI 应该如何表现
├── 结构映射 (Structure Map) - 项目架构和模式
└── 工作流编排 (Workflow Orchestration) - 代理和命令使用
```

---

### 6. 使用学习 Prompts

**阅读**: [learning-prompts/README.md](learning-prompts/README.md)

**使用方法**：
1. 选择感兴趣的主题
2. 复制对应的 prompt
3. 在 Claude Code 中运行
4. 观察并记录结果
5. 迭代改进

---

## 学习路径

### 初级（1-2 周）

```
Day 1-3: 理解基础
├── PROJECT_INDEX 使用指南
├── Claude Code 基础概念
└── 实战：创建项目索引

Day 4-7: Prompt Engineering
├── /sc:index-repo 深度分析
├── AI 工程原则
└── 实战：优化项目命令

Day 8-14: Skills 系统
├── Claude Skills 基础
├── 创建第一个 Skill
└── 实战：/sc:code-pattern
```

### 中级（3-4 周）

```
Week 3: SuperClaude 深入
├── /sc:pm 项目管理代理
├── /sc:implement 实现命令
├── MCP 系统理解
└── 工作流设计

Week 4: MCP 开发
├── Serena MCP 深度解析
├── Context7 MCP 使用
├── 自定义 MCP 服务器
└── 实战：Learning Analytics MCP
```

### 高级（5-8 周）

```
Week 5-6: 高级主题
├── 多代理协作模式
├── 自我改进循环
├── 性能优化
└── 安全和隐私

Week 7-8: 综合项目
├── 动态索引系统
├── 系统集成
├── 文档和分享
└── 社区贡献
```

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

---

## 贡献指南

这个集合是动态更新的，欢迎：

1. **报告问题**：发现错误或不清晰的地方
2. **建议改进**：有更好的组织方式
3. **分享经验**：你的学习心得和技巧
4. **贡献内容**：新的主题或示例

---

## 许可

与主项目保持一致。

---

**开始你的 AI Engineering 之旅！** 🚀
