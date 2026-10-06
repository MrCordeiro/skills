"""Excalidraw diagram helpers — correct-by-default element builders and file writer.

Usage from a diagram generator script:

    import sys; sys.path.insert(0, "<skill-dir>/lib")   # absolute path, no "~"
    from excalidraw import labeled_box, free_text, connect, write_diagram

    elements = []
    e, a = labeled_box("ask", 100, 100, 200, 80, "#812578", "#631e5d", "User asks", text_color="#ffffff")
    elements.extend(e)
    e, b = labeled_box("answer", 380, 100, 200, 80, "#3ec2cf", "#1996a2", "Agent answers")
    elements.extend(e)
    connect(elements, "arr-ask-answer", a, b)
    write_diagram("<temp-dir>/diagram-example.excalidraw", elements)
"""

import json
from collections import OrderedDict
from pathlib import Path

_REFS_DIR = Path(__file__).parent.parent / "references"

with open(_REFS_DIR / "appstate-template.json", encoding="utf-8") as _f:
    APP_STATE = json.load(_f)

# ---------------------------------------------------------------------------
# Counters
# ---------------------------------------------------------------------------

_seed = 100
_idx = 200


def seed():
    """Return a globally unique seed value."""
    global _seed
    _seed += 1
    return _seed


def idx():
    """Return a globally unique fractional index string.

    Excalidraw uses fractional indexing for element ordering.
    Uses 'aXXX' format (e.g. a201, a202) which matches working diagrams
    and keeps lexicographic order = numeric order.
    """
    global _idx
    _idx += 1
    return f"a{_idx}"


def reset():
    """Reset counters — useful when generating multiple diagrams in one script."""
    global _seed, _idx
    _seed = 100
    _idx = 200


# ---------------------------------------------------------------------------
# Element builders
# ---------------------------------------------------------------------------

def make_box(id, x, y, w, h, fill, stroke, bound_elements=None,
             stroke_width=2, stroke_style="solid"):
    """Create a rectangle element."""
    return {
        "id": id, "type": "rectangle",
        "x": x, "y": y, "width": w, "height": h, "angle": 0,
        "strokeColor": stroke, "backgroundColor": fill,
        "fillStyle": "solid", "strokeWidth": stroke_width,
        "strokeStyle": stroke_style,
        "roughness": 0, "opacity": 100,
        "groupIds": [], "frameId": None,
        "index": idx(), "roundness": {"type": 3},
        "seed": seed(), "version": 1, "versionNonce": seed(),
        "isDeleted": False,
        "boundElements": bound_elements if bound_elements is not None else [],
        "updated": 1, "link": None, "locked": False,
    }


def make_text(id, x, y, w, h, text, font_size=16, container_id=None,
              color="#25222a", align="center", valign="middle"):
    """Create a text element (bound to a container or standalone)."""
    return {
        "id": id, "type": "text",
        "x": x, "y": y, "width": w, "height": h, "angle": 0,
        "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100,
        "groupIds": [], "frameId": None,
        "index": idx(), "roundness": None,
        "seed": seed(), "version": 1, "versionNonce": seed(),
        "isDeleted": False, "boundElements": [],
        "updated": 1, "link": None, "locked": False,
        "text": text, "fontSize": font_size, "fontFamily": 5,
        "textAlign": align, "verticalAlign": valign,
        "containerId": container_id, "originalText": text,
        "autoResize": True, "lineHeight": 1.25,
    }


def free_text(id, x, y, text, font_size=16, color="#25222a"):
    """Create standalone (uncontained) text with auto-calculated dimensions."""
    lines = text.split("\n")
    w = max(len(l) for l in lines) * font_size * 0.6 + 20
    h = len(lines) * font_size * 1.25
    return make_text(id, x, y, w, h, text, font_size, container_id=None,
                     color=color, align="left", valign="top")


def labeled_box(prefix, x, y, w, h, fill, stroke, label,
                font_size=16, text_color="#25222a",
                stroke_width=None, stroke_style="solid"):
    """Create a box with centered text label.

    Returns (elements_list, box_id) — extend your elements list with the first.
    Bidirectional bindings are wired automatically.
    Text is sized to its content; verticalAlign="middle" centers it in the box.
    """
    box_id = f"box-{prefix}"
    text_id = f"txt-{prefix}"
    sw = stroke_width if stroke_width is not None else (1 if stroke_style == "dashed" else 2)
    box = make_box(box_id, x, y, w, h, fill, stroke,
                   bound_elements=[{"id": text_id, "type": "text"}],
                   stroke_width=sw, stroke_style=stroke_style)
    # Text dimensions based on content, not container — Excalidraw centers via verticalAlign
    lines = label.split("\n")
    text_h = len(lines) * font_size * 1.25
    text_w = max(len(l) for l in lines) * font_size * 0.6 + 10
    text_x = x + (w - text_w) / 2
    text_y = y + (h - text_h) / 2
    text = make_text(text_id, text_x, text_y, text_w, text_h, label, font_size,
                     container_id=box_id, color=text_color)
    return [box, text], box_id


def make_arrow(id, x, y, points, start_id=None, end_id=None,
               color="#6f677e", stroke_width=2):
    """Create an arrow element. Width/height are derived from points."""
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    w = max(xs) - min(xs)
    h = max(ys) - min(ys)
    sb = {"elementId": start_id, "focus": 0, "gap": 2, "fixedPoint": None} if start_id else None
    eb = {"elementId": end_id, "focus": 0, "gap": 2, "fixedPoint": None} if end_id else None
    return {
        "id": id, "type": "arrow",
        "x": x, "y": y, "width": w, "height": max(h, 1), "angle": 0,
        "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": stroke_width,
        "strokeStyle": "solid",
        "roughness": 0, "opacity": 100,
        "groupIds": [], "frameId": None,
        "index": idx(), "roundness": {"type": 2},
        "seed": seed(), "version": 1, "versionNonce": seed(),
        "isDeleted": False, "boundElements": [],
        "updated": 1, "link": None, "locked": False,
        "points": points, "lastCommittedPoint": None,
        "startBinding": sb, "endBinding": eb,
        "startArrowhead": None, "endArrowhead": "arrow", "elbowed": False,
    }


def bind_arrow(elements, arrow_id, box_id):
    """Add an arrow reference to a box's boundElements list.

    Call this after creating both the arrow and the box.
    Finds the box by id in the elements list and appends the arrow binding.
    """
    for el in elements:
        if el["id"] == box_id and isinstance(el.get("boundElements"), list):
            el["boundElements"].append({"id": arrow_id, "type": "arrow"})
            return
    raise ValueError(f"Box '{box_id}' not found in elements")


def _find(elements, el_id):
    for el in elements:
        if el["id"] == el_id:
            return el
    raise ValueError(f"Element '{el_id}' not found in elements")


def connect(elements, arrow_id, from_box_id, to_box_id, color="#6f677e",
            stroke_width=2):
    """Draw a straight arrow between two boxes and bind it to both.

    The arrow leaves the side of the source box that faces the target box
    and enters the facing side of the target box. Appends the arrow to
    `elements` and returns its id. Use make_arrow + bind_arrow only when you
    need a bent arrow with your own points.
    """
    a = _find(elements, from_box_id)
    b = _find(elements, to_box_id)
    acx, acy = a["x"] + a["width"] / 2, a["y"] + a["height"] / 2
    bcx, bcy = b["x"] + b["width"] / 2, b["y"] + b["height"] / 2
    dx, dy = bcx - acx, bcy - acy
    if abs(dx) >= abs(dy):  # target is mostly left or right
        sx = a["x"] + a["width"] if dx > 0 else a["x"]
        ex = b["x"] if dx > 0 else b["x"] + b["width"]
        sy, ey = acy, bcy
    else:                   # target is mostly above or below
        sy = a["y"] + a["height"] if dy > 0 else a["y"]
        ey = b["y"] if dy > 0 else b["y"] + b["height"]
        sx, ex = acx, bcx
    elements.append(make_arrow(arrow_id, sx, sy, [[0, 0], [ex - sx, ey - sy]],
                               start_id=from_box_id, end_id=to_box_id,
                               color=color, stroke_width=stroke_width))
    bind_arrow(elements, arrow_id, from_box_id)
    bind_arrow(elements, arrow_id, to_box_id)
    return arrow_id


def check_layout(elements):
    """Return a list of layout problems. An empty list means no problems found.

    Checks: duplicate ids, rectangles that partly overlap (full containment is
    allowed, for group frames), labels wider or taller than their box, and
    arrows whose bound boxes do not list the arrow back.
    """
    problems = []
    seen = set()
    for el in elements:
        if el["id"] in seen:
            problems.append(f"Duplicate id '{el['id']}'")
        seen.add(el["id"])

    rects = [el for el in elements if el["type"] == "rectangle"]

    def inside(p, q):  # p is fully inside q
        return (p["x"] >= q["x"] and p["y"] >= q["y"]
                and p["x"] + p["width"] <= q["x"] + q["width"]
                and p["y"] + p["height"] <= q["y"] + q["height"])

    for i, p in enumerate(rects):
        for q in rects[i + 1:]:
            overlap = (p["x"] < q["x"] + q["width"] and q["x"] < p["x"] + p["width"]
                       and p["y"] < q["y"] + q["height"] and q["y"] < p["y"] + p["height"])
            if overlap and not inside(p, q) and not inside(q, p):
                problems.append(f"Boxes '{p['id']}' and '{q['id']}' partly overlap")

    by_id = {el["id"]: el for el in elements}
    for el in elements:
        if el["type"] == "text" and el.get("containerId"):
            box = by_id.get(el["containerId"])
            if box is None:
                problems.append(f"Text '{el['id']}' refers to missing box '{el['containerId']}'")
            elif el["width"] > box["width"] - 10 or el["height"] > box["height"] - 10:
                problems.append(
                    f"Label of '{box['id']}' does not fit: text {el['width']:.0f}x{el['height']:.0f}, "
                    f"box {box['width']}x{box['height']}. Make the box larger or add a line break.")
        if el["type"] == "arrow":
            for side in ("startBinding", "endBinding"):
                bnd = el.get(side)
                if not bnd:
                    continue
                box = by_id.get(bnd["elementId"])
                if box is None:
                    problems.append(f"Arrow '{el['id']}' {side} refers to missing box '{bnd['elementId']}'")
                elif not any(b["id"] == el["id"] for b in box["boundElements"]):
                    problems.append(f"Box '{box['id']}' does not list arrow '{el['id']}'. Call bind_arrow.")
    return problems


# ---------------------------------------------------------------------------
# File writer
# ---------------------------------------------------------------------------

def write_diagram(path, elements):
    """Write an Excalidraw file that excalidraw.com and ExcalidrawZ will accept.

    Handles: full appState, correct key order, indent=2, round-trip validation.
    Raises ValueError if check_layout finds problems.
    """
    problems = check_layout(elements)
    if problems:
        raise ValueError("Layout problems:\n- " + "\n- ".join(problems))

    # Validate before writing
    for el in elements:
        if "id" not in el:
            raise ValueError(f"Element missing 'id': {el}")
        if "type" not in el:
            raise ValueError(f"Element missing 'type': {el}")
        be = el.get("boundElements")
        if be is None:
            raise ValueError(
                f"Element '{el['id']}' has boundElements=None — must be [] (empty list)")

    # Enforce key order (ExcalidrawZ requires this)
    doc = OrderedDict([
        ("type", "excalidraw"),
        ("version", 2),
        ("source", "https://excalidraw.com"),
        ("elements", elements),
        ("appState", APP_STATE),
        ("files", {}),
    ])

    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2)

    # Round-trip validation
    with open(path, encoding="utf-8") as f:
        check = json.load(f)
    if len(check["elements"]) != len(elements):
        raise RuntimeError(
            f"Round-trip failed: wrote {len(elements)} elements, read back {len(check['elements'])}")

    return path
