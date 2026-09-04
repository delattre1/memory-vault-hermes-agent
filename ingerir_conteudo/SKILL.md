---
name: ingerir_conteudo
description: Use when the owner sends something they want remembered — a screenshot, a link, or a plain description of a place/recipe/product/gift idea — and wants it saved for later, not answered right now.
---

# Ingerir conteúdo — skeleton (text only)

This is the thin-skeleton version: it proves the plumbing (a saved
message becomes a searchable fact), not the real image/link extraction
— that lands next. For now the input is the owner's own text
description of what they want saved (e.g. "salva isso: praia em
Santorini, Grécia — restaurante à beira-mar").

## Gather

The content to save is the owner's message itself — no fetch needed
yet (image and link handling are separate, later skills).

## Filter

From the owner's text, work out:

- `summary` — one sentence.
- `tags` — a short comma-separated list of the concepts involved
  (e.g. `viagem,praia,grecia,restaurante`).
- `entities` — the proper nouns involved (place names, dish names,
  product names, person names).
- `actionability` — one of `reserva`, `compra`, `calendario`,
  `nenhuma` (does this content point at a real-world action later?).

## Post

Call `fact_store` with `action=add`. Two things matter for how you
write `content`, both load-bearing (see
`docs/superpowers/specs/2026-09-03-jessie-content-memory-pivot-design.md`,
§6.1 — `fact_store`'s own entity linking is a simple regex over
capitalized phrases and quoted terms, not real NLP):

- Put every entity from your extraction in double quotes inside the
  sentence, even if it's also capitalized (e.g. `"Santorini"`,
  `"Grécia"`) — quoting is a second, independent way `fact_store`
  recognizes a term, so an entity that's quoted AND capitalized is
  linked reliably even if one signal alone would have missed it.
- Pass `tags` as the same concepts from your extraction, comma-separated,
  plus `acao:<actionability>` (e.g. `acao:reserva`, or `acao:nenhuma`
  when nothing applies). `tags` doesn't depend on the regex at all —
  it's the reliable fallback.

Example call:

```
fact_store(
  action="add",
  content='Post de "viagem": praia em "Santorini", "Grécia" — restaurante à beira-mar, possível "reserva".',
  tags="viagem,praia,grecia,restaurante,acao:reserva",
)
```

After the call, confirm to the owner in one line what you understood
and saved (e.g. "salvei: Santorini, praia, grécia, restaurante") — this
is what lets them correct you immediately if the extraction is wrong.
