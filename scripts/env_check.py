#!/usr/bin/env python3
"""
Environment Health Check for CS146S Assignments

This script automatically detects and fixes common environment issues.
Run it from the project root: python scripts/env_check.py

Author: CS146S Student
Week: 5 - Agentic Development with Warp
"""
import subprocess
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional
import shutil


@dataclass
class CheckResult:
    """Result of a single health check."""
    name: str
    passed: bool
    message: str
    fix_command: Optional[str] = None
    auto_fix: Optional[callable] = None


class Colors:
    """Terminal colors for pretty output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


class EnvHealthCheck:
    """Environment health checker and auto-fixer."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.results: List[CheckResult] = []

    def _run_command(self, cmd: List[str], capture_output: bool = True) -> subprocess.CompletedProcess:
        """Run a command and return the result."""
        try:
            return subprocess.run(
                cmd,
                capture_output=capture_output,
                text=True,
                timeout=5
            )
        except subprocess.TimeoutExpired:
            return subprocess.CompletedProcess(cmd, -1, "", "Command timed out")
        except FileNotFoundError:
            return subprocess.CompletedProcess(cmd, -1, "", "Command not found")
        except Exception as e:
            return subprocess.CompletedProcess(cmd, -1, "", str(e))

    def check_python_version(self) -> CheckResult:
        """Check if Python >= 3.10 is available."""
        try:
            result = self._run_command([sys.executable, "--version"])
            if result.returncode != 0:
                return CheckResult(
                    name="Python Version",
                    passed=False,
                    message=f"❌ Cannot detect Python version",
                    fix_command="Install Python 3.10+ via Conda or pyenv"
                )

            version_str = result.stdout.strip().split()[-1]
            version_parts = version_str.split(".")
            major, minor = int(version_parts[0]), int(version_parts[1])

            if major >= 3 and minor >= 10:
                return CheckResult(
                    name="Python Version",
                    passed=True,
                    message=f"✅ Python {version_str} detected"
                )
            else:
                return CheckResult(
                    name="Python Version",
                    passed=False,
                    message=f"❌ Python {version_str} is too old (need >=3.10)",
                    fix_command="conda create -n cs146s python=3.12 -y"
                )
        except Exception as e:
            return CheckResult(
                name="Python Version",
                passed=False,
                message=f"❌ Cannot detect Python: {e}",
                fix_command="Install Python 3.10+ via Conda or pyenv"
            )

    def check_conda(self) -> CheckResult:
        """Check if Conda is available."""
        # First try: conda in PATH
        result = self._run_command(["conda", "--version"])
        if result.returncode == 0:
            version = result.stdout.strip()
            return CheckResult(
                name="Conda",
                passed=True,
                message=f"✅ Conda {version} available and working"
            )

        # Second try: find conda in common locations
        conda_paths = [
            Path.home() / "miniconda3" / "bin" / "conda",
            Path.home() / "anaconda3" / "bin" / "conda",
            Path("/opt/homebrew/bin/conda"),
            Path("/usr/local/bin/conda"),
            Path.home() / "miniconda3" / "condabin" / "conda",
        ]

        for conda_path in conda_paths:
            if conda_path.exists():
                return CheckResult(
                    name="Conda",
                    passed=False,
                    message=f"⚠️  Conda found at {conda_path} but not in PATH",
                    fix_command=f"export PATH='{conda_path.parent}:$PATH' && conda init zsh"
                )

        return CheckResult(
            name="Conda",
            passed=False,
            message="❌ Conda not found",
            fix_command="Install Miniconda from https://docs.conda.io/en/latest/miniconda.html"
        )

    def check_poetry(self) -> CheckResult:
        """Check if Poetry is installed and working."""
        # Check if poetry is in PATH
        poetry_path = shutil.which("poetry")
        if not poetry_path:
            # Try ~/.local/bin
            local_poetry = Path.home() / ".local" / "bin" / "poetry"
            if local_poetry.exists():
                return CheckResult(
                    name="Poetry",
                    passed=False,
                    message=f"⚠️  Poetry found at {local_poetry} but not in PATH",
                    fix_command=f"export PATH='{local_poetry.parent}:$PATH'"
                )

            return CheckResult(
                name="Poetry",
                passed=False,
                message="❌ Poetry not installed",
                fix_command="curl -sSL https://install.python-poetry.org | python3 -"
            )

        # Test if poetry actually works
        result = self._run_command([poetry_path, "--version"])
        if result.returncode == 0:
            version = result.stdout.strip()
            # Check if it's using the right Python
            if "python3.10" in result.stderr or "python@3.10" in result.stderr:
                return CheckResult(
                    name="Poetry",
                    passed=False,
                    message=f"⚠️  Poetry {version} is broken (bad Python interpreter)",
                    fix_command="Reinstall Poetry: curl -sSL https://install.python-poetry.org | python3 -"
                )
            return CheckResult(
                name="Poetry",
                passed=True,
                message=f"✅ Poetry {version} working"
            )

        return CheckResult(
            name="Poetry",
            passed=False,
            message="❌ Poetry exists but fails to run",
            fix_command="Reinstall Poetry: curl -sSL https://install.python-poetry.org | python3 -"
        )

    def check_conda_env(self) -> CheckResult:
        """Check if cs146s conda environment exists."""
        result = self._run_command(["conda", "env", "list"])
        if result.returncode != 0:
            return CheckResult(
                name="Conda Environment",
                passed=False,
                message="⚠️  Cannot check conda environments (conda not working)",
                fix_command="Fix conda first"
            )

        if "cs146s" in result.stdout:
            return CheckResult(
                name="Conda Environment",
                passed=True,
                message="✅ cs146s conda environment exists"
            )

        return CheckResult(
            name="Conda Environment",
            passed=False,
            message="❌ cs146s conda environment not found",
            fix_command="conda create -n cs146s python=3.12 -y"
        )

    def check_dependencies(self) -> CheckResult:
        """Check if dependencies are installed."""
        lock_file = self.project_root / "poetry.lock"
        if not lock_file.exists():
            return CheckResult(
                name="Dependencies",
                passed=False,
                message="❌ poetry.lock not found",
                fix_command="poetry lock && poetry install"
            )

        # Check if we can import fastapi
        result = self._run_command(
            ["poetry", "run", "python", "-c", "import fastapi; print('OK')"],
            capture_output=True
        )

        if result.returncode == 0 and "OK" in result.stdout:
            return CheckResult(
                name="Dependencies",
                passed=True,
                message="✅ Dependencies installed"
            )

        return CheckResult(
            name="Dependencies",
            passed=False,
            message="❌ Dependencies not installed or incomplete",
            fix_command="poetry install"
        )

    def check_database(self) -> CheckResult:
        """Check if database exists."""
        db_path = self.project_root / "week5" / "data" / "app.db"
        if db_path.exists():
            return CheckResult(
                name="Database",
                passed=True,
                message=f"✅ Database exists at {db_path}"
            )

        return CheckResult(
            name="Database",
            passed=False,
            message="❌ Database not found (run: cd week5 && make seed)",
            fix_command="cd week5 && make seed"
        )

    def check_tests(self) -> CheckResult:
        """Check if tests can be discovered."""
        result = self._run_command(
            ["poetry", "run", "pytest", "--collect-only", "-q"],
            capture_output=True
        )

        # Check if any tests were collected
        if "test session starts" in result.stdout or "collected" in result.stdout:
            # Count tests
            lines = result.stdout.split("\n")
            for line in lines:
                if "collected" in line or "test" in line.lower():
                    return CheckResult(
                        name="Tests",
                        passed=True,
                        message=f"✅ Tests discoverable"
                    )

        return CheckResult(
            name="Tests",
            passed=False,
            message="⚠️  Tests may not be properly configured",
            fix_command="Check PYTHONPATH and test configuration"
        )

    def run_all_checks(self) -> List[CheckResult]:
        """Run all health checks."""
        self.results = [
            self.check_python_version(),
            self.check_conda(),
            self.check_conda_env(),
            self.check_poetry(),
            self.check_dependencies(),
            self.check_database(),
            self.check_tests(),
        ]
        return self.results

    def print_report(self):
        """Print a formatted health check report."""
        print("\n" + "=" * 70)
        print(f"{Colors.BOLD}🏥 CS146S Environment Health Check{Colors.END}")
        print("=" * 70 + "\n")

        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)

        for result in self.results:
            color = Colors.GREEN if result.passed else (Colors.YELLOW if "⚠️" in result.message else Colors.RED)
            print(f"{color}{result.message}{Colors.END}")
            if not result.passed and result.fix_command:
                print(f"   {Colors.BLUE}💡 Fix: {result.fix_command}{Colors.END}")
            print()

        print("=" * 70)
        print(f"{Colors.BOLD}Summary: {passed}/{total} checks passed{Colors.END}")

        if passed == total:
            print(f"{Colors.GREEN}✅ Environment is healthy!{Colors.END}")
        elif passed >= total - 2:
            print(f"{Colors.YELLOW}⚠️  Environment has minor issues{Colors.END}")
            print(f"{Colors.BLUE}Run the suggested fix commands above{Colors.END}")
        else:
            print(f"{Colors.RED}❌ Environment needs major repair{Colors.END}")
            print(f"\n{Colors.BOLD}Suggested auto-fix:{Colors.END}")
            print("1. Ensure conda is initialized: source ~/miniconda3/etc/profile.d/conda.sh")
            print("2. Activate environment: conda activate cs146s")
            print("3. Reinstall Poetry if needed: curl -sSL https://install.python-poetry.org | python3 -")
            print("4. Install dependencies: poetry install")

        print("=" * 70 + "\n")

        # Export environment setup command
        conda_path = Path.home() / "miniconda3"
        if conda_path.exists():
            print(f"{Colors.BLUE}📝 Quick setup command:{Colors.END}")
            print(f"source ~/miniconda3/etc/profile.d/conda.sh && conda activate cs146s && export PATH=\"$HOME/.local/bin:$PATH\"\n")


def main():
    """Main entry point."""
    # Find project root
    current_path = Path(__file__).resolve()
    project_root = current_path.parent.parent

    if not (project_root / "pyproject.toml").exists():
        print(f"Error: Could not find project root at {project_root}")
        sys.exit(1)

    checker = EnvHealthCheck(project_root)
    checker.run_all_checks()
    checker.print_report()

    # Exit with error code if checks failed
    passed = sum(1 for r in checker.results if r.passed)
    total = len(checker.results)
    sys.exit(0 if passed >= total - 1 else 1)


if __name__ == "__main__":
    main()
