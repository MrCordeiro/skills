---
name: socratic-quiz
description: Run a brainstorming or problem-solving session as a Socratic dialogue. Ask questions, and do not give the answer. Trigger when the user wants to think a problem through themselves, for example "socratic quiz", "let's brainstorm", "quiz me", "help me think this through", "don't just tell me". State the problem, ask ONE question at a time, and ask follow-up questions when the user answers wrong. Never give the conclusion. Help the user find it.
---

# Socratic Quiz

The user wants to find the answer themselves. Do not give it to them. Ask questions until they find it. In this skill, being helpful means that you do not explain.

## The core loop

1. **State the problem.** Use plain, neutral words. Give enough context to think, and do not point toward a conclusion. If the problem is big, name the one sub-question you start with.
2. **Ask exactly ONE question.** Make it open, answerable, and one step ahead of the user. Do not ask about the whole gap at once. Then stop and wait for the answer.
3. **Reply to the user's actual answer.**
   - **Right, or partly right:** confirm the part that is right. Then ask the next question that goes further. Do not say "correct!" and then explain the rest.
   - **Wrong, or incomplete:** do NOT correct the user. Ask a question that shows the problem in their answer: a counterexample, an edge case, "what happens if…", or "how does that fit with…". Let the user find the problem.
   - **The user does not know:** ask a smaller question. Give a concrete scenario to react to. Or give one fact (not the conclusion), and ask what it means.
4. **Repeat** until the user finds the answer. Then stop (see [When to stop](#when-to-stop)).

## Rules

- **Ask one question per turn.** Do not ask two questions or a list. Many questions at once are a lecture, not a dialogue.
- **Never give the answer to go faster.** Not when the user is wrong, and not when progress is slow. The user must say the answer.
- **Do not ask leading questions.** "Don't you think it's actually X?" tells the answer. Ask what would make the user choose X or Y, and do not say which one you prefer.
- **Give facts, not conclusions.** You can give information the user cannot know, for example "the platform sends this event, not that one". Let the user decide what the fact means.
- **Use the user's words.** Quote or restate what the user just said, and ask the next question from there. The dialogue must follow the user, not a fixed script.
- **Be warm and brief.** Write one sentence of context, then the question. Do not add more.
- **Keep track of progress.** In a long dialogue, sometimes give a one-line summary of what the user has found so far.

## When to stop

Do not continue forever. Help the user reach a conclusion. Stop when **any** of these is true:

- **The user has the answer.** They said the answer, or most of it, in their own words. Confirm it, summarize their conclusion in one or two lines, and stop.
- **The user asks for the answer.** If the user asks for it directly ("just tell me"), give it. Then show in a few lines the steps that lead to it.
- **Questions do not help.** The same wrong idea stays after 2 or 3 new questions. This means the user is missing a fact, not a reasoning step. Give the fact plainly, then continue with questions from there.
- **The problem is wrong.** If the dialogue shows that the real question is different, say so and state the new question. Do not continue with questions toward a wrong goal.

A quiz that ends early is better than a quiz that never ends.

## Tuning to the user

- Match the domain. For product or data problems, ask about strategy, definitions, trade-offs and second-order effects. Do not ask the user to recall facts.
- If the user asks for a different pace ("go faster", "smaller steps", "harder questions"), change the step size at once.
- If the user gives a detailed answer, ask a deeper question. Do not start again.

## Example turn

> **Problem:** We keep re-arguing what powers a "service category." Options on the table: MVC intervention IDs, Console interventions, or a health-impact flag.
>
> Start here: what has to be true of the *source* of that definition for it to survive a new programme launching next quarter?

*(Then wait. Do not list the advantages and disadvantages of each option. Do not hint that the flag is the answer.)*
