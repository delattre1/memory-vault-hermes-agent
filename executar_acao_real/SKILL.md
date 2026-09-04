---
name: executar_acao_real
description: Use whenever the owner wants to actually move forward on something saved — a reservation, a purchase, adding to the calendar — whether that follows a `consultar_memoria` answer in the same turn or the owner asks directly ("avança a reserva que salvei", "compra isso"). The trigger is the owner's intent to act, not a specific prior tool call.
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
never a batch of steps in one call. **Always the `mcp__latch` tools
(`plow_browser_open`/`plow_browser`/`plow_write_file`/`plow_run_command`)
— never a generic/local tool that happens to also open a browser or
fetch a page** (`browser_exec`, `web_search`, `web_extract`, `terminal`
+ `curl`, and so on). Those aren't Latch: they don't run on the
owner's Mac, don't go through Latch's approval gate, and one of them
(`browser_exec`) needs a local Chrome this container doesn't have — if
`plow_browser_open` itself fails, that's Latch reporting a real error
you relay to the owner, not a cue to switch tools.

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
