from pathlib import Path

import pytest

# A skill is any top-level folder with a SKILL.md -- no shared name prefix
# (the fm-* convention was specific to the meal-planning domain this
# project pivoted away from; see docs/roadmap.md).
ROOT = Path(__file__).resolve().parent.parent
SKILL_DIRS = sorted(
    p.name
    for p in ROOT.iterdir()
    if p.is_dir() and not p.name.startswith(".") and (p / "SKILL.md").is_file()
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
