"""Home COPY of config.yaml is shadowed; vault gates have to land on the seed."""

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def _load():
    path = ROOT / "image/merge_mv_seed_config.py"
    spec = importlib.util.spec_from_file_location("merge_mv_seed", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_overlay_keeps_relay_and_stamps_vault_gates():
    merge = _load()
    seed = {
        "mcp_servers": {"plow": {"url": "stdio"}},
        "plugins": {"enabled": ["other"], "entries": {"other": {}}},
        "display": {"busy_ack_enabled": False},
    }
    ours = {
        "_config_version": 39,
        "group_sessions_per_user": False,
        "memory": {"provider": "holographic"},
        "mcp_servers": {"latch": {"url": "https://api.plow.co/v1/relay/devices/${DOMO_DEVICE_UID}/mcp"}},
        "plugins": {
            "enabled": ["plow-chat-platform"],
            "entries": {"plow-chat-platform": {"allow_tool_override": False}},
            "hermes-memory-store": {"db_path": "${HERMES_HOME}/memory_store.db"},
        },
        "platform_toolsets": {"plow_chat": ["memory", "skills", "terminal"]},
    }
    out = merge.overlay(seed, ours)
    assert out["mcp_servers"]["plow"]["url"] == "stdio"
    assert "latch" in out["mcp_servers"]
    assert out["memory"]["provider"] == "holographic"
    assert out["group_sessions_per_user"] is False
    assert out["_config_version"] == 39
    assert "plow-chat-platform" in out["plugins"]["enabled"]
    assert "other" in out["plugins"]["enabled"]
    assert out["plugins"]["hermes-memory-store"]["db_path"] == "${HERMES_HOME}/memory_store.db"
    assert out["display"]["busy_ack_enabled"] is False
    merge._require(out)


def test_require_rejects_web_in_the_toolset():
    merge = _load()
    seed = {
        "memory": {"provider": "holographic"},
        "mcp_servers": {"latch": {}},
        "group_sessions_per_user": False,
        "platform_toolsets": {"plow_chat": ["memory", "web"]},
    }
    with pytest.raises(SystemExit, match="web"):
        merge._require(seed)
