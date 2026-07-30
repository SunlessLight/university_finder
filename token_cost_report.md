#1 — The @workflows/03_discover_longlist.md mention, turn one: ~16,000 tokens in a single shot
When your first message tagged @workflows/resume.md @workflows/03_discover_longlist.md, the harness pre-expanded both files into the context before I did anything:

Attachment	Size
03_discover_longlist.md (868 lines — full UK/USA/Australia/Singapore/Malaysia/China/HK/Japan playbooks)	63,918 chars ≈ 16,000 tokens
resume.md (109 lines)	6,454 chars ≈ 1,600 tokens
Skill listing (~40 skills + descriptions)	13,423 chars ≈ 3,350 tokens
Agent-type listing	4,404 chars ≈ 1,100 tokens
SessionStart hook (using-superpowers skill dump)	3,511 chars ≈ 880 tokens
Hook success log	3,908 chars ≈ 980 tokens
Deferred-tools listing	2,274 chars ≈ 570 tokens
Total first API call: cache_creation_input_tokens = 46,726, on top of a 26,403-token baseline already in cache (system prompt + tool defs) — so the session was at 73,129 tokens before I'd read a single file or run a single command. 03_discover_longlist.md alone is ~65% of that turn-one injection. It's a big file by design (every per-country trap ever learned across every student), but only the Australia/Singapore/Malaysia/China sections were relevant to Foo De Mi — the UK/USA/Japan/HK playbooks (roughly half the file) rode along for free.

#2 — Writing the 12 plan files: the most individual turns, ~29,000 tokens of output
Each plan file was its own thinking → tool_use(Write) round-trip. The Write tool itself is cheap on the result side (it just confirms "file created," ~230 chars each) — the cost was in what I had to generate: full, self-contained plan content, 12 times. Summed output across those turns: ~29,100 tokens — close to double the size of the entire status.md file. This phase (turns ~38–66) also accounts for the most distinct messages in the session — one Write call per file, 12 in a row.

#3 — Redundant tool calls (smaller, but avoidable)
status.md alone cost 19,527 chars (~4,880 tokens) to read once — it's a genuinely large per-student file.
I ran check_master_list.py three times during the gap analysis (once truncated with head -200, once via a redirect that didn't work, once finally with --limit 200) before landing on the right flag. That's avoidable duplication — same ~2,400-token output paid for twice extra.
#4 — This very question
Diagnosing this pulled the raw .jsonl transcript, wrote and ran several analysis scripts, and read back their output (~12K chars for one intermediate file alone) — a few thousand more tokens spent explaining the problem.

Bottom line
By the end of this session (last recorded turn): cache_read + cache_creation ≈ 185,338 tokens — matching your "200k+ fast" observation almost exactly. Of the ~159K tokens added during this session, the single @-mention in your first message accounts for ~29% of it, before any real work started. The 12-file plan-writing pass is the second-largest chunk and the busiest in terms of message count.

Actionable takeaway: 03_discover_longlist.md is the recurring cost here — it'll do this every time it's @-mentioned or auto-read for Stage 3 work. Worth considering whether it should be split (a short per-country index + separate per-country trap files), so a single-country session only pulls in what's relevant instead of all eight countries' worth of playbook every time.