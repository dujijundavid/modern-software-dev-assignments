# Claude Code 学习 Prompts 集合

> 精心设计的 prompts，帮助你深入理解 Claude Code 的各个层面

---

## 使用指南

### 如何使用这些 Prompts

1. **直接复制粘贴**：在 Claude Code 中直接使用
2. **根据项目调整**：替换 `{project}` 等占位符
3. **渐进式学习**：从基础到高级，按顺序尝试
4. **记录结果**：观察 AI 的响应，理解其工作方式

---

## 第一部分：Claude Code 基础

### 1.1 了解 Claude Code 能力

```
请全面介绍 Claude Code 的能力，包括：

1. 核心功能：Claude Code 能做什么？
2. 与其他 AI 编程工具的区别：独特之处是什么？
3. 适用场景：哪些任务最合适？
4. 限制：什么情况下不适合使用？

请用具体示例说明每个点。
```

### 1.2 理解上下文管理

```
解释 Claude Code 如何管理和维护上下文：

1. Context Window 的工作原理
2. 长对话中的上下文保持
3. 项目上下文如何传递
4. 如何优化 token 使用

请用我的项目 {modern-software-dev-assignments} 作为示例。
```

### 1.3 工具调用机制

```
深入解释 Claude Code 的工具调用机制：

1. AI 如何决定调用哪个工具？
2. 工具调用的决策过程
3. 并行工具调用的条件
4. 工具调用失败的处理

请用实际代码示例说明。
```

---

## 第二部分：CLAUDE.md 配置

### 2.1 CLAUDE.md 最佳实践

```
分析 CLAUDE.md 文件的最佳实践：

1. 应该包含哪些部分？
2. 如何组织信息？
3. 如何定义 AI 团队角色？
4. 如何与 PROJECT_INDEX.json 配合？

请读取我项目的 CLAUDE.md 并给出改进建议。
```

### 2.2 子代理（Sub-Agent）设计

```
解释 Claude Code 的子代理系统：

1. 子代理与主代理的关系
2. 何时应该使用子代理？
3. 如何定义新的子代理？
4. 子代理间的协作模式

请用我项目中的配置（fastapi-expert, python-testing-expert 等）作为示例。
```

### 2.3 自定义命令设计

```
教授如何设计有效的自定义命令（Slash Commands）：

1. 命令文件的基本结构（YAML front matter）
2. 如何定义命令的目的和范围
3. 如何编写清晰的执行指令
4. 命令间的复用模式

请分析我项目中的命令：/week, /explore-week, /test-week
并建议一个新命令 /review-pr 用于 PR 评审。
```

---

## 第三部分：SuperClaude 深度解析

### 3.1 SuperClaude 架构理解

```
深入分析 SuperClaude 的架构设计：

1. PM Agent 的角色和职责
2. 命令系统的组织方式
3. MCP 服务器的动态加载机制
4. PDCA 循环在 AI 工作流中的应用

请参考 ~/.claude/commands/sc/ 中的命令文件进行分析。
```

### 3.2 /sc:pm 项目管理代理

```
详细解释 /sc:pm 的工作原理：

1. 会话生命周期管理
2. Serena MCP 记忆系统集成
3. 子代理的自动委托机制
4. 自我纠错和改进循环

请展示一个完整的工作流示例，从用户请求到完成。
```

> 📘 **Deep Dive**: For a comprehensive English explanation of `/sc:pm`, see:
> → [sc-pm-explained.md](./sc-pm-explained.md) - Complete guide with diagrams, code examples, and real workflow

### 3.3 /sc:implement 实现命令

```
分析 /sc:implement 命令的设计：

1. Persona 激活机制
2. MCP 工具的选择逻辑
3. 代码生成模式
4. 质量保证机制

请用它来实现一个 FastAPI 的 CRUD 端点作为示例。
```

### 3.4 /sc:index-repo 索引生成

```
深入分析 /sc:index-repo 的 Prompt Engineering：

1. 问题-解决方案框架
2. 分阶段执行流设计
3. 模板化输出策略
4. Token 效率优化

请将其原理应用到创建一个"每周学习笔记索引"命令。
```

---

## 第四部分：Claude Skills 系统

### 4.1 Skills 基础

```
全面介绍 Claude Code 的 Skills 系统：

1. 什么是 Skill？与命令的区别？
2. Skill 的类型：user skills vs managed skills vs plugin skills
3. 如何发现可用的 Skills？
4. 如何创建自定义 Skill？

请列出当前环境中所有可用的 Skills。
```

### 4.2 创建自定义 Skill

```
指导我创建一个自定义 Skill：

我想创建一个 /sc:code-pattern Skill，用于：
1. 识别项目中的代码模式
2. 推荐最佳实践
3. 生成模式文档

请帮我设计这个 Skill 的完整结构，包括：
- YAML front matter
- 主要指令
- 执行流程
- 输出模板
```

### 4.3 Document Skills 插件

```
深入讲解 document-skills 插件：

1. 可用的 document skills 有哪些？
2. docx, pptx, pdf, xlsx skills 的能力
3. 如何在项目中使用这些 skills
4. 如何组合多个 document skills

请用我的项目文档作为示例，演示 document-skills 的使用。
```

### 4.4 Skill 的最佳实践

```
总结设计高质量 Skill 的最佳实践：

1. 命名约定
2. 描述写作
3. 指令组织
4. 参数设计
5. 错误处理
6. 测试策略

请分析一个你认为是"优秀设计"的 Skill 并解释原因。
```

---

## 第五部分：MCP (Model Context Protocol)

### 5.1 MCP 基础理解

```
解释 Model Context Protocol (MCP)：

1. MCP 的设计目的
2. Client-Server 架构
3. Tools vs Resources vs Prompts
4. 如何在 Claude Code 中使用 MCP

请列出我当前配置的所有 MCP 服务器。
```

### 5.2 Serena MCP 深度解析

```
深入分析 Serena MCP 服务器：

1. 它提供的核心工具
2. 符号搜索机制 (find_symbol, find_referencing_symbols)
3. 代码编辑工具的工作原理
4. 记忆系统 (list_memories, read_memory, write_memory)

请用 Serena MCP 分析我项目中的 week2/app/services/extract.py
```

### 5.3 Context7 MCP

```
讲解 Context7 MCP 的使用：

1. 如何查找库文档
2. resolve-library-id vs get-library-docs
3. 代码模式 vs 信息模式
4. 如何高效获取文档

请用它查找 FastAPI 的最新中间件文档。
```

### 5.4 开发自定义 MCP 服务器

```
指导开发一个自定义 MCP 服务器：

我想创建一个 "Learning Progress MCP"：
- 跟踪每周学习进度
- 管理学习笔记
- 生成学习报告

请设计：
1. 服务器架构
2. 提供的 Tools
3. Resources 结构
4. 实现建议（Python/FastMCP）
```

---

## 第六部分：Prompt Engineering 进阶

### 6.1 Prompt 分层设计

```
教授 Prompt 分层设计方法：

请分析 /sc:index-repo 的 Prompt，展示：
1. Layer 1: Persona 层设计
2. Layer 2: Process 层设计
3. Layer 3: Output 层设计
4. Layer 4: Validation 层设计

然后用同样的方法分析我项目中的 /week 命令。
```

### 6.2 并行执行 Prompt 设计

```
讲解如何在 Prompt 中激活并行执行：

1. 并行触发的关键词
2. 任务独立性设计
3. 结果合并策略
4. 同步点设置

请设计一个 Prompt，并行分析我项目中所有周的测试覆盖率。
```

### 6.3 验证驱动的 Prompt 设计

```
深入讲解验证机制的设计：

1. 自我验证触发器
2. 质量检查清单设计
3. 阈值验证模式
4. 用户视角检查

请为我项目中的 /refactor 命令添加验证机制。
```

### 6.4 Token 优化策略

```
教授 Token 使用的优化策略：

1. 渐进式信息揭示
2. 按需深入模式
3. 索引 vs 直接读取的权衡
4. 上下文压缩技巧

请分析我当前项目的 Token 使用效率，给出优化建议。
```

---

## 第七部分：工作流设计

### 7.1 完整开发工作流

```
设计一个完整的 AI 辅助开发工作流：

从需求到部署，包含：
1. 需求分析阶段
2. 设计阶段
3. 实现阶段
4. 测试阶段
5. 代码审查阶段
6. 部署阶段

请指定每个阶段使用的：
- Claude Code 命令
- Sub-agent
- MCP 工具
- 验证机制
```

### 7.2 学习工作流

```
设计一个 AI 辅助学习工作流：

基于 BPRT 循环（Build-Prompt-Reflect-Teach）：
1. Build: 如何用 AI 辅助实现
2. Prompt: 如何优化 AI 交互
3. Reflect: 如何比较人工 vs AI 输出
4. Teach: 如何生成学习笔记

请用 Week 2 的内容作为示例演示完整流程。
```

### 7.3 调试工作流

```
设计一个 AI 辅助调试工作流：

当遇到错误时：
1. 根因分析：如何让 AI 帮助找到根本原因
2. 解决方案生成：如何获得多种解决方案
3. 验证：如何确保修复有效
4. 预防：如何避免类似错误

请用一个实际错误场景演示完整流程。
```

---

## 第八部分：高级主题

### 8.1 多代理协作模式

```
讲解多代理协作的设计模式：

1. 顺序协作（Sequential）
2. 并行协作（Parallel）
3. 层次协作（Hierarchical）
4. 对等协作（Peer-to-Peer）

请设计一个场景，需要 3 个以上代理协作完成。
```

### 8.2 自我改进循环

```
讲解 AI 的自我改进机制：

1. PDCA 在 AI 工作流中的应用
2. 如何让 AI 从错误中学习
3. 知识库的自动更新
4. 模式识别和形式化

请为我项目设计一个"自动改进系统"。
```

### 8.3 性能优化

```
讲解 Claude Code 的性能优化：

1. Token 使用优化
2. MCP 工具的动态加载
3. 缓存策略
4. 并行执行优化

请分析并优化我项目中的 /sc:pm 命令性能。
```

### 8.4 安全和隐私

```
讲解 Claude Code 的安全和隐私考虑：

1. 敏感信息处理
2. 权限管理
3. MCP 服务器的安全
4. 代码泄露风险

请审查我项目的安全配置，给出改进建议。
```

---

## 实战项目

### P1: 创建 /sc:weekly-progress 命令

```
项目：创建一个每周进度追踪命令

功能需求：
1. 分析当前周的完成状态
2. 与学习目标对比
3. 生成进度报告
4. 建议下一步行动

请帮我：
1. 设计命令结构
2. 编写完整的 Prompt
3. 定义验证机制
4. 测试命令效果
```

### P2: 构建 Learning Analytics MCP

```
项目：创建学习分析 MCP 服务器

功能需求：
1. 跟踪每周学习时间
2. 分析测试覆盖率趋势
3. 生成学习笔记摘要
4. 推荐学习重点

请帮我：
1. 设计 MCP 服务器架构
2. 定义 Tools 和 Resources
3. 实现（用 FastMCP）
4. 集成到 Claude Code
```

### P3: 优化项目索引系统

```
项目：创建动态索引系统

功能需求：
1. 自动检测代码变更
2. 增量更新索引
3. 维护变更历史
4. 智能相关性推荐

请帮我：
1. 分析当前 PROJECT_INDEX 的局限
2. 设计动态索引方案
3. 实现自动化更新
4. 添加可视化功能
```

---

## 学习路径

### 初级路径（1-2 周）

```
Week 1: 基础理解
- Day 1-2: Claude Code 基础 (第一部分)
- Day 3-4: CLAUDE.md 配置 (第二部分)
- Day 5-7: 实战：优化项目配置

Week 2: Skills 系统
- Day 1-3: Claude Skills 基础 (第四部分)
- Day 4-5: 创建第一个自定义 Skill
- Day 6-7: 实战项目 P1
```

### 中级路径（3-4 周）

```
Week 3: SuperClaude 深入
- Day 1-3: SuperClaude 架构 (第三部分)
- Day 4-5: Prompt Engineering (第六部分)
- Day 6-7: 工作流设计 (第七部分)

Week 4: MCP 开发
- Day 1-3: MCP 系统理解 (第五部分)
- Day 4-7: 实战项目 P2
```

### 高级路径（5-8 周）

```
Week 5-6: 高级主题
- 多代理协作模式
- 自我改进循环
- 性能优化

Week 7-8: 综合项目
- 实战项目 P3
- 系统集成
- 文档和分享
```

---

## 学习技巧

### 1. 主动实验

```
不要只是阅读，要：
- 复制 prompts 到 Claude Code
- 观察响应
- 修改 prompts
- 比较效果
```

### 2. 记录发现

```
创建学习笔记：
- 记录有效的 prompts
- 记录失败的尝试
- 记录改进思路
- 定期回顾整理
```

### 3. 构建示例

```
用自己的项目：
- 替换通用示例
- 测试边界情况
- 验证假设
- 迭代改进
```

### 4. 分享交流

```
- 写博客分享经验
- 参与 Claude Code 社区
- 贡献自定义 commands/skills
- 帮助其他学习者
```

---

## 相关资源

- [Prompt Engineering 分析](../prompt-engineering/01-index-repo-analysis.md)
- [AI 工程原则](../prompt-engineering/02-ai-engineering-principles.md)
- [PROJECT_INDEX 使用](../project-patterns/01-project-index-usage.md)
- [官方文档](https://docs.anthropic.com/claude-code)
