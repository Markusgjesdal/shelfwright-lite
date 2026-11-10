---
name: product-qa
description: Check a digital product folder or .zip before launch - missing README or licence, empty or junk files, bad file names, broken links, leftover placeholders, oversized files - and write a pass/fail QA report. Use when someone says "QA my product", "check my zip before I upload", "is this ready to sell", or right before publishing a template, PDF, or code pack.
---

# Product QA

Finds the boring mistakes that cause refunds and bad first impressions, before a buyer does. A script does the mechanical checks; you then do a short manual pass. Output: `qa-report.md` next to the product.

## When to use
- Right before uploading a product to a store, and again after any change to the files.
- When a buyer reports a missing or broken file (re-run to find siblings of the same problem).

## When not to use
- To judge listing copy: that's `listing-writer` / `listing-audit`.
- To test whether code in the product works: run its own tests. This skill checks the package, not the program.

## Inputs
- **Required:** path to the product folder or `.zip` the buyer will download.
- **Optional:** the listing text (`listing.md`), to check that "what's inside" matches the files.

## Steps
1. Run the checker (Python 3, standard library only):
   ```
   python scripts/qa_check.py <folder-or-zip> --out qa-report.md
   ```
   Add `--listing listing.md` if a listing exists; the script then checks that file names and counts mentioned there exist. Use `--max-mb 50` to change the size warning, and `--skip-content "GLOB"` (repeatable) for files that mention placeholder words on purpose, such as checklists or templates. `--help` lists all options.
2. Read `qa-report.md`. For each **BLOCKER**, fix it or tell the user exactly what to fix. **WARN** items need a decision, not always a change.
3. Walk `checklists/manual-qa.md` (things a script can't judge: does the PDF open and look right, do screenshots match, is the README's first step correct). Add your findings to the report under "Manual pass".
4. If you have a way to check web links (a fetch tool), test the external links the script listed. Otherwise leave them as "not checked" in the report. Never say a link works if you didn't load it.
5. Give the user a 3-line chat summary: blockers count, warnings count, verdict (`READY` only with 0 blockers and the manual pass done).

## Output
`qa-report.md`: verdict, blockers, warnings, passed checks, external links (checked / not checked), manual pass notes.

## Rules
- Report what you found, not what you expect. "Not checked" is a valid answer.
- Don't delete or rewrite the user's product files unless they ask. Suggest the fix.
- Never upload or publish. The user does that.

## Files in this skill
- `scripts/qa_check.py` — mechanical checks on a folder or zip; writes a Markdown report. Stdlib only, no network.
- `scripts/test_qa_check.py` — tests: `python scripts/test_qa_check.py`.
- `checklists/manual-qa.md` — the human-judgement pass.
