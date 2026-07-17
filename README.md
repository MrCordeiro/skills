# Skills

A collection of reusable AI skills for Copilot, Claude, and other AI agents — built for Product Managers and anyone who wants more structured, intentional interactions with their AI assistant.

## What is a skill?

A skill is a Markdown file with a YAML frontmatter block. The agent reads the `description` field to decide when to activate the skill, then follows the instructions in the file body.

```
skill/
└── socratic-quiz.md   ← name + description (frontmatter) + behaviour (body)
```

Skills live in the `skill/` directory and follow a consistent format so any supporting agent or tool can discover and load them automatically.

## Available skills

| Skill | Trigger phrases | Description |
|-------|----------------|-------------|
| [socratic-quiz](skill/socratic-quiz.md) | "socratic quiz", "let's brainstorm", "quiz me", "help me think this through", "don't just tell me" | Run a problem-solving session as a Socratic dialogue — the agent asks questions instead of handing over answers. |

## How to use

### GitHub Copilot

Point Copilot at this repo (or copy skills into your own repository's `skill/` folder). Copilot reads skill files automatically when they are present in the workspace.

Trigger a skill by using one of its listed phrases in your prompt:

> "Quiz me on why our retention dropped last quarter."

### Claude (via Projects)

Add the skill file contents to your Project instructions, or paste them into the conversation as context.

### Any other agent

Copy the raw Markdown — frontmatter included — into the agent's system prompt or context window.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to author a new skill and submit a pull request.
