import subprocess


def test():
    """
    Run all pytests
    """
    subprocess.run(["poetry", "run", "pytest"])


def lint():
    """
    Run linter
    """
    subprocess.run(["poetry", "run", "ruff", "check"])
    subprocess.run(["poetry", "run", "pyright", "jrotatelog"])


def format():
    """
    Run formatter
    """
    subprocess.run(["poetry", "run", "ruff", "format"])
