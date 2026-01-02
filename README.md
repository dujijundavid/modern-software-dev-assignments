# Assignments for CS146S: The Modern Software Developer

This is the home of the assignments for [CS146S: The Modern Software Developer](https://themodernsoftware.dev), taught at Stanford University fall 2025.

## 🚀 Quick Start

**New here?** Follow the setup instructions below.

**Having environment issues?** See the [Environment Setup Guide](docs/week5/guides/quick-start.md).

**Looking for documentation?** Check the [Documentation Index](docs/INDEX.md).

## 🔧 Repo Setup
These steps work with Python 3.12.

1. Install Anaconda
   - Download and install: [Anaconda Individual Edition](https://www.anaconda.com/download)
   - Open a new terminal so `conda` is on your `PATH`.

2. Create and activate a Conda environment (Python 3.12)
   ```bash
   conda create -n cs146s python=3.12 -y
   conda activate cs146s
   ```

3. Install Poetry
   ```bash
   curl -sSL https://install.python-poetry.org | python -
   ```

4. Install project dependencies with Poetry (inside the activated Conda env)
   From the repository root:
   ```bash
   poetry install --no-interaction
   ```

## Documentation

Comprehensive course documentation is available in the [`/docs/`](docs/) directory:

### Quick Links

- **[Master Index](docs/INDEX.md)** - Main navigation hub for all documentation
- **[Weekly Documentation Index](docs/weeks/INDEX.md)** - Detailed week-by-week guides
- **[Quick Reference Guide](docs/QUICK_REFERENCE.md)** - Key concepts, patterns, and debugging tips
- **[Templates](docs/templates/)** - Reusable documentation templates

### Completed Weeks

#### Week 1: Prompting Techniques (1,157 lines)
- **[Overview](docs/weeks/week01/overview.md)** - K-shot prompting, chain-of-thought, tool calling
- **[Implementation](docs/weeks/week01/implementation.md)** - Complete httpstatus reversal case study
- **[Reflection](docs/weeks/week01/reflection.md)** - Learning outcomes and lessons learned

#### Week 2: LLM-Powered Applications (821 lines)
- **[Overview](docs/weeks/week02/overview.md)** - LLM integration fundamentals, structured output
- **[Implementation](docs/weeks/week02/implementation.md)** - Action item extractor implementation
- **[Reflection](docs/weeks/week02/reflection.md)** - Testing and refactoring journey

#### Week 3: MCP Server Development (721 lines)
- **[Overview](docs/weeks/week03/overview.md)** - Comprehensive MCP protocol guide (438 lines)
- **[Implementation](docs/weeks/week03/implementation.md)** - MCP server architecture and tools
- **[Reflection](docs/weeks/week03/reflection.md)** - Async programming and deployment

#### Week 4: Slash Commands & SubAgents (925 lines)
- **[Overview](docs/weeks/week04/overview.md)** - 4-Layer Prompt Model, SubAgents collaboration
- **[Implementation](docs/weeks/week04/implementation.md)** - architect-hub and tdd-cycle automations
- **[Reflection](docs/weeks/week04/reflection.md)** - Critical analysis of design flaws

### Documentation Metrics

- **Total weeks documented**: 4
- **Complete weeks**: 3 (Weeks 1, 2, 4)
- **Partial weeks**: 1 (Week 3 - overview complete)
- **Total documentation**: 3,624 lines
- **Average per week**: 906 lines

### Content Highlights

| Week | Focus | Achievement |
|------|-------|-------------|
| Week 1 | Prompting Techniques | Complete httpstatus reversal case study |
| Week 2 | LLM Integration | Best organized (14 source files → 3 docs) |
| Week 3 | MCP Protocol | Best pre-learning (438-line comprehensive guide) |
| Week 4 | SubAgents | Strongest reflection (critical analysis) |

For more details, see the [Weekly Documentation Index](docs/weeks/INDEX.md).