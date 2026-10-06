# Excalidraw Engine

This engine makes box-and-arrow diagrams: user flows, system overviews, process maps, decision trees and concept maps. You write a short Python script that uses `lib/excalidraw.py`. The script writes a `.excalidraw` file. The user opens the file at excalidraw.com and can move boxes, edit text and export an image.

## Process

1. List every box and every arrow before you write code. Give each box a short id, a label and a meaning from `references/color-palette.md`.
2. Put the boxes on the grid (see [Layout](#layout)).
3. Write the generator script to `<temp-dir>/<name>_gen.py` and run it with `python3` (on Windows, `python` or `py`).
4. If `write_diagram` raises a `ValueError`, fix every problem in the message and run the script again.
5. Give the user the `.excalidraw` file path and the instructions in [Give the result to the user](#give-the-result-to-the-user).

## Script template

```python
import sys
sys.path.insert(0, "<skill-dir>/lib")   # absolute path; Python does not expand "~"
from excalidraw import labeled_box, free_text, connect, write_diagram

# (fill, stroke) pairs from references/color-palette.md
PRIMARY = ("#ffffff", "#6f677e")
START   = ("#812578", "#631e5d")   # needs text_color="#ffffff"
SUCCESS = ("#3ec2cf", "#1996a2")

elements = [free_text("title", 100, 30, "Checkout flow", font_size=28)]

e, cart = labeled_box("cart", 100, 100, 200, 80, *START, "Cart", text_color="#ffffff")
elements.extend(e)
e, pay = labeled_box("pay", 380, 100, 200, 80, *PRIMARY, "Payment")
elements.extend(e)
e, done = labeled_box("done", 660, 100, 200, 80, *SUCCESS, "Order placed")
elements.extend(e)

connect(elements, "arr-cart-pay", cart, pay, color="#25222a")
connect(elements, "arr-pay-done", pay, done, color="#25222a")

write_diagram("<temp-dir>/checkout.excalidraw", elements)
```

## Functions

| Function | Use it to | Returns |
|---|---|---|
| `labeled_box(prefix, x, y, w, h, fill, stroke, label, font_size=16, text_color="#25222a", stroke_style="solid")` | Draw a box with centred text. The box id is `box-<prefix>`. | `(elements_list, box_id)`. Add the list to `elements` with `extend`. |
| `free_text(id, x, y, text, font_size=16, color="#25222a")` | Write a title, a note or a group label outside a box | One element. Add it with `append`. |
| `connect(elements, arrow_id, from_box_id, to_box_id, color="#6f677e")` | Draw a straight arrow between two boxes. It picks the facing sides and binds the arrow to both boxes. | The arrow id. It adds the arrow to `elements` itself. |
| `make_arrow(id, x, y, points, start_id, end_id, color)` + `bind_arrow(elements, arrow_id, box_id)` | Draw a bent arrow. `x, y` is the start point. `points` are relative to it and start with `[0, 0]`. Call `bind_arrow` once for each bound box. | One element. Add it with `append`. |
| `check_layout(elements)` | Find problems before you write the file. `write_diagram` also calls it. | A list of problems. An empty list means no problems found. |
| `write_diagram(path, elements)` | Write the `.excalidraw` file | The path |
| `reset()` | Reset the id counters. Call it between diagrams when one script makes more than one diagram. | Nothing |

Rules for ids:

- Give every element a unique id.
- Name arrows `arr-<from>-<to>`.
- Use the box id that `labeled_box` returns. Do not type `box-<prefix>` yourself.

## Layout

Place boxes on a grid. Do not place them freely.

| Setting | Value |
|---|---|
| Standard box | 200 × 80 |
| Horizontal gap between boxes | 80 |
| Vertical gap between rows | 60 |
| First box | x = 100, y = 100 |
| Title | `free_text` at x = 100, y = 30, `font_size=28` |
| Column n (from 0) | x = 100 + n × 280 |
| Row n (from 0) | y = 100 + n × 140 |

- **Direction.** Make the main flow go left to right. Use top to bottom only for hierarchies, such as an org chart or a decision tree.
- **Label length.** A label fits in a box when `characters × font_size × 0.6 + 20 ≤ box width`. For a 200-wide box with font size 16, that is 18 characters per line. Add `\n` to make a second line. If a label needs 3 or more lines, make the box larger instead (for example 280 × 100) and keep the same grid gaps.
- **Decisions.** Draw a decision as a box with the Decision color and a label that ends with `?`. Write the outcome on each outgoing arrow's path as `free_text` near the arrow, for example "yes" and "no".
- **Groups.** To show that boxes belong together, draw a frame around them:
  1. Call `labeled_box("grp-<name>", x, y, w, h, "transparent", "#b5afbd", "", stroke_style="dashed")`. Make the frame 30 larger than the boxes on each side, and 30 more at the top for the name.
  2. Add the frame to `elements` **before** the boxes inside it, so it is drawn behind them.
  3. Write the group name with `free_text(..., font_size=14, color="#9a93a6")` at the top-left corner, inside the frame.
  4. `check_layout` allows a box that is fully inside another box. It reports a frame that only partly covers a box.
  5. Do not confuse a frame with an External box. A frame has no fill and a light grey-purple stroke (`#b5afbd`). An External box has a white fill and a near-black stroke (`#25222a`).
- **Arrows.** Use `connect` for every arrow when you can. Use `make_arrow` only when a straight line would cross a box. With 3 or more points, Excalidraw draws a smooth curve through the points.
- **Size.** Use at most 15 boxes in one diagram. If you need more, split the content into 2 diagrams.

## Give the result to the user

You cannot see a `.excalidraw` file. Do not say that the diagram looks correct. Say that the layout checks passed.

Tell the user:

1. The full path of the `.excalidraw` file.
2. To view it: go to https://excalidraw.com, open the menu, select **Open**, and select the file. Or open it in the Excalidraw extension for VS Code.
3. To get an image: in Excalidraw, open the menu, select **Export image**, and select **PNG**. The file already sets the export scale to 2x.

If the user needs a PNG from you directly, and the content is a list, a table or a flow with straight arrows, use the HTML engine instead.

## Limits

- The engine makes rectangles, text and arrows only. It does not make ellipses, diamonds, images or frames.
- `references/appstate-template.json` sets the canvas settings. Do not edit it.
- Excalidraw uses font family 5 (Excalifont, a hand-drawn style). Lines are straight (`roughness` 0).
