# /sc:git 实战指南：从原理到最佳实践

> **目标读者**：希望深度理解 `/sc:git` 并在实际项目中应用最佳实践的开发者
>
> **前置知识**：基本 Git 操作（add, commit, push, pull）
>
> **阅读时间**：约 25 分钟
>
> **实战价值**：⭐⭐⭐⭐⭐（每日必用）

---

## 📋 目录

1. [为什么需要 /sc:git？](#part-1-为什么需要-scgit深度理解)
2. [核心功能深度解析](#part-2-核心功能深度解析)
3. [实战场景演练](#part-3-实战场景step-by-step)
4. [最佳实践与决策框架](#part-4-最佳实践与决策框架)
5. [进阶技巧](#part-5-进阶技巧)
6. [速查表](#part-6-速查表)

---

## Part 1: 为什么需要 /sc:git？（深度理解）

### 1.1 传统 Git 工作流的痛点

让我们先看看传统方式的问题：

#### **痛点 1：Commit Message 编写困难**

```bash
# ❌ 传统方式：纠结写什么
$ git commit -m "update"
# 或者更糟糕：
$ git commit -m "fix bug"
# 或者：
$ git commit -m "update stuff"
# 问题：一周后你自己都看不懂改了什么
```

**为什么难？**
- 需要遵循团队规范（Conventional Commits）
- 需要总结变更内容（抽象能力）
- 需要用英文表达（语言障碍）
- 需要格式正确（type/syntax）

#### **痛点 2：忘记 add 文件或提交错误内容**

```bash
# ❌ 传统方式：容易遗漏
$ git add app.py
$ git commit -m "add new feature"
# 提交后发现：忘记 add tests/test_app.py
# 或者：不小心把 .env 也加进去了
```

**后果：**
- 后续修复 commit（使用 `--amend` 或新 commit）
- Commit history 不清晰
- 可能泄露敏感信息（.env 文件）

#### **痛点 3：缺乏一致性的工作流**

```bash
# 团队成员 A 的习惯
$ git commit -m "add feature"

# 团队成员 B 的习惯
$ git commit -m "feat: add user auth"

# 团队成员 C 的习惯
$ git commit -m "feature/add-user-auth"

# 问题：CI/CD 工具无法识别，无法自动生成 CHANGELOG
```

#### **痛点 4：重复性命令输入**

```bash
# 每次都要输入
$ git status
$ git add .
$ git commit -m "..."  # 还要想 message
$ git push
```

---

### 1.2 /sc:git 的解决方案

`/sc:git` 通过 **AI 驱动的自动化** 解决以上所有问题：

#### **✅ Smart Commits：自动生成规范的 Commit Message**

```bash
# ✅ /sc:git 方式
$ /sc:git commit --smart-commit

# AI 自动分析代码变更：
# - 检测到 app/routers/auth.py 是新增的认证路由
# - 检测到 tests/test_auth.py 是对应测试
# - 识别为新功能（feat）

# 自动生成：
"feat(auth): add user authentication endpoint

- Implement JWT-based authentication
- Add login/logout endpoints
- Include comprehensive tests

Closes #123"
```

**对比：**
- ❌ 传统：`git commit -m "update"` （2 秒，但无信息）
- ✅ `/sc:git`：自动生成规范的 commit message（3 秒，信息完整）

#### **✅ Status Analysis：智能状态分析 + 建议**

```bash
$ /sc:git status

📊 Repository Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Branch: feature/add-tags
Changes: 3 modified, 1 new file

📝 Modified Files:
  • week2/app/routers/notes.py (+12 lines)
  • week2/app/models.py (+5 lines)
  • week2/tests/test_notes.py (+8 lines)

✨ New Files:
  • week2/app/routers/tags.py

💡 AI 建议:
  检测到两个逻辑变更：
  1. Add tags feature (tags.py, models.py)
  2. Update notes to use tags (notes.py, test_notes.py)

  推荐拆分为两个提交：
  Step 1: git add week2/app/tags.py week2/app/models.py
         /sc:git commit --smart-commit
  Step 2: git add week2/app/notes.py week2/tests/test_notes.py
         /sc:git commit --smart-commit

🚀 Next Steps:
  /sc:git commit --smart-commit --interactive
```

**对比：**
- ❌ 传统 `git status`：只告诉你"有 3 个修改，1 个新增"
- ✅ `/sc:git status`：告诉你"为什么有变更" + "接下来做什么"

#### **✅ Workflow Optimization：最佳实践自动化**

```bash
$ /sc:git checkout -b add-user-auth

✨ Branch Created: add-user-auth
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Branch Type: feature
🎯 Base Branch: master

💡 Best Practices:
  1. Keep changes focused on single feature
  2. Write descriptive commits
  3. Update tests as you go
  4. Delete branch after merging

📝 Suggested Commit Prefix:
  feat(auth): ...
```

---

### 1.3 设计哲学

理解设计哲学，有助于你正确使用 `/sc:git`：

#### **🎯 AI-First：让 AI 做它擅长的事**

```
┌─────────────────────────────────────────┐
│        人机协作的黄金分工                   │
└──────────────────┬──────────────────────┘
                   │
         ┌─────────┼─────────┐
         │         │         │
    ┌────▼────┐ ┌──▼───┐ ┌──▼─────┐
    │  人类   │ │  AI  │ │  Git  │
└───┬────────┘ └──┬───┘ └──┬─────┘
    │             │         │
  ✅ 决策        ✅ 分析    ✅ 存储
  ✅ 审查        ✅ 生成    ✅ 历史
  ✅ 创造        ✅ 模式    ✅ 分支
```

**AI 擅长的：**
- ✅ 分析代码模式（识别 feat/fix/docs）
- ✅ 生成规范格式（Conventional Commits）
- ✅ 检测潜在问题（敏感文件、测试缺失）

**人类擅长的：**
- ✅ 决策"是否提交"（review AI 的建议）
- ✅ 理解业务上下文（为什么这样改）
- ✅ 处理复杂情况（冲突、回滚）

#### **📐 Convention over Configuration：遵循业界标准**

```yaml
/sc:git 的设计原则:
  默认行为:
    - Conventional Commits 规范
    - Feature Branch 工作流
    - 标准的分支命名 (feat-*, fix-*, hotfix-*)

  可定制性:
    - 自定义 type 列表
    - 项目特定的 scope
    - 集成 JIRA/Linear ticket
```

**好处：**
- ✅ 开箱即用（无需配置）
- ✅ 跨项目一致性（团队协作友好）
- ✅ 工具生态兼容（CI/CD, CHANGELOG 生成）

#### **🚀 Progressive Enhancement：渐进式增强**

```
Level 1: 基础使用
  /sc:git commit --smart-commit
  → 自动生成 commit message

Level 2: 交互式使用
  /sc:git commit --interactive
  → 逐步确认每个文件

Level 3: 工作流集成
  /sc:git status (自动检查)
  /sc:git push (自动更新 PR)

Level 4: 多代理协作
  Agent A: 开发
  Agent B: 测试
  Agent C: /sc:git commit
  Agent D: /sc:git push
```

---

## Part 2: 核心功能深度解析

### 2.1 Smart Commits（智能提交）

#### **工作原理：**

```
[代码变更]
     ↓
[1. 文件类型分析]
     ├─ app/routers/*.py → feat/fix (API 变更)
     ├─ tests/*.py → test (测试)
     ├─ README.md → docs (文档)
     └─ pyproject.toml → chore (配置)
     ↓
[2. 内容差异分析]
     ├─ 新增函数 → feat
     ├─ 修改逻辑 → fix/refactor
     ├─ 删除代码 → refactor
     └─ 格式调整 → style
     ↓
[3. Scope 提取]
     ├─ 路径提取：app/routers/auth.py → auth
     ├─ 模块提取：app/models.py → models
     └─ 上下文推断：相关文件 → 统一 scope
     ↓
[4. Message 生成]
     <type>(<scope>): <subject>

     <body>

     <footer>
```

#### **实现细节：**

**如何识别变更类型？**

```python
# 伪代码示例
def detect_change_type(diff):
    if "def new_function" in diff:
        return "feat"
    elif "fix bug" in diff or "resolve issue" in diff:
        return "fix"
    elif "# TODO" in diff or "FIXME" in diff:
        return "fix"
    elif "refactor" in diff or "simplify" in diff:
        return "refactor"
    elif file.path.endswith(".md"):
        return "docs"
    elif file.path == "tests/":
        return "test"
    else:
        return "chore"
```

**如何生成 Scope？**

```python
# 伪代码示例
def extract_scope(file_path):
    # 从路径提取
    if "app/routers/auth.py":
        return "auth"
    if "app/db.py":
        return "db"

    # 从模块名提取
    if "models.py":
        return "models"

    # 从上下文推断
    related_files = get_related_files(file_path)
    if all(f.startswith("app/api/") for f in related_files):
        return "api"

    return None  # 没有 scope
```

#### **实战案例：**

**场景：你修改了认证相关的代码**

```bash
# 传统方式
$ git commit -m "update auth"

# /sc:git 方式
$ /sc:git commit --smart-commit

# AI 分析：
# 文件 1: app/routers/auth.py (+15 lines)
#   - 新增 login_token 函数
#   - 修改 verify_password 函数
# 文件 2: tests/test_auth.py (+20 lines)
#   - 新增测试 login_token

# AI 推断：
# - 新增函数 → feat
# - 路径 routers/auth.py → scope: auth
# - 关键词 login_token, verify_password → subject: add token-based authentication

# 生成：
"feat(auth): add token-based authentication

- Implement login_token endpoint for JWT tokens
- Update verify_password to use bcrypt
- Add comprehensive tests for token flow

Closes #45"
```

---

### 2.2 Status Analysis（状态分析）

#### **超越 git status：**

```bash
# ❌ 传统 git status
$ git status
On branch master
Changes not staged for commit:
  modified:   app.py
  modified:   models.py
  modified:   tests/test_app.py

# 问题：
# - 改了什么？不知道
# - 为什么要改？不知道
# - 接下来做什么？不知道
```

```bash
# ✅ /sc:git status
$ /sc:git status

📊 Repository Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 Branch: master
📝 Changes: 3 files modified

🔍 Change Summary:
  • app.py (+25 lines, -5 lines)
    ├─ Added: export_data() function
    └─ Modified: process_request() to handle CSV export

  • models.py (+8 lines)
    └─ Added: ExportData model

  • tests/test_app.py (+35 lines)
    └─ Added: test_export_data()

💡 Detected Intent:
  You're implementing a CSV export feature.

⚠️  Pre-commit Checks:
  ✓ All changes staged
  ✓ No sensitive files detected
  ⚠️  tests/test_app.py has 2 failing tests

🚀 Recommended Next Steps:
  1. Fix failing tests: poetry run pytest tests/test_app.py::test_export_data
  2. Review changes: /sc:git diff
  3. Commit: /sc:git commit --smart-commit

💬 Commit Preview:
  feat(data): add CSV export functionality

  - Implement export_data() endpoint
  - Add ExportData model
  - Include comprehensive tests
```

#### **智能建议引擎：**

**检测未完成的工作：**

```bash
$ /sc:git status

⚠️  Unfinished Work Detected:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Found TODO comments:
  • app.py:45 - TODO: Add error handling
  • app.py:78 - FIXME: Refactor this function

💡 Suggestion:
  Consider completing these before committing, or create follow-up issues.
```

**推荐拆分提交策略：**

```bash
$ /sc:git status

💡 Suggested Split Strategy:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Detected 2 logical changes:

  Commit 1: Add database schema
    Files: app/models.py, migrations/001_add_users.sql
    Suggested message: feat(db): add user schema

  Commit 2: Implement authentication
    Files: app/auth.py, tests/test_auth.py
    Suggested message: feat(auth): add JWT authentication

Run:
  $ git add app/models.py migrations/
  $ /sc:git commit --smart-commit
  $ git add app/auth.py tests/
  $ /sc:git commit --smart-commit
```

**预警潜在问题：**

```bash
$ /sc:git status

🚨 Security Warning:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  Possible sensitive data detected:
  • .env contains API keys
  • config.py has hardcoded passwords

💡 Recommendations:
  - Remove these files from commit
  - Add to .gitignore
  - Use environment variables instead

Continue anyway? [y/N]
```

---

### 2.3 Workflow Optimization（工作流优化）

#### **最佳实践自动化：**

**提交前检查清单：**

```bash
$ /sc:git commit --smart-commit

✅ Pre-commit Checklist:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ All changes staged
✓ No sensitive files (.env, secrets)
✓ Commit message follows Conventional Commits
⚠️  3 tests failing

💡 Recommendation:
  Run tests first: poetry run pytest
  or
  Commit with --no-verify (not recommended)

Continue? [y/N]
```

**分支命名规范：**

```bash
$ /sc:git checkout -b user-auth

⚠️  Branch Naming Suggestion:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Your branch name: user-auth

Suggested: feature/user-auth
          or: feat/user-auth

Reason: Feature branches should start with 'feature/' or 'feat-'

Use suggested name? [y/N]
```

**合并策略建议：**

```bash
$ /sc:git merge feature/add-tags

🔀 Merge Strategy: feature/add-tags → master
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ No conflicts detected
✓ Tests passing

📝 Suggested merge commit:
  "Merge feature/add-tags into master

  Implements tags feature for notes:
  - Add tag creation endpoint
  - Add tag filtering on notes
  - Include comprehensive tests

  Closes #123"

Accept? [y/N]
```

#### **集成能力：**

**与 CI/CD 集成：**

```yaml
# .github/workflows/auto-version.yml
name: Auto Version

on:
  push:
    branches: [master]

jobs:
  version:
    runs-on: ubuntu-latest
    steps:
      - name: Parse commit messages
        run: |
          # /sc:git 生成的 Conventional Commits
          # 自动触发版本号更新
          if git log -1 --pretty=%B | grep "^feat:"; then
            echo "MINOR=true" >> $GITHUB_ENV
          elif git log -1 --pretty=%B | grep "^fix:"; then
            echo "PATCH=true" >> $GITHUB_ENV
          fi
```

**与 Warp 自动化结合：**

```bash
# Warp saved prompt
name: Git Commit Flow
prompt: |
  Run through the full commit workflow:
  1. Check status: /sc:git status
  2. Stage files: git add .
  3. Commit: /sc:git commit --smart-commit
  4. Push: /sc:git push

  Review each step before proceeding.
```

**多代理工作流支持：**

```
┌─────────────────────────────────────────┐
│       Multi-Agent Git Workflow            │
└──────────────────┬──────────────────────┘
                   │
         ┌─────────┼─────────┐
         │         │         │
    ┌────▼────┐ ┌──▼───┐ ┌──▼─────┐
    │Agent A  │ │Agent B│ │Agent C │
└───┬────────┘ └──┬───┘ └──┬─────┘
    │开发功能    │运行测试 │ /sc:git│
    │           │       │ 提交   │
    ↓           ↓       ↓
  新代码    测试通过  规范commit
```

---

## Part 3: 实战场景（Step-by-Step）

### 场景 1：日常开发循环（个人项目）

#### **完整工作流：**

```bash
# Step 1: 开始工作前 - 检查状态
$ /sc:git status

✅ Working directory clean
📍 Branch: master
📅 Last commit: 2 hours ago

💡 Ready to start new work!

# Step 2: 创建功能分支
$ /sc:git checkout -b feature/add-notes-search

✨ Branch Created: feature/add-notes-search
📋 Branch Type: feature
🎯 Base Branch: master

# Step 3: 编写代码...
[你的开发工作]
- 修改 app/routers/notes.py
- 添加搜索功能
- 更新 tests/test_notes.py

# Step 4: 提交变更
$ /sc:git status

📊 Repository Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Modified: app/routers/notes.py (+25 lines)
Modified: tests/test_notes.py (+15 lines)

💡 Detected Intent:
  Implementing search functionality for notes

🚀 Next Steps:
  $ /sc:git commit --smart-commit

$ /sc:git commit --smart-commit

✅ Commit Created!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"feat(notes): add search functionality

- Implement full-text search on notes
- Add query parameters for filtering
- Include comprehensive tests

Tests: 15/15 passing"

# Step 5: 推送到远程
$ /sc:git push

✅ Pushed to origin/feature/add-notes-search
🔗 Create PR: https://github.com/.../compare
```

#### **实战技巧：**

**何时拆分提交？**

```bash
# ❌ 坏例子：所有变更一次性提交
$ /sc:git commit --smart-commit
# 结果：feat: add search, refactor auth, fix tests
# 问题：混合了多个逻辑变更

# ✅ 好例子：拆分为多个提交
$ /sc:git status

💡 Suggested Split:
  Commit 1: Refactor authentication
    Files: app/auth.py
  Commit 2: Add search functionality
    Files: app/notes.py, tests/test_notes.py

$ git add app/auth.py
$ /sc:git commit --smart-commit
# → "refactor(auth): simplify login flow"

$ git add app/notes.py tests/
$ /sc:git commit --smart-commit
# → "feat(notes): add search functionality"
```

**如何修复遗漏的文件？**

```bash
# 场景：提交后发现忘记 add 某个文件

$ /sc:git commit --smart-commit
# → "feat(api): add user endpoint"

# 发现：忘记 tests/test_api.py

# 方法 1: Amend（如果还没 push）
$ git add tests/test_api.py
$ /sc:git commit --amend --smart-commit
# → "feat(api): add user endpoint" (更新了 body)

# 方法 2: 新 commit（如果已经 push）
$ git add tests/test_api.py
$ /sc:git commit --smart-commit
# → "test(api): add tests for user endpoint"
```

**什么时候用 `--amend`？**

```yaml
✅ 使用 amend 的场景:
  - 忘记 add 相关文件
  - Commit message 有错别字
  - 小的代码调整（1-2 行）
  - 还没有 push 到远程

❌ 不要使用 amend 的场景:
  - 已经 push 到远程（会改写历史）
  - 大的代码变更（应该新 commit）
  - 团队协作中其他人可能基于此 commit 工作
```

---

### 场景 2：团队协作工作流

#### **Feature Branch Workflow：**

```bash
# Step 1: 同步最新代码
$ /sc:git pull origin master

✅ Pulled 3 new commits from origin/master

# Step 2: 创建功能分支
$ /sc:git checkout -b feature/user-profile

✨ Branch Created: feature/user-profile
💡 Tip: Keep changes focused on single feature

# Step 3: 开发与提交
[编写代码...]

$ /sc:git commit --smart-commit

✅ Commit Created!
"feat(profile): add user profile page

- Implement profile view
- Add avatar upload
- Include unit tests

Closes #45"

# Step 4: 推送并创建 PR
$ /sc:git push -u origin feature/user-profile

✅ Pushed to origin/feature/user-profile
🔗 Create PR: https://github.com/repo/pull/new

# Step 5: 处理反馈
[收到 review 评论，修改代码...]

$ /sc:git commit --smart-commit

✅ Commit Created!
"fix(profile): resolve avatar upload issue

Reviewer feedback:
- Fix file validation
- Add error handling

Fixes #47"

$ /sc:git push

# Step 6: 合并后清理分支
$ /sc:git checkout master
$ /sc:git pull origin master
$ /sc:git branch -d feature/user-profile

✅ Branch deleted: feature/user-profile
```

#### **Code Review 最佳实践：**

**Commit message 帮助 reviewer 理解变更：**

```bash
# ❌ 坏的 commit message
$ git log --oneline
abc123 fix stuff
def456 update
ghi789 add feature

# Reviewer 看到后：
# - "fix stuff" 修了什么？
# - "update" 更新了什么？
# - "add feature" 添加了什么功能？

# ✅ 好的 commit message（/sc:git 生成）
$ git log --oneline
abc123 fix(auth): resolve JWT token expiration
def456 refactor(db): optimize query performance
ghi789 feat(api): add rate limiting

# Reviewer 看到后：
# - 认证模块的 JWT token 过期问题修复
# - 数据库查询性能优化
# - API 新增了限流功能
```

**拆分大 PR 为多个逻辑提交：**

```bash
# ❌ 坏例子：一个 huge commit
$ git log --stat
commit abc123
Author: You
Date: ...

  feat: add user system

  app/routers/auth.py     | 150 +++++++++++++++++++
  app/routers/user.py     | 200 ++++++++++++++++++++
  app/models.py           | 100 +++++++++++
  tests/test_auth.py      | 120 +++++++++++++
  tests/test_user.py      | 130 +++++++++++++
  docs/api.md             |  50 ++++++
  7 files changed, 750 insertions(+)

# Reviewer 看到后：
# - 750 行代码，一次性 review 压力大
# - 认证 + 用户功能混在一起
# - 难以逐个功能审查

# ✅ 好例子：拆分为多个 commit
$ git log --oneline
abc123 docs(user): document user API
def456 test(user): add user endpoint tests
ghi789 feat(user): add user profile endpoint
jkl012 refactor(db): extract user model
mno345 feat(auth): add JWT authentication

# Reviewer 看到后：
# - 每个 commit 职责清晰
# - 可以逐个 review
# - 容易理解演进过程
```

**使用 Interactive Rebase 清理历史：**

```bash
# 场景：在 PR 之前清理 commit 历史
$ git log --oneline
abc345 fix typo
abc344 fix another typo
abc343 wip
abc342 feat: add feature
abc341 init

# 使用 interactive rebase
$ /sc:git rebase -i HEAD~5

# /sc:git 会提供引导
🔀 Interactive Rebase: Last 5 Commits
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
abc345 fix typo
abc344 fix another typo
abc345 wip
abc346 feat: add feature
abc347 init

💡 Suggested Actions:
  - Squash abc345, abc344, abc343 → "feat: add feature"
  - Keep abc342, abc341 separate

Apply suggested? [y/N]

# 结果：清理后的历史
$ git log --oneline
def123 feat: add feature
abc124 init
```

---

### 场景 3：紧急修复流程（Hotfix）

#### **Hotfix Workflow：**

```bash
# Step 1: 从 master 创建 hotfix 分支
$ /sc:git checkout master
$ /sc:git pull origin master
$ /sc:git checkout -b hotfix/critical-security-fix

✨ Branch Created: hotfix/critical-security-fix
🚨 Priority: HIGH
💡 Keep changes minimal and focused

# Step 2: 快速修复
[修复代码...]

# Step 3: 提交（使用 fix 类型）
$ /sc:git commit --smart-commit

✅ Commit Created!
"fix(security): resolve SQL injection vulnerability

- Sanitize user input in search query
- Add parameterized queries
- Include regression tests

Security: CVE-2024-XXXX
Critical: YES"

# Step 4: 推送与 PR
$ /sc:git push -u origin hotfix/critical-security-fix

✅ Pushed to origin/hotfix/critical-security-fix
🔗 Create PR: https://github.com/repo/pull/new

# Step 5: 合并回 master
$ /sc:git checkout master
$ /sc:git merge hotfix/critical-security-fix --fast-forward

✅ Merged hotfix into master
📝 Merge commit generated

# Step 6: 合并回 develop（如果存在）
$ /sc:git checkout develop
$ /sc:git merge hotfix/critical-security-fix

✅ Merged hotfix into develop

# Step 7: 打 tag 并发布
$ /sc:git tag -a v1.2.1 -m "Hotfix: Security patch"

✅ Tag created: v1.2.1
📦 Release notes:
  - Security: SQL injection fix
  - Severity: Critical

# Step 8: 清理
$ /sc:git branch -d hotfix/critical-security-fix
$ /sc:git push origin --tags

✅ Branch deleted
✅ Tags pushed
```

#### **/sc:git 在 Hotfix 中的作用：**

**快速生成规范的 commit message：**

```bash
# ❌ 传统方式：压力大，容易出错
$ git commit -m "fix"
# 或：
$ git commit -m "urgent fix"

# ✅ /sc:git 方式：自动生成详细 message
$ /sc:git commit --smart-commit
# → "fix(security): resolve SQL injection vulnerability
#
#     - Sanitize user input
#     - Add parameterized queries
#     - Include regression tests
#
#     Security: CVE-2024-XXXX"
```

**自动检测遗漏的测试文件：**

```bash
$ /sc:git commit --smart-commit

⚠️  Warning: No test files detected
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This is a critical security fix. Are you sure you don't need tests?

Continue anyway? [y/N]

# 你想起：确实需要添加回归测试
# 取消 commit，添加测试，重新提交
```

**智能建议合并策略：**

```bash
$ /sc:git merge hotfix/critical-security-fix

💡 Merge Strategy Recommendation:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This is a critical hotfix. Suggested strategy:
  - Use --fast-forward for master
  - Use --no-ff for develop (to preserve hotfix history)

Apply suggested? [y/N]
```

---

### 场景 4：代码审查与合并

#### **作为 Reviewer：**

```bash
# Step 1: 查看 PR 的 commit 历史
$ /sc:git log origin/feature/add-tags --oneline

abc123 feat(tags): add tag filtering
def456 feat(tags): add tag creation endpoint
ghi789 refactor(notes): extract tag logic

# ✅ 通过 /sc:git 生成的 commit message：
# - 清晰的演进过程
# - 每个 commit 的 scope 和目的明确
# - 容易理解代码结构

# Step 2: 查看某个 commit 的详细信息
$ /sc:git show abc123

✅ Commit: abc123
Type: feat
Scope: tags
Subject: add tag filtering

Changes:
  app/routers/tags.py | +25 lines
  tests/test_tags.py  | +15 lines

Commit Message:
  "feat(tags): add tag filtering

  - Implement ?tag=xxx query parameter
  - Support multiple tags: ?tag=python&tag=tutorial
  - Include unit tests

  Closes #78"

# Step 3: Review 代码
[查看 diff，留下评论...]

# Step 4: 批准或请求修改
```

#### **作为 Maintainer：**

```bash
# Step 1: 合并 PR
$ /sc:git merge feature/add-tags --interactive

🔀 Merge Interactive Mode
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Branch: feature/add-tags → master

✓ No conflicts detected
✓ All checks passing

📝 Suggested Merge Commit:
  "Merge feature/add-tags into master

  Implements tags feature for notes:
  - Add tag creation endpoint
  - Add tag filtering on notes
  - Extract tag logic from notes module
  - Include comprehensive tests

  Commits: 3
  Files changed: 8
  Lines added: 150
  Tests added: 45

  Closes #78, #79"

Accept? [y/N]

# Step 2: 推送
$ /sc:git push origin master

✅ Pushed to origin/master
✅ PR #78 automatically closed (by "Closes #78")
```

---

## Part 4: 最佳实践与决策框架

### 4.1 何时使用 /sc:git？

#### **✅ 推荐使用（90% 的场景）：**

```yaml
日常开发提交:
  适用条件:
    - 需要规范的 commit message
    - 希望获得 AI 的建议
    - 团队协作项目
  示例命令:
    - /sc:git commit --smart-commit
    - /sc:git status

功能开发:
  适用条件:
    - 新功能、bug 修复
    - 需要清晰的变更历史
  示例命令:
    - /sc:git checkout -b feature-*
    - /sc:git commit --smart-commit

Code Review:
  适用条件:
    - 作为 reviewer 查看变更
    - 作为 maintainer 合并 PR
  示例命令:
    - /sc:git show <commit>
    - /sc:git merge --interactive
```

#### **❌ 不推荐使用（10% 的场景）：**

```yaml
快速临时提交（WIP）:
  原因:
    - 不需要规范的 message
    - 可能会被 squash 或 rebase
  替代方案:
    - git commit -m "wip"
    - git commit -m "tmp"

脚本自动化:
  原因:
    - 脚本需要完全控制
    - /sc:git 的交互性不适合
  替代方案:
    - 直接使用 git 命令
    - 或使用 GitPython 等库

完全控制 message 格式:
  原因:
    - /sc:git 有自己的格式
    - 可能与你的需求不匹配
  替代方案:
    - 自定义 /sc:git 模板
    - 或使用原生命令

性能敏感场景:
  原因:
    - AI 分析需要时间
    - 大批量操作不适合
  示例:
    - 批量重命名文件
    - 历史重写
  替代方案:
    - 使用 git 原生命令
    - 或编写专门的脚本
```

#### **决策树：**

```
需要提交代码？
    │
    ├─ 是 → 日常开发？
    │       │
    │       ├─ 是 → ✅ 使用 /sc:git commit --smart-commit
    │       │
    │       └─ 否 → 临时提交？
    │               │
    │               ├─ 是 → ❌ 使用 git commit -m "wip"
    │               │
    │               └─ 否 → 脚本自动化？
    │                       │
    │                       ├─ 是 → ❌ 使用 git 原生命令
    │                       │
    │                       └─ 否 → ✅ 使用 /sc:git
    │
    └─ 否 → 需要查看状态？
            │
            └─ 是 → ✅ 使用 /sc:git status
```

---

### 4.2 常见陷阱与解决方案

#### **陷阱 1：过度依赖自动化**

**症状：**
```bash
$ /sc:git commit --smart-commit
# AI 生成："feat(api): add user endpoint"

# 你没有 review，直接 push
# 后来发现：AI 把类型识别错了，应该是 fix 而不是 feat
```

**解决方案：**
```bash
# ✅ 好习惯：review AI 的建议
$ /sc:git commit --smart-commit

✅ Commit Generated:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Type: feat
Scope: api
Subject: add user endpoint

Full message:
  "feat(api): add user endpoint"

Accept? [y/N or e to edit]

# 你可以：
# - y: 接受
# - N: 拒绝，手动输入
# - e: 编辑 AI 的建议
```

#### **陷阱 2：忘记预检查**

**症状：**
```bash
$ /sc:git commit --smart-commit
# 提交了
# 后来发现：忘记更新测试
# 或者：把 .env 也提交了
```

**解决方案：**
```bash
# ✅ 好习惯：提交前先 status
$ /sc:git status

📊 Repository Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Modified: app.py
Modified: tests/test_app.py  ← AI 检测到测试
Modified: .env                ← AI 警告敏感文件

⚠️  Warning:
  .env contains sensitive data

💡 Recommendation:
  - Remove .env from commit
  - Add to .gitignore

Proceed with commit? [y/N]
```

#### **陷阱 3：分支管理混乱**

**症状：**
```bash
$ git branch
* feature/add-auth
  feature/add-profile
  feature/user-page
  fix/login-bug
  refactor-api
  temp-stuff
# 问题：太多未合并的分支
```

**解决方案：**
```bash
# ✅ 好习惯：定期清理
$ /sc:git status

💡 Branch Cleanup:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Detected 5 feature branches:
  - feature/add-auth (merged, can delete)
  - feature/add-profile (stale, 30 days old)
  - feature/user-page (active, recent commits)
  - fix/login-bug (merged, can delete)
  - refactor-api (abandoned, no commits)

Suggested actions:
  $ git branch -d feature/add-auth
  $ git branch -d fix/login-bug
  $ git branch -D refactor-api

Apply cleanup? [y/N]

# 同时，遵循分支命名规范
$ /sc:git checkout -b feature/new-auth

✨ Branch Created: feature/new-auth
📋 Follows naming convention: feature/*
```

---

### 4.3 与其他工具集成

#### **与 Warp：**

**创建 Saved Prompt：**

```bash
# Warp saved prompt
name: "Git Commit with /sc:git"
description: "Full commit workflow using /sc:git"
prompt: |
  Run the following git workflow:
  1. Check status: /sc:git status
  2. Review changes: /sc:git diff
  3. Stage files: git add .
  4. Commit with AI: /sc:git commit --smart-commit
  5. Push: /sc:git push

  After each step, pause for confirmation.
  If any step fails, stop and ask for guidance.
```

**集成到工作流自动化：**

```bash
# Warp workflow
name: "Feature Development"
steps:
  - name: "Start new feature"
    command: "/sc:git checkout -b feature/${feature_name}"

  - name: "Development"
    # 你的开发工作...

  - name: "Commit changes"
    command: "/sc:git commit --smart-commit"

  - name: "Push and create PR"
    command: "/sc:git push -u origin ${branch_name}"
```

#### **与 CI/CD：**

**自动触发版本号：**

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    branches: [master]

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - name: Parse commit type
        id: parse
        run: |
          # /sc:git 生成的 Conventional Commits
          TYPE=$(git log -1 --pretty=%B | grep -oE "^(feat|fix|docs|refactor|test|chore):" | cut -d: -f1)

          if [ "$TYPE" = "feat" ]; then
            echo "INCREMENT=minor" >> $GITHUB_OUTPUT
          elif [ "$TYPE" = "fix" ]; then
            echo "INCREMENT=patch" >> $GITHUB_OUTPUT
          else
            echo "INCREMENT=none" >> $GITHUB_OUTPUT
          fi

      - name: Create release
        if: steps.parse.outputs.INCREMENT != 'none'
        run: |
          # 使用 semantic-release 或类似工具
          npm version ${{ steps.parse.outputs.INCREMENT }}
          git push --tags
```

**Commit message 触发 CI 流程：**

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [master]

jobs:
  check-commit:
    runs-on: ubuntu-latest
    steps:
      - name: Check for deployment marker
        id: check
        run: |
          # /sc:git 生成的 commit message
          MESSAGE=$(git log -1 --pretty=%B)

          if echo "$MESSAGE" | grep -q "\[deploy\]"; then
            echo "should_deploy=true" >> $GITHUB_OUTPUT
          fi

      - name: Deploy to production
        if: steps.check.outputs.should_deploy == 'true'
        run: |
          # 部署逻辑
          ./deploy.sh
```

#### **与 GitHub/GitLab：**

**自动关闭 Issue：**

```bash
# /sc:git 生成的 commit message
$ /sc:git commit --smart-commit

✅ Commit Generated:
"feat(auth): add JWT authentication

- Implement login endpoint
- Add token refresh logic
- Include comprehensive tests

Closes #123"

# Push 到 GitHub 后，Issue #123 自动关闭
```

**生成 CHANGELOG：**

```bash
# 使用 conventional-changelog 工具
# 配合 /sc:git 的 Conventional Commits

$ npm install -g conventional-changelog

$ conventional-changelog -p angular -i CHANGELOG.md -s

# 自动生成：
# ## 1.2.0 (2024-01-05)
#
# ### Features
# - **auth:** add JWT authentication (#123)
# - **notes:** add search functionality (#45)
#
# ### Bug Fixes
# - **db:** resolve connection timeout (#67)
```

**关联 Code Review：**

```bash
# 在 GitLab CI 中
# .gitlab-ci.yml
code_quality:
  script:
    - /sc:git status
    - /sc:git diff HEAD~1 | quality-check
  only:
    - merge_requests
```

---

## Part 5: 进阶技巧

### 5.1 自定义 Commit 模板

#### **修改默认的 Type 列表：**

```yaml
# ~/.config/sc-git/config.yml
commit_types:
  feat:
    description: "新功能"
  fix:
    description: "Bug 修复"
  docs:
    description: "文档更新"
  style:
    description: "格式调整"
  refactor:
    description: "重构"
  perf:
    description: "性能优化"
  test:
    description: "测试"
  chore:
    description: "构建/工具"

  # 项目特定的 type
  epic:
    description: "史诗级功能"
  story:
    description: "用户故事"
```

#### **添加项目特定的 Scope：**

```yaml
# 项目根目录: .sc-git.yml
scopes:
  backend: "后端 API"
  frontend: "前端界面"
  database: "数据库"
  deployment: "部署配置"
  infrastructure: "基础设施"

  # 项目特定的 scope
  auth: "认证授权"
  payment: "支付系统"
  notification: "通知系统"
```

#### **集成 JIRA/Linear Ticket：**

```yaml
# .sc-git.yml
ticket_integration:
  provider: jira  # or linear, github

  patterns:
    - "(PROJ-\\d+)"
    - "(LINEAR-\\d+)"

  commit_template: |
    {type}({scope}): {subject}

    {body}

    {ticket}

  example: |
    feat(auth): add OAuth2 login

    - Implement Google OAuth
    - Add token management
    - Include tests

    PROJ-123
```

---

### 5.2 多代理协作模式

#### **并行开发流程：**

```
┌─────────────────────────────────────────┐
│     Multi-Agent Parallel Workflow        │
└──────────────────┬──────────────────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
┌───▼────┐   ┌────▼───┐   ┌─────▼─────┐
│Agent A │   │Agent B │   │Agent C   │
└───┬────┘   └────┬───┘   └─────┬─────┘
    │            │             │
┌───▼────┐   ┌──▼────┐   ┌────▼────┐
│Feature 1│   │Feature 2│  │Tests    │
│开发     │   │开发     │  │编写     │
└────┬───┘   └────┬───┘   └────┬────┘
     │            │            │
     └────────┬───┴────────────┘
              │
         ┌────▼────┐
         │Agent D  │
         └────┬────┘
              │
         /sc:git commit
```

**实战案例：**

```python
# 多代理协作脚本
import asyncio
from anthropic import Anthropic

async def multi_agent_workflow():
    # Agent A: 开发认证功能
    agent_a = Agent("backend-developer")
    auth_code = await agent_a.develop_feature("OAuth2 login")

    # Agent B: 开发支付功能
    agent_b = Agent("backend-developer")
    payment_code = await agent_b.develop_feature("Stripe integration")

    # Agent C: 编写测试
    agent_c = Agent("python-testing-expert")
    tests = await agent_c.write_tests([auth_code, payment_code])

    # Agent D: 使用 /sc:git 提交
    agent_d = Agent("git-specialist")
    await agent_d.commit_changes([
        ("feat(auth): add OAuth2 login", auth_code),
        ("feat(payment): add Stripe integration", payment_code),
        ("test: add comprehensive tests", tests)
    ])
```

---

### 5.3 性能优化

#### **大型仓库的优化策略：**

```yaml
性能优化配置:
  # 增量分析（只分析变更的文件）
  incremental_analysis: true

  # 并行处理（多文件并发分析）
  parallel_processing: true

  # 缓存（缓存分析结果）
  cache:
    enabled: true
    ttl: 3600  # 1 hour
    path: ~/.cache/sc-git

  # 延迟加载（需要时才分析）
  lazy_loading: true
```

#### **批量操作的最佳实践：**

```bash
# ❌ 不好的做法：循环调用 /sc:git
for file in *.py; do
    /sc:git commit --smart-commit  # 每次都启动 AI 分析
done

# ✅ 好的做法：批量提交
/sc:git commit --smart-commit --batch
# AI 一次性分析所有变更，生成一个 commit
```

#### **缓存和增量分析：**

```bash
# 第一次运行：完整分析
$ /sc:git status
# AI 分析所有文件（耗时：5 秒）

# 第二次运行：增量分析
$ /sc:git status
# AI 只分析变更的文件（耗时：1 秒）
# 使用缓存避免重复分析
```

---

## Part 6: 速查表

### 6.1 常用命令

| 命令 | 用途 | 示例 |
|------|------|------|
| `/sc:git status` | 智能状态分析 | 查看变更 + AI 建议 |
| `/sc:git commit --smart-commit` | 自动生成 commit message | 提交当前变更 |
| `/sc:git commit -i` | 交互式提交 | 逐步确认每个文件 |
| `/sc:git commit --amend --smart-commit` | 修正最后一个 commit | 遗漏文件或 message 错误 |
| `/sc:git checkout -b feature-*` | 创建功能分支 | 遵循命名规范 |
| `/sc:git merge --interactive` | 引导式合并 | 冲突解决辅助 |
| `/sc:git show <commit>` | 查看 commit 详情 | Code Review 时使用 |
| `/sc:git diff` | 查看变更差异 | 提交前 review |
| `/sc:git push` | 推送到远程 | 自动检测 upstream |
| `/sc:git pull` | 拉取远程变更 | 智能合并策略 |

---

### 6.2 Commit 类型速查

| Type | 中文名 | 使用场景 | 示例 |
|------|--------|----------|------|
| `feat` | 新功能 | 添加用户可见的功能 | `feat(auth): add OAuth2 login` |
| `fix` | Bug 修复 | 修复问题 | `fix(db): resolve connection timeout` |
| `docs` | 文档 | 更新文档 | `docs(readme): update installation guide` |
| `style` | 格式 | 代码格式调整（不影响功能） | `style: fix indentation` |
| `refactor` | 重构 | 代码重构（不改变功能） | `refactor(auth): simplify login flow` |
| `perf` | 性能 | 性能优化 | `perf(api): optimize database queries` |
| `test` | 测试 | 添加或修改测试 | `test(api): add integration tests` |
| `chore` | 构建/工具 | 构建、工具配置 | `chore: update dependencies` |

**选择决策树：**

```
添加了新功能？
  ├─ 是 → feat
  └─ 否 → 修复了 bug？
          ├─ 是 → fix
          └─ 否 → 改了文档？
                  ├─ 是 → docs
                  └─ 否 → 改了格式？
                          ├─ 是 → style
                          └─ 否 → 重构？
                                  ├─ 是 → refactor
                                  └─ 否 → 性能？
                                          ├─ 是 → perf
                                          └─ 否 → 测试？
                                                  ├─ 是 → test
                                                  └─ 否 → chore
```

---

### 6.3 Scope 常见值

| 项目类型 | 常用 Scope | 示例 |
|----------|-----------|------|
| **Web 应用** | auth, user, api, db, frontend, backend | `feat(auth): add login` |
| **移动应用** | ui, network, storage, analytics | `fix(ui): resolve layout issue` |
| **库/框架** | core, utils, docs, examples | `refactor(core): simplify API` |
| **DevOps** | deploy, ci, infra, monitoring | `chore(deploy): update k8s config` |

**如何选择 Scope？**

```yaml
规则:
  1. 从文件路径提取：
     - app/routers/auth.py → auth
     - app/db/models.py → db

  2. 从模块名提取：
     - user_service.py → user
     - payment_handler.py → payment

  3. 从功能推断：
     - 多个文件相关 → 统一 scope
     - 跨模块变更 → 无 scope 或 common
```

---

### 6.4 常见问题 FAQ

**Q1: /sc:git 会修改我的代码吗？**

A: **不会。** `/sc:git` 只分析代码并生成 commit message，不修改代码内容。它是一个"只读"的分析工具。

---

**Q2: 可以同时支持多个 commit 规范吗？**

A: **可以。** 通过自定义配置支持项目特定的规范。例如：

```yaml
# .sc-git.yml
convention:
  type: custom  # or angular, conventionalcommits

  custom_types:
    epic: "史诗级功能"
    story: "用户故事"
    task: "任务"
```

---

**Q3: 如何撤销 /sc:git 生成的 commit？**

A: **与传统 Git 相同。**

```bash
# 撤销最后一个 commit（保留更改）
$ git reset HEAD~1

# 撤销最后一个 commit（丢弃更改）
$ git reset --hard HEAD~1

# 撤销已 push 的 commit
$ git revert <commit-hash>
```

---

**Q4: /sc:git 适合大型团队吗？**

A: **非常适合。** 统一的 commit 规范有助于：

- ✅ Code Review（清晰的变更历史）
- ✅ 自动化（CI/CD, CHANGELOG 生成）
- ✅ 知识共享（新人更容易理解代码演进）
- ✅ 问题追踪（自动关联 Issue）

---

**Q5: /sc:git 支持哪些 Git 平台？**

A: **所有主流平台。** GitHub, GitLab, Bitbucket, Gitee 等。因为 `/sc:git` 只是生成 commit message，与平台无关。

---

**Q6: 可以离线使用吗？**

A: **取决于 AI 实现。** 如果使用本地 LLM（如 Ollama），可以完全离线。如果使用云端 API（如 OpenAI），需要网络连接。

---

**Q7: 如何处理敏感信息？**

A: `/sc:git` 有内置的安全检查：

```bash
$ /sc:git commit --smart-commit

🚨 Security Warning:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  Possible sensitive data detected:
  • .env contains API keys
  • config.py has hardcoded passwords

💡 Recommendations:
  - Remove these files from commit
  - Add to .gitignore
  - Use environment variables instead

Continue anyway? [y/N]
```

---

**Q8: /sc:git 会影响 Git 性能吗？**

A: **有轻微影响。** AI 分析需要额外时间（通常 1-3 秒）。可以通过以下方式优化：

- ✅ 启用缓存（`cache.enabled: true`）
- ✅ 增量分析（`incremental_analysis: true`）
- ✅ 并行处理（`parallel_processing: true`）

---

**Q9: 可以与 pre-commit hooks 集成吗？**

A: **可以。** 在 `.git/hooks/pre-commit` 中添加：

```bash
#!/bin/bash
# .git/hooks/pre-commit

# 运行 /sc:git 的预检查
/sc:git status --pre-commit-only

# 如果检测到问题，退出
if [ $? -ne 0 ]; then
    echo "❌ Pre-commit checks failed"
    exit 1
fi
```

---

**Q10: 如何贡献 /sc:git 的改进？**

A: `/sc:git` 是开源项目，欢迎贡献：

1. Fork 仓库
2. 创建功能分支
3. 提交 PR（使用 `/sc:git commit --smart-commit` 😄）
4. 等待 review

---

## 附录

### A. Conventional Commits 规范

**完整规范：** https://www.conventionalcommits.org/

**基本格式：**

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**示例：**

```
feat(api): add user authentication

- Implement JWT-based authentication
- Add login/logout endpoints
- Include error handling

Closes #123
Breaking change: The auth endpoint now requires Bearer token
```

---

### B. /sc:git vs 其他工具

| 工具 | 类型 | 优势 | 劣势 |
|------|------|------|------|
| **/sc:git** | AI 驱动 | 智能分析、自动化、上下文感知 | 需要网络（云端 AI） |
| **commitizen** | 交互式 CLI | 稳定、可预测 | 需要手动回答问题 |
| **gitmoji** | Gitmoji 图标 | 可视化、有趣 | 不适合严肃项目 |
| **semantic-release** | 自动发布 | 完全自动化 | 配置复杂、学习曲线 |

**推荐组合：**

```yaml
小型项目:
  - /sc:git（日常提交）
  - GitHub Releases（发布）

中型项目:
  - /sc:git（日常提交）
  - semantic-release（自动发布）
  - conventional-changelog（生成 CHANGELOG）

大型项目:
  - /sc:git（开发团队）
  - commitizen（CI/CD）
  - Lint-staged（预提交检查）
```

---

### C. 扩展阅读

**必读文章：**

1. **"How to Write a Git Commit Message"**
   - Chris Beams
   - https://chris.beams.io/posts/git-commit/

2. **"The Art of the Commit"**
   - ThoughtBot
   - https://thoughtbot.com/blog/the-art-of-the-commit

3. **"Git Workflow for Teams"**
   - Atlassian
   - https://www.atlassian.com/git/tutorials/comparing-workflows

**相关工具：**

1. **Conventional Changelog**
   - 自动生成 CHANGELOG
   - https://github.com/conventional-changelog/conventional-changelog

2. **Commitlint**
   - Lint commit message
   - https://commitlint.js.org/

3. **Semantic Release**
   - 自动版本发布
   - https://github.com/semantic-release/semantic-release

---

## 总结

`/sc:git` 是一个**AI 驱动的 Git 增强工具**，通过智能分析、自动化和最佳实践，让 Git 工作流更高效、更规范。

### **核心价值：**

```
✅ Smart Commits：自动生成规范的 commit message
✅ Status Analysis：智能状态分析 + AI 建议
✅ Workflow Optimization：最佳实践自动化
```

### **适用场景：**

```
✅ 日常开发提交（90% 的场景）
✅ 团队协作项目
✅ Code Review 与合并
✅ CI/CD 集成
```

### **关键原则：**

```
1. 人机协作：AI 分析，人类决策
2. 渐进增强：从基础到高级
3. 工具集成：与 Warp、CI/CD、GitHub/GitLab 无缝配合
```

**开始使用：**

```bash
# 今天就开始
$ /sc:git status
$ /sc:git commit --smart-commit

# 体验 AI 驱动的 Git 工作流
```

---

**Happy Coding! 🚀**

---

*文档版本：v1.0.0*
*最后更新：2025-01-05*
*作者：基于 SuperClaude /sc:git 实现*
