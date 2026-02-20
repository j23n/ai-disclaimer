"""Static data: tool list, phase presets, oversight levels, and defaults."""
from __future__ import annotations

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
