# Prompt 分层设计方法：深度解析

> 从 Anthropic AI Engineer 与 AI 学习专家的双重视角，解析顶尖 Prompt 的分层架构

---

## 目录

1. [四层框架概览](#四层框架概览)
2. [案例分析一：/sc:index-repo](#案例分析一scindex-repo)
3. [案例分析二：/week 命令](#案例分析二week-命令)
4. [对比分析与改进建议](#对比分析与改进建议)
5. [实战模板](#实战模板)

---

## 四层框架概览

```
┌─────────────────────────────────────────────────────────────────┐
│                    Prompt 分层架构                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Layer 1: Persona 层 (角色认知层)                         │   │
│  │ "你是谁？" - 建立 AI 的身份、角色、行为模式               │   │
│  │ • 显式角色定义                                           │   │
│  │ • 隐式行为暗示                                           │   │
│  │ • 约束条件设定                                           │   │
│  └─────────────────────────────────────────────────────────┘   │
│                          │                                      │
│                          ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Layer 2: Process 层 (流程执行层)                         │   │
│  │ "怎么做？" - 定义任务分解、执行顺序、并行策略             │   │
│  │ • 阶段划分 (Phases)                                      │   │
│  │ • 步骤序列 (Steps)                                        │   │
│  │ • 并行触发 (Parallel hints)                              │   │
│  │ • 门控验证 (Validation gates)                            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                          │                                      │
│                          ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Layer 3: Output 层 (输出模板层)                         │   │
│  │ "产出什么？" - 规范输出格式、占位符、结构约束             │   │
│  │ • 模板定义 (Templates)                                   │   │
│  │ • 占位符 (Placeholders)                                  │   │
│  │ • 视觉层级 (Visual hierarchy)                            │   │
│  │ • 长度约束 (Length constraints)                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                          │                                      │
│                          ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Layer 4: Validation 层 (质量验证层)                      │   │
│  │ "做得对吗？" - 自我审查、质量检查、用户确认               │   │
│  │ • 检查清单 (Checklists)                                   │   │
│  │ • 质量阈值 (Quality thresholds)                          │   │
│  │ • 用户视角 (User perspective)                            │   │
│  │ • 验证触发器 (Validation triggers)                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 设计哲学：从下往上 vs 从上往下

| 方法 | 描述 | 适用场景 |
|------|------|----------|
| **从下往上** | 先定义输出模板 → 再设计流程 → 最后设定角色 | 需要特定格式输出的任务 |
| **从上往下** | 先设定角色 → 定义流程 → 规范输出 | 需要特定行为模式的任务 |
| **混合方法** | 同步设计四层，迭代优化 | 复杂任务系统 |

---

## 案例分析一：/sc:index-repo

> 来源：`~/.claude/commands/sc/index-repo.md`
>
> 目标：94% token 减少 (58K → 3K) 的代码库索引生成器

---

### Layer 1: Persona 层设计

```yaml
显式角色: 无直接 "You are..." 声明
隐式角色: "Index Creator activated" 📊
角色特征:
  - 分析型：需要理解项目结构
  - 组织型：需要提取和分类信息
  - 效率导向：以 token 节省为首要目标
行为暗示:
  - "Parallel analysis" → 并行思考能力
  - "Quality checks" → 自我审查意识
约束条件:
  - "Index size < 5KB" → 输出长度约束
  - "Human-readable format" → 格式约束
```

**设计分析：**


📊 **Index Creator activated**


> **隐式角色激活机制**:
> - 没有 "You are an expert..." 的显式声明
> - 通过 "activated" 状态暗示这是一个专门的"索引创建器"
> - 📊 emoji 强化"数据分析"的角色特征

**Anthropic AI Engineer 视角：**
- ✅ 简洁：无需冗长的角色描述
- ✅ 功能导向：角色通过功能定义
- ⚠️ 可改进：可以添加更明确的能力边界

**AI 学习专家视角：**
- ✅ 状态激活式：用 "activated" 触发 AI 进入特定模式
- ✅ 视觉锚点：emoji 帮助 AI 识别当前上下文
- ⚠️ 可改进：缺乏行为准则的显式声明

---

### Layer 2: Process 层设计

```yaml
执行流: 4 个明确的阶段 (Phases)
阶段命名: 动词导向 (Analyze → Extract → Generate → Validate)

Phase 1: Analyze Repository Structure
  并行策略: "5 concurrent Glob searches"
  输入: 文件系统模式 (Glob patterns)
  产出: 文件分类列表

Phase 2: Extract Metadata
  依赖: Phase 1 的输出
  动作: 提取入口点、模块、依赖
  产出: 元数据集合

Phase 3: Generate Index
  依赖: Phase 2 的输出
  模板: 预定义的 markdown 结构
  产出: PROJECT_INDEX.md

Phase 4: Validation
  触发: Phase 3 完成后
  方法: 检查清单 (checklist)
  产出: 质量确认
```

**设计亮点：**

```markdown
### Phase 1: Analyze Repository Structure

**Parallel analysis** (5 concurrent Glob searches):

1. **Code Structure**
   src/**/*.{ts,py,js,tsx,jsx}
   lib/**/*.{ts,py,js}
   superclaude/**/*.py
```

> **关键设计说明**:
> - "Parallel analysis" + 数字 "5" = 关键触发词，激活并发思维
> - 精确的 Glob 模式，直接可执行

**流程设计技巧：**

| 技巧 | 示例 | 效果 |
|------|------|------|
| 数字量化 | "5 concurrent Glob searches" | 明确并行度，激活并发思维 |
| 视觉分隔 | 用 `↓` 或空行分隔阶段 | 清晰的数据流向 |
| 输出声明 | 每个阶段明确 "Output:" | 确保 AI 知道期望产出 |
| 门控设计 | Phase 4 是验证阶段 | 质量保证机制 |

---

### Layer 3: Output 层设计

```markdown
## 📁 Project Structure
{tree view of main directories}

## 🚀 Entry Points
- CLI: {path} - {description}
- API: {path} - {description}

## 📦 Core Modules
### Module: {name}
- Path: {path}
- Exports: {list}
- Purpose: {1-line description}
```

**模板设计分析：**

| 要素 | 设计 | 作用 |
|------|------|------|
| **Emoji 标题** | 📁 🚀 📦 🔧 📚 🧪 🔗 📝 | 视觉分类，快速扫描 |
| **占位符** | `{path}`, `{name}` | 明确填充位置 |
| **约束说明** | `{1-line description}` | 长度限制 |
| **层级结构** | `##` → `###` → `-` | 信息层级 |
| **一致性** | 所有模块用相同格式 | 可解析性 |

**Anthropic AI Engineer 视角：**
- ✅ 机器友好：结构化模板便于解析
- ✅ 人类友好：emoji 和缩进提高可读性
- ✅ 约束明确：`1-line` 防止冗长描述
- ⚠️ 可改进：缺少必需/可选字段的标记

**占位符设计模式：**

```yaml
简单占位符:      {path}
约束占位符:      {1-line description}
列表占位符:      {list}
枚举示例:        - CLI: {path} - {description}
                  - API: {path} - {description}
```

---

### Layer 4: Validation 层设计

```markdown
### Phase 4: Validation

Quality checks:
- [ ] All entry points identified?
- [ ] Core modules documented?
- [ ] Index size < 5KB?
- [ ] Human-readable format?
```

**验证设计分析：**

| 维度 | 检查项 | 类型 |
|------|--------|------|
| **完整性** | All entry points identified? | 二元 |
| **覆盖性** | Core modules documented? | 二元 |
| **量化约束** | Index size < 5KB? | 可测量 |
| **用户视角** | Human-readable format? | 主观 |

**验证触发技巧：**

```markdown
🔑 关键词: "Quality checks:", "Validation"
📋 格式: "- [ ]" 检查清单格式
🎯 量化: "< 5KB" 可测量的阈值
👥 用户: "Human-readable" 提醒最终用户
```

**AI 学习专家视角：**
- ✅ 自我验证触发：让 AI 在输出前检查
- ✅ 多维度验证：完整、覆盖、量化、用户
- ✅ 可执行检查：每个检查项都可以验证
- ⚠️ 可改进：缺少失败时的处理策略

---

## 案例分析二：/week 命令

> 来源：`.claude/commands/week.md`
>
> 目标：帮助 CS146S 课程的周作业助手

---

### Layer 1: Persona 层设计

```yaml
显式角色: "You are working on the CS146S Modern Software Developer course"
角色定位:
  - 课程助手 (Course Assistant)
  - 周作业向导 (Weekly Assignment Guide)
能力范围:
  - 理解周作业要求
  - 检查实现状态
  - 提供指导帮助
约束条件:
  - "Always ask clarifying questions if the week or specific task isn't clear"
```

**设计对比：**

| 维度 | /sc:index-repo | /week |
|------|----------------|-------|
| 角色声明方式 | 隐式 (activated) | 显式 (You are...) |
| 角色具体性 | 功能型 | 课程场景型 |
| 约束明确性 | 隐式 (通过模板) | 显式 (Always ask...) |
| Emoji 使用 | 📊 | 无 |

---

### Layer 2: Process 层设计

```yaml
流程结构: 线性步骤 (非 Phase 模式)

Step 1: 理解上下文
  "First, understand which week they're working on"
  方法: "reviewing the context of their request"

Step 2: 检查周作业要求
  "Review the week's assignment requirements in the corresponding week/ directory"

Step 3: 检查学习笔记
  "Check learning_notes/ for relevant concepts and techniques"

Step 4: 理解实现状态
  "Understand what's already implemented vs what needs to be done"

Step 5: 提供帮助
  "Provide guidance or implementation help appropriate for that week's focus"
```

**流程设计对比：**

| 特征 | /sc:index-repo | /week |
|------|----------------|-------|
| 阶段命名 | Phase 1-4 | Step 1-5 (隐式) |
| 并行提示 | 显式 "5 concurrent" | 无 |
| 验证门控 | 专门的 Phase 4 | 无 |
| 流向标记 | 无显式箭头 | 数字列表 |
| 目录结构 | 独立的每个阶段 | 连续的段落 |

**/week 流程的问题：**

```yaml
问题 1: 缺少阶段分隔
  - 所有步骤在一个段落中
  - 没有 Phase/Step 的明确标记

问题 2: 没有验证门控
  - 没有 "Validation" 阶段
  - 缺少质量检查

问题 3: Weekly Focus Areas 是静态列表
  - 列出了 8 周的主题
  - 但没有使用机制
```

---

### Layer 3: Output 层设计

```yaml
输出规范: 无明确模板

隐式输出:
  - "guidance or implementation help"
  - 回应类型不固定

Weekly Focus Areas (知识库):
  Week 1: Prompting techniques
  Week 2: LLM-powered web apps with FastAPI
  Week 3: MCP Server development
  Week 4: Claude Code automation
  Week 5: Warp multi-agent workflows
  Week 6: Security with Semgrep
  Week 7: AI code review with Graphite Diamond
  Week 8: Multi-stack development
```

**输出层对比：**

| 维度 | /sc:index-repo | /week |
|------|----------------|-------|
| 模板定义 | 完整 markdown 模板 | 无 |
| 占位符 | {path}, {name} 等 | 无 |
| 长度约束 | < 5KB | 无 |
| 视觉层级 | emoji + 标题 | 纯文本 |
| 输出类型 | 文件 (PROJECT_INDEX.md) | 对话回应 |

---

### Layer 4: Validation 层设计

```yaml
验证机制: 行为约束声明

"Always ask clarifying questions if the week or specific task isn't clear"

功能: 输入验证 (而非输出验证)
  - 确保理解用户意图
  - 避免错误假设
```

> **注**: 这是 /week 命令中唯一的验证相关内容

**验证层对比：**

| 维度 | /sc:index-repo | /week |
|------|----------------|-------|
| 验证阶段 | 专门的 Phase 4 | 无专门阶段 |
| 检查清单 | 4 项质量检查 | 无 |
| 量化阈值 | < 5KB | 无 |
| 验证类型 | 输出质量验证 | 输入理解验证 |

---

## 对比分析与改进建议

---

### 综合对比表

| 层级 | 维度 | /sc:index-repo | /week | 差距分析 |
|------|------|----------------|-------|----------|
| **Layer 1** | 角色声明 | 隐式 (activated) | 显式 (You are...) | 两种风格各有优势 |
| | 行为暗示 | 📊 视觉锚点 | 无 | /week 可添加 emoji |
| | 约束条件 | 隐式 (通过模板) | 显式 (Always ask) | /week 约束更清晰 |
| **Layer 2** | 阶段划分 | Phase 1-4 明确 | 隐式步骤 | /week 缺少结构化 |
| | 并行提示 | "5 concurrent" | 无 | /week 可添加并行分析 |
| | 验证门控 | 专门的 Phase 4 | 无 | /week 缺少验证 |
| | 流向标记 | 隐式 (标题分隔) | 数字列表 | 都可改进 |
| **Layer 3** | 模板定义 | 完整 markdown | 无 | /week 严重缺失 |
| | 占位符 | {path}, {name} | 无 | /week 严重缺失 |
| | 长度约束 | < 5KB | 无 | /week 可添加 |
| | 视觉层级 | emoji + 标题 | 纯文本 | /week 可改进 |
| **Layer 4** | 检查清单 | 4 项具体检查 | 无 | /week 严重缺失 |
| | 质量阈值 | 量化指标 | 无 | /week 可添加 |
| | 验证触发 | Phase 4 触发 | 行为约束 | 类型不同 |

---

### /week 命令改进方案

**改进后的 /week.md：**

```markdown
---
name: week
description: CS146S weekly assignment assistant with structured analysis
---

# 📚 Week Assignment Assistant

You are working on the CS146S Modern Software Developer course. The user wants help with a specific weekly assignment.

## Layer 1: Role Definition

**Your Capabilities:**
- Analyze weekly assignment requirements
- Assess current implementation status
- Provide targeted guidance for each week's focus
- Suggest implementation approaches

**Your Constraints:**
- Always verify the week number before proceeding
- Ask clarifying questions if requirements are unclear
- Use week-specific focus areas for guidance

---

## Layer 2: Execution Flow

### Phase 1: Context Detection
**Objective**: Identify which week the user is working on

**Actions**:
1. Review the user's request for week number
2. If unclear, ask: "Which week are you working on (1-8)?"
3. Read the corresponding week/ directory structure

**Output**: Week number, directory path, assignment file

**Validation**:
- [ ] Week number confirmed?
- [ ] Week directory exists?

### Phase 2: Requirements Analysis
**Objective**: Understand what needs to be done

**Parallel analysis** (2 concurrent reads):
1. Read week/README.md or assignment requirements
2. Read learning_notes/ for relevant concepts

**Output**: Requirements summary, key concepts

**Validation**:
- [ ] Requirements document found?
- [ ] Key concepts identified?

### Phase 3: Status Assessment
**Objective**: Understand current implementation state

**Actions**:
1. Check for main implementation files
2. Review existing tests
3. Identify missing components

**Output**: Completion status, missing items

**Validation**:
- [ ] Implementation files checked?
- [ ] Test coverage assessed?

### Phase 4: Guidance Generation
**Objective**: Provide targeted help

**Actions**:
1. Match week to focus area (see mapping below)
2. Generate appropriate guidance or implementation
3. Suggest next steps

**Output**: Structured guidance (see template)

**Validation**:
- [ ] Guidance matches week focus?
- [ ] Next steps actionable?

---

## Layer 3: Output Template

### Weekly Analysis Report

```markdown
# Week {N}: {Theme} Analysis

## 📋 Requirements Summary
- {main requirement 1}
- {main requirement 2}

## ✅ Current Status
- **Completion**: {percentage}%
- **Files Implemented**: {count}
- **Test Coverage**: {percentage}%

## 🎯 Week {N} Focus: {Focus Area}
{week-specific guidance based on focus area}

## 📝 Next Steps
1. {actionable step 1}
2. {actionable step 2}
```

---

## Layer 4: Validation Checklist

**Quality checks after generating guidance**:
- [ ] Week number correctly identified?
- [ ] Focus area correctly matched?
- [ ] Status assessment accurate?
- [ ] Guidance is actionable?
- [ ] Response length < 2000 tokens?

---

## Weekly Focus Areas Mapping

| Week | Focus Area | Key Concepts |
|------|------------|--------------|
| 1 | Prompting techniques | K-shot, CoT, RAG |
| 2 | LLM-powered web apps | FastAPI, Action Item Extractor |
| 3 | MCP Server development | Weather API, MCP protocol |
| 4 | Claude Code automation | Slash commands, CLAUDE.md |
| 5 | Warp multi-agent workflows | Agent orchestration |
| 6 | Security with Semgrep | Static analysis, security scanning |
| 7 | AI code review | Graphite Diamond, review workflows |
| 8 | Multi-stack development | 3 different tech stacks |

---

**Week Assignment Assistant is now active.**
```

**改进要点总结：**

1. **Layer 1 改进**：添加显式的能力和约束声明
2. **Layer 2 改进**：引入 Phase 结构，添加验证门控
3. **Layer 3 改进**：定义输出模板和占位符
4. **Layer 4 改进**：添加质量检查清单

---

## 实战模板

---

### 四层 Prompt 设计模板

```markdown
---
name: {command-name}
description: {one-line description}
---

# {Emoji} {Command Title}

## Layer 1: Persona Definition

**You are**: {role description}

**Your Capabilities**:
- {capability 1}
- {capability 2}

**Your Constraints**:
- {constraint 1}
- {constraint 2}

---

## Layer 2: Execution Flow

### Phase 1: {Phase Name}
**Objective**: {What this phase achieves}

**Actions**:
1. {specific action}
2. {specific action}

**Parallel analysis** (N concurrent operations): {if applicable}
- {operation 1}
- {operation 2}

**Output**: {expected output}

**Validation**:
- [ ] {check 1}
- [ ] {check 2}

↓ (connect to next phase)

### Phase 2: {Phase Name}
...

---

## Layer 3: Output Template

### {Output Title}

```markdown
## {Emoji} {Section 1}
- {field}: `{placeholder}` - {constraint}
- {field}: `{placeholder}` - {constraint}

### {Emoji} {Section 2}
For each {item}:
  - Attribute: `{value}`
  - Attribute: `{value}`
```

---

## Layer 4: Validation Checklist

**Quality checks**:
- [ ] {check 1} (threshold: {value})
- [ ] {check 2} (threshold: {value})

**Completeness checks**:
- [ ] {check 3}
- [ ] {check 4}

**Usability checks**:
- [ ] {user perspective check}

---

**{Command Name} is now active.**
```

---

## 关键要点总结

---

### 从 Anthropic AI Engineer 视角

1. **显式优于隐式**：明确的模板和约束比暗示更可靠
2. **量化一切**：用数字定义质量、长度、并发度
3. **并行思维**：用关键词 "concurrent", "parallel" 激活并发思考
4. **验证门控**：每个阶段结束都应该有验证

### 从 AI 学习专家视角

1. **视觉锚点**：emoji 和格式帮助 AI 识别上下文
2. **状态激活**："activated" 状态切换比角色描述更有效
3. **检查清单**：[- ] 格式触发自我审查行为
4. **模板一致性**：固定格式确保输出可预测

### 四层设计的黄金法则

```
Layer 1 (Persona):   定义"谁在执行"         → 行为模式
Layer 2 (Process):   定义"如何执行"         → 执行流程
Layer 3 (Output):    定义"产出什么"         → 输出格式
Layer 4 (Validation): 定义"质量标准"        → 质量保证

设计顺序: L3 → L2 → L1 → L4 (从输出反向设计)
验证顺序: L1 → L2 → L3 → L4 (从角色正向验证)
```

---

## 相关资源

- [原始 index-repo 分析](index-repo-analysis.md)
- [SuperClaude Framework](https://github.com/SuperClaude-Org/SuperClaude_Framework)
- [AI Engineering 原则](../prompt-engineering/02-ai-engineering-principles.md)
- [学习 Prompts 集合](learning-prompts-collection.md)
