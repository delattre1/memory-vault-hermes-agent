---
name: mv-learn
description: Use when the owner corrects something about a saved item ("isso é receita, não produto", "essa entidade tá errada", "não era isso que eu quis dizer") — fixes it in place, right away.
---

# Aprender com uso

Most of the learning loop is already native and automatic, not this
skill's job:

- `mv-recall` already calls `fact_feedback` on every fact it
  cites — that trains `fact_store`'s trust score on its own.
- Hermes' own skill-authoring loop (`hermes journey`) is the deeper
  mechanism for learning across sessions.

This skill's job is narrower: when the owner corrects a specific saved
item, fix that one fact **immediately**, not as a batch job for later.

## Gather

Find the fact_id being corrected — from the conversation just now if
it's still in context, otherwise `fact_store(action="search", ...)`
for it. Never guess a fact_id.

## Filter

Work out what actually changes: a wrong tag, a wrong category, a
detail the extraction got backwards. Keep everything else about the
fact as-is — including the `relacao:*` tags (an update rewrites `tags`
wholesale; dropping them silently disconnects the fact from the graph)
— a correction fixes the one thing named, it doesn't re-extract from
scratch.

## Post

Call `fact_store(action="update", fact_id=..., ...)` with the fix
right away. Confirm in one line what changed (e.g. "corrigido: essa é
uma receita, não um produto"). A correction that only gets logged for
later isn't a fix — the next question about that item must already see
it corrected.
