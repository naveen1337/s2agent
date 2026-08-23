"""Tests for rendering prompts/system_prompt.md with sample variables."""

from pathlib import Path

import pytest
from jinja2 import UndefinedError

from prompts.render import render_prompt, split_frontmatter

PROMPT = Path(__file__).parent.parent / "prompts" / "system_prompt.md"

APPLIANCES = [
    {
        "name": "fridge",
        "category": "refrigeration",
        "specs": {"capacity_liters": 350, "energy_class": "A++", "noise_db": 38},
        "common_issues": [
            {"symptom": "Not cooling", "fix": "Check condenser coils for dust; clean if dirty."},
            {"symptom": "Water leaking", "fix": "Clear the defrost drain hole at the back."},
        ],
        "faqs": [
            {
                "question": "What size fridge for a family of four?",
                "answer": "300-400 liters is typical.",
            },
        ],
    },
    {
        "name": "washing machine",
        "category": "laundry",
        "specs": {"load_kg": 8, "spin_rpm": 1400, "energy_class": "A"},
        "common_issues": [
            {"symptom": "Vibrating loudly", "fix": "Level the feet and redistribute the load."},
        ],
    },
    {
        "name": "home AC",
        "category": "climate",
        "specs": {"cooling_btu": 12000, "noise_db": 32},
        "faqs": [
            {"question": "How often to clean filters?", "answer": "Every 2-4 weeks in heavy use."},
        ],
    },
]

VARS = {
    "assistant_name": "HomeHelper",
    "brand_tone": "warm and practical",
    "rules": [
        "Never fabricate model numbers, prices, or energy ratings.",
        "Never use markdown tables; present relational data in json code blocks.",
    ],
    "dos": ["State units explicitly (liters, dB, kWh/year, BTU)."],
    "donts": ["Don't promise repairs or warranty outcomes."],
    "appliances": APPLIANCES,
    "maintainer_notes": ["Keep specs in sync with manufacturer datasheets."],
    "max_response_words": 200,
}


@pytest.fixture()
def rendered() -> str:
    return render_prompt(PROMPT, VARS)


class TestFrontmatter:
    def test_meta_parsed(self):
        meta, body = split_frontmatter(PROMPT.read_text())
        assert meta["version"] == "0.2.0"
        assert meta["schema_version"] == 1
        assert "variables" in meta and "annotations" in meta
        assert "{% for" in body

    def test_all_variables_declared_required(self):
        meta, _ = split_frontmatter(PROMPT.read_text())
        assert set(meta["variables"]) == set(VARS)

    def test_no_default_filters_in_template(self):
        body = split_frontmatter(PROMPT.read_text())[1]
        assert "| default(" not in body


class TestRenderedContent:
    def test_variables_applied(self, rendered):
        assert "HomeHelper" in rendered
        assert "warm and practical" in rendered

    def test_all_appliances_rendered(self, rendered):
        assert "Fridge (refrigeration)" in rendered
        assert "Washing Machine (laundry)" in rendered
        assert "Home Ac (climate)" in rendered

    def test_specs_as_json_block(self, rendered):
        assert '"capacity_liters": 350' in rendered
        assert '"spin_rpm": 1400' in rendered
        assert '"cooling_btu": 12000' in rendered
        assert "```json" in rendered

    def test_no_markdown_tables(self, rendered):
        assert "| Spec | Value |" not in rendered
        assert "|------|" not in rendered

    def test_issues_and_faqs(self, rendered):
        assert "**Not cooling** → Check condenser coils" in rendered
        assert "Q: How often to clean filters?" in rendered

    def test_lists_rendered(self, rendered):
        assert "- Never fabricate model numbers" in rendered
        assert "- State units explicitly" in rendered
        assert "- Don't promise repairs" in rendered
        assert "- Keep specs in sync with manufacturer datasheets." in rendered

    def test_max_response_words_respected(self, rendered):
        assert "under 200 words" in rendered

    def test_empty_knowledge_base_fallback(self):
        out = render_prompt(PROMPT, {**VARS, "appliances": []})
        assert "No appliance knowledge loaded." in out


class TestAnnotations:
    def test_priority_blocks_unwrapped(self, rendered):
        assert "{% priority" not in rendered
        assert "{% endpriority" not in rendered
        assert "Treat this section as authoritative for fridge." in rendered

    def test_notes_stripped(self):
        from prompts.render import strip_annotations

        assert strip_annotations('{% note "todo" %}Keep this.') == "Keep this."


class TestStrictness:
    def test_missing_required_key_raises(self):
        bad = [{**APPLIANCES[0]}]
        del bad[0]["name"]
        with pytest.raises(Exception, match="name"):
            render_prompt(PROMPT, {**VARS, "appliances": bad})

    def test_missing_top_level_variable_raises(self):
        with pytest.raises(UndefinedError, match="rules"):
            render_prompt(PROMPT, {k: v for k, v in VARS.items() if k != "rules"})


if __name__ == "__main__":
    out = render_prompt(PROMPT, VARS)
    print(out)
