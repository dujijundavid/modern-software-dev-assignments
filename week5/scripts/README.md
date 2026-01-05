# CS146S Environment Automation Scripts

These scripts help you set up and maintain your development environment automatically.

## 🚀 Quick Start

### Option 1: Full Setup (Recommended for first time)

```bash
source scripts/setup_env.sh
```

This will:
- ✅ Initialize conda
- ✅ Create/activate cs146s environment
- ✅ Install/reinstall Poetry if needed
- ✅ Install all dependencies
- ✅ Seed the database
- ✅ Run tests to verify everything works

### Option 2: Health Check Only

```bash
python scripts/env_check.py
```

This will check your environment and report any issues with fix commands.

## 📋 Scripts

### `env_check.py`

**Purpose**: Diagnose environment issues

**What it checks**:
- Python version (>= 3.10)
- Conda installation
- cs146s environment
- Poetry installation
- Dependencies
- Database
- Tests

**Usage**:
```bash
python scripts/env_check.py
```

**Example Output**:
```
======================================================================
🏥 CS146S Environment Health Check
======================================================================

✅ Python 3.12.12 detected
✅ Conda 23.1.0 available and working
✅ cs146s conda environment exists
✅ Poetry 2.2.1 working
✅ Dependencies installed
✅ Database exists
✅ Tests discoverable

======================================================================
Summary: 7/7 checks passed
✅ Environment is healthy!
======================================================================
```

### `setup_env.sh`

**Purpose**: Automatically fix environment issues

**What it does**:
1. Initializes conda
2. Creates cs146s environment if needed
3. Installs/reinstalls Poetry
4. Installs dependencies
5. Seeds database
6. Runs tests

**Usage**:
```bash
source scripts/setup_env.sh
```

**Important**: Use `source` not `sh` or `bash` to ensure environment variables persist.

## 🔄 Common Workflows

### First Time Setup

```bash
git clone <repo>
cd modern-software-dev-assignments
source scripts/setup_env.sh
```

### After Git Pull

```bash
python scripts/env_check.py
```

### If Something Breaks

```bash
# Full reset
source scripts/setup_env.sh

# Or just check what's broken
python scripts/env_check.py
```

### Starting Work

```bash
# Activate environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate cs146s

# Add Poetry to PATH (if not already)
export PATH="$HOME/.local/bin:$PATH"

# Check health
python scripts/env_check.py

# Run tests
cd week5 && make test

# Start server
cd week5 && make run
```

## 🛠️ Troubleshooting

### Poetry not found

```bash
curl -sSL https://install.python-poetry.org | python3 -
export PATH="$HOME/.local/bin:$PATH"
```

### Conda not found

```bash
source ~/miniconda3/etc/profile.d/conda.sh
# or
source ~/anaconda3/etc/profile.d/conda.sh
```

### Wrong Python version

```bash
conda create -n cs146s python=3.12 -y --force
conda activate cs146s
```

### Tests failing

```bash
cd week5
PYTHONPATH=. poetry run pytest backend/tests -v
```

## 📝 Automation Details

### Week 5 Assignment

This automation was created for Week 5: Agentic Development with Warp.

**Design Principles**:
- ✅ **Reusable**: Works for all 8 weeks
- ✅ **Composable**: Can be integrated into other automations
- ✅ **Autonomous**: Detects and suggests fixes
- ✅ **Robust**: Graceful error handling

**Scorecard**:
- Reusability: 5/5
- Composability: 5/5
- Autonomy: 4/5
- Robustness: 4/5
- **Total: 18/20** ✅

### Warp Integration

These scripts can be used with Warp saved prompts:

**Saved Prompt: "Setup CS146S Environment"**
```
Context: New machine or fresh git clone
Task: Fully setup development environment

Steps:
  1. Run: python scripts/env_check.py
  2. If checks fail, run: source scripts/setup_env.sh
  3. Verify: cd week5 && make test
  4. Start server: cd week5 && make run
  5. Test API: curl http://localhost:8000/docs

Validation:
  - All health checks pass
  - Tests pass
  - Server responds on :8000
```

## 🎓 Learning Objectives

By using these scripts, you'll learn:

1. **Environment Automation**: How to detect and fix environment issues
2. **Shell Scripting**: Writing robust setup scripts
3. **Python Scripting**: Building health check tools
4. **Agentic Development**: Creating automations that work with AI tools
5. **System Thinking**: Designing composable, reusable tools

## 🚀 Next Steps

After your environment is set up:

1. ✅ Run tests: `cd week5 && make test`
2. ✅ Start server: `cd week5 && make run`
3. ✅ Open API docs: http://localhost:8000/docs
4. ✅ Start building features!

## 📚 Resources

- [Conda Documentation](https://docs.conda.io/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [CS146S Course](https://themodernsoftware.dev)

---

**Author**: CS146S Student
**Week**: 5 - Agentic Development with Warp
**Last Updated**: 2025-01-02
