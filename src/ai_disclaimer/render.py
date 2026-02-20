"""Markdown and HTML renderers."""
from __future__ import annotations

import html

# CSS kept at module level to avoid f-string brace conflicts.
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


def make_bars(human_pct: int, width: int = 10) -> tuple[str, str]:
    human_blocks = round(human_pct / 100 * width)
    ai_blocks = width - human_blocks
    return ("█" * human_blocks), ("░" * ai_blocks)


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
    BAR_W = 10
    header_human = 3 + 1 + 1 + BAR_W
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
    lines.append(oversight["description"] + "\n")

    lines.append("### Process\n")
    lines.append(process + "\n")

    lines.append("### Accountability\n")
    lines.append(accountability + "\n")

    lines.append(
        f"---\n*Last updated: {project['date']} · "
        f"Generated with [ai-disclaimer](https://github.com/j23n/ai-disclaimer)*\n"
    )

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

    tool_items = []
    for t in tools:
        model_tag = f' <span class="aidc-tag">{e(t["model"])}</span>' if t["model"] else ""
        tool_items.append(f'<li>{e(t["name"])}{model_tag} &middot; {e(t["mode"])}</li>')
    tools_html = '<ul class="aidc-tools">\n' + "\n".join(tool_items) + "\n</ul>"

    if project["policy_url"]:
        intro_html = (
            f'<p class="aidc-intro">This project uses AI-assisted development tools. '
            f'See the <a href="{e(project["policy_url"])}">AI usage policy</a> for details.</p>'
        )
    else:
        intro_html = '<p class="aidc-intro">This project uses AI-assisted development tools.</p>'

    legend_html = (
        '<div class="aidc-legend">'
        '<span><span class="aidc-dot" style="background:var(--f-bar-human)"></span>Human</span>'
        '<span><span class="aidc-dot" style="background:var(--f-bar-ai)"></span>AI</span>'
        "</div>"
    )

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

    theme_attr = f' data-theme="{theme}"' if theme in ("light", "dark") else ""

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
