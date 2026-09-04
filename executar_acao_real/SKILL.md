---
name: executar_acao_real
description: Use when a fact `consultar_memoria` cited carries an `acao:*` tag other than `acao:nenhuma` (reserva, compra, calendario) and the owner wants to actually move on it, not just hear about it.
---

# Executar ação real

This skill does not implement its own approval gate — it relies
entirely on Plow Latch's, which is already enforced underneath every
call it makes. Its job is to ask Latch for the narrowest thing that
moves the specific action forward, never more.

## Gather

Read the `acao:*` tag on the fact that triggered this (from
`consultar_memoria`'s citation) and the owner's own message for
specifics (a date, a restaurant name, a budget) — ask for what's
missing before acting if the fact alone isn't enough to act on
correctly.

## Filter

Map the tag to the narrowest Latch capability for *this one step*,
never a batch of steps in one call:

- `acao:reserva` → `plow_browser_open`/`plow_browser` to find and
  submit the reservation on the relevant site.
- `acao:compra` → `plow_browser_open`/`plow_browser` to add to cart —
  **never completes checkout**; that always stops for an explicit
  human confirmation, same rule as any purchase.
- `acao:calendario` → `plow_write_file` or the calendar tool already
  wired through Latch, to add the one event described.

## Post

Report plainly what happened: whether Latch's gate approved
automatically (an existing always-allow rule matched) or asked the
owner first, and what the actual outcome was — never claim an action
completed if the gate rejected it or the owner never answered. If
rejected or timed out, say so and stop; don't retry silently or fall
back to a different action on your own judgment.
