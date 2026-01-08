#!/bin/bash
# Python Environment Health Check
# 用途：快速诊断当前使用的Python版本和工具链配置

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🔍 Python环境诊断工具"
echo "================================"

# 检查系统Python
echo -e "\n📍 1. 系统默认Python (which python3)"
SYSTEM_PYTHON=$(which python3 2>/dev/null || echo "未找到")
SYSTEM_VERSION=$(python3 --version 2>/dev/null || echo "N/A")
echo "   路径: $SYSTEM_PYTHON"
echo "   版本: $SYSTEM_VERSION"

# 检查当前激活的Python
echo -e "\n📍 2. 当前激活的Python ($PYTHON_VERSION)"
if [ -n "$CONDA_DEFAULT_ENV" ]; then
    echo -e "   ${GREEN}✓ Conda环境: $CONDA_DEFAULT_ENV${NC}"
    echo "   路径: $CONDA_PREFIX"
else
    echo -e "   ${YELLOW}⚠ 未激活Conda环境${NC}"
fi

# 检查Poetry环境
echo -e "\n📍 3. Poetry虚拟环境"
if poetry env info -p &>/dev/null; then
    POETRY_PYTHON=$(poetry run which python 2>/dev/null)
    POETRY_VERSION=$(poetry run python --version 2>/dev/null)
    echo -e "   ${GREEN}✓ Poetry环境已配置${NC}"
    echo "   版本: $POETRY_VERSION"
    echo "   路径: $POETRY_PYTHON"

    # 检查是否在项目目录
    if [ -f "pyproject.toml" ]; then
        REQUIRED_PYTHON=$(grep -oP 'python = "\K[^"]+' pyproject.toml 2>/dev/null || echo "未指定")
        echo "   项目要求: $REQUIRED_PYTHON"
    fi
else
    echo -e "   ${RED}✗ Poetry环境未初始化${NC}"
    echo "   运行: poetry install"
fi

# 检查PATH中的Python
echo -e "\n📍 4. PATH中的Python顺序"
echo "$PATH" | tr ':' '\n' | grep -i python | nl

# 检查常见工具
echo -e "\n📍 5. 工具链检查"
check_tool() {
    if command -v $1 &>/dev/null; then
        echo -e "   ${GREEN}✓ $1${NC} ($(which $1))"
    else
        echo -e "   ${RED}✗ $1 未安装${NC}"
    fi
}

check_tool "poetry"
check_tool "conda"
check_tool "uv"
check_tool "pipx"

# 推荐操作
echo -e "\n💡 推荐操作:"
if [ -z "$CONDA_DEFAULT_ENV" ] && [ -f "pyproject.toml" ]; then
    echo -e "   ${YELLOW}1. 激活conda环境: conda activate cs146s${NC}"
    echo -e "   ${YELLOW}2. 或使用Poetry shell: poetry shell${NC}"
fi

if ! poetry env info -p &>/dev/null && [ -f "pyproject.toml" ]; then
    echo -e "   ${YELLOW}3. 初始化Poetry环境: poetry install${NC}"
fi

echo -e "\n✅ 诊断完成"