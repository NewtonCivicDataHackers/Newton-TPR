#!/usr/bin/env python3
"""Expand positional ditto marks in TPR section text (pre-normalization pass).

A "ditto line" repeats tokens from the line above using ditto marks (curly
quotes “ ” or a straight "). Each ditto mark copies the whitespace-delimited
token at the SAME position from the nearest preceding non-ditto reference
line. This is a mechanical pre-normalization pass (see SKILL.md "Pre-
normalization"): it resolves source shorthand into explicit text BEFORE
structured extraction, and touches ONLY lines containing ditto marks — every
other line is preserved byte-for-byte.

Section 84 (speed zones) writes multi-segment stanzas as:
    0.84 miles at 25 miles per hour
    0.52 “ “ 30 “ “ “
where the second line means "0.52 miles at 30 miles per hour".

Usage:
    python3 expand_dittos.py SECTION.txt            # write SECTION.expanded.txt
    python3 expand_dittos.py SECTION.txt -o OUT.txt
    python3 expand_dittos.py --test                 # run self-tests
"""
import re
import sys

DITTO = {"“", "”", '"'}  # “ ” and straight "


def is_ditto(tok):
    return tok in DITTO


def expand_dittos(text):
    """Return (expanded_text, expansions, issues).

    expansions: list of (lineno, original, expanded) for each line changed.
    issues:     list of (lineno, reason, line) for ditto lines left unchanged.
    A non-blank line with no ditto marks becomes the reference for the lines
    below it; expanded ditto lines do NOT themselves become references.
    """
    lines = text.split("\n")
    out, expansions, issues = [], [], []
    ref = None
    for i, line in enumerate(lines, start=1):
        toks = line.split()
        if any(is_ditto(t) for t in toks):
            if ref is None:
                issues.append((i, "ditto line with no preceding reference", line))
                out.append(line)
            elif len(toks) != len(ref):
                issues.append((i, f"token count {len(toks)} != reference {len(ref)}", line))
                out.append(line)
            else:
                new = [ref[j] if is_ditto(t) else t for j, t in enumerate(toks)]
                indent = line[: len(line) - len(line.lstrip())]
                expanded = indent + " ".join(new)
                out.append(expanded)
                expansions.append((i, line.strip(), expanded.strip()))
        else:
            out.append(line)
            if toks:  # non-blank, non-ditto line is the new reference
                ref = toks
    return "\n".join(out), expansions, issues


SPEED_PHRASE = re.compile(r"\d+(?:\.\d+)? miles at \d+ miles per hour")


def _selftest():
    cases = [
        # (input, expected_expanded_lines_present)
        ("0.84 miles at 25 miles per hour\n0.52 “ “ 30 “ “ “",
         "0.52 miles at 30 miles per hour"),
        # mixed “ and ”
        ("2.810 miles at 35 miles per hour\n0.595 ” “ 30 ” “ “",
         "0.595 miles at 30 miles per hour"),
        # chained dittos both reference the same full line
        ("0.10 miles at 15 miles per hour\n0.20 “ “ 25 “ “ “\n0.30 “ “ 35 “ “ “",
         "0.30 miles at 35 miles per hour"),
    ]
    for src, expect in cases:
        exp, _, issues = expand_dittos(src)
        assert expect in exp, f"FAIL: {expect!r} not in {exp!r}"
        assert not issues, f"unexpected issues: {issues}"
    # token-count mismatch is flagged, not silently expanded
    bad = "0.84 miles at 25 miles per hour\n0.52 “ 30 “"
    exp, _, issues = expand_dittos(bad)
    assert issues and "token count" in issues[0][1], "mismatch should be flagged"
    assert "“" in exp, "mismatched ditto line should be left unchanged"
    # non-ditto lines are preserved byte-for-byte
    src = "Header line, unchanged.\n0.84 miles at 25 miles per hour\n0.52 “ “ 30 “ “ “\nending at X."
    exp, _, _ = expand_dittos(src)
    eo = exp.split("\n")
    assert eo[0] == "Header line, unchanged." and eo[3] == "ending at X."
    print("self-tests: PASS")


def main(argv):
    if "--test" in argv:
        _selftest()
        return 0
    args = [a for a in argv[1:] if not a.startswith("-")]
    if not args:
        print(__doc__)
        return 2
    src_path = args[0]
    out_path = None
    if "-o" in argv:
        out_path = argv[argv.index("-o") + 1]
    elif src_path.endswith(".txt"):
        out_path = src_path[:-4] + ".expanded.txt"
    text = open(src_path, encoding="utf-8").read()
    expanded, expansions, issues = expand_dittos(text)
    if out_path:
        open(out_path, "w", encoding="utf-8").write(expanded)
    print(f"expanded {len(expansions)} ditto line(s); {len(issues)} issue(s)")
    for ln, reason, line in issues:
        print(f"  ISSUE line {ln}: {reason}: {line.strip()!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
