#!/usr/bin/env python3
"""Placeholder gate for family_profile.json (US-01, roadmap.md).

Same convention as plow-pbc/life-assistant-hermes-agent's ld_config_gate.py:
gate(config) returns the joined failure text (empty string == pass), scoped
here to one check -- no [UPPER_SNAKE] placeholder from
fm-shared/references/family_profile.example.json survives into the real
config. main() is a thin CLI wrapper: it exits non-zero and prints the
failure when the gate does not pass, unlike ld_config_gate.py's own
always-zero-exit convention -- this is what every skill's compose.override.yml
gate check needs to fail loudly rather than silently.
"""
import json
import re
import sys

_PLACEHOLDER_RE = re.compile(r"^\[[A-Z][A-Z0-9_]*\]$")


def _all_strings(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for value in node.values():
            yield from _all_strings(value)
    elif isinstance(node, list):
        for value in node:
            yield from _all_strings(value)


def gate(config):
    """Return the failure text for a parsed config (empty string == pass)."""
    if any(_PLACEHOLDER_RE.match(s) for s in _all_strings(config)):
        return "an unfilled [UPPER_SNAKE] placeholder remains"
    return ""


def main(argv):
    if len(argv) != 2:
        sys.stderr.write("usage: config_gate.py <family_profile.json>\n")
        return 2
    with open(argv[1], encoding="utf-8") as f:
        config = json.load(f)
    failure = gate(config)
    if failure:
        sys.stderr.write(failure + "\n")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
