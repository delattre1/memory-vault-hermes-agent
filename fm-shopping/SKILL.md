---
name: fm-shopping
description: Consolidates the weekly meal plan into a shopping list. Use when the user asks for the shopping list, or after generating a meal plan and the user wants to see what to buy.
---

# Shopping List — skeleton

This is the thin-skeleton version: consolidation only, no market/Latch
integration yet — that lands once this handoff is proven.

## Gather

Run `fm-planner` first if `/opt/data/mm/meal-plan.json` does not exist yet
— this skill never invents a plan of its own.

## Filter

Run, by absolute path, no arguments:

    /opt/data/skills/fm-shopping/scripts/consolidate.py

It reads `/opt/data/mm/meal-plan.json` and writes
`/opt/data/mm/shopping-list.json`. You never see the meal plan's raw
content here — only the script's stdout line confirming how many items it
wrote.

## Post

Read `/opt/data/mm/shopping-list.json` and show the list to the user.
