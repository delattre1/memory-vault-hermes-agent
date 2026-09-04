---
name: consultar_memoria
description: Use when the owner asks an open question that should draw on what they've saved — an itinerary from saved places, a recipe from the pantry, gift ideas, a recap of what was saved recently — rather than a fresh answer from scratch.
---

# Consultar memória

No ranking script of our own — `fact_store` already returns results
ordered by relevance × trust. Pick the action by the shape of the
question, then synthesize.

## Gather

- **Two or more entities named or implied** (e.g. ingredients from the
  pantry, two places at once) → `fact_store(action="reason",
  entities=[...])` — facts connected to more than one of them at the
  same time. This is the one that answers "what can I cook with X and
  Y" or "what connects these saved things".
- **One clear central entity** (a person, a single place, a single
  topic) → `fact_store(action="probe", entity="...")` — everything
  saved about it.
- **Neither** (a broad or vague question — "o que eu andei salvando
  esse mês?") → `fact_store(action="search", query="...")` as the
  general fallback.

If the question involves the owner's own pantry or people they know,
read `USER.md` (the `memory` tool) first — that's where that lives,
not in `fact_store` (see `runtime/SOUL.md`, "Two kinds of memory").

## Filter

None — use what `fact_store` returned as-is, within the `limit` you
asked for. Don't re-rank it yourself.

## Post

Synthesize a real answer from the facts you got back — an itinerary,
a recipe match, a gift list, a recap — not a raw list of what was
retrieved. Cite what you actually used.

If any fact you cited carries an `acao:*` tag other than
`acao:nenhuma`, say so and hand off to `executar_acao_real` instead of
just describing the action.

After answering, call `fact_feedback(action="helpful", fact_id=...)`
on every fact you actually cited — that's what trains `fact_store` for
next time. Don't rate facts you looked at but didn't use.
