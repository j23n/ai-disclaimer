"""Config persistence: dataclasses for settings, serialized as JSON."""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict, field
from pathlib import Path

CONFIG_FILENAME = ".ai-disclaimer.json"


@dataclass
class ProjectConfig:
    name: str
    policy_url: str
    date: str


@dataclass
class ToolConfig:
    name: str
    model: str
    mode: str


@dataclass
class PhaseConfig:
    name: str
    preset: str
    human: int | None
    ai: int | None


@dataclass
class OversightConfig:
    label: str
    description: str


@dataclass
class OutputConfig:
    format: str
    filename: str
    theme: str


@dataclass
class DisclaimerConfig:
    project: ProjectConfig
    tools: list[ToolConfig] = field(default_factory=list)
    phases: list[PhaseConfig] = field(default_factory=list)
    oversight: OversightConfig = field(default_factory=lambda: OversightConfig("", ""))
    process: str = ""
    accountability: str = ""
    output: OutputConfig = field(default_factory=lambda: OutputConfig("Markdown", "", "auto"))

    @classmethod
    def from_dict(cls, d: dict) -> DisclaimerConfig:
        proj = d.get("project", {})
        out = d.get("output", {})
        return cls(
            project=ProjectConfig(**proj),
            tools=[ToolConfig(**t) for t in d.get("tools", [])],
            phases=[PhaseConfig(**p) for p in d.get("phases", [])],
            oversight=OversightConfig(**d.get("oversight", {"label": "", "description": ""})),
            process=d.get("process", ""),
            accountability=d.get("accountability", ""),
            output=OutputConfig(**out),
        )


def save_config(cfg: DisclaimerConfig, path: Path = Path(CONFIG_FILENAME)) -> None:
    path.write_text(json.dumps(asdict(cfg), indent=2), encoding="utf-8")


def load_config(path: Path = Path(CONFIG_FILENAME)) -> DisclaimerConfig | None:
    try:
        return DisclaimerConfig.from_dict(json.loads(path.read_text(encoding="utf-8")))
    except Exception:
        return None
