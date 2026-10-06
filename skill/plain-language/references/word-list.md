# Word List

`lib/check_text.py` reads the tables in this file. To change what the checker reports, edit this file. Do not edit the script.

Table format:

- **Never:** the words to find. Separate different phrases with a comma. Separate spelling variants with ` / `. The checker also finds the usual verb forms of the first word (for example, `lands on` also finds `land on`, `landed on` and `landing on`). Add irregular forms yourself (for example, `led with`).
- **Use instead:** the suggestion that the checker shows.
- A phrase with a note in brackets, such as `surfaces (verb)`, is reported as a **warning**, because the same word can be correct in another meaning. All other phrases are reported as **errors**.

## Metaphors and vague verbs

Use the plainest verb that has the meaning. Do not use a spatial or physical metaphor in place of a plain verb.

| Never | Use instead |
|---|---|
| sits with / sits in (of data, code or tasks) | is, uses |
| lands on, landed in | is recorded in, is added to |
| carries (verb) | contains, has, includes |
| rides on | uses, is sent on |
| keys off | is based on |
| surfaces (verb) | shows, displays |
| leads with, led with | starts with |
| lives in (of data, code or tasks) | is in |
| baked into, baked in | included in, written into |
| load-bearing | critical, required |
| sticky, sticks (verb), stuck (of a setting) | permanent, is not reversed |
| under the hood | internally |
| spin up, spun up | start, create |
| wire up, wired up | connect |
| reach for, reached for | use |
| flavour of / flavor of | type of |
| points at (verb) | is, refers to |
| propagates | spreads, is copied to |
| holds (of a rule) | is true |
| kept as trace | kept for reference |
| superseded by | replaced by |
| carve-out / carve out | exception |
| asymmetry | the two do not match |
| is noise | is unreliable, cannot be trusted |
| moves the needle / move the needle | changes the result, increases the metric |
| low-hanging fruit | easy task, quick win |
| circle back | discuss again, reply later |
| double-click on, double click on | look at in detail |
| deep dive, dive into, delve into | detailed review, study, look at |
| boil the ocean | do too much at once |
| at the end of the day | finally, in the end |
| on the same page | agree |
| touch base | talk, meet |
| bandwidth (of people) | time, capacity |
| north star (as a metaphor) | main goal (keep "north star metric" when the team uses that term) |

## AI filler and inflated words

These words make text longer or vaguer. Readers see them as signs of text that nobody edited.

| Never | Use instead |
|---|---|
| leverage / leverages / leveraging | use |
| utilize / utilise | use |
| facilitate | help, make possible |
| robust | strong, reliable (or say what it resists) |
| seamless / seamlessly | (say what the user does not have to do) |
| game-changer / game changer | (say what changes, with a number) |
| unlock, unlocks, unlocked | make possible, allow |
| empower | let, allow |
| streamline | simplify, make faster |
| elevate | improve |
| foster | build, support |
| harness | use |
| holistic | complete, full |
| synergy / synergies | (say what each part gives the other) |
| cutting-edge / state-of-the-art | new, current |
| best-in-class / world-class | (give the comparison) |
| paramount | most important |
| crucial (of a choice) | important, required |
| landscape (of a market) | market, options, competitors |
| journey (of a user) | steps, process (keep "user journey" when the team uses that term) |
| navigate (of a problem) | handle, deal with |
| tapestry, realm | (delete) |
| it is worth noting / it's worth noting | (delete; state the fact) |
| it is important to note / it's important to note | (delete; state the fact) |
| in today's fast-paced | (delete) |
| needless to say | (delete) |
| in conclusion / to summarize / in summary | (delete the summary, or keep only new facts) |
| I hope this helps | (delete) |
| great question | (delete) |
| let's dive in / let us dive in | (delete) |
| basically / essentially | (delete) |
| a wide range of / a variety of | many, several (or give the number) |
| in order to | to |
| due to the fact that | because |
| at this point in time | now |
| with regard to / with respect to | about |

## Known abbreviations

The checker does not ask you to spell out these abbreviations. Add your team's common abbreviations to this line, separated by commas.

Known: AI, API, CSS, CSV, HTML, ID, JSON, OK, PDF, PNG, SMS, SQL, UI, URL, USSD, UX, PM, PR, Q1, Q2, Q3, Q4
