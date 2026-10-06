# Skills

Reusable skills for Product Managers. A skill gives an AI agent (Claude, Copilot or another agent) clear instructions for one type of task.

## What is a skill?

A skill is a Markdown file that starts with a frontmatter block. The frontmatter is metadata written in YAML (a simple text format for settings). The agent reads the `description` field to decide when to use the skill. Then it follows the instructions in the file body.

```
skill/
├── socratic-quiz.md   ← single-file skill: frontmatter + body
└── draw/              ← folder skill: SKILL.md + supporting files
    ├── SKILL.md
    ├── references/
    └── lib/
```

Skills are in the `skill/` directory. They all use the same format, so any agent or tool that supports skills can find and load them.

## Available skills

| Skill | Trigger phrases | Description |
|-------|----------------|-------------|
| [socratic-quiz](skill/socratic-quiz.md) | "socratic quiz", "let's brainstorm", "quiz me", "help me think this through", "don't just tell me" | Run a problem-solving session as a Socratic dialogue. The agent asks questions and does not give the answer. |
| [draw](skill/draw/SKILL.md) | "draw", "diagram", "flowchart", "user flow", "heat map", "status board", "file tree" | Make a diagram as a PNG (tables, heat maps, pipelines, file trees) or an editable Excalidraw file (flows, system maps). |
| [plain-language](skill/plain-language/SKILL.md) | "plain language", "simplify this", "make this readable", "check my writing", "de-slop" | Edit text so busy readers read it: finding first, no filler, Simplified Technical English. Includes a checker script. |

## How to use

### GitHub Copilot

Open this repository in your workspace, or copy skills into the `skill/` folder of your own repository. Copilot reads skill files that are in the workspace.

To use a skill, include one of its trigger phrases in your prompt:

> "Quiz me on why our retention dropped last quarter."

### Claude (via Projects)

Add the contents of the skill file to your Project instructions, or paste them into the conversation.

### Any other agent

Copy the full Markdown file, including the frontmatter, into the agent's system prompt or context.

## Contributing

[CONTRIBUTING.md](CONTRIBUTING.md) explains how to write a new skill and open a pull request.
