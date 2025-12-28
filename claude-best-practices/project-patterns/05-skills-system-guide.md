# Claude Code Skills 系统：完全指南

> 理解 Skills 机制，掌握 AI 能力扩展

---

## 一、核心概念 (Core Concepts)

### 1.1 What is a Skill?

**Skill（技能）** 是 Claude Code 中可复用的 prompt 模板和工具链封装机制。每个 Skill 都是一个自包含的功能单元，可以被 AI 自动发现并在合适的上下文中调用。

#### 核心特点

| 特性 | 说明 |
|------|------|
| **name** | Skill 的唯一标识符，如 `sc:pm`, `document-skills:pdf` |
| **description** | 功能描述，定义何时以及如何使用该 Skill |
| **prompt** | 执行指令的模板，可以是多步骤的复杂流程 |
| **args** | 可选参数，支持用户输入传递 |

#### 为什么 Skills 重要？

```
传统 Prompt 方式：
用户请求 → AI 分析 → 生成回复 → 每次重新思考

Skills 方式：
用户请求 → AI 匹配 Skill → 执行预定义流程 → 一致性输出
                ↓
            可复用、可测试、可优化
```

**核心价值**：
- **可复用性**：一次编写，多处使用
- **可组合性**：Skills 可以调用其他 Skills
- **自动发现**：AI 根据上下文智能选择合适的 Skill
- **一致性**：相同任务产生一致的结果

---

### 1.2 Skill vs CLI Commands

虽然两者看起来相似，但设计理念和使用场景有本质区别。

#### 对比表格

| 维度 | CLI Commands | Skills |
|------|-------------|--------|
| **触发方式** | 用户显式调用（如 `/week`） | AI 自动发现并调用 |
| **文件位置** | `~/.claude/commands/` | `~/.claude/skills/` 或插件目录 |
| **用途** | 特定任务的快捷方式 | 通用能力的封装 |
| **参数传递** | 命令行参数 | 自然语言上下文 |
| **发现机制** | 用户记忆 | 自动语义匹配 |
| **适用场景** | 重复性工作流 | 跨场景复用能力 |
| **YAML 配置** | 必需 | 必需 |
| **资源文件** | 可选 | 常包含（模板、脚本） |

#### 使用场景决策树

```
用户请求
    │
    ├─ 是否是特定项目的重复性工作？
    │   ├─ 是 → CLI Command
    │   │   示例：/test-week, /explore-week
    │   │
    │   └─ 否 → 继续判断
    │
    ├─ 是否是通用能力，可用于多个项目？
    │   ├─ 是 → Skill
    │   │   示例：document-skills:pdf, sc:implement
    │   │
    │   └─ 否 → 继续判断
    │
    ├─ 是否需要 AI 智能判断何时使用？
    │   ├─ 是 → Skill
    │   │   示例：code-reviewer 自动触发
    │   │
    │   └─ 否 → CLI Command
    │
    └─ 需要用户明确控制执行时机 → CLI Command
```

#### 实际示例

```yaml
# CLI Command - 用户主动调用
/sc:pm "恢复昨天的工作会话"
→ PM Agent 立即执行

# Skill - AI 自动发现
"帮我审查这段代码的安全性"
→ AI 匹配到 python-security-expert Skill
→ 自动调用安全审查流程
```

---

### 1.3 Why Skills Matter

#### 1. 认知负载降低

```
无 Skills：每次请求都需要完整描述
用户: "帮我分析代码，找出所有函数，检查它们的命名规范，
      查看参数类型，然后生成一个文档，包含函数签名、
      描述、使用示例..."

有 Skills：简洁意图表达
用户: "生成 API 文档"
→ api-documentor Skill 自动执行完整流程
```

#### 2. 质量一致性

```
手动方式：
第1次：生成了完整的文档
第2次：遗漏了使用示例
第3次：格式不一致

Skill 方式：
每次执行相同的流程 → 一致的质量输出
```

#### 3. 团队协作

```
创建优质 Skill → 团队共享 → 统一工作标准

示例：code-reviewer Skill
- 定义了统一的审查标准
- 所有团队成员使用相同的检查清单
- 代码质量保持一致
```

---

## 二、Skills 的三种类型 (Three Types of Skills)

Claude Code 中的 Skills 分为三类，每种有不同的来源、权限和使用方式。

#### 类型对比总览

| 类型 | 位置 | 来源 | 示例 | 修改权限 | 命名空间 |
|------|------|------|------|----------|----------|
| **User Skills** | `~/.claude/skills/*.md` | 用户创建 | `code-pattern`, `test-helper` | 完全控制 | 简单名称 |
| **Managed Skills** | 系统内置 | SuperClaude 等 | `sc:pm`, `sc:implement` | 只读 | `sc:` 前缀 |
| **Plugin Skills** | 插件目录 | 第三方插件 | `document-skills:pdf` | 只读 | `plugin-name:` 前缀 |

---

### 2.1 User Skills (用户自定义)

**User Skills** 是用户自己创建的技能，存储在用户配置目录中。

#### 文件位置

```bash
# macOS/Linux
~/.claude/skills/
├── code-pattern.md
├── test-helper.md
└── api-documentor.md

# Windows
%APPDATA%\claude\skills\
```

#### 创建权限

| 操作 | 权限 |
|------|------|
| 创建 | ✅ 用户可创建 |
| 修改 | ✅ 完全控制 |
| 删除 | ✅ 用户可删除 |
| 分享 | ✅ 可复制给他人 |

#### 适用场景

- 项目特定的代码模式
- 个人工作流优化
- 实验性功能
- 学习和探索

#### 示例：创建 User Skill

```markdown
---
name: code-pattern
description: "识别项目中的代码模式，推荐最佳实践，生成模式文档。当用户询问代码模式、最佳实践或需要生成模式文档时使用。"
---

# Code Pattern Analyzer

## When to Use

激活此 Skill 当：
- 用户询问 "what patterns are used in this code?"
- 用户请求 "best practices for [feature]"
- 用户想要 "generate pattern documentation"

## Analysis Process

1. **Pattern Discovery**
   - 搜索重复的代码结构
   - 识别架构模式
   - 记录命名约定
   - 记录设计模式

2. **Pattern Classification**
   - Creational Patterns
   - Structural Patterns
   - Behavioral Patterns
   - Project-Specific Patterns

3. **Documentation Generation**
   每个模式包含：
   - Pattern name
   - Problem it solves
   - Implementation example
   - When to use/avoid
```

---

### 2.2 Managed Skills (托管技能)

**Managed Skills** 是由系统或框架（如 SuperClaude）提供的预构建技能。

#### 文件位置

```bash
# SuperClaude 命令（作为 Managed Skills）
~/.claude/commands/sc/
├── pm.md
├── implement.md
├── index-repo.md
└── ...
```

#### 特点

| 特性 | 说明 |
|------|------|
| **来源** | SuperClaude、官方、第三方框架 |
| **更新** | 通过包管理器自动更新 |
| **权限** | 只读（用户不能直接修改） |
| **命名** | 使用前缀（如 `sc:`）避免冲突 |

#### SuperClaude Managed Skills

当前环境中有 **28 个 SuperClaude Skills**：

| Skill | 功能 | 类别 |
|-------|------|------|
| `sc:agent` | Meta-system task orchestration | orchestration |
| `sc:document` | Generate focused documentation | documentation |
| `sc:spawn` | Intelligent breakdown and delegation | orchestration |
| `sc:estimate` | Development estimates with analysis | planning |
| `sc:spec-panel` | Multi-expert specification review | review |
| `sc:index-repo` | 94% token reduction indexing | optimization |
| `sc:implement` | Feature implementation with persona | development |
| `sc:troubleshoot` | Diagnose and resolve issues | debugging |
| `sc:business-panel` | Business Panel Analysis | analysis |
| `sc:improve` | Code quality improvements | optimization |
| `sc:recommend` | Command recommendation engine | utility |
| `sc:explain` | Clear explanations | education |
| `sc:reflect` | Task reflection and validation | quality |
| `sc:analyze` | Comprehensive code analysis | analysis |
| `sc:workflow` | Generate implementation workflows | planning |
| `sc:select-tool` | MCP tool selection | utility |
| `sc:help` | List all /sc commands | utility |
| `sc:load` | Session lifecycle management | session |
| `sc:README` | SuperClaude Commands help | utility |
| `sc:sc` | SuperClaude command dispatcher | core |
| `sc:research` | Adaptive planning and search | research |
| `sc:index` | Project documentation generation | documentation |
| `sc:build` | Build, compile, package projects | build |
| `sc:save` | Session context persistence | session |
| `sc:git` | Git operations with workflow | vcs |
| `sc:task` | Complex task management | task |
| `sc:design` | Architecture and API design | design |
| `sc:pm` | Project manager orchestration | orchestration |
| `sc:cleanup` | Code cleanup and optimization | maintenance |
| `sc:test` | Execute tests with coverage | testing |
| `sc:brainstorm` | Interactive requirements discovery | planning |

---

### 2.3 Plugin Skills (插件技能)

**Plugin Skills** 由第三方插件提供，扩展 Claude Code 的功能。

#### 文件位置

```bash
~/.claude/plugins/cache/<plugin-name>/
└── <version>/
    └── skills/
        ├── theme-factory/
        ├── pdf/
        └── ...
```

#### 特点

| 特性 | 说明 |
|------|------|
| **来源** | 社区插件、第三方扩展 |
| **安装** | 通过插件系统自动安装 |
| **更新** | 随插件更新 |
| **权限** | 只读 |
| **命名** | `plugin-name:skill-name` 格式 |

#### Document Skills Plugin

当前环境中有 **document-skills 插件**，提供 **14 个 Skills**：

| Skill | 功能 | 文件类型 |
|-------|------|----------|
| `document-skills:pdf` | PDF manipulation toolkit | .pdf |
| `document-skills:pptx` | Presentation creation/editing | .pptx |
| `document-skills:xlsx` | Spreadsheet operations | .xlsx, .csv |
| `document-skills:docx` | Document creation/editing | .docx |
| `document-skills:frontend-design` | Frontend interface design | Web UI |
| `document-skills:web-artifacts-builder` | React/Tailwind artifacts | HTML/JS |
| `document-skills:theme-factory` | 10 pre-set themes | Various |
| `document-skills:doc-coauthoring` | Documentation workflow | Docs |
| `document-skills:algorithmic-art` | p5.js generative art | JS |
| `document-skills:internal-comms` | Internal communication | Various |
| `document-skills:skill-creator` | Skill creation guide | Skills |
| `document-skills:canvas-design` | Visual design creation | Images |
| `document-skills:slack-gif-creator` | GIF creation | .gif |
| `document-skills:webapp-testing` | E2E testing with Playwright | Web |
| `document-skills:mcp-builder` | MCP server creation | MCP |
| `document-skills:brand-guidelines` | Anthropic brand assets | Brand |

---

## 三、如何发现 Skills (Discovering Skills)

### 3.1 Using /help Command

最简单的方式是使用内置的帮助命令。

```bash
# 列出所有可用的 commands 和 skills
/help

# 输出示例：
## Available Commands

### Slash Commands
/week          - CS146S course assistance
/explore-week  - Explore week's current state
/test-week     - Run and analyze weekly tests

### Skills (SuperClaude)
sc:pm          - Project manager orchestration
sc:implement   - Feature implementation
sc:index-repo  - Repository indexing
...

### Plugin Skills
document-skills:pdf  - PDF operations
document-skills:pptx - Presentation creation
...
```

---

### 3.2 Checking ~/.claude/skills/

直接查看用户 skills 目录：

```bash
# 列出所有 user skills
ls ~/.claude/skills/

# 查看特定 skill 的内容
cat ~/.claude/skills/code-pattern.md
```

#### 目录结构示例

```
~/.claude/skills/
├── code-pattern.md
│   ├── YAML front matter
│   └── Markdown content
├── test-helper.md
└── api-documentor.md
```

---

### 3.3 Plugin Skills Discovery

查看已安装的插件及其提供的 skills：

```bash
# 查看插件目录
ls ~/.claude/plugins/cache/

# 查看特定插件的 skills
ls ~/.claude/plugins/cache/anthropic-agent-skills/document-skills/*/skills/
```

#### 插件 Skills 结构

```
document-skills/
├── theme-factory/
│   └── SKILL.md
├── pdf/
│   ├── SKILL.md
│   └── resources/
│       └── templates/
└── pptx/
    └── SKILL.md
```

---

## 四、创建自定义 Skills (Creating Custom Skills)

### 4.1 Skill 文件结构

一个完整的 Skill 由以下部分组成：

```
my-custom-skill/
├── SKILL.md                  # 主文件（必需）
│   ├── YAML front matter     # 元数据
│   └── Markdown content      # 指令内容
├── resources/                # 资源文件（可选）
│   ├── templates/            # 代码/文档模板
│   ├── examples/             # 使用示例
│   └── scripts/              # 辅助脚本
└── README.md                 # Skill 文档（可选）
```

#### 最小结构

单个 `.md` 文件即可：

```markdown
---
name: my-skill
description: "What this skill does"
---

# Skill instructions here
```

---

### 4.2 YAML Front Matter 配置

YAML front matter 定义了 Skill 的元数据和调用条件。

#### 必需字段

```yaml
---
name: my-skill-name           # Skill 名称
description: "When to use this skill"
---
```

#### 可选字段

```yaml
---
name: my-skill
description: "Clear description of when to activate"
category: development         # Skill 类别
complexity: intermediate      # beginner/intermediate/advanced
mcp-servers: [context7, sequential]  # 需要的 MCP 工具
personas: [python-expert]     # 需要的 persona
version: "1.0.0"              # Skill 版本
author: "Your Name"           # 作者
license: MIT                  # 许可证
---
```

#### Description 最佳实践

```yaml
# ❌ Bad - 太模糊
description: "Help with code"

# ✅ Good - 明确用途和触发条件
description: "Analyze Python code for PEP8 compliance issues. Use when user asks about code style, linting, or formatting problems in Python files."
```

---

### 4.3 编写 Skill 指令

Skill 内容应该清晰、结构化，并包含执行流程。

#### 内容结构

```markdown
---
name: test-helper
description: "Comprehensive testing assistant for pytest. Use when user needs help with writing tests, improving coverage, or debugging test failures."
---

# Test Helper Skill

## When to Use

激活此 Skill 当用户提及：
- "write tests for..."
- "improve test coverage"
- "debug test failure"
- "pytest [issue]"

**不要在以下情况使用**：
- 集成测试（使用 integration-test skill）
- E2E 测试（使用 e2e-test skill）

## Process

### Phase 1: Understand Requirements
1. 阅读功能代码
2. 识别测试场景
3. 确定覆盖目标

### Phase 2: Design Tests
1. 创建测试文件结构
2. 定义 fixtures
3. 列出测试用例

### Phase 3: Implementation
1. 编写测试代码
2. 添加断言
3. 处理边界情况

### Phase 4: Verification
1. 运行测试
2. 检查覆盖率
3. 修复失败

## Output Format

```python
# tests/test_feature.py
import pytest
from app.services.feature import Service

@pytest.fixture
def sample_data():
    """Create sample test data."""
    return {"key": "value"}

class TestFeature:
    """Test suite for Feature service."""

    def test_success_case(self, sample_data):
        """Test successful execution."""
        result = Service.process(sample_data)
        assert result is not None
```

## Commands Reference

```bash
# Run specific test file
pytest tests/test_feature.py -v

# Run with coverage
pytest --cov=app --cov-report=html

# Run failing tests only
pytest -x
```
```

---

### 4.4 完整示例

#### 示例 1：代码模式分析器

```markdown
---
name: code-pattern
description: "Identify and document code patterns in the project. Use when user asks about code patterns, best practices, or wants to generate pattern documentation."
category: analysis
complexity: intermediate
---

# Code Pattern Analyzer

## Purpose

识别项目中的代码模式，推荐最佳实践，生成可维护的模式文档。

## When to Activate

- 用户询问："what patterns are used in this code?"
- 用户请求："best practices for [feature]"
- 用户想要："generate pattern documentation"

## Analysis Framework

### 1. Pattern Discovery

搜索以下模式类型：

#### Creational Patterns
- Factory / Builder / Singleton
- Dependency Injection patterns
- Repository pattern

#### Structural Patterns
- Adapter / Decorator / Facade
- Composition patterns
- Module organization

#### Behavioral Patterns
- Strategy / Observer / Command
- State machine patterns
- Event handling patterns

#### Project-Specific Patterns
- Custom conventions
- Architecture decisions
- Team standards

### 2. Pattern Documentation Template

```markdown
## Pattern: [Pattern Name]

**Purpose**: What problem does this solve?

**Context**: When is this pattern applicable?

**Implementation**:
\`\`\`python
# Example code showing the pattern
\`\`\`

**Benefits**:
- Benefit 1
- Benefit 2

**Trade-offs**:
- Potential drawback 1
- Mitigation strategy

**Related Patterns**:
- [Pattern A] - complementary approach
- [Pattern B] - alternative approach
```

### 3. Output Structure

生成结构化的模式文档：

1. **Executive Summary**
   - Total patterns found
   - Pattern distribution by category
   - Key insights

2. **Pattern Catalog**
   - Detailed documentation for each pattern
   - Code examples
   - Usage guidelines

3. **Best Practices**
   - Recommended patterns for new code
   - Patterns to avoid
   - Migration guides

## Example Output

See [PROJECT_PATTERNS.md](./PROJECT_PATTERNS.md) for generated documentation.

## Related Skills

- `sc:index-repo` - For repository-wide analysis
- `code-reviewer` - For pattern adherence review
```

---

#### 示例 2：测试助手

```markdown
---
name: test-helper
description: "Comprehensive testing assistant for pytest projects. Use when user needs help with writing tests, improving coverage, or debugging test failures."
category: testing
complexity: beginner
mcp-servers: [serena]
personas: [python-testing-expert]
---

# Pytest Test Helper

## Quick Start

当用户需要测试相关帮助时，激活此 Skill。

## Test Development Checklist

### Before Writing Tests
- [ ] Understand the feature requirements
- [ ] Identify edge cases
- [ ] Set up test fixtures
- [ ] Configure test database

### Test Structure Template

```python
# tests/test_feature.py
import pytest
from app.services.feature import Service

@pytest.fixture
def sample_data():
    """Create sample test data."""
    return {"key": "value"}

class TestFeature:
    """Test suite for Feature service."""

    def test_success_case(self, sample_data):
        """Test successful execution."""
        result = Service.process(sample_data)
        assert result is not None

    def test_error_handling(self):
        """Test error cases."""
        with pytest.raises(ValueError):
            Service.process(invalid_data)
```

### Coverage Targets

| Component | Target | Current | Gap |
|-----------|--------|---------|-----|
| Services  | 90%    | __%     | __% |
| Routers   | 85%    | __%     | __% |
| Models    | 95%    | __%     | __% |

## Commands Reference

```bash
# Run specific test file
pytest tests/test_feature.py -v

# Run with coverage
pytest --cov=app --cov-report=html

# Run failing tests only
pytest -x

# Show print statements
pytest -s

# Run specific test
pytest tests/test_feature.py::TestFeature::test_success_case
```

## Common Patterns

### Async Tests

```python
@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result == expected
```

### Mocking

```python
from unittest.mock import Mock, patch

@patch('app.services.feature.external_api')
def test_with_mock(mock_api):
    mock_api.return_value = {"data": "test"}
    result = Service.process()
    assert mock_api.called
```

### Fixtures

```python
@pytest.fixture
def db_session():
    """Create a test database session."""
    session = create_test_session()
    yield session
    session.close()
    cleanup_test_db()
```

## Debugging Failed Tests

```bash
# Show detailed output
pytest -vv

# Stop on first failure
pytest -x

# Drop into debugger on failure
pytest --pdb

# Show local variables on failure
pytest -l
```
```

---

## 五、当前环境 Skills 完整列表

### 5.1 User Skills (SuperClaude) - 28 skills

| Skill | Description | Category |
|-------|-------------|----------|
| `sc:agent` | Meta-system task orchestration | orchestration |
| `sc:document` | Generate focused documentation | documentation |
| `sc:spawn` | Intelligent breakdown and delegation | orchestration |
| `sc:estimate` | Development estimates with analysis | planning |
| `sc:spec-panel` | Multi-expert specification review | review |
| `sc:index-repo` | Repository indexing (94% token reduction) | optimization |
| `sc:implement` | Feature implementation with persona | development |
| `sc:troubleshoot` | Diagnose and resolve issues | debugging |
| `sc:business-panel` | Business Panel Analysis | analysis |
| `sc:improve` | Code quality improvements | optimization |
| `sc:recommend` | Command recommendation engine | utility |
| `sc:explain` | Clear explanations | education |
| `sc:reflect` | Task reflection and validation | quality |
| `sc:analyze` | Comprehensive code analysis | analysis |
| `sc:workflow` | Generate implementation workflows | planning |
| `sc:select-tool` | MCP tool selection | utility |
| `sc:help` | List all /sc commands | utility |
| `sc:load` | Session lifecycle management | session |
| `sc:README` | SuperClaude Commands help | utility |
| `sc:sc` | SuperClaude command dispatcher | core |
| `sc:research` | Adaptive planning and search | research |
| `sc:index` | Project documentation generation | documentation |
| `sc:build` | Build, compile, package projects | build |
| `sc:save` | Session context persistence | session |
| `sc:git` | Git operations with workflow | vcs |
| `sc:task` | Complex task management | task |
| `sc:design` | Architecture and API design | design |
| `sc:pm` | Project manager orchestration | orchestration |
| `sc:cleanup` | Code cleanup and optimization | maintenance |
| `sc:test` | Execute tests with coverage | testing |
| `sc:brainstorm` | Interactive requirements discovery | planning |

---

### 5.2 Project Skills (CS146S) - 7 skills

| Skill | Description | Use Case |
|-------|-------------|----------|
| `test-week` | Run and analyze tests for a specific week | Testing |
| `review-pr` | PR review (quick/standard/thorough) | Code Review |
| `explore-week` | Deep dive into week's current state | Analysis |
| `week` | CS146S course assignment helper | General |
| `mcp-server` | MCP server development (Week 3) | Development |
| `refactor` | Systematic code cleanup (Week 2) | Refactoring |
| `llm-extract` | LLM extraction functionality (Week 2) | AI Integration |

---

### 5.3 Plugin Skills (document-skills) - 14 skills

| Skill | Description | File Types |
|-------|-------------|------------|
| `document-skills:pdf` | PDF manipulation toolkit | .pdf |
| `document-skills:pptx` | Presentation creation/editing | .pptx |
| `document-skills:xlsx` | Spreadsheet operations | .xlsx, .csv |
| `document-skills:docx` | Document creation/editing | .docx |
| `document-skills:frontend-design` | Frontend interface design | Web UI |
| `document-skills:web-artifacts-builder` | React/Tailwind artifacts | HTML/JS |
| `document-skills:theme-factory` | 10 pre-set themes | Various |
| `document-skills:doc-coauthoring` | Documentation workflow | Docs |
| `document-skills:algorithmic-art` | p5.js generative art | JS |
| `document-skills:internal-comms` | Internal communication | Various |
| `document-skills:skill-creator` | Skill creation guide | Skills |
| `document-skills:canvas-design` | Visual design creation | Images |
| `document-skills:slack-gif-creator` | GIF creation | .gif |
| `document-skills:webapp-testing` | E2E testing with Playwright | Web |
| `document-skills:mcp-builder` | MCP server creation | MCP |
| `document-skills:brand-guidelines` | Anthropic brand assets | Brand |

---

## 六、最佳实践与进阶技巧

### 6.1 Skill Design Principles

#### 1. 单一职责原则 (Single Responsibility)

```yaml
# ✅ Good - 专注单一功能
name: pytest-test-helper
description: "Help with pytest testing"

# ❌ Bad - 太宽泛
name: helper
description: "Help with everything"
```

#### 2. 清晰的触发条件

```yaml
# ✅ Good - 明确的触发条件
description: "Generate API documentation from FastAPI routes.
              Use when user asks for API docs, endpoint documentation,
              or OpenAPI specification."

# ❌ Bad - 模糊的描述
description: "Help with documentation"
```

#### 3. Token 效率

```yaml
# 保持 Skill 文件在合理大小（推荐 < 5000 tokens）
# 使用引用而非重复内容

# ✅ Good - 引用通用模板
See [TEST_TEMPLATE](./resources/test-template.py) for structure.

# ❌ Bad - 重复大段代码
```python
# 100 lines of template code here...
```
```

#### 4. 资源组织

```
my-skill/
├── SKILL.md              # 主文件，保持简洁
└── resources/            # 大型资源放这里
    ├── templates/
    │   └── test-template.py
    ├── examples/
    │   └── basic-test.py
    └── scripts/
        └── setup.sh
```

---

### 6.2 Common Pitfalls

#### 陷阱 1：描述过于宽泛

```yaml
# ❌ Bad - 太宽泛
description: "Help with code"

# ✅ Good - 具体明确
description: "Analyze Python code for PEP8 compliance issues.
              Use when user mentions: 'code style', 'linting',
              'formatting problems', 'PEP8'"
```

#### 陷阱 2：Scope 过大

```yaml
# ❌ Bad - 覆盖范围太大
name: document-generator
description: "Generate all types of documentation"

# ✅ Good - 聚焦特定类型
name: api-documentor
description: "Generate API documentation from FastAPI routes"
```

#### 陷阱 3：缺少上下文

```yaml
# ❌ Bad - 只有代码示例
# [大量代码示例]

# ✅ Good - 包含使用指导
## When to Use
激活此 Skill 当：
- 用户提到 "API documentation"
- 需要 OpenAPI spec
- 生成 endpoint docs

## When NOT to Use
- 用户需要用户手册（use user-guide skill）
- 需要 README（use readme-generator skill）
```

---

### 6.3 高级模式

#### 1. Skill 链式调用

```yaml
---
name: feature-development
description: "Complete feature development workflow"
---

# Feature Development Workflow

## Process

1. **Design Phase**
   → Call `sc:design` for architecture

2. **Implementation Phase**
   → Call `sc:implement` for coding

3. **Testing Phase**
   → Call `test-helper` for tests

4. **Review Phase**
   → Call `code-reviewer` for quality check
```

#### 2. 条件分支

```markdown
## Decision Tree

```
User Request
    │
    ├─ Is it a FastAPI project?
    │   ├─ Yes → Use FastAPI patterns
    │   └─ No  → Check framework
    │
    ├─ Is it a Django project?
    │   ├─ Yes → Use Django patterns
    │   └─ No  → Use generic Python patterns
```
```

#### 3. 可组合的 Skill 片段

```markdown
## Reusable Components

### Test Template Fragment
（在多个 tests 中引用的基础结构）

### Documentation Template Fragment
（文档生成的标准模板）

### Review Checklist Fragment
（代码审查的标准检查清单）
```

---

## 七、总结与资源

### 快速参考

| 主题 | 关键点 |
|------|--------|
| **什么是 Skill** | 可复用的 prompt 模板和工具链 |
| **三种类型** | User, Managed, Plugin |
| **发现方法** | `/help`, `~/.claude/skills/`, 插件目录 |
| **创建方法** | 创建 `.md` 文件 + YAML front matter |
| **最佳实践** | 单一职责、清晰描述、Token 效率 |

### 命名速查

| 类型 | 命名格式 | 示例 |
|------|----------|------|
| User | `simple-name` | `code-pattern` |
| Managed | `prefix:name` | `sc:pm` |
| Plugin | `plugin:name` | `document-skills:pdf` |

### 学习路径

#### 初级（第 1-2 周）
1. 理解 Skill vs Command 区别
2. 阅读现有 Skills（`sc:pm`, `test-helper`）
3. 创建第一个简单 Skill

#### 中级（第 3-4 周）
1. 学习 Skill 设计原则
2. 创建带资源的复杂 Skill
3. 掌握 Skill 链式调用

#### 高级（第 5+ 周）
1. 创建 Skill 组合系统
2. 优化 Token 效率
3. 分享和发布 Skills

### 相关资源

- [Prompt Engineering 分析](../prompt-engineering/01-index-repo-analysis.md)
- [子代理系统](02-subagent-system.md)
- [CLAUDE.md 最佳实践](03-claude-md-best-practices.md)
- [Learning Prompts - Skills 部分](../learning-prompts/README.md#第四部分claude-skills-系统)
- [官方文档](https://docs.anthropic.com/claude-code)

---

**开始创建你的第一个 Skill！** 🚀
