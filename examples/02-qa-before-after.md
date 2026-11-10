# Example 2: product QA, before and after

**This is our own example.** The product folder is a tiny sample we made up for this demonstration (`weekly-planner`: a README and a CSV), with four mistakes planted on purpose so you can see what `product-qa` reports. The reports below are real output from `scripts/qa_check.py` run on 2026-11-06. It is not a customer's product.

## Before: the folder as first saved
```
weekly-planner/
  README.md      (links to guide.pdf, contains the word TODO)
  planner.csv
  notes.txt      (empty)
```
Command:
```
python <skills folder>/product-qa/scripts/qa_check.py weekly-planner --out qa-report.md
```
Result (exit code 1, meaning blockers found):
```
3 blocker(s), 1 warning(s)

Blockers
- No LICENSE/LICENCE file. State what the buyer may and may not do.
- Empty file: notes.txt
- Broken local link in README.md: guide.pdf

Warnings
- Placeholder TODO in README.md line 5
```
Every item is something a buyer would notice: a missing guide that the README promises, an empty file in the download, no licence, and an unfinished note.

## The fixes (what we changed by hand, the skill never edits your files)
- Deleted the empty `notes.txt`.
- Fixed the README link to point at a file that exists (`planner.csv`) and removed the TODO.
- Added a one-line `LICENSE.txt`.

## After: same command
Result (exit code 0):
```
0 blocker(s), 0 warning(s)

Passed
- README present.
- Licence file present.
- 3 files, 0.00 MB total.
```
The verdict says "ready after manual pass" because the script cannot judge what only a person can: whether the CSV opens and looks right, whether the README's first step is correct. The skill then walks `checklists/manual-qa.md` for those. A script result alone is never "READY".

## What to take from it
- The mechanical mistakes are caught in seconds and reported with the file and line.
- External links are listed as "not checked" unless your agent can load them. The skill never claims a link works unless it was loaded.
- You run it again after every change to the files, not just once.
