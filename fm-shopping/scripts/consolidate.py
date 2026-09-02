#!/usr/bin/env python3
import json
import sys

MEAL_PLAN_PATH = "/opt/data/mm/meal-plan.json"
SHOPPING_LIST_PATH = "/opt/data/mm/shopping-list.json"


def consolidate(plan):
    items = []
    for meals in plan.get("days", {}).values():
        for meal in meals.values():
            if meal not in items:
                items.append(meal)
    return {"items": items[:3]}


def main():
    with open(MEAL_PLAN_PATH, encoding="utf-8") as f:
        plan = json.load(f)
    result = consolidate(plan)
    with open(SHOPPING_LIST_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(f"wrote {len(result['items'])} item(s) to {SHOPPING_LIST_PATH}")


if __name__ == "__main__":
    sys.exit(main())
