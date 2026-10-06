---
name: plain-language
description: Edit or check text so that busy people read it and act on it. Put the finding first, cut what the reader does not need, and rewrite in Simplified Technical English (plain verbs, active voice, short sentences, no metaphors, no em dashes, no AI filler). Includes a checker script. Trigger on "plain language", "simplify this", "make this readable", "edit this", "check my writing", "too long", "de-slop", "STE", "simplified technical english". Also use as the last step before you give any document, update, spec or message to other people.
---

# Plain Language

Make the text short and plain. The reader must read all of it, understand it on the first read, and know what to do next.

## Terms

- **Reader:** the person who will read the text. If the text has more than one reader, use the most senior reader who is not an expert in the topic.
- **Bottom line:** the one fact, decision or request that the reader must take away.
- `<skill-dir>` is the absolute path of the folder that contains this file.
- `python3` is the Python 3 command. On Windows, use `python` or `py` instead.

## Core behaviour

1. **Find the reader and the bottom line.** Use the conversation and the text. Do not ask the user unless the text has no clear purpose. Write both down in one line each before you edit.
2. **Do the structure pass.** Apply [Structure rules](#structure-rules). This pass usually removes the most words. Do it before you change any sentence.
3. **Do the sentence pass.** Apply [Sentence rules](#sentence-rules).
4. **Run the checker.** Save the text to `<temp-dir>/draft.md` and run:

   ```bash
   python3 <skill-dir>/lib/check_text.py <temp-dir>/draft.md
   ```

5. **Fix the problems.** Fix every **error**. For each **warning**, fix it, or keep the text and know the reason (for example, a passive verb where the actor is unknown). Run the checker again until it reports 0 errors.
6. **Give the result.** See [Output](#output).

## Structure rules

- Put the bottom line in the first sentence. Do not start with background, history or the question.
- State the finding. Do not say that someone answered a question. Write "Six-month services get a 14-day grace period." Do not write "Grace period discrepancy resolved:".
- If the reader must do something, say what, who and by when, in the first paragraph.
- Delete each sentence the reader would not miss. Test each paragraph: "If I delete this, does the reader lose a fact, a decision or an action?" If the answer is no, delete it.
- Delete a closing summary that repeats the body.
- Delete preamble ("This document describes..."), throat-clearing ("As discussed..."), and offers ("Let me know if you have questions").
- Use a list for 3 or more parallel items. Use a table to compare items across the same attributes. Use at most one level of nested bullets.
- Use headings only when the text is longer than about 300 words.
- Put a source or a date in a note at the end of the sentence: "(2026-08-10, product team.)"

## Sentence rules

1. Use the plainest verb that has the meaning. Do not use a spatial or physical metaphor in place of a plain verb. `references/word-list.md` lists the words to replace.
2. Use active voice. Name who does the action. Use passive voice only when the actor is unknown or not important.
3. Write one idea per sentence. Keep each sentence under 25 words.
4. Use the same word for the same thing every time. Do not change words for variety.
5. Do not use idioms, metaphors or em dashes.
6. Spell out each abbreviation the first time you use it in a document: "Data Engineering (DE)".
7. Give numbers, not adjectives. Write "3 of 12 clinics", not "several clinics".
8. Keep domain terms exactly as the team uses them (for example grace period, dose interval, refill, pipeline, epic). A term of art is not a metaphor.

## Rules

- Do not change facts, numbers, names, dates or decisions.
- Do not add content that is not in the original text.
- Do not edit quoted words. The checker skips block quotes (lines that start with `>`), but it checks quotes inside a sentence. Ignore problems inside those quotes.
- Keep the Markdown formatting of the original (headings, links, tables, code).
- Keep the meaning when you shorten. If a sentence is unclear, ask the user what it means. Do not guess.
- To change which words the checker reports, edit `references/word-list.md`. Do not edit the script.

## Exception: engineering documents

Some documents belong to engineers, for example a technical design marked as an engineering document. In these documents, keep technical terms and code names as they are. Fix only the structure rules and the errors that the checker reports. Tell the user that you applied the exception.

## Output

- **If the user asked for an edit:** give the rewritten text first. Then give at most 5 bullets that say what you changed. For example: "Moved the decision to the first sentence" or "Cut 2 paragraphs of background (40% shorter)". Then list any warnings you kept, with the reason.
- **If the user asked for a review only:** list the problems in order of importance, with the line number and a suggested fix. Start with structure problems, then checker errors, then warnings. Do not rewrite the text.
- **If you used this skill as the last step of another task:** give only the edited text. Do not report the changes.

## When to stop

Stop when **any** of these is true:

- **The text is done.** The checker reports 0 errors, you checked every warning, and the bottom line is in the first sentence.
- **The meaning is unclear.** A sentence can mean two things, and only the author knows which. Ask the user, and stop until they answer.
- **The user stops you.** The user says the text is good enough.

## Tuning to the user

- If the user says "shorter", cut by at least a third. Remove whole paragraphs before you shorten sentences.
- If the user gives a word limit, meet it. Say how many words the result has.
- If the reader is outside the company (a partner, a funder or a customer), remove all internal names, code names and team abbreviations.
- If the user adds a word to avoid, add it to `references/word-list.md` so the checker finds it next time.

## Example turn

> **User:** Make this readable: "Following up on our discussion last week, it's worth noting that after a deep dive into the data, the team has leveraged the new dashboard to surface some key insights: notably, the refill reminder flow is underperforming and we should probably circle back on it in Q4."
>
> **Agent:** Refill reminders do not work as well as planned. We will review the reminder flow in Q4.
>
> - Moved the finding to the first sentence.
> - Cut the background about last week's meeting and the dashboard.
> - Replaced "deep dive", "leveraged", "surface" and "circle back" with plain words.
> - Removed the em dash and split the text into 2 sentences.
>
> One question: the original says "underperforming". Against which target? If you give me the number, I will add it.

*(Do not invent the missing number, and do not keep "underperforming" without asking. "Underperforming" needs a target to have a meaning.)*
