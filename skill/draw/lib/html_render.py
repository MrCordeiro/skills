"""Render an HTML file to a PNG with a headless Chromium-based browser, then trim.

Standard helper for the ``draw`` skill's HTML engine. Works on macOS, Windows
and Linux. Needs Pillow (``python3 -m pip install Pillow``) and one installed
browser: Google Chrome, Chromium, Microsoft Edge or Brave. The helper finds the
browser itself. To use a specific browser, set the environment variable
``DRAW_BROWSER`` to the full path of its executable.

Default viewport is ``(1280, 900)`` at 2x device scale, so the output is
2560 px wide. Bottom whitespace is cropped automatically; right-side
whitespace stays (set the viewport width so the content fits).

Usage from Python
-----------------
    import sys
    sys.path.insert(0, "<skill-dir>/lib")   # absolute path, no "~"
    from html_render import render_html_to_png

    render_html_to_png("<temp-dir>/my_diagram.html", "<temp-dir>/my_diagram.png")

Usage from a shell
------------------
    python3 <skill-dir>/lib/html_render.py <input.html> <output.png> [width height]
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

# Executable names to look up on PATH (Linux, and any OS where the user added one).
_PATH_NAMES = [
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
    "chrome", "msedge", "microsoft-edge", "microsoft-edge-stable", "brave-browser",
]

# macOS application bundles, checked in /Applications and ~/Applications.
_MAC_APPS = ["Google Chrome", "Chromium", "Microsoft Edge", "Brave Browser"]

# Windows install locations, relative to Program Files or %LOCALAPPDATA%.
_WIN_RELATIVE = [
    "Google/Chrome/Application/chrome.exe",
    "Microsoft/Edge/Application/msedge.exe",
    "Chromium/Application/chrome.exe",
    "BraveSoftware/Brave-Browser/Application/brave.exe",
]


def find_browser() -> str:
    """Return the path of a Chromium-based browser, or raise FileNotFoundError."""
    override = os.environ.get("DRAW_BROWSER")
    if override:
        if Path(override).exists() or shutil.which(override):
            return override
        raise FileNotFoundError(f"DRAW_BROWSER is set to {override!r}, but that file does not exist")

    for name in _PATH_NAMES:
        found = shutil.which(name)
        if found:
            return found

    candidates: list[Path] = []
    if sys.platform == "darwin":
        for root in (Path("/Applications"), Path.home() / "Applications"):
            candidates += [root / f"{app}.app/Contents/MacOS/{app}" for app in _MAC_APPS]
    elif os.name == "nt":
        roots = [os.environ.get(v) for v in ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA")]
        candidates += [Path(r) / rel for r in roots if r for rel in _WIN_RELATIVE]
    for c in candidates:
        if c.exists():
            return str(c)

    raise FileNotFoundError(
        "No Chrome, Chromium, Edge or Brave browser found. Install one, or set "
        "DRAW_BROWSER to the full path of the browser executable.")


def render_html_to_png(
    html_path: str | Path,
    png_path: str | Path,
    *,
    viewport: tuple[int, int] = (1280, 900),
    scale: int = 2,
    trim_bottom: bool = True,
) -> Path:
    """Render *html_path* to *png_path* with a headless browser; trim bottom whitespace.

    Args:
        html_path: input HTML file (must exist on disk; inline ``<style>`` is fine).
        png_path: output PNG file. Parent directory must exist.
        viewport: ``(width, height)`` of the browser window. Width drives the
            final image width; height is a "max"; bottom whitespace is trimmed.
        scale: device-pixel ratio (default 2, retina). Final image dimensions
            are ``viewport`` × ``scale``.
        trim_bottom: when True, crop pure-background rows off the bottom.

    Returns:
        The output PNG path (as Path), trimmed.
    """
    html_path = Path(html_path).expanduser().resolve()
    png_path = Path(png_path).expanduser().resolve()
    if not html_path.exists():
        raise FileNotFoundError(html_path)
    if png_path.exists():
        png_path.unlink()

    cmd = [
        find_browser(),
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--no-first-run",
        "--no-default-browser-check",
        f"--force-device-scale-factor={scale}",
        f"--window-size={viewport[0]},{viewport[1]}",
        f"--screenshot={png_path}",
        html_path.as_uri(),
    ]
    if hasattr(os, "geteuid") and os.geteuid() == 0:
        cmd.insert(1, "--no-sandbox")  # Chromium refuses to run as root otherwise (Docker, CI)
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if not png_path.exists():
        raise RuntimeError(
            f"The browser did not write {png_path}.\nCommand: {' '.join(cmd)}\n"
            f"Exit code: {result.returncode}\n{result.stderr[-2000:]}")

    if trim_bottom:
        from PIL import Image

        img = Image.open(png_path).convert("RGB")
        # Sample background from the bottom-middle pixel and trim rows that match.
        bg = img.getpixel((img.width // 2, img.height - 1))[:3]  # type: ignore[index]
        y = img.height - 1
        while y > 0:
            row_matches_bg = all(
                img.getpixel((x, y))[:3] == bg  # type: ignore[index]
                for x in range(10, img.width - 10, 50)
            )
            if not row_matches_bg:
                break
            y -= 1
        img.crop((0, 0, img.width, min(y + 40, img.height))).save(png_path)

    return png_path


if __name__ == "__main__":
    if len(sys.argv) not in (3, 5):
        print("Usage: html_render.py <input.html> <output.png> [width height]", file=sys.stderr)
        sys.exit(2)
    vp = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) == 5 else (1280, 900)
    print(f"wrote {render_html_to_png(sys.argv[1], sys.argv[2], viewport=vp)}")
