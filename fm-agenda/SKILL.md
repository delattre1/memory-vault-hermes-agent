---
name: fm-agenda
description: Reads the family's calendar and reports upcoming events. Use when the user asks what's on the calendar, about upcoming appointments, or to test the calendar connection.
---

# Agenda — skeleton

This is the thin-skeleton version: prove the calendar read works through
Latch's `gog`, no relevance filtering yet (that lands in US-12, adapted
from `plow-pbc/life-assistant-hermes-agent`'s `ld-calendar-nudge`).

## Gather

Read `calendar.account` and `calendar.sources` from
`/opt/data/mm/family_profile.json`, comma-join the sources' `calendar_id`
values, then call `plow_run_command` with this argv, substituting only
those config-supplied values:

    ["gog", "calendar", "events", "list", "--account=<calendar.account>",
     "--calendars=<comma-joined calendar_ids>",
     "--from=now", "--days=1", "--json", "--results-only", "--sort=start",
     "--max=5"]

## Post

Report every event returned — title, start time, whoever else is
attending, if present. No filtering by relevance yet; that is a later
skill. If the call fails (no calendar connected, bad account), say so
plainly instead of inventing an event.
