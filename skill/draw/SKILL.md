---
name: draw
description: Make a diagram as an image or an editable file. Choose one of three engines. HTML render makes a PNG for tables, heat maps, status boards and left-to-right pipelines. Excalidraw makes an editable box-and-arrow file for flows, system maps and decision trees. Tree makes a PNG of a folder or file hierarchy. Trigger when the user asks for a visual, not a text answer: "draw", "diagram", "make a diagram of", "visualize this", "flowchart", "user flow", "heat map", "status board", "excalidraw", "file tree".
---

# Draw

Turn content that the user gives you into one clear diagram, made with the engine that fits the content.

## Terms

- `<skill-dir>` is the absolute path of the folder that contains this file. Always use the absolute path in code. Python does not expand `~`.
- `<temp-dir>` is your scratchpad or temp directory. Write all generated files there, unless the user names a different folder.
- **Engine** is one of the three ways to make a diagram: HTML render, Excalidraw or Tree.
- `python3` is the Python 3 command. On Windows, use `python` or `py` instead.
- The skill works on macOS, Windows and Linux. Do not write operating-system paths (such as `C:\...` or `/Users/...`) into scripts. Build paths from `<skill-dir>` and `<temp-dir>`.

## Core behaviour

1. **Get the content.** Make a list of every item (box, row, cell or file) and every link between items. Take them from the conversation, the files, or the data the user gave you. If you cannot make the list, ask the user for the missing items. Do not invent items.
2. **Choose the engine.** Go through [Choose the engine](#choose-the-engine) from the top. Use the first row that matches.
3. **Read the engine guide.** Read the reference file for that engine in full before you write any code.
4. **Make the diagram.** Follow the process in the engine guide.
5. **Check the result.** Do every check in the engine guide. Fix each problem and make the diagram again until all checks pass.
6. **Give the result to the user.** Give the full path of the output file. Add one sentence that says what the diagram shows. For Excalidraw, add the instructions to open the file.

## Choose the engine

Go through the rows in order. Use the first row that matches.

| # | If this is true | Use | Read | Output |
|---|---|---|---|---|
| 1 | The user names an engine ("excalidraw", "HTML", "tree") | That engine | Its guide | See below |
| 2 | The content is a folder, file or package hierarchy | Tree | [Tree engine](#tree-engine) in this file | PNG |
| 3 | The content is a table, a matrix, a heat map, a status list or a card grid | HTML render | `references/html-render.md` | PNG |
| 4 | The content is a flow in stages, every arrow goes in the same direction, and no arrow skips a stage | HTML render | `references/html-render.md` | PNG |
| 5 | The content has arrows that branch, loop back, cross or skip stages | Excalidraw | `references/excalidraw.md` and `references/color-palette.md` | `.excalidraw` file |
| 6 | The user wants to move or edit the boxes after you finish | Excalidraw | `references/excalidraw.md` and `references/color-palette.md` | `.excalidraw` file |
| 7 | None of the rows above match | HTML render | `references/html-render.md` | PNG |

This skill does not make charts with axes (bar, line, scatter, pie). If the user asks for one of these, say that this skill does not make charts, and make the chart with a charting library instead.

## Tree engine

1. Write the hierarchy as text with the characters `│ ├ └ ─`. Use the output of the `tree` command, or write it by hand.
2. To add a description to a line, add spaces, then `— ` (an em dash and a space), then the description. Align all the em dashes in one column.
3. End every folder name with `/`.
4. Render it:

   ```python
   import sys
   sys.path.insert(0, "<skill-dir>/lib")
   from tree_png import render_tree_png

   render_tree_png(tree_text, "<temp-dir>/tree.png")                 # white page, for documents
   render_tree_png(tree_text, "<temp-dir>/tree.png", theme="dark")   # dark page, for Slack or dark mode
   ```

5. Open the PNG. Check that the tree lines show as lines, not as empty boxes. If they show as boxes, the helper found no monospace font. Set the environment variable `DRAW_MONO_FONT` to the file name or full path of a monospace `.ttf` font, and render again.

From a shell, run `python3 <skill-dir>/lib/tree_png.py <input.txt> <output.png>`. The tree engine needs `Pillow` (`python3 -m pip install Pillow`).

## Rules

- Make one diagram for each request. If the content needs more than one diagram, make the first one and ask before you make more.
- Use the words the user uses for items. Do not rename them.
- Keep labels short: at most 6 words, or one code identifier.
- Give every diagram a title that says what it shows.
- Use color only to show meaning. Use only the tiko.org brand colors and the functional colors in `references/color-palette.md`. Do not add other colors.
- Add a legend when the diagram uses more than 2 colors or statuses.
- Do not edit files in `<skill-dir>`. Copy an example to `<temp-dir>` and edit the copy.
- If a render command fails, show the user the error and the fix you will try. Do not switch engines without telling the user.

## When to stop

Stop when **any** of these is true:

- **The diagram is done.** All checks in the engine guide pass, and you gave the user the file path.
- **The content is missing.** You asked the user for the missing items and they have not answered.
- **The engine cannot run.** A required tool (Python 3, Pillow, or a Chrome, Chromium, Edge or Brave browser) is missing and cannot be installed. Tell the user what is missing and the command to install it.

## Tuning to the user

- If the user says "simpler" or "too busy", remove items before you remove labels. Show at most 10 items.
- If the user says the diagram is for a slide, use a viewport width of 1280 and at most 3 colors.
- If the user says the diagram is for print, use the default white themes. Do not use `theme="dark"`.

## Example turn

> **User:** Draw our onboarding funnel: sign-up, verify email, complete profile, first project. Mark "verify email" as at risk.
>
> **Agent:** *(Goes through the table. Row 4 matches: a flow in stages with every arrow in one direction. Reads `references/html-render.md`, copies `examples/conditions_flow.html`, makes a 4-stage pipeline with the "verify email" card as `.box.raw`, renders and checks the PNG.)*
>
> Here is the funnel: `<temp-dir>/onboarding_funnel.png`. It shows the four stages from left to right, and "Verify email" is yellow to mark it as at risk.

*(Do not use Excalidraw for this request. The flow has no branches, and the user did not ask to edit it.)*
