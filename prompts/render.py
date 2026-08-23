"""Render prompts/*.md templates with frontmatter and custom annotations."""

import re
from pathlib import Path

import yaml
from jinja2 import Environment, StrictUndefined

PRIORITY_RE = re.compile(r"\{%\s*priority\s+\w+\s*%\}(.*?)\{%\s*endpriority\s*%\}", re.DOTALL)
NOTE_RE = re.compile(r"\{%\s*note\s+\".*?\"\s*%\}")


def split_frontmatter(text: str) -> tuple[dict, str]:
    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        return yaml.safe_load(fm), body.strip()
    return {}, text


def strip_annotations(body: str) -> str:
    body = PRIORITY_RE.sub(r"\1", body)
    return NOTE_RE.sub("", body)


def render_prompt(path: Path | str, variables: dict) -> str:
    path = Path(path)
    env = Environment(undefined=StrictUndefined, keep_trailing_newline=True)
    _, body = split_frontmatter(path.read_text())
    content = env.from_string(strip_annotations(body)).render(**variables)
    return content
