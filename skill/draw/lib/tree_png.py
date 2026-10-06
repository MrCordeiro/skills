"""Render a source-tree / file-tree diagram to PNG.

Use this instead of Excalidraw for file-tree diagrams — box-and-arrow
diagrams are wrong for directory hierarchies. A monospace tree with
aligned descriptions reads better, renders instantly, and looks good
pasted into Slack / docs.

Accepted input is the output of the standard `tree` command or a hand-
written equivalent using the box-drawing characters ``│ ├ └ ─``. Each
line may include an em-dash-prefixed description (aligned in the source
text) — the renderer colour-codes everything after the em dash.

Usage
-----
    import sys
    sys.path.insert(0, "<skill-dir>/lib")   # absolute path, no "~"
    from tree_png import render_tree_png

    render_tree_png(\"\"\"project/
├── cli.py                  — argparse shell
└── core/
    ├── engine.py           — main orchestrator
    └── utils.py            — helpers
\"\"\", "<temp-dir>/project-tree.png")
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# --- theme ---

FONT_SIZE = 15
LINE_HEIGHT = 20
PAD = 28
SUPERSAMPLE = 2

# Colours follow the tiko.org brand palette (see references/color-palette.md).
THEMES = {
    "dark": {
        # Dark page, for Slack and dark-mode documents.
        "bg": (37, 34, 42),           # #25222a near-black
        "fg": (229, 227, 232),        # #e5e3e8 lilac grey
        "tree_glyph": (111, 103, 126),  # #6f677e grey-purple
        "desc": (154, 147, 166),      # #9a93a6 muted grey-purple
        "dir_color": (62, 194, 207),  # #3ec2cf teal
        "root_color": (200, 139, 194),  # #c88bc2 light plum
    },
    "printer": {
        # White page, for documents and printing.
        "bg": (255, 255, 255),
        "fg": (37, 34, 42),           # #25222a near-black
        "tree_glyph": (181, 175, 189),  # #b5afbd light grey-purple
        "desc": (111, 103, 126),      # #6f677e grey-purple
        "dir_color": (129, 37, 120),  # #812578 plum
        "root_color": (184, 48, 150),  # #b83096 magenta
    },
}

TREE_CHARS = set("│├└─ ")

# Monospace font file names, in preference order. Pillow searches the system
# font folders for each name (macOS: /Library/Fonts, /System/Library/Fonts,
# ~/Library/Fonts; Windows: %WINDIR%\Fonts; Linux: XDG data dirs and
# ~/.local/share/fonts). The font must contain the box-drawing glyphs.
# Pillow's built-in default font does not, so the tree lines render as empty
# boxes if no candidate is found. To use another font, set the environment
# variable DRAW_MONO_FONT to a font file name or a full path.
_REGULAR = [
    "SFNSMono.ttf", "Menlo.ttc", "Monaco.ttf",          # macOS
    "CascadiaMono.ttf", "consola.ttf",                  # Windows
    "DejaVuSansMono.ttf", "LiberationMono-Regular.ttf",  # Linux
    "NotoSansMono-Regular.ttf", "cour.ttf", "Courier New.ttf",
]
FONT_NAMES = {
    "default": _REGULAR,
    "printer": [
        "Courier New Bold.ttf", "courbd.ttf", "consolab.ttf",
        "DejaVuSansMono-Bold.ttf", "LiberationMono-Bold.ttf",
        *_REGULAR,
    ],
}


def _load_font(size: int = FONT_SIZE, *, variant: str = "default") -> ImageFont.ImageFont:
    names = FONT_NAMES.get(variant, FONT_NAMES["default"])
    override = os.environ.get("DRAW_MONO_FONT")
    if override:
        names = [override, *names]
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    print("tree_png: no monospace font found; tree lines may render as boxes. "
          "Set DRAW_MONO_FONT to a monospace .ttf file.", file=sys.stderr)
    return ImageFont.load_default()


def render_tree_png(
    tree_text: str,
    output_path: str | Path,
    *,
    font_size: int = FONT_SIZE,
    line_height: int = LINE_HEIGHT,
    pad: int = PAD,
    theme: str = "printer",
    supersample: int = SUPERSAMPLE,
) -> Path:
    """Render `tree_text` as a PNG at `output_path`. Returns the path.

    `tree_text` is any multi-line string using ``│ ├ └ ─`` box-drawing
    characters. Lines may end with an em-dash description, e.g.::

        project/
        ├── cli.py              — argparse shell
        └── core/
            └── engine.py       — main orchestrator

    The em dash separates the filename from its description. The root
    line, directories (names ending in "/"), files and descriptions each
    get their own theme colour. `theme` may be `"dark"` or `"printer"`, and
    defaults to `"printer"`.
    `supersample` renders at a higher resolution then downsamples for
    smoother text.
    """
    try:
        palette = THEMES[theme]
    except KeyError as exc:
        valid = ", ".join(sorted(THEMES))
        raise ValueError(f"Unknown theme {theme!r}. Expected one of: {valid}") from exc

    scale = max(1, supersample)
    font_variant = "printer" if theme == "printer" else "default"
    font = _load_font(font_size * scale, variant=font_variant)
    lines = tree_text.splitlines()

    def measure(text: str) -> int:
        bbox = font.getbbox(text)
        return int(bbox[2] - bbox[0])

    max_w = max((measure(line) for line in lines), default=0)
    scaled_pad = pad * scale
    scaled_line_height = line_height * scale
    img_w = int(max_w + scaled_pad * 2)
    img_h = int(scaled_line_height * len(lines) + scaled_pad * 2)

    img = Image.new("RGB", (img_w, img_h), palette["bg"])
    draw = ImageDraw.Draw(img)

    for i, line in enumerate(lines):
        y = scaled_pad + i * scaled_line_height

        # Split into tree prefix + content
        k = 0
        while k < len(line) and line[k] in TREE_CHARS:
            k += 1
        prefix, rest = line[:k], line[k:]

        x = scaled_pad
        if prefix:
            draw.text((x, y), prefix, fill=palette["tree_glyph"], font=font)
            x += measure(prefix)

        # Split content at first "— " (em dash + space)
        if "— " in rest:
            idx = rest.index("— ")
            name, desc = rest[:idx], rest[idx:]
        else:
            name, desc = rest, ""

        if i == 0:
            colour = palette["root_color"]
        elif name.rstrip().endswith("/"):
            colour = palette["dir_color"]
        else:
            colour = palette["fg"]
        draw.text((x, y), name, fill=colour, font=font)
        x += measure(name)

        if desc:
            draw.text((x, y), desc, fill=palette["desc"], font=font)

    out = Path(output_path)
    if scale > 1:
        img = img.resize((img_w // scale, img_h // scale), Image.Resampling.LANCZOS)
    img.save(out)
    return out


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 tree_png.py <input.txt> <output.png>", file=sys.stderr)
        sys.exit(2)
    src = Path(sys.argv[1]).read_text(encoding="utf-8")
    render_tree_png(src, sys.argv[2])
    print(f"wrote {sys.argv[2]}")
