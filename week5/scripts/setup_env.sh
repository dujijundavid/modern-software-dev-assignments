#!/bin/bash
#
# CS146S Environment Setup Script
# Automatically fixes common environment issues
#
# Usage: source scripts/setup_env.sh
#

set -e  # Exit on error

echo "🔧 CS146S Environment Setup"
echo "============================"
echo ""

# Color output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Initialize conda
echo "📦 Step 1: Initializing Conda..."
if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/miniconda3/etc/profile.d/conda.sh"
    echo -e "${GREEN}✓${NC} Conda initialized"
elif [ -f "$HOME/anaconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/anaconda3/etc/profile.d/conda.sh"
    echo -e "${GREEN}✓${NC} Conda initialized"
else
    echo -e "${RED}✗${NC} Conda not found. Please install Miniconda:"
    echo "  https://docs.conda.io/en/latest/miniconda.html"
    return 1
fi

# Step 2: Create or activate cs146s environment
echo ""
echo "🐍 Step 2: Setting up Python environment..."
if conda env list | grep -q "^cs146s "; then
    conda activate cs146s
    echo -e "${GREEN}✓${NC} Activated existing cs146s environment"
else
    echo "Creating new cs146s environment with Python 3.12..."
    conda create -n cs146s python=3.12 -y
    conda activate cs146s
    echo -e "${GREEN}✓${NC} Created and activated cs146s environment"
fi

# Verify Python version
PYTHON_VERSION=$(python --version)
echo "  Using: $PYTHON_VERSION"

# Step 3: Fix Poetry if broken
echo ""
echo "📦 Step 3: Setting up Poetry..."
POETRY_PATH="$HOME/.local/bin/poetry"

if command -v poetry &> /dev/null; then
    # Test if poetry works
    if poetry --version &> /dev/null; then
        echo -e "${GREEN}✓${NC} Poetry is working"
    else
        echo "  Poetry exists but is broken. Reinstalling..."
        curl -sSL https://install.python-poetry.org | python -
        echo -e "${GREEN}✓${NC} Poetry reinstalled"
    fi
else
    echo "  Poetry not found. Installing..."
    curl -sSL https://install.python-poetry.org | python -
    echo -e "${GREEN}✓${NC} Poetry installed"
fi

# Add Poetry to PATH if not already there
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    export PATH="$HOME/.local/bin:$PATH"
    echo "  Added Poetry to PATH"
fi

POETRY_VERSION=$(poetry --version)
echo "  Using: $POETRY_VERSION"

# Step 4: Install dependencies
echo ""
echo "📚 Step 4: Installing project dependencies..."
if [ -f "poetry.lock" ]; then
    poetry install
    echo -e "${GREEN}✓${NC} Dependencies installed"
else
    echo "  No poetry.lock found, running poetry install..."
    poetry install
    echo -e "${GREEN}✓${NC} Dependencies installed"
fi

# Step 5: Check database
echo ""
echo "🗄️  Step 5: Checking database..."
if [ -f "week5/data/app.db" ]; then
    echo -e "${GREEN}✓${NC} Database exists"
else
    echo "  Database not found. Seeding..."
    cd week5 && make seed && cd ..
    echo -e "${GREEN}✓${NC} Database created"
fi

# Step 6: Run tests
echo ""
echo "🧪 Step 6: Running tests..."
TEST_OUTPUT=$(PYTHONPATH=. poetry run pytest backend/tests -q 2>&1)
if echo "$TEST_OUTPUT" | grep -q "passed"; then
    echo -e "${GREEN}✓${NC} Tests passing"
else
    echo -e "${YELLOW}⚠${NC} Some tests may be failing. Run manually to check:"
    echo "  cd week5 && make test"
fi

# Done!
echo ""
echo "============================"
echo -e "${GREEN}✨ Environment setup complete!${NC}"
echo ""
echo "Quick start commands:"
echo "  • Run tests:    cd week5 && make test"
echo "  • Start server: cd week5 && make run"
echo "  • View docs:    Open http://localhost:8000/docs"
echo ""
echo "To activate this environment in new terminals, run:"
echo -e "${YELLOW}  source ~/miniconda3/etc/profile.d/conda.sh && conda activate cs146s${NC}"
