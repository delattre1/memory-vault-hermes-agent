from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SKILLS = (
    "ingerir_conteudo",
    "consultar_memoria",
    "executar_acao_real",
    "aprender_com_uso",
)


def deploy_hook():
    return (ROOT / "deploy-hook").read_text()


def test_deploy_hook_seeds_every_skill():
    for skill in SKILLS:
        assert f'"{skill}"' in deploy_hook() or skill in deploy_hook(), (
            f"deploy-hook does not seed {skill}"
        )


def test_deploy_hook_seeds_skills_copy_if_absent():
    text = deploy_hook()
    # The agent's own edits are kept, never overwritten by a re-seed.
    assert "keeping agent-owned" in text
    # The staging shape an interrupted copy leaves behind is *.incoming.
    assert "dest.incoming" in text


def test_deploy_hook_publishes_soul_md_every_deploy():
    text = deploy_hook()
    assert "runtime/SOUL.md" in text
    assert "published SOUL.md" in text


def test_compose_override_carries_no_skill_mounts():
    # Skills ride the deploy-hook seed into the agent's home, not :ro
    # mounts -- a :ro mount makes the agent's own skill edits die with
    # EROFS. The file itself is legitimate for other things a container
    # needs (HERMES_PROVIDER/HERMES_MODEL, read by plow-init from the real
    # process environment, never from the home .env) -- only a `volumes:`
    # section reintroducing the old mount-based skill delivery is the
    # regression this guards against.
    override = ROOT / "compose.override.yml"
    if not override.is_file():
        return
    assert "volumes:" not in override.read_text(), (
        "compose.override.yml declares volumes: -- skills are seeded by "
        "the deploy-hook now, not mounted read-only"
    )


def test_no_meal_planning_leftovers_remain():
    for name in ("fm-planner", "fm-shopping", "fm-homework", "fm-agenda", "fm-shared"):
        assert not (ROOT / name).exists(), f"{name} is a leftover of the pivoted domain"


def test_env_example_documents_the_dotenv_contract():
    text = (ROOT / ".env.example").read_text()
    for key in ("PLOW_HOME_CHANNEL", "DOMO_DEVICE_UID", "DOMO_MCP_TOKEN"):
        assert key in text, f".env.example does not document {key}"
    # Bare keys, no blank-value assignments: a present-but-empty key would
    # clobber a credential the container supplies (see the file's own comment).
    for line in text.splitlines():
        stripped = line.strip()
        for key in ("DOMO_DEVICE_UID", "DOMO_MCP_TOKEN"):
            if stripped == key:
                break
        else:
            if any(stripped.startswith(k + "=") for k in ("DOMO_DEVICE_UID", "DOMO_MCP_TOKEN")):
                raise AssertionError(f".env.example assigns a blank credential: {stripped!r}")


def test_descriptor_is_documented_in_env_example():
    example = (ROOT / ".env.example").read_text()
    assert "PLOW_HOME_CHANNEL=" in example


def test_readme_points_at_the_real_spec():
    readme = (ROOT / "README.md").read_text()
    assert "2026-09-03-jessie-content-memory-pivot-design.md" in readme
    spec = ROOT / "docs/superpowers/specs/2026-09-03-jessie-content-memory-pivot-design.md"
    assert spec.is_file(), "README links a spec that does not exist"


def test_skills_tsv_declares_no_connectors():
    # No connectors skill -- Latch is the only mcp_server (same shape the
    # sibling agents ship).
    content = (ROOT / "skills.tsv").read_text().strip()
    assert not content
