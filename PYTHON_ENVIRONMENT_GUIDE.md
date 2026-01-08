# Python环境管理指南

## 问题诊断

你的环境实际上是配置良好的，但可能遇到以下问题：

### 当前状态
- 系统Python: 3.14.2 (Homebrew)
- Conda环境: Python 3.12.12 (cs146s)
- Poetry虚拟环境: Python 3.12.12 ✅

### 常见问题场景

1. **直接用`pip install`** → 安装到系统Python 3.14.2
2. **未激活conda/poetry环境** → 用系统Python
3. **新终端窗口** → 环境未激活

## 解决方案

### 方案A：使用Poetry（推荐用于这个项目）

```bash
# 1. 进入项目目录
cd /path/to/modern-software-dev-assignments

# 2. 激活Poetry环境
poetry shell

# 3. 安装依赖
poetry install

# 4. 运行命令（在poetry shell内）
python --version  # 应显示3.12.12
pytest week1/
```

**优点**：
- 项目独立，不干扰其他项目
- 依赖管理精确（poetry.lock）
- 与项目配置一致

**缺点**：
- 每次需要`poetry shell`

### 方案B：使用Conda环境

```bash
# 1. 激活conda环境
conda activate cs146s

# 2. 在conda环境内用Poetry
poetry install
poetry run pytest week1/
```

**优点**：
- Python版本管理统一
- 可以安装非Python依赖

**缺点**：
- 需要记住激活环境
- 与Poetry可能有冲突

### 方案C：使用UV（新工具，极快）

```bash
# 1. UV自动创建虚拟环境
uv venv --python 3.12

# 2. 激活环境
source .venv/bin/activate

# 3. 安装依赖
uv pip install -r requirements.txt
```

**优点**：
- 速度极快（比pip快10-100倍）
- 智能依赖解析

**缺点**：
- 新工具，生态还不够成熟
- 需要维护requirements.txt

## 工具选择建议

### 对于这个项目（CS146S）
```
Poetry (主要) + Conda (Python版本管理)
```

### 工作流程
```bash
# 启动工作
conda activate cs146s        # 激活Python 3.12
cd modern-software-dev-assignments
poetry shell                 # 激活项目虚拟环境

# 开发
python app/main.py           # 运行应用
pytest week1/                # 运行测试

# 退出
exit                         # 退出poetry shell
conda deactivate             # 退出conda环境
可选）
```

## 防止未来的问题

### 1. 创建别名（可选）

在 `~/.zshrc` 中添加：
```bash
# CS146S项目快捷方式
alias cs146s="cd ~/Desktop/github_repos/modern-software-dev-assignments && conda activate cs146s && poetry shell"
```

### 2. 使用direnv（自动激活）

```bash
# 安装direnv
brew install direnv

# 在项目中创建.envrc
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc
echo 'layout_poetry' > .envrc
direnv allow
```

### 3. Pre-commit检查

在 `.pre-commit-config.yaml` 中：
```yaml
repos:
  - repo: local
    hooks:
      - id: check-python-version
        name: Check Python version
        entry: python3.12 --version
        language: system
```

## 快速诊断

运行项目中的诊断脚本：
```bash
./check-python-env.sh
```

## 常见错误和解决

### 错误1: ModuleNotFoundError

```bash
# ❌ 错误
pip install some-package
python script.py  # 找不到some-package

# ✅ 正确
poetry add some-package
poetry run python script.py
```

### 错误2: Python版本不匹配

```bash
# ❌ 错误
python --version  # 3.14.2
# 但项目需要3.12

# ✅ 正确
poetry run python --version  # 3.12.12
```

### 错误3: 依赖冲突

```bash
# ❌ 错误
pip install package-a  # 安装到系统
poetry add package-b   # 可能冲突

# ✅ 正确
poetry add package-a package-b  # 统一管理
```

## 工具命令对照表

| 操作 | Poetry | Conda | pip | UV |
|------|--------|-------|-----|-----|
| 安装依赖 | `poetry install` | `conda install` | `pip install` | `uv pip install` |
| 添加包 | `poetry add pkg` | `conda install pkg` | `pip install pkg` | `uv pip install pkg` |
| 激活环境 | `poetry shell` | `conda activate env` | `source venv/bin/activate` | `source .venv/bin/activate` |
| 运行命令 | `poetry run cmd` | (直接运行) | `python -m cmd` | `uv run cmd` |
| 查看依赖 | `poetry show` | `conda list` | `pip list` | `uv pip list` |

## 总结

**最重要的规则**：
1. ✅ 总是使用`poetry run`或`poetry shell`
2. ✅ 不要直接用`pip install`（除非在虚拟环境中）
3. ✅ 运行`./check-python-env.sh`诊断问题
4. ✅ 遇到问题时先检查`which python`和`python --version`

**不要做的事**：
1. ❌ 不要全局`pip install`
2. ❌ 不要混用conda和pip（除非你知道后果）
3. ❌ 不要忽略Python版本要求
