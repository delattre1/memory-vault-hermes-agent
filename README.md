# jessie-hermes-assistant

Jessie is a family assistant for parents with kids: weekly meal plans,
the shopping list, school material, the kids' routine — one Hermes
agent, reached over Plow Chat, acting on the owner's own Mac through
Plow Latch.

## What it can and cannot reach

- Reads `family_profile.json` (family members, dietary restrictions,
  calendar sources) — mounted read-only, never written by a skill.
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
agent-mgr deploy jessie-assistant
agent-mgr activate jessie-assistant   # only once per AGENT_HOME
agent-mgr up jessie-assistant
agent-mgr sign-in jessie-assistant    # OpenRouter credential, once per AGENT_HOME
agent-mgr set-latch jessie-assistant  # Latch pair, once per AGENT_HOME
agent-mgr check-latch jessie-assistant
```

Editing `runtime/SOUL.md`, `config.yaml`, or a skill only needs
`agent-mgr deploy jessie-assistant` again — `activate`, `sign-in`, and
`set-latch` mint per-instance credentials and only need to run once
against a given `AGENT_HOME`.

## Testing

```sh
uv run --no-project --python 3.12 --with pytest==8.4.2 --with pyyaml==6.0.2 pytest -q tests/
```

## How to audit the agent

Every session — what was sent, what Jessie reasoned, what she did — is
recorded by Hermes itself; nothing here is bespoke logging.

```sh
# Recent sessions
docker exec --user "$(id -u):$(id -g)" hermes-jessie-assistant hermes sessions list

# One interaction, full reasoning and tool calls, human-readable
docker exec --user "$(id -u):$(id -g)" hermes-jessie-assistant \
  hermes sessions export --session-id <id> --format md

# The last week, secrets redacted, ready for review
docker exec --user "$(id -u):$(id -g)" hermes-jessie-assistant \
  hermes sessions export --newer-than 7d --format md --redact

# Browse visually instead of the command line
docker exec --user "$(id -u):$(id -g)" hermes-jessie-assistant hermes dashboard
```

`runtime/SOUL.md` requires that any action with a real effect (a
purchase, a message sent, a calendar change) be identifiable afterward
through `hermes sessions export` — never only through the chat reply.
