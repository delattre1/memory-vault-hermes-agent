from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIRS = sorted(
    p.name for p in ROOT.glob("fm-*") if p.is_dir() and p.name != "fm-shared"
)


@pytest.mark.parametrize("skill", SKILL_DIRS)
def test_every_skill_has_a_skill_md(skill):
    assert (ROOT / skill / "SKILL.md").is_file()


@pytest.mark.parametrize("skill", SKILL_DIRS)
def test_every_skill_md_frontmatter_names_itself(skill):
    text = (ROOT / skill / "SKILL.md").read_text()
    frontmatter = text.split("---")[1] if text.startswith("---") else ""
    assert f"name: {skill}" in frontmatter


@pytest.mark.parametrize("skill", SKILL_DIRS)
def test_every_skill_md_description_says_when_to_use_it(skill):
    text = (ROOT / skill / "SKILL.md").read_text()
    frontmatter = text.split("---")[1] if text.startswith("---") else ""
    assert "Use when" in frontmatter
