"""Check a text against the plain-language rules. Standard library only.

Reports each problem as ``<file>:<line>: <severity> [<rule>] <message>``.
Exit code: 0 when there are no errors, 1 when there is at least one error,
2 for a usage problem.

Rules
-----
- em-dash         error    An em dash, or a dash used as one (" -- ", " – ").
- word-list       error    A phrase from references/word-list.md.
                  warning  A word-list phrase that has a note in brackets.
- lead-label      error    A line that starts with a label such as "Resolved:"
                           or "X confirmed:" instead of the finding.
- long-sentence   warning  A sentence with more than --max-words words.
- passive         warning  A possible passive verb ("was decided"). Keep it
                           only if the actor is unknown or not important.
- abbreviation    warning  An abbreviation that is not spelled out the first
                           time it is used, for example "Data Engineering (DE)".

Markdown is supported: front matter, code blocks, inline code, URLs, link
targets, HTML comments and block quotes are not checked.

Usage
-----
    python3 check_text.py <file> [<file> ...]
    python3 check_text.py -            # read from standard input
    python3 check_text.py --max-words 20 --words my-list.md draft.md
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

DEFAULT_WORDS = Path(__file__).resolve().parent.parent / "references" / "word-list.md"

# Phrases that the word list itself suggests. They look passive but are allowed.
PASSIVE_ALLOWED = re.compile(
    r"\b(is|are|was|were|be|been)\s+(based on|recorded in|added to|sent on|copied to|"
    r"not reversed|replaced by|included in|written into|kept for reference|"
    r"required|needed|allowed|called|named|located|done|used to)\b", re.I)

IRREGULAR_PARTICIPLES = (
    "built|done|made|given|taken|written|sent|shown|known|found|kept|held|set|put|"
    "read|run|seen|chosen|paid|told|sold|left|lost|met|led|won|begun|drawn|driven|"
    "broken|spoken|stolen|thrown|worn|torn|hidden|brought|bought|caught|taught|"
    "thought|understood|felt|meant|spent|sent|lent|cut|hit|shut|split|spread|"
    "forgotten|gotten|ridden|risen|frozen|chosen|proven|shown")
PASSIVE = re.compile(
    r"\b(am|is|are|was|were|be|been|being)\s+(?:\w+ly\s+)?"
    r"(\w{3,}ed|" + IRREGULAR_PARTICIPLES + r")\b", re.I)
# Words ending in -ed that are usually adjectives after "is/are".
ED_ADJECTIVES = {
    "interested", "tired", "excited", "worried", "concerned", "pleased", "satisfied",
    "surprised", "confused", "bored", "scared", "married", "detailed", "limited",
    "related", "advanced", "experienced", "qualified", "complicated", "dedicated",
    "focused", "aligned", "blocked", "supposed", "expected", "unexpected", "used",
    "red", "bed", "need", "seed", "feed", "speed", "embed",
}

LEAD_LABEL = re.compile(
    r"^\s*(?:[-*+]\s+|\d+\.\s+)?(?:\*\*|__)?\s*"
    r"(resolved|confirmed|fixed|answered|settled|clarified|"
    r"[\w\s'-]{1,40}?\s(?:resolved|confirmed|settled|clarified|fixed))\s*(?:\*\*|__)?\s*:", re.I)

EM_DASH = re.compile(r"—|\s--\s|\s–\s")
ABBREV = re.compile(r"\b([A-Z][A-Z0-9&]{1,}[a-z]?)\b")
# Capitalised words used for emphasis, not abbreviations.
EMPHASIS = {"ONE", "NOT", "ALL", "ANY", "AND", "OR", "NO", "YES", "MUST", "NEVER", "ALWAYS",
            "ONLY", "DO", "DONT", "NEW", "TODO", "NOTE", "STOP", "WARNING", "IMPORTANT"}
WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9'’-]*")


@dataclass
class Entry:
    pattern: re.Pattern
    shown: str
    suggestion: str
    severity: str


@dataclass
class Problem:
    line: int
    severity: str
    rule: str
    message: str


# --------------------------------------------------------------------------
# Word list
# --------------------------------------------------------------------------

def _verb_forms(word: str) -> set[str]:
    """Return common inflections of a verb given in any form."""
    w = word.lower()
    if not re.fullmatch(r"[a-z]+", w):
        return {w}
    if w.endswith("ies"):
        base = w[:-3] + "y"
    elif w.endswith("ied"):
        base = w[:-3] + "y"
    elif w.endswith("es") and re.search(r"(s|x|z|ch|sh)es$", w):
        base = w[:-2]
    elif w.endswith("s") and not w.endswith("ss"):
        base = w[:-1]
    elif w.endswith("ing") and len(w) > 5:
        base = w[:-3]
    elif w.endswith("ed") and len(w) > 4:
        base = w[:-2]
    else:
        base = w
    forms = {w, base}
    if base.endswith("y") and len(base) > 2 and base[-2] not in "aeiou":
        forms |= {base[:-1] + "ies", base[:-1] + "ied", base + "ing"}
    elif base.endswith("e"):
        forms |= {base + "s", base + "d", base[:-1] + "ing"}
    else:
        es = "es" if re.search(r"(s|x|z|ch|sh)$", base) else "s"
        forms |= {base + es, base + "ed", base + "ing"}
        if re.fullmatch(r"[^aeiou]*[aeiou][bdgmnprt]", base):  # sit -> sitting, spin -> spinning
            forms |= {base + base[-1] + "ing", base + base[-1] + "ed"}
    return forms


def _phrase_pattern(phrase: str) -> re.Pattern:
    words = phrase.split()
    first = "|".join(sorted((re.escape(f) for f in _verb_forms(words[0])), key=len, reverse=True))
    rest = r"[\s-]+".join(re.escape(w) for w in words[1:])
    body = f"(?:{first})" + (r"[\s-]+" + rest if rest else "")
    return re.compile(rf"(?<![\w-]){body}(?![\w-])", re.I)


def load_word_list(path: Path) -> tuple[list[Entry], set[str]]:
    entries: list[Entry] = []
    known: set[str] = set()
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.lower().startswith("known:"):
            known |= {a.strip() for a in line.split(":", 1)[1].split(",") if a.strip()}
            continue
        if not line.startswith("|") or set(line) <= set("|-: "):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2 or cells[0].lower() == "never":
            continue
        never, suggestion = cells[0], cells[1]
        for group in re.split(r",\s*(?![^()]*\))", never):  # commas outside brackets
            note = re.search(r"\(([^)]*)\)", group)
            severity = "warning" if note else "error"
            group = re.sub(r"\([^)]*\)", "", group)
            for variant in group.split(" / "):
                phrase = variant.strip().strip("`")
                if phrase:
                    entries.append(Entry(_phrase_pattern(phrase), phrase, suggestion, severity))
    return entries, known


# --------------------------------------------------------------------------
# Markdown cleaning
# --------------------------------------------------------------------------

def clean_lines(text: str) -> list[tuple[int, str]]:
    """Return (line number, checkable text) pairs with Markdown noise removed."""
    out: list[tuple[int, str]] = []
    text = text.replace("’", "'").replace("‘", "'")  # curly apostrophes
    lines = text.splitlines()
    i = 0
    if lines and lines[0].strip() == "---":  # YAML front matter
        for j in range(1, len(lines)):
            if lines[j].strip() == "---":
                i = j + 1
                break
    in_fence = False
    in_comment = False
    for n in range(i, len(lines)):
        line = lines[n]
        stripped = line.strip()
        if stripped.startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if in_comment:
            if "-->" in line:
                in_comment = False
                line = line.split("-->", 1)[1]
            else:
                continue
        if "<!--" in line:
            before, after = line.split("<!--", 1)
            if "-->" in after:
                line = before + after.split("-->", 1)[1]
            else:
                line, in_comment = before, True
        if stripped.startswith(">"):
            continue  # quoted words belong to someone else
        line = re.sub(r"`[^`]*`", " ", line)                 # inline code
        line = re.sub(r"\]\([^)]*\)", "]", line)             # link targets
        line = re.sub(r"https?://\S+", " ", line)            # bare URLs
        line = re.sub(r"<[^>]+>", " ", line)                 # HTML tags
        out.append((n + 1, line))
    return out


def sentences(lines: list[tuple[int, str]]) -> list[tuple[int, str]]:
    """Split into sentences. Headings, table rows and list items end a sentence."""
    result: list[tuple[int, str]] = []
    buf, start = "", 0

    def flush():
        nonlocal buf
        if buf.strip():
            result.append((start, buf.strip()))
        buf = ""

    for n, line in lines:
        s = line.strip()
        if not s or s.startswith("#") or s.startswith("|"):
            flush()
            continue
        if re.match(r"^([-*+]|\d+\.)\s", s):
            flush()
            s = re.sub(r"^([-*+]|\d+\.)\s+", "", s)
        if not buf:
            start = n
        for part in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'*(])", s):
            if buf:
                buf += " "
            buf += part
            if re.search(r"[.!?][\"')*]*$", part):
                flush()
                start = n
    flush()
    return result


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------

def check(text: str, entries: list[Entry], known: set[str], max_words: int) -> list[Problem]:
    problems: list[Problem] = []
    lines = clean_lines(text)

    for n, line in lines:
        if EM_DASH.search(line):
            problems.append(Problem(n, "error", "em-dash",
                                    "Dash used to join ideas. Use a full stop, a comma, a colon or brackets."))
        if LEAD_LABEL.match(line):
            label = LEAD_LABEL.match(line).group(1)
            problems.append(Problem(n, "error", "lead-label",
                                    f'Line starts with "{label.strip()}:". Start with the finding itself.'))
        if line.strip().startswith("|"):
            prose = " ".join(line.strip().strip("|").split("|"))
        else:
            prose = line
        taken: list[tuple[int, int]] = []
        for e in entries:
            for m in e.pattern.finditer(prose):
                # Variants and longer phrases can match the same words. Report once.
                if any(m.start() < end and start < m.end() for start, end in taken):
                    continue
                taken.append(m.span())
                problems.append(Problem(n, e.severity, "word-list",
                                        f'"{m.group(0)}": use {e.suggestion}.'))

    defined: set[str] = set()
    for n, sent in sentences(lines):
        words = WORD.findall(sent)
        if len(words) > max_words:
            problems.append(Problem(n, "warning", "long-sentence",
                                    f"{len(words)} words (limit {max_words}). Split it into sentences with one idea each."))
        for m in PASSIVE.finditer(sent):
            if PASSIVE_ALLOWED.match(sent, m.start()) or m.group(2).lower() in ED_ADJECTIVES:
                continue
            problems.append(Problem(n, "warning", "passive",
                                    f'"{m.group(0)}" may be passive. Name who does it, unless the actor is unknown or not important.'))
        for m in ABBREV.finditer(sent):
            abbr = m.group(1)
            key = abbr[:-1] if abbr[-1] == "s" and abbr[:-1].isupper() else abbr
            if (key in known or key in defined or key in EMPHASIS or len(key) > 5
                    or not any(c.isalpha() for c in key)):
                continue
            defined.add(key)
            explained = (re.search(rf"\(\s*{re.escape(key)}s?\s*\)", sent)
                         or re.search(rf"\b{re.escape(abbr)}\s*\([^)]{{4,}}\)", sent))
            if not explained:
                problems.append(Problem(n, "warning", "abbreviation",
                                        f'"{abbr}" is not spelled out on first use. Write the full name, then ({key}).'))
    problems.sort(key=lambda p: (p.line, p.severity != "error"))
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Check text against plain-language rules.")
    ap.add_argument("files", nargs="+", help="Markdown or text files; '-' reads standard input")
    ap.add_argument("--words", type=Path, default=DEFAULT_WORDS, help="word list file")
    ap.add_argument("--max-words", type=int, default=25, help="longest sentence allowed (default 25)")
    args = ap.parse_args(argv)

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if not args.words.exists():
        print(f"Word list not found: {args.words}", file=sys.stderr)
        return 2
    entries, known = load_word_list(args.words)

    errors = warnings = 0
    for f in args.files:
        if f == "-":
            name, text = "<stdin>", sys.stdin.buffer.read().decode("utf-8")
        else:
            name, text = f, Path(f).read_text(encoding="utf-8")
        for p in check(text, entries, known, args.max_words):
            print(f"{name}:{p.line}: {p.severity} [{p.rule}] {p.message}")
            errors += p.severity == "error"
            warnings += p.severity == "warning"
    print(f"{errors} error(s), {warnings} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
