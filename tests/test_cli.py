import subprocess
import os

def test_cli_help():
    """Test if CLI --help works."""
    result = subprocess.run(["python", "src/datacleancraft/cli.py", "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Usage" in result.stdout

def test_cli_run(tmp_path):
    """Test full CLI run."""
    input_file = "examples/input_sample.csv"
    output_file = "examples/output.csv"

    result = subprocess.run([
        "python", "src/datacleancraft/cli.py",
        "--input-path", input_file,
        "--output-path", str(output_file),
    ], capture_output=True, text=True)

    assert result.returncode == 0
    assert  os.path.isfile(output_file)
