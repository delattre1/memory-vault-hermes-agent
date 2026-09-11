# memory-vault-hermes-agent

Memory Vault is a second memory for saved content: send it a screenshot
or a link — a trip, a recipe, a product, a gift idea — and it keeps it
without asking you to categorize anything. Later, ask it something
that only makes sense cross-referencing what you saved (an itinerary
from your saved places, a recipe from what's in the pantry, gift
ideas), and — when it makes sense — it acts for real through Plow
Latch. One Hermes agent, reached over Plow Chat. It is not a person
and not a character: when asked, it says it's a memory assistant.

Full architecture: `docs/superpowers/specs/2026-09-03-jessie-content-memory-pivot-design.md`.
Day-by-day build plan: `docs/roadmap.md`.

## What it can and cannot reach

- Saved content lives in Hermes' own built-in memory (the
  `holographic` fact store) — no database of our own. The owner's
  profile (people, pantry) lives in `USER.md` via the native `memory`
  tool. Neither is written by hand outside those tools.
- Acts on the owner's Mac through Plow Latch: browsing, and whatever
  else the owner has approved. Every Latch action goes through Latch's
  own approval gate — nothing runs unattended the first time.
- Has no email or messaging identity of its own. It reads the owner's
  own accounts through Latch; see `runtime/SOUL.md` for the rule that it
  never presents itself as the owner.
- Does not move money or place a real purchase without an explicit
  human confirmation step.

## Bringing it up

```sh
agent-mgr deploy memory-vault
agent-mgr activate memory-vault   # only once per AGENT_HOME
agent-mgr up memory-vault
agent-mgr sign-in memory-vault    # OpenRouter credential, once per AGENT_HOME
agent-mgr set-latch memory-vault  # Latch pair, once per AGENT_HOME
agent-mgr check-latch memory-vault
```

Editing `runtime/SOUL.md`, `config.yaml`, or a skill only needs
`agent-mgr deploy memory-vault` again — `activate`, `sign-in`, and
`set-latch` mint per-instance credentials and only need to run once
against a given `AGENT_HOME`.

## Testing

```sh
uv run --no-project --python 3.12 --with pytest==8.4.2 --with pyyaml==6.0.2 pytest -q tests/
```

## How to audit the agent

Every session — what was sent, what the Vault reasoned, what it did — is
recorded by Hermes itself; nothing here is bespoke logging.

```sh
# Recent sessions
docker exec --user "$(id -u):$(id -g)" hermes-memory-vault hermes sessions list

# One interaction, full reasoning and tool calls, human-readable
docker exec --user "$(id -u):$(id -g)" hermes-memory-vault \
  hermes sessions export --session-id <id> --format md

# The last week, secrets redacted, ready for review
docker exec --user "$(id -u):$(id -g)" hermes-memory-vault \
  hermes sessions export --newer-than 7d --format md --redact

# Browse visually instead of the command line
docker exec --user "$(id -u):$(id -g)" hermes-memory-vault hermes dashboard
```

`runtime/SOUL.md` requires that any action with a real effect (a
purchase, a message sent, a calendar change) be identifiable afterward
through `hermes sessions export` — never only through the chat reply.
