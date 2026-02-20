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

**Tools**

- Claude Code (Anthropic) · `claude-sonnet-4-6` · Agentic

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

**Oversight**: Supervised

AI agents work autonomously per session; human reviews all output before merging.

### Process

AI agents propose changes as PRs, which are reviewed and merged by me. I try to make interactions transparent in the relevant issues or proposed patches. AI-authored commits are tagged with `Co-Authored-By` in the git history.

### Accountability

The human author(s) are solely responsible for the content, accuracy, and fitness-for-purpose of this project.

---
*Last updated: 2026-02-20 · Generated with [ai-disclaimer](https://github.com/j23n/ai-disclaimer)*
