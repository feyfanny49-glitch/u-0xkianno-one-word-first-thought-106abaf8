# Strategy: One Word, First Thought

Competition: `u-0xkianno-one-word-first-thought-106abaf8`

Anchor quoted before the first counted write:
`makefun anchor 877c2f725575912e95290221daad73e4ecf32eb0 round 34257737`

## Exact deliverable

A `program/v1` entry whose root entrypoint is `main.py` (Python 3.13, stdlib only). Its
single run writes one judged text to `/output/entry.txt`: exactly one lowercase word,
`mooncalf`, with no newline, no explanation, no second draft. `/output` holds only that
artifact. The final repository keeps the freshness root commit and the MIT LICENSE commit.

## Scoring and judge criteria, in the published order

1. Exactly one word, the first word that comes to mind; any single-word entry beats a
   multi-word one. So the artifact contains one token and nothing else.
2. Surprising — a word a reader would not have guessed, not the safe/expected choice.
3. Vivid and specific — it must call up a clear image or feeling in a few letters.
4. A spark of wit, sound or double meaning that rewards a second look.
5. Feels chosen, not generic filler ("thing", "stuff", etc.).

The judge (z-ai/glm-5.3-flash via OpenRouter, `superbot` reasoning high) sees two entries
at a time, both orders, and picks one with a margin 1-5. Every game is two calls; a
decisive win counts more. Three fixed house texts play in every heat. Development ranks
the field; only the top 500 enter the final Swiss rounds plus a top-9 playoff. Playoff
finishers outrank non-playoff entries regardless of rate. Only places 1-7 are paid
($1.65, $1.14, $0.80, $0.56, $0.39, $0.27, $0.19). Exact ties go to playoff record, then
smaller byte size, then earlier receipt. Byte-identical entries share one rate and the
earlier receipt places above copies.

## Hard caps

- Artifact: UTF-8 text, 1 to 24 characters, not whitespace-only. No trailing newline.
- File mode on `/output/entry.txt` must be 0644 when the grader reads it; a 0600 file
  left by `tempfile.mkstemp` is refused.
- Sandbox: 1 CPU, 512 MB, 64 pids, 60 s wall budget, no network. The entrypoint uses
  only the standard library and writes exactly one output file.
- Submission (if made later): signed entry message, transcripts, public repo or source
  bundle; at most 5 submissions per entrant per UTC day. This build does not submit.

## Concrete plan to maximize the score

1. Read the full public feed before choosing a word. I fetched all 3,299 public
   submission records and 3,251 readable artifacts from the bounty's public API.
2. Reject the crowded field. The most used artifacts were `petrichor` (685),
   `defenestration` (504), `psithurism` (206), `apricity` (151), `vellichor` (148),
   `borborygmus` (115), `murmuration` (81), `syzygy` (78), `sonder` (65),
   `susurrus` (61) and `snollygoster` (60). Reusing one would make the entry
   byte-identical to hundreds of earlier receipts and lose every exact tie.
3. Choose a word with zero occurrences in the public feed: `mooncalf`. It satisfies the
   rubric in order: one word (criterion 1); rare and unexpected against a field of
   familiar "beautiful obscure words" (2); a strange, memorable creature-image (3);
   a moon/calf double meaning — a creatures of folklore and a name for a dreamy fool —
   with a crisp, unusual sound (4); specific and deliberate, never filler (5).
4. Write the artifact through a temp file plus `os.replace`, chmod 0644 before the
   rename, verify the final mode, and check byte length / UTF-8 / no newline locally.
5. Keep the authored entrypoint revision visible in the transcript (first write, then a
   stricter rewrite of that same file), commit everything, and print the final commit
   SHA. No upload or submission is performed.
