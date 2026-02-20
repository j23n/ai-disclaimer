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

## Examples

You can see the markdown output in the section below and the corresponding HTML:

> ![](examples/ai_disclaimer.png)

Source code: [here](examples/ai_disclaimer.html)


> ## 🤖 AI Disclaimer
> 
> This project uses AI-assisted development tools. See the [AI usage policy](https://j23n.com/public/posts/2026/my-ai-policy) for details.
> 
> **Tools**
> 
> - Claude Code (Anthropic) · `claude-sonnet-4-6` · Agentic
>
> ### Contribution Profile
> 
> ```
> Phase                               Human│ AI
> ─────────────────────────────────────────┼───────────────
> Requirements & Scope       85%   ████████│░░          15%
> Architecture & Design      85%   ████████│░░          15%
> Implementation              5%           │░░░░░░░░░░  95%
> Testing                   not started
> Documentation              20%         ██│░░░░░░░░    80%
> ```
>
> **Oversight**: Collaborative
>
> Human and AI co-author decisions; human reviews all output.
>
> ### Process
>
> AI agent operated autonomously across multi-step tasks. Human reviewed diffs, resolved conflicts, and approved merges.
>
> ### Accountability
>
> The human author(s) are solely responsible for the content, accuracy, and fitness-for-purpose of this project.
> 
> ---
> *Last updated: 2026-02-20 · Generated with [ai-disclaimer](https://github.com/j23n/ai-disclaimer)*
