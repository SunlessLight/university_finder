"""
apply_report_fx.py — re-convert the ringgit prose in a delivered Markdown file, from pairs on disk.

The 2026-09 FX refresh recomputed spreadsheets only. Reports, guides and recommendations state
their ringgit figures in free prose, each worded and rounded differently, so no tool can recompute
them: someone has to read each figure against its foreign-currency basis. That reading is done once
per file (by an agent) and written as a fragment; this tool is the deterministic half — it checks
the fragment against the file and applies it in ONE pass.

Why not a chain of str.replace: with "RM 25,000 -> RM 22,000" and "RM 22,000 -> RM 19,000" in the
same file, the second replace re-converts the first one's output. One regex pass cannot.

Fragment (.tmp/fx_prose/<slug>/<name>.json):
    {"file": "data/students/<slug>/reports/<name>.md",
     "currency": "USD", "old_rate": 4.70,
     "pairs": [{"old": "~RM 313,600", "new": "~RM 269,500", "count": 1, "basis": "USD 66,720"},
               {"old": "(~RM 4.70 per USD)", "new": "(~RM 4.04 per USD)", "count": 1, "kind": "rate"}],
     "left_alone": [{"text": "RM 0", "count": 2, "why": "zero"}]}
A pair may carry its own "currency" + "old_rate" when one file converts two currencies.

Refuses (and writes nothing for that fragment) when: an `old` / `text` does not occur exactly
`count` times; a ringgit figure in the file is covered by neither list; a `new` still holds the old
rate. Warns when new/old is more than 4% away from the rate ratio — rounding is allowed, a slipped
digit is not. Backs the file up beside the fragment before the first write.

Usage:
    python tools/apply_report_fx.py --fragment .tmp/fx_prose/<slug>/<name>.json --dry-run
    python tools/apply_report_fx.py --dir .tmp/fx_prose/<slug>            # every fragment in it
    python tools/apply_report_fx.py --inventory <slug>                    # which files state which rate
"""

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shortlist_schema import FX_TO_MYR  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
# A ringgit figure: "RM 313,600", "RM3.19", "~RM 1.74 million", "MYR 84k". The "~" may sit either side.
RM_FIGURE = re.compile(r"(?:RM|MYR)\s?~?\d(?:[\d,]*\d)?(?:\.\d+)?(?:\s?(?:million|bn|[mMkK])\b)?")
SCALE = {"million": 1e6, "m": 1e6, "bn": 1e9, "k": 1e3}
RATIO_TOLERANCE = 0.04
CURRENCY_WORD = r"(?:USD|US\$|GBP|£|AUD|A\$|SGD|S\$|CNY|RMB|EUR|€|JPY|HKD|CAD|TWD|dollar|pound|yuan|euro)"
RATE_LINE = re.compile(
    r"(?i)(exchange rate|\bFX\b|conver(?:t|sion)[^.|\n]{0,40}(?:rate|at)"
    r"|RM\s?\d\.\d{1,3}\b(?!\s*(?:million|m\b|k\b|bn))|\b\d\.\d{1,3}\s*(?:MYR|RM)\b|per\s+" + CURRENCY_WORD + r"|=\s*RM)")
NOT_DELIVERED = {"status.md", "research_notes.md", "plan.md", "student_life_research.md"}


def _number(text):
    """The first ringgit figure in `text` as a float, or None."""
    m = RM_FIGURE.search(text)
    if not m:
        return None
    n = re.search(r"\d(?:[\d,]*\d)?(?:\.\d+)?", m.group())
    unit = re.search(r"(million|bn|[mMkK])$", m.group())
    return float(n.group().replace(",", "")) * (SCALE[unit.group().lower()] if unit else 1)


def apply_fragment(path, dry_run):
    """Validate one fragment and apply it. Returns a list of error strings ([] = applied)."""
    frag = json.loads(path.read_text(encoding="utf-8"))
    target = REPO_ROOT / frag["file"]
    text = target.read_bytes().decode("utf-8")
    pairs, left = frag.get("pairs", []), frag.get("left_alone", [])
    errors, warnings = [], []

    # Longest first, so "~RM 436,000" wins over "RM 436,000" when both are listed.
    targets = {p["old"]: p for p in pairs}
    targets.update({e["text"]: e for e in left if e["text"] not in targets})
    if not targets:
        return [f"{path.name}: no pairs and nothing left alone"]
    pattern = re.compile("|".join(re.escape(t) for t in sorted(targets, key=len, reverse=True)))

    seen, spans = {}, []
    for m in pattern.finditer(text):
        seen[m.group()] = seen.get(m.group(), 0) + 1
        spans.append(m.span())
    for t, entry in targets.items():
        if seen.get(t, 0) != entry["count"]:
            errors.append(f"{t!r}: expected {entry['count']}, found {seen.get(t, 0)}")
    for m in RM_FIGURE.finditer(text):
        if not any(s <= m.start() and m.end() <= e for s, e in spans):
            line = text.count("\n", 0, m.start()) + 1
            errors.append(f"line {line}: {m.group()!r} is in neither pairs nor left_alone")

    for p in pairs:
        cur, old_rate = p.get("currency", frag["currency"]), p.get("old_rate", frag["old_rate"])
        if p.get("kind") == "rate":
            if str(old_rate) in p["new"] or f"{old_rate:.2f}" in p["new"]:
                errors.append(f"{p['old']!r}: the new rate statement still holds {old_rate}")
            continue
        a, b = _number(p["old"]), _number(p["new"])
        if a and b and abs(b / a - FX_TO_MYR[cur] / old_rate) > RATIO_TOLERANCE:
            warnings.append(f"{p['old']!r} -> {p['new']!r}: ratio {b / a:.3f}, rate ratio "
                            f"{FX_TO_MYR[cur] / old_rate:.3f} ({p.get('basis', 'no basis given')})")

    for w in warnings:
        print(f"  WARN {w}")
    if errors:
        return [f"{path.name}: {e}" for e in errors]

    new_text = pattern.sub(lambda m: targets[m.group()].get("new", m.group()), text)
    replaced = sum(p["count"] for p in pairs)
    print(f"  {'would replace' if dry_run else 'replaced'} {replaced} figure(s), "
          f"left {sum(e['count'] for e in left)} alone: {frag['file']}")
    if not dry_run:
        backup = path.parent / "backup" / target.name
        backup.parent.mkdir(exist_ok=True)
        if not backup.exists():
            shutil.copy2(target, backup)
        target.write_bytes(new_text.encode("utf-8"))
    return []


def inventory(slug):
    """Print the lines that state an exchange rate, per delivered file. A reading aid, not a
    verdict: the wording varies too much to classify by pattern, so a person sorts stale from
    current (and skips noise like "converted stair landings")."""
    base = REPO_ROOT / "data" / "students" / slug
    print("current:", {k: v for k, v in FX_TO_MYR.items() if k not in ("MYR", "RMB")})
    files = list(base.glob("reports/*.md")) + list(base.glob("*.md")) + list(base.glob("application_prep/*.md"))
    for f in sorted(files):
        name = f.relative_to(base).as_posix()
        text = f.read_text(encoding="utf-8")
        figures = len(RM_FIGURE.findall(text))
        if name in NOT_DELIVERED or not figures:
            continue
        hits = [(i, line) for i, line in enumerate(text.splitlines(), 1) if RATE_LINE.search(line)]
        print(f"## {name}  ringgit figures={figures}  rate lines={len(hits)}")
        for i, line in hits[:4]:
            m = RATE_LINE.search(line)
            print(f"   {i}: ...{line[max(0, m.start() - 60):m.end() + 50]}")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--fragment", help="One fragment JSON.")
    group.add_argument("--dir", help="A folder of fragment JSONs (each applied independently).")
    group.add_argument("--inventory", metavar="SLUG", help="List the rate statements in a student's files.")
    parser.add_argument("--dry-run", action="store_true", help="Validate and report; write nothing.")
    args = parser.parse_args()
    if args.inventory:
        inventory(args.inventory)
        return

    paths = [Path(args.fragment)] if args.fragment else sorted(Path(args.dir).glob("*.json"))
    failed = []
    for path in paths:
        print(path.name)
        failed += apply_fragment(path, args.dry_run)
    for line in failed:
        print(f"REFUSED {line}")
    print(f"{len(paths)} fragment(s), {len({f.split(':')[0] for f in failed})} refused")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
