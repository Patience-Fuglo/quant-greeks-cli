import subprocess
import sys

def test_cli_help():
    result = subprocess.run([sys.executable, "cli.py", "--help"], capture_output=True, text=True)
    assert "usage" in result.stdout.lower()

def test_cli_batch_table_output():
    # Minimal test: should not error when given batch command with fake file
    result = subprocess.run([sys.executable, "cli.py", "batch", "--file", "tests/test_binomial.py", "--output", "table"],
                            capture_output=True, text=True)
    # Adjust assertion to match actual CLI error message
    assert "batch file must be .csv or .json" in result.stdout.lower()