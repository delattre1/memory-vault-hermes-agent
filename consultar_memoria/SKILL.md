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
- **A self-reflective question about patterns across everything
  saved** ("o que eu aparentemente gosto?", "o que isso diz sobre
  mim?", "analisa o que eu salvei", "faça um resumo do que eu tenho
  guardado") → `fact_store(action="search", query="", limit=200)` (or
  the highest `limit` available) — pull as broad a sample as you can,
  not a targeted match. This shape is answered differently; see Post.
- **Neither** (a broad or vague question — "o que eu andei salvando
  esse mês?") → `fact_store(action="search", query="...")` as the
  general fallback.

If the question involves the owner's own pantry or people they know,
read `USER.md` (the `memory` tool) first — that's where that lives,
not in `fact_store` (see `runtime/SOUL.md`, "Two kinds of memory").

## Filter

Drop any result with empty `tags`. Every fact `ingerir_conteudo` ever
writes has tags — an untagged fact is leftover owner-profile data that
leaked into `fact_store` by mistake (a known gap: it belongs in
`memory`/`USER.md` and sometimes ends up written to both), not real
saved content, and must never be cited or shown to the owner as
something they saved.

Otherwise, use what `fact_store` returned as-is, within the `limit`
you asked for — no ranking script of our own on top of it. (The
self-reflective question above is the one exception: there, counting
how often each tag actually appears IS the analysis, not a ranking
imposed on individual results.)

## Post

Synthesize a real answer from the facts you got back — an itinerary,
a recipe match, a gift list, a recap — not a raw list of what was
retrieved. Cite what you actually used.

**For the self-reflective question**, the answer is different in
kind: count how often each tag/theme actually appears across what came
back, and say what you notice — the category that dominates, one
interesting or unexpected pattern, maybe an `acao:*` tag that shows up
over and over with nothing ever done about it. This is an analysis of
what the owner chose to save, not a recommendation engine — never
invent a pattern the counted facts don't actually show, and never
stretch a handful of saves into a sweeping claim. Plain and specific
beats a corporate-report tone: "você salvou 18 restaurantes, a maioria
japoneses e italianos" over "you show a strong affinity for East Asian
and Mediterranean cuisine."

If any fact you cited carries an `acao:*` tag other than
`acao:nenhuma`, say so and hand off to `executar_acao_real` instead of
just describing the action.

After answering, call `fact_feedback(action="helpful", fact_id=...)`
on every fact you actually cited — that's what trains `fact_store` for
next time. Don't rate facts you looked at but didn't use. Skip this
for the self-reflective question — nothing there was individually
cited, the count across all of them was.

## When there's nothing relevant

If every result comes back empty or unrelated (after dropping
untagged ones above), say plainly that there's nothing saved about
that yet — don't stretch an unrelated fact into an answer, and don't
invent one. "Você não salvou nada sobre isso ainda" is a complete,
correct answer.
