# 🚀 Simple Start Guide

## Problem: The long command is annoying!

```bash
source /Users/David/miniconda3/etc/profile.d/conda.sh && conda activate cs146s && export PATH="/Users/David/.local/bin:$PATH" && cd /Users/David/Desktop/github_repos/modern-software-dev-assignments && python scripts/env_check.py
```

## Solution: Add this to your ~/.zshrc

```bash
# CS146S Aliases
alias cs146s="source ~/miniconda3/etc/profile.d/conda.sh && conda activate cs146s && export PATH=\"\$HOME/.local/bin:\$PATH\""
alias cs-check='cd ~/Desktop/github_repos/modern-software-dev-assignments && python scripts/env_check.py'
alias cs-test='cd ~/Desktop/github_repos/modern-software-dev-assignments/week5 && make test'
alias cs-run='cd ~/Desktop/github_repos/modern-software-dev-assignments/week5 && make run'
```

Then reload your shell:
```bash
source ~/.zshrc
```

## Now you can use simple commands!

### Activate environment
```bash
cs146s
```

### Check environment health
```bash
cs-check
```

### Run tests
```bash
cs-test
```

### Start server
```bash
cs-run
```

## Even simpler: One command for everything!

```bash
cs146s && cs-check && cs-test && cs-run
```

That's it! 🎉

---

## Why was the command so long?

The long command had 4 parts:

1. **Initialize conda** (because it's not in your shell profile)
2. **Activate cs146s environment** (to get Python 3.12)
3. **Add Poetry to PATH** (because it's in ~/.local/bin)
4. **Run the command** (env check, test, etc.)

Our alias (`cs146s`) handles the first 3 parts automatically!

---

## Alternative: Permanent Fix

If you want conda to always be available, run:

```bash
conda init zsh
```

Then restart your terminal. You'll only need:

```bash
conda activate cs146s
```

But some people prefer not to have conda in every shell, so the `cs146s` alias gives you control!

---

**Tip**: Share this `cs146s` alias with your classmates - they probably have the same problem! 🎓
