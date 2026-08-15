"""
check_social_post.py — confidentiality gate for a drafted social-media post/thread.

This repo is public-facing and holds PDPA-sensitive student data (`data/students/`,
`data/form/`), while `workflows/social_media.md` turns finished repo work into a public
Twitter/X draft. The two must never touch: a draft that leaks a student's name, a
data-path fragment, or a live credential is not "ready" no matter how good the copy is.
This tool is the deterministic half of that gate — the same WAT split `check_master_list.py`
already uses for the master list, applied here to a social draft instead of a CSV row.

KNOWN LIMITATION: this checker only scans the working tree of the file you point it at.
It does not scan git history. If a draft's topic touches something that was once leaked
and has since been scrubbed (a commit that briefly held a real name or a token before
being fixed), a clean run here does not prove that leak is gone — say so to whoever is
relying on the "clean" result, don't let it read as a guarantee.

Checks (use --check to run a subset while iterating on a fix):
  names    any live student slug (data/students/*/ directory name), or a close variant
           of one, appearing anywhere in the draft text. Slugs are read live off disk —
           nothing is hardcoded — so this never goes stale as students are added or
           archived. Reuses difflib.get_close_matches the same way tools/apply_backfill.py
           uses it to fuzzy-match a fragment's column name against SHORTLIST_HEADERS: here
           the "column list" is the live slug list, and each word-run in the draft is the
           candidate being matched.
  paths    a literal `data/students/`, `data/form/`, or `.tmp/<slug>/` fragment appearing
           in the draft text (the first two are fixed strings; the third is a substring
           check against each live slug).
  secrets  credential-shaped strings: `sk-...`, `fc-...`, `AKIA...`, an `api_key=`/`password=`
           assignment, a `Bearer <token>` header, or a long base64-looking literal. This is
           the same regex family `.claude/agents/commit-drafter.md` (Step 4) already
           describes by hand for its own safety sweep, implemented here as real regexes
           instead of prose so a social draft gets the identical check.

Exit 0 clean, exit 1 with findings printed per check — same `ok` / `FAIL (n)` block style
as check_master_list.py's run()/main(). EXCEPTION: if `names` is among the requested checks
and no live student slugs can be read (no `data/students/` in this worktree/clone), that
check cannot actually run — it prints `SKIP names` instead of `ok names` and the whole run
exits 1, because "couldn't check" must never look like "checked, clean" for a safety gate.

Usage:
    python tools/check_social_post.py --file .tmp/social/twitter_thread.md
    python tools/check_social_post.py --file .tmp/social/draft.md --check secrets
    python tools/check_social_post.py --file .tmp/social/draft.md --limit 5
"""

import argparse
import difflib
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
STUDENTS_DIR = REPO_ROOT / "data" / "students"

CHECKS = ["names", "paths", "secrets"]

# Fixed data-path fragments that must never appear literally in a public draft, regardless
# of whether any student folder currently exists. `.tmp/<slug>/` is handled separately in
# check_paths() because it needs a live slug to build the fragment.
_FIXED_PATH_FRAGMENTS = ("data/students/", "data/form/")

# Credential-shaped string families, mirroring the safety sweep commit-drafter.md (Step 4)
# already describes by hand: sk-/fc- style API keys, AWS access keys, api_key/password
# assignments, Bearer auth headers, and long base64-looking literals (access tokens,
# encoded secrets). The base64 pattern requires a digit, an uppercase and a lowercase
# letter in the run so ordinary long lowercase words don't trip it.
_SECRET_PATTERNS = [
    ("OpenAI-style key (sk-...)", re.compile(r"\bsk-[A-Za-z0-9]{10,}\b")),
    ("Firecrawl-style key (fc-...)", re.compile(r"\bfc-[A-Za-z0-9]{10,}\b")),
    ("AWS access key (AKIA...)", re.compile(r"\bAKIA[0-9A-Z]{12,}\b")),
    ("api_key assignment", re.compile(r"api[_-]?key\s*[=:]\s*['\"]?[\w\-]{6,}", re.IGNORECASE)),
    ("password assignment", re.compile(r"password\s*[=:]\s*['\"]?\S{4,}", re.IGNORECASE)),
    ("Bearer token", re.compile(r"\bBearer\s+[A-Za-z0-9\-_.=]{8,}")),
    (
        "long base64-looking literal",
        re.compile(r"\b(?=[A-Za-z0-9+/]{32,}={0,2}\b)(?=\S*\d)(?=\S*[A-Z])(?=\S*[a-z])[A-Za-z0-9+/]{32,}={0,2}"),
    ),
]

# Word-run lengths tried when hunting for a student's name written out in prose (e.g. a
# slug "ong-kyan" showing up as "Ong Kyan" in draft text). 1 catches a bare slug typed as
# one hyphenated token; 2-4 catch it spread across a few space-separated words.
_NAME_NGRAM_SIZES = (1, 2, 3, 4)
_NAME_CLOSE_MATCH_CUTOFF = 0.82


def load_slugs():
    """Live student slugs — data/students/*/ directory names. Empty list if the folder
    doesn't exist (this worktree deliberately doesn't carry real student PII)."""
    if not STUDENTS_DIR.exists():
        return []
    return sorted(p.name for p in STUDENTS_DIR.iterdir() if p.is_dir())


def _redact(value):
    """Never echo a full secret back in a finding — just enough to identify it."""
    return value if len(value) <= 10 else value[:6] + "...(redacted)"


def check_names(text, slugs):
    """Live student slugs, or close variants of one, written out in the draft text.

    Builds word n-grams (1-4 words, hyphen-joined, lowercased) from the draft and fuzzy
    matches each against the live slug list with difflib.get_close_matches — the same
    call apply_backfill.py uses to match a fragment's column name against
    SHORTLIST_HEADERS, applied here to prose instead of a column name.

    KNOWN LIMITATION: the word regex ([a-z']+) drops digits, so a slug like "ong-kyan-2"
    can never be reconstructed from an n-gram here — nothing in this checker does a plain
    substring scan for a bare slug, so a digit-suffixed slug written out in prose can slip
    through undetected.
    """
    if not slugs:
        return []
    findings = set()
    words = re.findall(r"[a-z']+", text.lower())
    for n in _NAME_NGRAM_SIZES:
        for i in range(len(words) - n + 1):
            gram = "-".join(words[i : i + n])
            if len(gram) < 3:
                continue
            match = difflib.get_close_matches(gram, slugs, n=1, cutoff=_NAME_CLOSE_MATCH_CUTOFF)
            if not match:
                continue
            slug = match[0]
            if gram == slug:
                findings.add(f"{gram!r} matches student slug {slug!r} exactly")
            else:
                findings.add(f"{gram!r} is a close variant of student slug {slug!r}")
    return sorted(findings)


def check_paths(text, slugs):
    """Literal data/students/, data/form/, or .tmp/<slug>/ fragments in the draft text.

    The first two are checked regardless of whether any student folder currently
    exists — they're PDPA-sensitive roots by construction, not by who's in them right
    now. The .tmp/<slug>/ case needs a live slug to build the fragment against.
    """
    findings = []
    for fragment in _FIXED_PATH_FRAGMENTS:
        if fragment in text:
            findings.append(f"literal path fragment {fragment!r} found in draft")
        backslashed = fragment.replace("/", "\\")
        if backslashed in text:
            findings.append(f"literal path fragment {backslashed!r} found in draft")
    for slug in slugs:
        fragment = f".tmp/{slug}/"
        if fragment in text:
            findings.append(f"literal path fragment {fragment!r} found in draft (student: {slug})")
        backslashed = fragment.replace("/", "\\")
        if backslashed in text:
            findings.append(f"literal path fragment {backslashed!r} found in draft (student: {slug})")
    return findings


def check_secrets(text):
    """Credential-shaped strings — see _SECRET_PATTERNS for the regex family."""
    findings = []
    for label, pattern in _SECRET_PATTERNS:
        for m in pattern.finditer(text):
            findings.append(f"{label}: {_redact(m.group(0))!r}")
    return findings


def run(text, slugs, wanted):
    results = {}
    if "names" in wanted:
        results["names"] = check_names(text, slugs)
    if "paths" in wanted:
        results["paths"] = check_paths(text, slugs)
    if "secrets" in wanted:
        results["secrets"] = check_secrets(text)
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Confidentiality gate for a drafted social-media post — checks it for "
        "student PII and credential-shaped secrets before it can be called ready."
    )
    parser.add_argument("--file", help="Path to the draft to check.")
    parser.add_argument("--check", help=f"Comma list of checks to run (default all): {', '.join(CHECKS)}")
    parser.add_argument("--limit", type=int, default=15, help="Max findings shown per check (default 15).")
    args = parser.parse_args()

    if not args.file:
        sys.exit("ERROR: --file is required.")

    file_path = Path(args.file)
    if not file_path.is_absolute():
        file_path = REPO_ROOT / file_path
    if not file_path.exists():
        sys.exit(f"ERROR: {file_path} not found.")

    wanted = CHECKS
    if args.check:
        wanted = [c.strip().lower() for c in args.check.split(",") if c.strip()]
        unknown = [c for c in wanted if c not in CHECKS]
        if unknown:
            sys.exit(f"ERROR: unknown check(s) {unknown}. Valid: {', '.join(CHECKS)}")

    text = file_path.read_text(encoding="utf-8")
    slugs = load_slugs()

    results = run(text, slugs, wanted)

    # "names" is the gate's most important check — it's the one that catches a real student
    # slug written into a public draft. If it was requested but there are no live slugs to
    # check against, the check did not run at all; that must never print/exit the same as a
    # check that ran and found nothing (see docstring EXCEPTION above).
    names_skipped = "names" in wanted and not slugs

    total = sum(len(v) for v in results.values())
    label = file_path.relative_to(REPO_ROOT) if file_path.is_relative_to(REPO_ROOT) else file_path
    slug_note = (
        f"{len(slugs)} live student slug(s)"
        if slugs
        else "no data/students/ found — names/paths checks limited to fixed literals"
    )
    print(f"{label} — {slug_note}, {total} finding(s)")
    for name in CHECKS:
        findings = results.get(name)
        if findings is None:
            continue
        if name == "names" and names_skipped:
            print(f"  SKIP {name} — no data/students/ found, cannot verify")
            continue
        if not findings:
            print(f"  ok   {name}")
            continue
        print(f"  FAIL {name} ({len(findings)})")
        for line in findings[: args.limit]:
            print(f"       {line}")
        if len(findings) > args.limit:
            print(f"       ... and {len(findings) - args.limit} more")

    sys.exit(1 if (total or names_skipped) else 0)


if __name__ == "__main__":
    main()
