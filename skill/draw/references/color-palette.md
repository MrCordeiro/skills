# Color Palette

All three engines use the tiko.org brand colors. This file lists the brand colors, then shows how the Excalidraw engine uses them. The HTML engine uses the same colors through the CSS variables in `assets/base.css`. The tree engine uses them in the `THEMES` in `lib/tree_png.py`.

## Brand colors

The tiko.org website theme defines these colors. (Source: the theme presets on tiko.org, read 2026-10-06.)

| Name | Hex | Use |
|---|---|---|
| Plum | `#812578` | Main brand color |
| Dark plum | `#631e5d` | Borders and text on plum tints |
| Magenta | `#b83096` | Second accent |
| Teal | `#3ec2cf` | Third accent, fills |
| Dark teal | `#1996a2` | Teal borders and teal text (more contrast than Teal) |
| Grey-purple | `#6f677e` | Muted text, neutral borders |
| Lilac grey | `#e5e3e8` | Light backgrounds, dividers |
| Ink | `#25222a` | Main text |
| White | `#ffffff` | Page background |

The brand has no green, yellow or red. For a warning or an error, use the **functional** colors in the tables below. Do not use functional colors for decoration.

Brand fonts: Stabil Grotesk for body text, Noto Serif for headings. Stabil Grotesk is a licensed font, so most machines show the fallback font in `base.css`. Excalidraw uses its own fonts and cannot use the brand fonts.

## Excalidraw: shape fills

Use the fill, stroke and text color from the same row. Each meaning has its own color, so a reader can tell any two meanings apart.

| Meaning | Fill | Stroke | Stroke style | Text color | Use for |
|---|---|---|---|---|---|
| **Primary / Neutral** | `#ffffff` | `#6f677e` | solid | `#25222a` | The default. Use for any box that has no other meaning in this table. |
| **Start / Trigger / Input** | `#812578` | `#631e5d` | solid | `#ffffff` | Entry points, triggers, user requests, incoming data |
| **End / Success / Output** | `#3ec2cf` | `#1996a2` | solid | `#25222a` | Outcomes, deliverables, success states |
| **AI / Algorithm** | `#f6dcef` | `#b83096` | solid | `#25222a` | AI models, machine learning, rules engines, scoring |
| **Data / Systems** | `#e5e3e8` | `#6f677e` | solid | `#25222a` | Databases, files, reports, servers, background jobs |
| **Human / Manual** | `#d9f3f6` | `#1996a2` | solid | `#25222a` | People, manual steps, reviews, approvals |
| **External / Third party** | `#ffffff` | `#25222a` | dashed | `#25222a` | Partners, vendors, external APIs, systems your team does not own |
| **Decision** (functional) | `#fff3c4` | `#b88600` | solid | `#25222a` | Decision points, conditions, branches |
| **Error / Risk** (functional) | `#fde2e2` | `#cf2e2e` | solid | `#25222a` | Errors, risks, blockers |

Pass the text color to `labeled_box` as `text_color`. The default is `#25222a`, so you only need to pass it for Start boxes:

```python
labeled_box("signup", 100, 100, 200, 80, "#812578", "#631e5d", "Sign-up", text_color="#ffffff")
```

To draw a dashed box, pass `stroke_style="dashed"`. The helper then sets the stroke width to 1.

## Excalidraw: text colors

| Purpose | Color | Use for |
|---|---|---|
| **Title** | `#25222a` | The diagram title and section headings |
| **Label in a box** | The text color from the fill table | Text inside any box |
| **Body / Detail** | `#6f677e` | Notes and descriptions outside boxes |
| **Muted / Caption** | `#9a93a6` | Group labels and text the reader can skip |

## Excalidraw: arrow colors

| Purpose | Color | Use for |
|---|---|---|
| **Primary flow** | `#25222a` | The main path through the diagram |
| **Secondary flow** | `#6f677e` | Optional paths and supporting links. This is the `connect` and `make_arrow` default. |
| **Colored flow** | The stroke color of the source box | Only when all arrows of one meaning must stand out, for example every arrow that leaves an AI box |

## Rules

1. Give related elements the same fill. If three boxes are AI components, make all three magenta.
2. Use at most 4 fill colors in one diagram. If you need more, keep the 4 most important meanings and use Primary for the rest.
3. Always use the fill, stroke and text color from the same row.
4. Do not give free text (text outside a box) a fill. Use a text color only.
5. Add a legend when the diagram uses more than 2 fill colors. Make the legend from small labelled boxes in the top-right corner.

## Use a different brand

To use the skill for a different organization, change the colors in these places. Keep the meanings and change only the hex values.

| File | What to change |
|---|---|
| `references/color-palette.md` | The brand table and the three Excalidraw tables |
| `assets/base.css` | The `--tiko-*` variables, the status colors, the fonts, and the `.ramp` end color |
| `examples/*.html` | The inlined copy of `base.css`. Copy the new `base.css` into each example. |
| `references/html-render.md` | The status table and the end color in `colour_for` |
| `lib/tree_png.py` | The `THEMES` colors |
| `lib/excalidraw.py` | The default `color` in `make_text`, `free_text`, `labeled_box`, `make_arrow` and `connect` |
| `references/excalidraw.md` | The colors in the script template and the group frame color |
| `references/appstate-template.json` | `currentItemStrokeColor` (the default color for lines the user draws later) |

Check text contrast for every fill and text pair. Normal text needs a contrast ratio of at least 4.5:1.
