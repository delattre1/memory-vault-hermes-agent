"""The usage reporter is the base image's own.

The plow-cloud-agents base ships the agent-index s6 service and the client at
/opt/plow/agent-index-client.py. A second copy here would shadow the base's
and drift from it, so this repo carries neither.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_the_reporter_comes_from_the_base_not_this_repo():
    assert not (ROOT / "image/s6-overlay/s6-rc.d/agent-index").exists()
    assert not (ROOT / "image/s6-overlay/s6-rc.d/user/contents.d/agent-index").exists()
    assert not (ROOT / "vendor/client.pin").exists()
    assert "agent-index-client" not in (ROOT / "Dockerfile").read_text()


def test_no_bespoke_s6_layout_outside_the_image_tree():
    """A bind mount whose source is missing does not fail: the runtime creates a
    DIRECTORY at the target. compose.yml is the runtime surface;
    compose.override.yml must not exist beside it.
    """
    assert not (ROOT / "docker/s6-rc.d").exists()
    assert (ROOT / "compose.yml").is_file()
    assert not (ROOT / "compose.override.yml").exists()
