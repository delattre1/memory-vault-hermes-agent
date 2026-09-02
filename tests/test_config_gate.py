import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GATE_SCRIPT = ROOT / "fm-shared" / "scripts" / "config_gate.py"
EXAMPLE = ROOT / "fm-shared" / "references" / "family_profile.example.json"
FILLED = ROOT / "tests" / "fixtures" / "family_profile.filled.json"


def _load_gate_module():
    spec = importlib.util.spec_from_file_location("config_gate", GATE_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_gate_passes_on_a_fully_filled_profile():
    config = json.loads(FILLED.read_text())
    gate = _load_gate_module()
    assert gate.gate(config) == ""


def test_gate_fails_on_an_unfilled_placeholder():
    config = json.loads(EXAMPLE.read_text())
    gate = _load_gate_module()
    message = gate.gate(config)
    assert "placeholder" in message


def test_main_exits_nonzero_on_the_example_with_placeholders():
    result = subprocess.run(
        [sys.executable, str(GATE_SCRIPT), str(EXAMPLE)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "placeholder" in (result.stdout + result.stderr)


def test_main_exits_zero_on_a_fully_filled_profile():
    result = subprocess.run(
        [sys.executable, str(GATE_SCRIPT), str(FILLED)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
