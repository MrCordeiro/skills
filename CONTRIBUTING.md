# Contributing

Thanks for wanting to add a skill! Skills are short, focused Markdown files that teach an AI agent a specific behaviour. This guide explains the format and the review process.

## Skill format

Each skill is a single Markdown file in the `skill/` directory. Use `skill/_template.md` as your starting point.

### Frontmatter contract

Every skill file **must** begin with a YAML frontmatter block:

```yaml
---
name: kebab-case-id
description: What the skill does and when to activate it. Include trigger phrases in quotes.
---
```

| Field | Purpose | Rules |
|-------|---------|-------|
| `name` | Machine identifier used to reference the skill | Lowercase, kebab-case, unique across the repo |
| `description` | The agent reads this to decide whether to invoke the skill | Must include the exact trigger phrases the user would say, in quotes |

### Writing good trigger phrases

The `description` field doubles as an activation signal. Include natural phrases a user would actually type:

✅ `"quiz me"`, `"help me think this through"`, `"let's brainstorm"`  
❌ Vague descriptions without example phrases

Aim for 3–6 distinct phrases covering different ways to express the same intent.

### Content conventions

- **One instruction per bullet.** Don't combine multiple rules into one point.
- **Imperative mood.** Write "Ask one question" not "The agent should ask one question."
- **Include an example turn.** Show what a good first exchange looks like — what the agent says, and a note on what it must *not* do.
- **Name your stop conditions.** Every skill should have a "When to stop" section so the agent knows how to close gracefully.
- **Keep it concise.** A skill is not a spec document. If a section isn't shaping behaviour, cut it.

## Adding a skill

1. Copy `skill/_template.md` to `skill/<your-skill-name>.md`.
2. Fill in the frontmatter (`name`, `description`).
3. Write the body following the conventions above.
4. Add a row for your skill to the table in `README.md`.
5. Test it with at least one AI agent — paste the file contents as a system prompt or skill context and verify it behaves as described.
6. Open a pull request using the PR template.

## Pull request checklist

See `.github/pull_request_template.md` — it will appear automatically when you open a PR.
