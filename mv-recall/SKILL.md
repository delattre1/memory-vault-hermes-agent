---
name: mv-recall
description: Use when the owner asks an open question that should draw on what they've saved — an itinerary from saved places, a recipe from the pantry, gift ideas, a recap of what was saved recently, what you know about a person, a timeline of what happened this week — rather than a fresh answer from scratch.
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
  saved about it. A person summary ("o que eu sei sobre a Ana?")
  asks for `limit=25` — the default 10 truncates months of events.
  A question about the *connection* ("o que o Pedro me recomendou?")
  is still this shape: probe who/what it names — facts tagged
  `relacao:*` state the connection, and the direction comes from
  each fact's own content, not co-occurrence.
- **A self-reflective question about patterns across everything
  saved** ("o que eu aparentemente gosto?", "o que isso diz sobre
  mim?", "analisa o que eu salvei", "faça um resumo do que eu tenho
  guardado") → `fact_store(action="search", query="", limit=200)` (or
  the highest `limit` available) — pull as broad a sample as you can,
  not a targeted match. This shape is answered differently; see Post.
- **A temporal recap** ("o que aconteceu comigo essa semana?", "meu
  mês em resumo", "o que eu andei fazendo?") → the same broad pull as
  the self-reflective question: `fact_store(action="search", query="",
  limit=200)`. The difference is the cut: keep the facts inside the
  asked window (read `created_at`, plus the dates the content states),
  order chronologically, narrate. One call — there is no date-range
  query in `fact_store`, so the window is cut on results, never on
  repeated filtered searches.
- **Neither** (a broad or vague question — "o que eu andei salvando
  esse mês?") → `fact_store(action="search", query="...")` as the
  general fallback.

If the question involves the owner's own pantry or people they know,
read `USER.md` (the `memory` tool) first — that's where that lives,
not in `fact_store` (see `runtime/SOUL.md`, "Two kinds of memory").

## If the probe comes back thin

Widen one step at a time, one call per step, stop as soon as the
answer's shape is there: `related(entity)` first (facts connected to
the entity through shared context — its neighborhood in the graph),
`search` as the last resort. And every result already carries
`created_at`/`updated_at` — a "quando comecei a falar sobre a Ana?"
reads the dates off results you already have, no second call.

## Filter

Drop any result with empty `tags`. Every fact `mv-ingest` ever
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
retrieved. Cite what you actually used. A cited fact carrying
`relacao:*` gets its connection named ("o João te recomendou o
restaurante X", not just "o restaurante X"). For a person question,
the answer is the union of both memories — who this person is to the
owner (`USER.md`) plus what's been saved about them, told in date
order. A person page, not a fact dump.

**For the self-reflective question**, the answer is different in
kind: count how often each tag/theme actually appears across what came
back, and say what you notice — the category that dominates, one
interesting or unexpected pattern, maybe an `acao:*` tag that shows up
over and over with nothing ever done about it, or a `relacao:*` tag
repeating across saves. This is an analysis of
what the owner chose to save, not a recommendation engine — never
invent a pattern the counted facts don't actually show, and never
stretch a handful of saves into a sweeping claim. Plain and specific
beats a corporate-report tone: "você salvou 18 restaurantes, a maioria
japoneses e italianos" over "you show a strong affinity for East Asian
and Mediterranean cuisine."

**Resurfacing** — after a real answer, one 🧠 line is allowed when a
strong connection sits in facts you cited or already fetched: a cited
entity also sits in ≥2 facts ≥14 days old, or a tag repeats across
≥3 facts spanning ≥30 days ("isso voltou a aparecer: 5 restaurantes
japoneses e 3 receitas de ramen"). One line, observation never an
order, span read off `created_at`. Skip it on a self-reflective
question (that answer already IS the analysis), on a temporal recap
(the timeline already IS the connection, narrated), on a turn that
hands off to `mv-act` (the action is the point), and when
this session already surfaced the same connection. Below threshold,
silence.

**For a temporal recap**, the answer is a timeline: the facts inside
the window, chronological, dated, in the owner's own life terms
("segunda você salvou X; quarta jantou no Y com Maria") — not a grouped
report, not a dump. Facts outside the window are dropped, not
mentioned. Facts cited this way are individually cited, so they get
`fact_feedback` as usual.

If any fact you cited carries an `acao:*` tag other than
`acao:nenhuma`, say so and hand off to `mv-act` instead of
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
