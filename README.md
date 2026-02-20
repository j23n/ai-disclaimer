# ai-disclaimer

Interactive CLI that generates an AI usage disclaimer for your project — as a Markdown snippet or a self-contained HTML card.

## Install

```sh
uv tool install .
```

## Usage

```sh
ai-disclaimer
```

Walks you through a short questionnaire (tools used, contribution split by phase, oversight level, process, accountability) and writes the output to stdout or a file.

## Output formats

**Markdown** — a fenced-code bar chart and plain text sections, ready to paste into any README.

**HTML** — a self-contained `<div>` (style included) with visual progress bars, using the [Flexoki](https://github.com/kepano/flexoki) color palette. Supports `light`, `dark`, and `auto` (follows OS preference) themes.

---

## AI Disclaimer

### Markdown

## 🤖 AI Disclaimer

This project uses AI-assisted development tools.

**Tools**: Claude Code (Anthropic) · `claude-sonnet-4-6` · Agentic

### Contribution Profile

```
Phase                               Human│ AI
─────────────────────────────────────────┼───────────────
Requirements & Scope       85%   ████████│░░          15%
Architecture & Design      85%   ████████│░░          15%
Implementation             20%         ██│░░░░░░░░    80%
Testing                   n/a
Documentation              20%         ██│░░░░░░░░    80%
```

**Oversight**: Supervised — AI agents work autonomously per session; human reviews all output before merging.

### Process

AI agents propose changes as PRs, which are reviewed and merged by me. I try to make interactions transparent in the relevant issues or proposed patches. AI-authored commits are tagged with `Co-Authored-By` in the git history.

### Accountability

The human author(s) are solely responsible for the content, accuracy, and fitness-for-purpose of this project.

---
*Last updated: 2026-02-20*

---

### HTML

<div>
<style>
/* ── Flexoki light tokens (default) ─────────────────────────────────── */
.aidc {
  --f-bg:         #FFFCF0;
  --f-bg-alt:     #F2F0E5;
  --f-border:     #E6E4D9;
  --f-head-bg:    #282726;
  --f-head-fg:    #FFFCF0;
  --f-head-muted: #9F9D96;
  --f-tx:         #100F0F;
  --f-tx-2:       #6F6E69;
  --f-tx-3:       #9F9D96;
  --f-bar-empty:  #CECDC3;
  --f-bar-human:  #4385BE;
  --f-bar-ai:     #8B7EC8;
  --f-tag-bg:     #F0EAEC;
  --f-tag-fg:     #5E409D;
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
/* ── Flexoki dark tokens (auto via media query) ──────────────────────── */
@media (prefers-color-scheme: dark) {
  .aidc:not([data-theme="light"]) {
    --f-bg:         #1C1B1A;
    --f-bg-alt:     #282726;
    --f-border:     #343331;
    --f-head-bg:    #100F0F;
    --f-head-fg:    #FFFCF0;
    --f-head-muted: #6F6E69;
    --f-tx:         #FFFCF0;
    --f-tx-2:       #9F9D96;
    --f-tx-3:       #6F6E69;
    --f-bar-empty:  #343331;
    --f-bar-human:  #205EA6;
    --f-bar-ai:     #5E409D;
    --f-tag-bg:     #261C39;
    --f-tag-fg:     #8B7EC8;
  }
}
/* ── Flexoki dark tokens (explicit override) ─────────────────────────── */
.aidc[data-theme="dark"] {
  --f-bg:         #1C1B1A;
  --f-bg-alt:     #282726;
  --f-border:     #343331;
  --f-head-bg:    #100F0F;
  --f-head-fg:    #FFFCF0;
  --f-head-muted: #6F6E69;
  --f-tx:         #FFFCF0;
  --f-tx-2:       #9F9D96;
  --f-tx-3:       #6F6E69;
  --f-bar-empty:  #343331;
  --f-bar-human:  #205EA6;
  --f-bar-ai:     #5E409D;
  --f-tag-bg:     #261C39;
  --f-tag-fg:     #8B7EC8;
}
/* ── Component styles (all colors via tokens) ────────────────────────── */
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
.aidc-intro a { color: var(--f-bar-human); }
.aidc-foot { background: var(--f-bg-alt); padding: 8px 16px; font-size: 12px; color: var(--f-tx-3); text-align: right; border-top: 1px solid var(--f-border); }
</style>
<div class="aidc">
  <div class="aidc-head">
    <span class="aidc-head-title">&#x1F916; AI Disclaimer</span>
    <span class="aidc-head-project">ai-disclaimer</span>
  </div>
  <div class="aidc-section">
    <p class="aidc-intro">This project uses AI-assisted development tools.</p>
    <ul class="aidc-tools">
<li>Claude Code (Anthropic) <span class="aidc-tag">claude-sonnet-4-6</span> &middot; Agentic</li>
</ul>
  </div>
  <div class="aidc-section">
    <div class="aidc-lbl">Contribution Profile</div>
    <div class="aidc-legend"><span><span class="aidc-dot" style="background:#4385BE"></span>Human</span><span><span class="aidc-dot" style="background:#8B7EC8"></span>AI</span></div>
    <div class="aidc-phase"><div class="aidc-phase-name">Requirements &amp; Scope</div><div class="aidc-bar-row"><div class="aidc-bar-track"><div class="aidc-bar-h" style="width:85%"></div><div class="aidc-bar-a" style="width:15%"></div></div><span class="aidc-bar-pct">85% human &middot; 15% AI</span></div></div>
<div class="aidc-phase"><div class="aidc-phase-name">Architecture &amp; Design</div><div class="aidc-bar-row"><div class="aidc-bar-track"><div class="aidc-bar-h" style="width:85%"></div><div class="aidc-bar-a" style="width:15%"></div></div><span class="aidc-bar-pct">85% human &middot; 15% AI</span></div></div>
<div class="aidc-phase"><div class="aidc-phase-name">Implementation</div><div class="aidc-bar-row"><div class="aidc-bar-track"><div class="aidc-bar-h" style="width:20%"></div><div class="aidc-bar-a" style="width:80%"></div></div><span class="aidc-bar-pct">20% human &middot; 80% AI</span></div></div>
<div class="aidc-phase"><div class="aidc-phase-name">Testing</div><div class="aidc-na">n/a</div></div>
<div class="aidc-phase"><div class="aidc-phase-name">Documentation</div><div class="aidc-bar-row"><div class="aidc-bar-track"><div class="aidc-bar-h" style="width:20%"></div><div class="aidc-bar-a" style="width:80%"></div></div><span class="aidc-bar-pct">20% human &middot; 80% AI</span></div></div>
  </div>
  <div class="aidc-section">
    <div class="aidc-lbl">Oversight</div>
    <div class="aidc-field-name">Supervised</div>
    <div class="aidc-field-val">AI agents work autonomously per session; human reviews all output before merging.</div>
  </div>
  <div class="aidc-section">
    <div class="aidc-lbl">Process</div>
    <p class="aidc-text">AI agents propose changes as PRs, which are reviewed and merged by me. I try to make interactions transparent in the relevant issues or proposed patches. AI-authored commits are tagged with <code>Co-Authored-By</code> in the git history.</p>
  </div>
  <div class="aidc-section">
    <div class="aidc-lbl">Accountability</div>
    <p class="aidc-text">The human author(s) are solely responsible for the content, accuracy, and fitness-for-purpose of this project.</p>
  </div>
  <div class="aidc-foot">Last updated: 2026-02-20</div>
</div>
</div>
