# Interaction Analyzer - Product Document

## 概述

智能对话分析系统，通过 LLM 驱动的模式识别，自动检测 AI 交互中的低效模式，提供可操作的改进建议。

## 核心能力

### 1. 智能检测 (非规则式)

使用 LLM 语义理解，而非硬编码规则：

```
检测维度：
├── 目标清晰度    → 用户意图是否模糊？是否需要澄清？
├── 工具选择      → 是否选对了工具？优先级是否正确？
├── 执行顺序      → 是否走了弯路？能否并行？
├── 沟通效率      → 是否来回过多？信息是否完整？
└── 上下文管理    → 是否遗漏关键信息？范围是否错误？
```

### 2. 混合触发模式

| 模式 | 触发条件 | 适用场景 |
|------|----------|----------|
| **自动触发** | LLM 检测到低效模式 | 实时优化 |
| **手动触发** | 用户调用 `/analyze` | 事后复盘 |

### 3. 可配置分析范围

```yaml
分析范围选项:
  - current_session: 当前会话
  - last_n_turns: 最近 N 轮对话
  - custom_range: 自定义时间/任务范围
  - cross_session: 跨会话模式识别
```

### 4. 三层输出体系

#### Layer 1: 用户视角（问题诊断）
```
┌─────────────────────────────────────┐
│  问题分析报告                         │
│  ┌─────────────────────────────────┐ │
│  │ 问题: 目标不明确                  │ │
│  │ 表现: 查了3个配置文件才确认需求   │ │
│  │ 根因: 未先问清楚用户最终目标      │ │
│  │ 建议: 使用 AskUserQuestion 工具  │ │
│  └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

#### Layer 2: AI 优化提示（系统改进）
```yaml
改进建议:
  - 下次类似任务，优先询问："查看状态 vs 生成文档？"
  - 确定产品范围: "Claude Code vs Claude Desktop?"
  - 使用专门命令: `claude mcp list` > `find` + `cat`
```

#### Layer 3: 可复用资产（知识沉淀）
```
assets/
├── prompts/
│   ├── system-check.md        # 系统状态检查 prompt
│   ├── config-analysis.md     # 配置分析 prompt
│   └── debug-workflow.md      # 调试工作流 prompt
├── workflows/
│   ├── goal-first.yml         # 目标优先工作流
│   ├── tool-selection.yml     # 工具选择决策树
│   └── parallel-exec.yml      # 并行执行模式
└── patterns/
    ├── anti-patterns.md       # 反模式识别
    └── best-practices.md      # 最佳实践
```

## 扩展分析维度

### 代码质量分析
- 检测代码异味、重复模式、安全漏洞
- 与最佳实践对比，提供重构建议

### 工作流优化
- 识别重复性任务，建议自动化
- 发现协作瓶颈，优化并发策略

### 最佳实践推荐
- 基于项目上下文，推荐特定模式
- 例如：FastAPI 项目 → `/sc:implement` + `@fastapi-expert`

## 应用场景

### 场景 A: 开发任务调试
```
问题: Bug 修复花了 5 轮对话
分析:
  - 目标偏移: 从"修复bug"变成"重构代码"
  - 工具低效: 逐个读取文件而非搜索
建议:
  - 先用 Grep 定位问题代码
  - 明确修复范围，避免 scope creep
```

### 场景 B: 文档生成
```
问题: 文档不完整，来回补充
分析:
  - 信息遗漏: 未检查所有相关文件
  - 结构缺失: 没有先确认文档结构
建议:
  - 使用 `/sc:index` 生成项目知识库
  - 定义文档模板后再填充内容
```

### 场景 C: ML 系统设计
```
问题: 模型迭代方向不明确
分析:
  - 目标模糊: "提升性能" vs "降低延迟"
  - 指标缺失: 没有定义评估标准
建议:
  - 先明确优化目标 (accuracy/latency/cost)
  - 建立基线和评估框架
```

## 技术架构

```
┌─────────────────────────────────────────────────────┐
│                 Interaction Analyzer                │
├─────────────────────────────────────────────────────┤
│  Input Layer                                        │
│  ├── Conversation History                           │
│  ├── User Feedback (explicit/implicit)              │
│  └── Configuration (analysis scope)                  │
├─────────────────────────────────────────────────────┤
│  Analysis Engine (LLM-Powered)                      │
│  ├── Pattern Recognition                            │
│  ├── Root Cause Analysis                            │
│  └── Solution Generation                            │
├─────────────────────────────────────────────────────┤
│  Output Layer                                       │
│  ├── User Report (markdown)                         │
│  ├── AI Suggestions (structured)                    │
│  └── Assets (prompts, workflows, patterns)          │
└─────────────────────────────────────────────────────┘
```

## 使用示例

### 自动触发模式
```markdown
[AI 检测到低效模式]
⚠️ 分析: 查询配置花费了 4 轮对话
📊 根因: 未先确认产品范围 (Claude Code vs Desktop)
💡 建议: 先运行 `claude mcp list` 确认环境
📦 已生成优化 prompt 到 .claude/prompts/check-env.md
```

### 手动触发模式
```bash
/analyze --scope=current --focus=tool-selection
```

## 设计原则

1. **非侵入式**: 不打断正常工作流，分析在后台进行
2. **可配置**: 用户控制分析深度和范围
3. **可复用**: 生成的资产可以直接用于未来任务
4. **持续学习**: 跨会话模式识别，积累最佳实践

## 下一步

1. 实现 LLM 分析引擎 (prompt 模板)
2. 构建模式识别库
3. 设计资产生成系统
4. 集成到 Claude Code workflow

---

*Version: 0.1.0*
*Status: Product Design*
*Author: Claude + User Co-creation*
