"""Interactive questionnaire prompts and input helpers."""
from __future__ import annotations

import sys
from datetime import date

import questionary

from .presets import (
    DEFAULT_ACCOUNTABILITY,
    MODES,
    OVERSIGHT,
    PHASE_PRESETS,
    PHASES,
    PROCESS_DEFAULTS,
    TOOLS,
)


def section(title: str) -> None:
    width = 60
    print(f"\n{'─' * width}")
    print(f"  {title}")
    print(f"{'─' * width}")


def ask(prompt: str, default: str = "", required: bool = False) -> str:
    while True:
        try:
            result = questionary.text(prompt, default=default).ask()
        except KeyboardInterrupt:
            sys.exit(0)
        if result is None:
            sys.exit(0)
        result = result.strip()
        if required and not result:
            print("  (this field is required)")
            continue
        return result


def choose(prompt: str, choices: list) -> str:
    try:
        result = questionary.select(prompt, choices=choices).ask()
    except KeyboardInterrupt:
        sys.exit(0)
    if result is None:
        sys.exit(0)
    return result


def confirm(prompt: str, default: bool = True) -> bool:
    try:
        result = questionary.confirm(prompt, default=default).ask()
    except KeyboardInterrupt:
        sys.exit(0)
    if result is None:
        sys.exit(0)
    return result


def collect_project() -> dict:
    section("Project Info")
    name = ask("Project name:", required=True)
    policy_url = ask("AI policy URL (optional, press Enter to skip):", default="")
    today = date.today().isoformat()
    d = ask("Date (YYYY-MM-DD):", default=today)
    return {"name": name, "policy_url": policy_url, "date": d or today}


def collect_tools() -> list[dict]:
    section("AI Tools Used")
    tools_used = []
    while True:
        tool_labels = [t["label"] for t in TOOLS]
        tool_label = choose("Select AI tool:", tool_labels)
        tool_entry = next(t for t in TOOLS if t["label"] == tool_label)

        if tool_entry["models"]:
            model_choices = tool_entry["models"] + ["Other (type below)"]
            model_choice = choose("Select model:", model_choices)
            if model_choice == "Other (type below)":
                model = ask("Model name:", required=True)
            else:
                model = model_choice
        else:
            model = ask("Model name (optional):", default="")

        mode = choose("Usage mode:", MODES)
        tools_used.append({"name": tool_label, "model": model, "mode": mode})

        if not confirm("Add another tool?", default=False):
            break
    return tools_used


def collect_phases() -> list[dict]:
    section("Contribution by Phase")
    print("  For each phase, pick a preset then optionally adjust percentages.")
    phases_out = []
    preset_labels = [p[0] for p in PHASE_PRESETS]

    for phase_name in PHASES:
        print(f"\n  Phase: {phase_name}")
        preset_label = choose(f"  Preset for '{phase_name}':", preset_labels)
        preset = next(p for p in PHASE_PRESETS if p[0] == preset_label)
        _, human_pct, ai_pct = preset

        if preset_label == "Custom":
            raw = ask("  Human %:", default="50")
            try:
                human_pct = max(0, min(100, int(raw)))
            except ValueError:
                human_pct = 50
            ai_pct = 100 - human_pct
        elif human_pct is not None:
            if confirm(f"  Adjust percentages? (currently {human_pct}% human / {ai_pct}% AI)", default=False):
                raw = ask("  Human %:", default=str(human_pct))
                try:
                    human_pct = max(0, min(100, int(raw)))
                except ValueError:
                    pass
                ai_pct = 100 - human_pct

        phases_out.append({
            "name": phase_name,
            "preset": preset_label,
            "human": human_pct,
            "ai": ai_pct,
        })
    return phases_out


def collect_oversight() -> dict:
    section("Oversight Level")
    label = choose("Select oversight level:", list(OVERSIGHT.keys()))
    default_desc = OVERSIGHT[label]
    print(f"  Default: {default_desc}")
    if confirm("  Edit description?", default=False):
        description = ask("  Description:", default=default_desc, required=True)
    else:
        description = default_desc
    return {"label": label, "description": description}


def collect_process(tools: list[dict]) -> str:
    section("Development Process")
    first_mode = tools[0]["mode"] if tools else "Mixed"
    key = first_mode if first_mode in PROCESS_DEFAULTS else "Mixed"
    default_text = PROCESS_DEFAULTS[key]
    print(f"  Suggested process (based on '{first_mode}' mode):")
    print(f"  {default_text}")
    if confirm("  Edit?", default=False):
        return ask("  Process description:", default=default_text, required=True)
    return default_text


def collect_accountability() -> str:
    section("Accountability Statement")
    print(f"  Default: {DEFAULT_ACCOUNTABILITY}")
    if confirm("  Edit?", default=False):
        return ask("  Statement:", default=DEFAULT_ACCOUNTABILITY, required=True)
    return DEFAULT_ACCOUNTABILITY


def collect_output() -> dict:
    section("Output")
    fmt = choose("Output format:", ["Markdown", "HTML"])
    theme = "auto"
    if fmt == "HTML":
        theme_choice = choose("Color theme:", ["Auto (system preference)", "Light", "Dark"])
        theme = {"Auto (system preference)": "auto", "Light": "light", "Dark": "dark"}[theme_choice]
    dest = choose("Write to:", ["stdout", "file"])
    filename = ""
    if dest == "file":
        ext = "md" if fmt == "Markdown" else "html"
        default_name = f"AI_DISCLAIMER.{ext}"
        filename = ask("Filename:", default=default_name, required=True)
    return {"format": fmt, "filename": filename, "theme": theme}
