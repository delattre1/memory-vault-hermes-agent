# Run the whole suite: this agent's contracts and the skill contract checks.
#
# Same runner the sibling agents use -- uv, no project, pinned pytest -- so a
# checkout needs nothing installed beyond uv itself.
test:
    uv run --no-project --python 3.12 --with pytest==8.4.2 --with pyyaml==6.0.2 pytest -q tests/
