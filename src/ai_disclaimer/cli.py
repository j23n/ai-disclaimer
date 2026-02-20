"""CLI entry point."""
from __future__ import annotations

import sys
from dataclasses import asdict
from datetime import date
from pathlib import Path

from .config import CONFIG_FILENAME, DisclaimerConfig, OutputConfig, load_config, save_config
from .prompts import (
    collect_accountability,
    collect_output,
    collect_oversight,
    collect_phases,
    collect_process,
    collect_project,
    collect_tools,
    confirm,
)
from .render import render_html, render_markdown


def _write_output(cfg: DisclaimerConfig) -> None:
    project = asdict(cfg.project)
    tools = [asdict(t) for t in cfg.tools]
    phases = [asdict(p) for p in cfg.phases]
    oversight = asdict(cfg.oversight)

    if cfg.output.format == "Markdown":
        content = render_markdown(project, tools, phases, oversight, cfg.process, cfg.accountability)
    else:
        content = render_html(project, tools, phases, oversight, cfg.process, cfg.accountability, theme=cfg.output.theme)

    if cfg.output.filename:
        with open(cfg.output.filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"\n✓ Written to {cfg.output.filename}")
    else:
        print()
        print(content)


def main() -> None:
    print("╔══════════════════════════════════════════╗")
    print("║       AI Disclaimer Generator            ║")
    print("╚══════════════════════════════════════════╝")
    print("  Answer each prompt to build your disclaimer.")
    print("  Press Ctrl-C at any time to exit.\n")

    config_path = Path(CONFIG_FILENAME)
    if config_path.exists():
        if confirm(f"Found {CONFIG_FILENAME}. Regenerate using saved settings?", default=True):
            cfg = load_config(config_path)
            if cfg is None:
                print(f"  Could not read {CONFIG_FILENAME}. Starting questionnaire.\n")
            else:
                cfg.project.date = date.today().isoformat()
                _write_output(cfg)
                return

    try:
        project = collect_project()
        tools = collect_tools()
        phases = collect_phases()
        oversight = collect_oversight()
        process = collect_process(tools)
        accountability = collect_accountability()
        output = collect_output()
    except KeyboardInterrupt:
        print("\nAborted.")
        sys.exit(0)

    cfg = DisclaimerConfig.from_dict({
        "project": project,
        "tools": tools,
        "phases": phases,
        "oversight": oversight,
        "process": process,
        "accountability": accountability,
        "output": output,
    })
    save_config(cfg, config_path)
    print(f"  Settings saved to {CONFIG_FILENAME}")

    _write_output(cfg)
