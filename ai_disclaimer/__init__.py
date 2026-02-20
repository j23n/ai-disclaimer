"""AI Disclaimer Generator — interactive CLI tool."""
from __future__ import annotations

import html
import sys
from datetime import date

import questionary

# ---------------------------------------------------------------------------
# Presets
# ---------------------------------------------------------------------------

TOOLS = [
    {
        "label": "Claude Code (Anthropic)",
        "models": [
            "claude-sonnet-4-6",
            "claude-opus-4-6",
            "claude-haiku-4-5-20251001",
        ],
    },
    {
        "label": "GitHub Copilot",
        "models": [
            "Claude Sonnet 4.6",
            "Claude Opus 4.6",
            "Claude Sonnet 4.5",
            "Claude Opus 4.5",
            "GPT-5.3-Codex",
            "GPT-5.2-Codex",
            "GPT-5.1-Codex",
            "GPT-4.1",
            "Gemini 3.1 Pro",
            "Gemini 3 Pro",
            "Gemini 2.5 Pro",
        ],
    },
    {
        "label": "Cursor",
        "models": [
            "Claude Sonnet 4.6",
            "Claude Opus 4.6",
            "Claude Sonnet 4.5",
            "Claude Opus 4.5",
            "GPT-5.3 Codex",
            "GPT-5.1 Codex",
            "GPT-5",
            "Gemini 3.1 Pro",
            "Gemini 3 Pro",
            "Composer 1.5",
        ],
    },
    {
        "label": "ChatGPT",
        "models": [
            "o3",
            "o4-mini",
            "GPT-4o",
        ],
    },
    {
        "label": "Gemini",
        "models": [
            "gemini-3.1-pro",
            "gemini-3-pro",
            "gemini-3-flash",
            "gemini-2.5-pro",
        ],
    },
    {
        "label": "Windsurf/Codeium",
        "models": [
            "SWE-1.5",
            "Claude Sonnet 4.6",
            "Claude Opus 4.6",
            "GPT-5.3-Codex",
            "Gemini 3.1 Pro",
        ],
    },
    {"label": "Other", "models": []},
]

MODES = [
    "Inline suggestion",
    "Conversational",
    "Agentic",
    "Mixed",
]

PHASE_PRESETS = [
    ("Human-led", 85, 15),
    ("Collaborative", 50, 50),
    ("AI-collaborative", 40, 60),
    ("AI-generated with human review", 20, 80),
    ("AI-generated", 5, 95),
    ("Not started", None, None),
    ("N/A", None, None),
    ("Custom", None, None),
]

PHASES = [
    "Requirements & Scope",
    "Architecture & Design",
    "Implementation",
    "Testing",
    "Documentation",
]

OVERSIGHT = {
    "Directed": "Human specifies tasks explicitly; AI executes with no autonomy.",
    "Collaborative": "Human and AI co-author decisions; human reviews all output.",
    "Supervised": "AI works semi-autonomously; human reviews key checkpoints.",
    "Autonomous": "AI drives end-to-end; human reviews final output only.",
}

PROCESS_DEFAULTS = {
    "Agentic": (
        "AI agent operated autonomously across multi-step tasks. "
        "Human reviewed diffs, resolved conflicts, and approved merges."
    ),
    "Conversational": (
        "Development driven through iterative dialogue with an AI assistant. "
        "Human directed each session and reviewed all generated output."
    ),
    "Inline suggestion": (
        "AI provided inline code completions accepted or rejected by the human developer. "
        "Human wrote the majority of logic and reviewed all suggestions."
    ),
    "Mixed": (
        "Combination of inline suggestions, conversational assistance, and agentic tasks. "
        "Human maintained editorial control throughout."
    ),
}

DEFAULT_ACCOUNTABILITY = (
    "The human author(s) are solely responsible for the content, "
    "accuracy, and fitness-for-purpose of this project."
)

# ---------------------------------------------------------------------------
# CSS for HTML renderer (module-level to avoid f-string brace conflicts)
# ---------------------------------------------------------------------------

_CSS = """
/* ── Flexoki tokens via light-dark() — single definition, no duplication ── */
.aidc {
  color-scheme: light dark;
  --f-bg:         light-dark(#FFFCF0, #1C1B1A);
  --f-bg-alt:     light-dark(#F2F0E5, #282726);
  --f-border:     light-dark(#E6E4D9, #343331);
  --f-head-bg:    light-dark(#282726, #100F0F);
  --f-head-fg:    #FFFCF0;
  --f-head-muted: light-dark(#9F9D96, #6F6E69);
  --f-tx:         light-dark(#100F0F, #FFFCF0);
  --f-tx-2:       light-dark(#6F6E69, #9F9D96);
  --f-tx-3:       light-dark(#9F9D96, #6F6E69);
  --f-bar-empty:  light-dark(#CECDC3, #343331);
  --f-bar-human:  light-dark(#D0A215, #AD8301);
  --f-bar-ai:     light-dark(#8B7EC8, #5E409D);
  --f-tag-bg:     light-dark(#F0EAEC, #261C39);
  --f-tag-fg:     light-dark(#5E409D, #8B7EC8);
  --f-link:       light-dark(#205EA6, #4385BE);
  /* Structure */
  font-family: system-ui, -apple-system, sans-serif;
  max-width: 560px;
  border: 1px solid var(--f-border);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,.08);
  background: var(--f-bg);
  color: var(--f-tx);
  font-size: 14px;
}
.aidc[data-theme="light"] { color-scheme: light; }
.aidc[data-theme="dark"]  { color-scheme: dark; }
/* ── Component styles ──────────────────────────────────────────────────── */
.aidc-head { background: var(--f-head-bg); color: var(--f-head-fg); padding: 12px 16px; display: flex; justify-content: space-between; align-items: baseline; }
.aidc-head-title { font-size: 16px; font-weight: 600; }
.aidc-head-project { font-size: 13px; color: var(--f-head-muted); }
.aidc-section { padding: 12px 16px; border-bottom: 1px solid var(--f-border); background: var(--f-bg); }
.aidc-section:last-of-type { border-bottom: none; }
.aidc-lbl { font-size: 11px; font-weight: 600; letter-spacing: .06em; text-transform: uppercase; color: var(--f-tx-2); margin-bottom: 8px; }
.aidc-tools { list-style: none; margin: 0; padding: 0; }
.aidc-tools li { padding: 2px 0; font-size: 13px; }
.aidc-tag { display: inline-block; background: var(--f-tag-bg); color: var(--f-tag-fg); font-family: ui-monospace, monospace; font-size: 11px; padding: 1px 5px; border-radius: 3px; }
.aidc-legend { display: flex; gap: 12px; font-size: 12px; color: var(--f-tx-2); margin-bottom: 10px; }
.aidc-dot { display: inline-block; width: 8px; height: 8px; border-radius: 2px; margin-right: 3px; vertical-align: middle; }
.aidc-phase { margin-bottom: 10px; }
.aidc-phase:last-child { margin-bottom: 0; }
.aidc-phase-name { font-size: 13px; margin-bottom: 4px; color: var(--f-tx); }
.aidc-bar-row { display: flex; align-items: center; gap: 8px; }
.aidc-bar-track { flex: 1; height: 12px; border-radius: 3px; overflow: hidden; background: var(--f-bar-empty); display: flex; }
.aidc-bar-h { background: var(--f-bar-human); height: 100%; }
.aidc-bar-a { background: var(--f-bar-ai); height: 100%; }
.aidc-bar-pct { font-size: 12px; color: var(--f-tx-2); white-space: nowrap; min-width: 120px; text-align: right; }
.aidc-na { font-size: 12px; color: var(--f-tx-3); font-style: italic; }
.aidc-field-name { font-weight: 600; font-size: 13px; color: var(--f-tx); }
.aidc-field-val { font-size: 13px; color: var(--f-tx-2); margin-top: 2px; }
.aidc-text { font-size: 13px; color: var(--f-tx-2); line-height: 1.5; margin: 0; }
.aidc-intro { font-size: 13px; color: var(--f-tx-2); margin: 0 0 8px; }
.aidc-intro a { color: var(--f-link); }
.aidc-foot { background: var(--f-bg-alt); padding: 8px 16px; font-size: 12px; color: var(--f-tx-3); display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--f-border); }
.aidc-foot a { color: var(--f-tx-3); text-decoration: none; }
.aidc-foot a:hover { text-decoration: underline; }
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

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


def make_bars(human_pct: int, width: int = 10) -> tuple[str, str]:
    human_blocks = round(human_pct / 100 * width)
    ai_blocks = width - human_blocks
    return ("█" * human_blocks), ("░" * ai_blocks)


# ---------------------------------------------------------------------------
# Collection functions
# ---------------------------------------------------------------------------

def collect_project() -> dict:
    section("Project Info")
    name = ask("Project name:", required=True)
    policy_url = ask("AI policy URL (optional, press Enter to skip):", default="")
    today = date.today().isoformat()
    d = ask(f"Date (YYYY-MM-DD):", default=today)
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
    # Map mode to a template key
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
        filename = ask(f"Filename:", default=default_name, required=True)
    return {"format": fmt, "filename": filename, "theme": theme}


# ---------------------------------------------------------------------------
# Renderers
# ---------------------------------------------------------------------------

def render_markdown(
    project: dict,
    tools: list[dict],
    phases: list[dict],
    oversight: dict,
    process: str,
    accountability: str,
) -> str:
    lines: list[str] = []

    lines.append("## 🤖 AI Disclaimer\n")

    if project["policy_url"]:
        lines.append(
            f"This project uses AI-assisted development tools. "
            f"See the [AI usage policy]({project['policy_url']}) for details.\n"
        )
    else:
        lines.append("This project uses AI-assisted development tools.\n")

    lines.append("**Tools**\n")
    for t in tools:
        model_str = f" · `{t['model']}`" if t["model"] else ""
        lines.append(f"- {t['name']}{model_str} · {t['mode']}")
    lines.append("")

    lines.append("### Contribution Profile\n")
    # Column layout (BAR_W=10):
    #   {name:<25} {human:>3}% {h_bar:>10}│{a_bar:<10} {ai:>3}%
    # │ sits at column 41 in both header and data rows.
    BAR_W = 10
    header_human = 3 + 1 + 1 + BAR_W  # "85% " + 10 bar chars = 15
    lines.append("```")
    lines.append(f"{'Phase':<25} {'Human':>{header_human}}│ AI")
    lines.append("─" * 41 + "┼" + "─" * (BAR_W + 1 + 3 + 1))
    for ph in phases:
        if ph["human"] is None:
            lines.append(f"{ph['name']:<25} {ph['preset'].lower()}")
        else:
            h_bar, a_bar = make_bars(ph["human"], BAR_W)
            lines.append(
                f"{ph['name']:<25} {ph['human']:>3}% {h_bar:>{BAR_W}}│{a_bar:<{BAR_W}} {ph['ai']:>3}%"
            )
    lines.append("```\n")

    lines.append(f"**Oversight**: {oversight['label']}\n")
    lines.append(oversight['description'] + "\n")

    lines.append("### Process\n")
    lines.append(process + "\n")

    lines.append("### Accountability\n")
    lines.append(accountability + "\n")

    lines.append(f"---\n*Last updated: {project['date']} · Generated with [ai-disclaimer](https://github.com/j23n/ai-disclaimer)*\n")

    return "\n".join(lines)


def render_html(
    project: dict,
    tools: list[dict],
    phases: list[dict],
    oversight: dict,
    process: str,
    accountability: str,
    theme: str = "auto",
) -> str:
    e = html.escape

    # Tools section
    tool_items = []
    for t in tools:
        model_tag = f' <span class="aidc-tag">{e(t["model"])}</span>' if t["model"] else ""
        tool_items.append(f'<li>{e(t["name"])}{model_tag} &middot; {e(t["mode"])}</li>')
    tools_html = '<ul class="aidc-tools">\n' + "\n".join(tool_items) + "\n</ul>"

    # Intro / policy link
    if project["policy_url"]:
        intro_html = (
            f'<p class="aidc-intro">This project uses AI-assisted development tools. '
            f'See the <a href="{e(project["policy_url"])}">AI usage policy</a> for details.</p>'
        )
    else:
        intro_html = '<p class="aidc-intro">This project uses AI-assisted development tools.</p>'

    # Legend
    legend_html = (
        '<div class="aidc-legend">'
        '<span><span class="aidc-dot" style="background:var(--f-bar-human)"></span>Human</span>'
        '<span><span class="aidc-dot" style="background:var(--f-bar-ai)"></span>AI</span>'
        "</div>"
    )

    # Phase bars
    phase_items = []
    for ph in phases:
        name = e(ph["name"])
        if ph["human"] is None:
            phase_items.append(
                f'<div class="aidc-phase">'
                f'<div class="aidc-phase-name">{name}</div>'
                f'<div class="aidc-na">{e(ph["preset"].lower())}</div>'
                f"</div>"
            )
        else:
            phase_items.append(
                f'<div class="aidc-phase">'
                f'<div class="aidc-phase-name">{name}</div>'
                f'<div class="aidc-bar-row">'
                f'<div class="aidc-bar-track">'
                f'<div class="aidc-bar-h" style="width:{ph["human"]}%"></div>'
                f'<div class="aidc-bar-a" style="width:{ph["ai"]}%"></div>'
                f"</div>"
                f'<span class="aidc-bar-pct">{ph["human"]}% human &middot; {ph["ai"]}% AI</span>'
                f"</div>"
                f"</div>"
            )
    phases_html = "\n".join(phase_items)

    # data-theme attribute for explicit light/dark override
    theme_attr = f' data-theme="{theme}"' if theme in ("light", "dark") else ""

    # Self-contained card — style + card wrapped in a plain div
    card = (
        f"<div>\n"
        f"<style>{_CSS}</style>\n"
        f'<div class="aidc"{theme_attr}>\n'
        f'  <div class="aidc-head">\n'
        f'    <span class="aidc-head-title">&#x1F916; AI Disclaimer</span>\n'
        f'    <span class="aidc-head-project">{e(project["name"])}</span>\n'
        f"  </div>\n"
        f'  <div class="aidc-section">\n'
        f"    {intro_html}\n"
        f"    {tools_html}\n"
        f"  </div>\n"
        f'  <div class="aidc-section">\n'
        f'    <div class="aidc-lbl">Contribution Profile</div>\n'
        f"    {legend_html}\n"
        f"    {phases_html}\n"
        f"  </div>\n"
        f'  <div class="aidc-section">\n'
        f'    <div class="aidc-lbl">Oversight</div>\n'
        f'    <div class="aidc-field-name">{e(oversight["label"])}</div>\n'
        f'    <div class="aidc-field-val">{e(oversight["description"])}</div>\n'
        f"  </div>\n"
        f'  <div class="aidc-section">\n'
        f'    <div class="aidc-lbl">Process</div>\n'
        f'    <p class="aidc-text">{e(process)}</p>\n'
        f"  </div>\n"
        f'  <div class="aidc-section">\n'
        f'    <div class="aidc-lbl">Accountability</div>\n'
        f'    <p class="aidc-text">{e(accountability)}</p>\n'
        f"  </div>\n"
        f'  <div class="aidc-foot">'
        f'<span>Last updated: {e(project["date"])}</span>'
        f'<span>Generated with <a href="https://github.com/j23n/ai-disclaimer">ai-disclaimer</a></span>'
        f'</div>\n'
        f"</div>\n"
        f"</div>"
    )

    return card + "\n"


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

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
