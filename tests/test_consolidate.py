import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "fm-shopping" / "scripts" / "consolidate.py"


def _load():
    spec = importlib.util.spec_from_file_location("consolidate", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_consolidate_extracts_three_items_from_a_meal_plan():
    plan = {
        "days": {
            "Mon": {"breakfast": "Eggs and toast", "lunch": "Grilled chicken", "dinner": "Soup"},
            "Tue": {"breakfast": "Eggs and toast", "lunch": "Pasta", "dinner": "Sandwich"},
        }
    }
    mod = _load()
    result = mod.consolidate(plan)
    assert result == {"items": ["Eggs and toast", "Grilled chicken", "Soup"]}


def test_consolidate_deduplicates_repeated_meals():
    plan = {"days": {"Mon": {"breakfast": "Eggs", "lunch": "Eggs", "dinner": "Eggs"}}}
    mod = _load()
    result = mod.consolidate(plan)
    assert result == {"items": ["Eggs"]}
