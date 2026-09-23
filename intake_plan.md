# Intake plan — match returning students by email, not nickname

_Written 2026-09-23. Execute in a fresh session (CLAUDE.md rule 6). Not yet executed._

## Problem

`ingest_form_csv.py` derives the student slug from the **nickname** field
(`map_row()` → `slug = slugify(name)`, line ~682). The only duplicate guards are:

```python
if slug in seen_slugs:                      # dupe within this CSV
if student_dir.exists() and not args.force: # folder already on disk
```

Both are **slug-identity** checks. A returning student who types a different nickname gets a new
slug, passes both guards, and silently becomes a second student folder.

**Hit for real on 2026-09-23.** Sheet row 9 was an existing student who had already been through
intake as `ng-kai-wang` (mid-Stage 3, 12-row UK longlist, `weights.json` derived). Their
re-submission said "NgKW" → new folder `data/students/ngkw/`. No error, no warning. It was caught
only by reading the roster by hand, and the duplicate was deleted manually.

The email **is already captured** — but only as free text appended to `profile.notes`
(line ~907: `note_bits.append(f"Contact: {email}")`). It is never a structured field, so nothing
can match on it.

### Current state of the data bank (measured 2026-09-23)

| | count |
|---|---|
| `profile.json` files | 29 |
| email recoverable by regex from `notes` | 25 |
| structured `contact_email` field | **0** |
| no email anywhere (`lai-zheng-yi`, `ong-kyan`, `toru`, `zafri`) | 4 |

The 4 with no email are pre-form or hand-built students. They can never be matched by email —
the check must degrade gracefully, not error.

## Objective

A returning respondent is **matched to their existing folder and skipped with a clear message**,
instead of creating a second folder. Email is the identity key; nickname stays the slug source.

## Changes

### 1. `tools/init_student.py` — add the field to `profile_template()`

Add `"contact_email": None` to the template. It is the source of truth for profile shape
(`01_intake.md` finalize step 7 compares against it), so it goes first or the new key reads as a
stray.

Place it next to `student_slug` / `name`, not inside `financial` or `needs`.

### 2. `tools/ingest_form_csv.py` — populate it

In `map_row()`, where `email` is already read (~line 692):

```python
profile["contact_email"] = email or None
```

Keep the existing `Contact: <email>` note line. Redundant, but it is what the 25 legacy profiles
are matched on in step 4, and removing it breaks the backfill's own source.

### 3. `tools/ingest_form_csv.py` — the guard

Before the `student_dir.exists()` check, build an index of existing students by email **once**,
outside the row loop:

```python
def _existing_by_email():
    """{lowercased email: slug} for every student already on disk.

    Reads the structured contact_email, falling back to the legacy 'Contact: <addr>'
    note line so students ingested before 2026-09-23 still match. Students with no
    email recorded at all (4 as of 2026-09-23) simply never match — that is correct,
    not a failure.
    """
```

Then per row, if the email matches an existing slug **that is not this row's own slug**:

```python
skipped.append((i, profile["name"], 
    f"email already belongs to student '{existing_slug}' — "
    f"likely a re-submission, not a new student (use --force to override)"))
continue
```

Requirements:
- **Case-insensitive**, stripped. Google returns mixed case.
- **`--force` must still override**, for the genuine "I really want to re-ingest this person" case.
- **Skip, never overwrite.** The existing folder holds the research. Same reasoning as the
  existing folder-exists guard.
- The message must **name the existing slug** — that is the whole value; without it the operator
  still has to grep.

### 4. One-off backfill of the 25 legacy profiles

A script (throwaway, `.tmp/`, not a permanent tool) that reads each `profile.json`, regexes
`Contact:\s*([^\s,]+@[^\s,]+)` out of `notes`, and writes it to `contact_email`. Leave the 4
without an email at `None`.

**Single read-modify-write pass over all 29 files** — not 29 `Edit` calls (CLAUDE.md: repetitive
edits go through a script). `data/students/` is gitignored with no undo, so dry-run and print the
diff first.

### 5. Docs

- `workflows/01_intake.md` — in "How to run" step 2, state that a re-submission by an existing
  email is skipped and names the existing slug. In the finalize section, drop the manual
  "grep the email first" advice once the tool does it.
- Delete the now-stale manual workaround from the `intake-duplicate-resubmission` memory, or
  rewrite it to say the tool handles it.

## Verification

1. `python tools/ingest_form_csv.py "data/form/responses.csv" --dry-run` against a CSV containing
   a **known existing** respondent → must report the skip and name the right slug.
2. Same CSV with `--force` → must still create.
3. A genuinely new email → must create as normal.
4. After the backfill: `contact_email` populated on 25 profiles, `None` on 4, and **no other key
   changed** (diff the JSON keys, not just eyeball it).
5. Confirm `profile_template()` and a freshly-ingested profile have identical key sets.

## Out of scope

- **Merging** a re-submission into the existing student. The 2026-09-23 case showed a
  re-submission can carry genuinely updated facts (that student's grades differed from their
  original intake). Deciding what to carry across is a judgment call and stays a conversation —
  the tool's job is only to stop the silent second folder.
- Changing what the slug is derived from. Nickname-derived slugs are fine and readable; the bug
  is the *matching*, not the naming.
