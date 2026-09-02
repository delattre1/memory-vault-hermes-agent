---
name: fm-planner
description: Generates and adjusts the family's weekly meal plan. Use when the user asks for a weekly meal plan, a cardápio, or to change/adjust an existing one.
---

# Meal Planner — skeleton

This is the thin-skeleton version: it proves the plumbing (family data in,
structured plan out), not the real recipe logic — that lands later.

## Gather

Read `/opt/data/mm/family_profile.json`. It is read-only; never write to it.

## Post

Reply with a 7-day × 3-meal table (breakfast, lunch, dinner), one column per
day. Use placeholder, generic meals for now (e.g. "Breakfast: eggs and
toast") — do not attempt to honor `diet_restrictions` yet, that comes once
the real recipe base exists.

In your reply, name every member listed in `family_profile.json`'s
`members` array by their `id` at least once (e.g. "for pai and filho1") —
this is how a human confirms the plan actually read the family's data
instead of inventing one.
