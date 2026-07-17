# Copilot instructions for this repository

This repository is a collection of AI skills — reusable Markdown files that teach an AI agent a specific behaviour. Each skill lives in `skill/` and follows a consistent format.

## When helping contributors

- **Creating a new skill:** follow the pattern in `skill/_template.md`. Copy it to `skill/<name>.md`, fill in the YAML frontmatter (`name` in kebab-case, `description` with trigger phrases), then write the body. Also add a row for the new skill to the skills table in `README.md`.
- **Improving an existing skill:** edit only the relevant sections; preserve the frontmatter and section structure.
- **Answering questions about the format:** refer to `CONTRIBUTING.md` for the authoritative authoring guide.

## Style rules for skill files

- Use imperative mood in instructions ("Ask one question", not "The agent should ask one question").
- One rule or instruction per bullet — do not combine.
- Every skill must have a "When to stop" section.
- Every skill must include an example turn showing what a good first exchange looks like.

## What NOT to do

- Do not add explanations or rationale inside skill files unless they are in a clearly labelled reference section.
- Do not invent frontmatter fields beyond `name` and `description`.
- Do not modify the `_template.md` file when creating a new skill — copy it instead.
