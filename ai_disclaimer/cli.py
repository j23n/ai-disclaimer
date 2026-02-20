"""CLI entry point."""
from __future__ import annotations

import sys

from .prompts import (
    collect_accountability,
    collect_output,
    collect_oversight,
    collect_phases,
    collect_process,
    collect_project,
    collect_tools,
)
from .render import render_html, render_markdown


def main() -> None:
    print("╔══════════════════════════════════════════╗")
    print("║       AI Disclaimer Generator            ║")
    print("╚══════════════════════════════════════════╝")
    print("  Answer each prompt to build your disclaimer.")
    print("  Press Ctrl-C at any time to exit.\n")

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

    if output["format"] == "Markdown":
        content = render_markdown(project, tools, phases, oversight, process, accountability)
    else:
        content = render_html(project, tools, phases, oversight, process, accountability, theme=output["theme"])

    if output["filename"]:
        with open(output["filename"], "w", encoding="utf-8") as f:
            f.write(content)
        print(f"\n✓ Written to {output['filename']}")
    else:
        print()
        print(content)
