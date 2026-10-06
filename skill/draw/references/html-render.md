# HTML Render Engine

This engine makes dense, data-driven visuals: heat maps, status boards, pipeline diagrams, card grids and comparison matrices. You write one HTML file with inline CSS. A headless browser takes a screenshot of it at 2x scale. The result is a PNG that the user can paste into a document, a slide or a ticket.

## Contents

- [Process](#process)
- [Setup](#setup)
- [Render](#render)
- [House style](#house-style)
- [Layouts](#layouts)
- [Check the PNG](#check-the-png)
- [Limits](#limits)
- [Examples](#examples)

## Process

1. Copy the example that matches your layout from `examples/` to `<temp-dir>/<name>.html`. If no example matches, start from an empty HTML file and paste all of `assets/base.css` into its `<style>` block.
2. Change the content. Do not edit the base CSS part. Put diagram-specific CSS below the `/* === diagram-specific === */` comment.
3. Render the HTML file to `<temp-dir>/<name>.png`.
4. Check the PNG. Fix and render again until every check passes.

## Setup

You need three things. Each works on macOS, Windows and Linux.

1. **Python 3.** The command is `python3` on macOS and Linux. On Windows it is `python` or `py`. In this guide, `python3` means the command for your system.
2. **Pillow.** Run `python3 -m pip install Pillow` once per machine.
3. **A Chromium-based browser:** Google Chrome, Chromium, Microsoft Edge or Brave. The helper finds the browser in the standard install folders and on the `PATH`. If it cannot find one, set the environment variable `DRAW_BROWSER` to the full path of the browser executable.

## Render

From a shell:

```bash
python3 <skill-dir>/lib/html_render.py <temp-dir>/my_diagram.html <temp-dir>/my_diagram.png 1280 900
```

Or from Python:

```python
import sys
sys.path.insert(0, "<skill-dir>/lib")
from html_render import render_html_to_png

render_html_to_png(
    "<temp-dir>/my_diagram.html",
    "<temp-dir>/my_diagram.png",
    viewport=(1280, 900),
)
```

- Use absolute paths. Python does not expand `~` in `sys.path`.
- The last two shell arguments are the viewport width and height. If you leave them out, the helper uses 1280 and 900.
- **Width:** set it to the width of the widest row of content. The helper does not remove extra space on the right.
- **Height:** set it larger than the content. The helper removes empty rows at the bottom.
- The PNG size is `viewport × 2`. For example, `(1280, 900)` gives a PNG 2560 pixels wide.
- If the render fails, the error message shows the browser command and its output. Show the message to the user.

## House style

`assets/base.css` is the only source of the house style. It uses the tiko.org brand (see `references/color-palette.md`). Every diagram contains a full copy of it at the top of its `<style>` block. This makes each HTML file complete on its own.

Main tokens:

- **Fonts:** Stabil Grotesk for text, with system sans-serif fonts as fallbacks. Noto Serif for the `h1` title, with Georgia as a fallback. A monospace font for code and identifiers.
- **Page:** white `#ffffff`, borders lilac grey `#e5e3e8`, text ink `#25222a`, muted text grey-purple `#6f677e`.
- **Brand variables:** `--tiko-plum`, `--tiko-plum-dark`, `--tiko-magenta`, `--tiko-teal`, `--tiko-teal-dark`, `--tiko-grey-purple`, `--tiko-lilac-grey`, `--tiko-ink`. Use these variables in diagram-specific CSS. Do not type hex values.
- **Status colors.** Each status has a colored left border and a light background.

| Class | Border | Background | Meaning |
|---|---|---|---|
| `.box.wired` | dark teal `#1996a2` | `#e6f7f9` | Done, shipped, working |
| `.box.raw` | amber `#e0a100` (functional) | `#fff8e1` | Partial, at risk, has a warning |
| `.box.off` | light grey-purple `#b5afbd` | `#f6f5f8` | Not started, not used, out of scope |
| `.box.accent` | plum `#812578` | `#f6edf5` | A system step or stage, with no status |

Other classes in `base.css`: `.box`, `.stack`, `.col-head`, `.arrow`, `.legend`, `.legend .chip`, `.legend .dot`, `table.heatmap`, `.ramp`, `.subtitle`, `.footnote`.

To change a color or size, change the CSS variable in the diagram-specific part (for example `:root { --radius: 4px; }`). Do not write new rules that conflict with `base.css`.

## Layouts

### Pipeline (staged flow)

Use when items move from a source, through a process, to a consumer, and each stage is a list of items.

- Use a CSS grid with one column for each stage and one narrow arrow column (60px) between each pair of stages. For n stages, the grid has 2n − 1 columns. For example, 3 stages give `stack | arrow | stack | arrow | stack`.
- Put each stage in a `.stack`. A stage can contain one card or many cards.
- Use at most 5 stages. If the flow has more, put it in two rows, or use the Excalidraw engine.
- Put a `→` character in each arrow column, inside `<div class="arrow">`.
- To show steps inside one column, put `↓` characters between the cards.
- Start from `examples/conditions_flow.html`.

```css
.grid { display: grid; grid-template-columns: 320px 60px 280px 60px 380px; }
```

### Heat map

Use when rows × columns contain numbers (counts, scores, percentages) and the reader must compare them by color.

- Use `<table class="heatmap">`.
- Calculate each cell color in Python, then write it as an inline `style`.
- Start from `examples/conditions_heatmap.html`.

Use this color formula. It goes from white (low) to tiko plum `#812578` (high) on a log scale:

```python
import math
log_max = math.log10(max_count)

def colour_for(count: int) -> tuple[str, str]:
    """Return (background, text colour) for a heat-map cell."""
    if count == 0:
        return ("#fafafa", "#d1d5db")
    t = math.log10(count) / log_max  # 0..1
    r = int(255 - (255 - 129) * t)
    g = int(255 - (255 -  37) * t)
    b = int(255 - (255 - 120) * t)
    fg = "#25222a" if t < 0.75 else "#ffffff"  # 0.75 keeps both text colours above 4.5:1 contrast
    return (f"rgb({r},{g},{b})", fg)
```

- Write a cell with a value as `<td class="cell" style="background:{bg};color:{fg}">{count:,}</td>`.
- Write an empty cell as `<td class="cell empty">·</td>`.
- Use the log scale when the largest value is more than 20 times the smallest non-zero value. Otherwise use a linear scale: replace `math.log10(count) / log_max` with `count / max_count`.
- If `max_count` is 1, use the linear scale. The log formula divides by zero.

### Status board (card grid)

Use for a flat list of items where each item has one status.

```html
<div class="stack">
  <div class="box wired"><span class="marker">✅</span>item 1</div>
  <div class="box raw"><span class="marker">⚠️</span>item 2</div>
  <div class="box off"><span class="marker">❌</span>item 3</div>
</div>
```

For more than one column, put the cards in `<div style="display:grid; grid-template-columns: repeat(4, 1fr); gap: 6px;">`.

### Comparison matrix

Use to compare options (columns) across attributes (rows).

- Use `<table class="heatmap">`, but put text in the cells, not numbers.
- Color each cell by meaning: `--status-wired-bg` for "supports", `--status-raw-bg` for "supports with limits", `--status-off-bg` for "does not support".

## Check the PNG

Open the PNG with your file-reading or image-viewing tool. Check each item:

1. No text is cut off on the right. If it is, make the viewport wider and render again.
2. No element overlaps another element.
3. No large empty area is on the right. If there is, make the viewport narrower and render again.
4. All text is readable on its background. In a heat map, the `0.75` value in `colour_for` gives readable text with the plum scale. If you change the end color of the scale, check the contrast again and change this value.
5. Nothing at the bottom was removed. See the trim limit below.

## Limits

- **Straight arrows only.** This engine shows arrows as `→` and `↓` characters between columns. For curved, diagonal or crossing arrows, use the Excalidraw engine.
- **No chart libraries.** The page is a static HTML screenshot. Do not use JavaScript, Mermaid, D3 or Graphviz.
- **The bottom trim samples pixels.** The helper removes bottom rows that have the same color as the bottom-middle pixel. If the last element on the page has the page background color, the helper can remove it. Keep `body` padding at 28px or more, and put footnotes in `.footnote`.
- **Scale 2 is required.** Without `--force-device-scale-factor=2`, the PNG is blurry when the user zooms in.

## Examples

| File | Layout | Content |
|---|---|---|
| `examples/conditions_flow.html` | 3-stage pipeline (5 grid columns) | Source containers → compiler steps → engine handlers, with a status on each handler |
| `examples/conditions_heatmap.html` | Heat map | Occurrence counts per category and container, on a log scale, with one shipped cell marked |

Copy an example and change the content. Do not write new CSS for something `base.css` already does.
