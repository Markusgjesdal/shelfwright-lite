# Shelfwright Lite

Three free agent skills for people who sell digital products (templates, PDFs, printables, small code or prompt packs):

| Skill | What it does | Writes |
|---|---|---|
| [`listing-writer`](skills/listing-writer/SKILL.md) | Writes an honest store listing (titles, summary, description, what's inside, FAQ, tags) from your product's own files, then runs a claims check for income promises, fake scarcity and invented numbers. | `listing.md` |
| [`product-qa`](skills/product-qa/SKILL.md) | Checks a product folder or `.zip` before upload: missing README or licence, empty or junk files, broken local links, leftover `TODO`s, odd file names, oversized files. A stdlib-only Python script does the mechanical checks; the agent does the manual pass. | `qa-report.md` |
| [`launch-checklist`](skills/launch-checklist/SKILL.md) | Makes a launch checklist (before launch, launch day, first week) with the store clicks you do yourself, in order. | `launch-checklist.md` |

Each skill is a folder with a `SKILL.md` (instructions for your agent) plus templates, checklists or a script where needed. Everything is plain text, so you can read it before you install it.

Shelfwright is independent. It is not made, endorsed or sponsored by the makers of any coding agent named below; their names appear only to say what the skills are compatible with.

## Requirements
- A coding agent that loads `SKILL.md` skill folders. As of November 2026 that includes Claude Code, Codex and Cursor.
- Python 3.8+ for `product-qa/scripts/qa_check.py` (standard library only, no network calls). The other two skills need no Python.

## Install

**Option A: copy the folders (works for any SKILL.md agent).** Download this repository (green **Code** button → **Download ZIP**), then copy the three folders inside `skills/` into your agent's skills folder so each one ends up at `<skills folder>/<skill name>/SKILL.md`. Copy the whole folder, not just `SKILL.md`, and start a new agent session.

| Agent tool | Personal (all projects) | Per project |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Codex | `~/.agents/skills/` (some versions: `~/.codex/skills/`) | `.agents/skills/` |
| Cursor | `~/.cursor/skills/` | `.cursor/skills/` |

The Codex and Cursor rows follow their documentation as of November 2026, which changes; check the tool's docs if a skill doesn't show up.

macOS / Linux, from the unzipped folder:
```
mkdir -p ~/.claude/skills && cp -r skills/* ~/.claude/skills/
```
Windows PowerShell, from the unzipped folder:
```
New-Item -ItemType Directory -Force $HOME\.claude\skills | Out-Null
Copy-Item -Recurse -Force .\skills\* $HOME\.claude\skills\
```

**Option B: the `skills` CLI.** Pass this repository's URL (copy it from your browser's address bar):
```
npx skills add <this repository's URL>
```

**Option C: as a Claude Code plugin.** This repository is also a plugin marketplace (`.claude-plugin/`). In Claude Code, using the `owner/repo` part of this page's URL:
```
/plugin marketplace add <owner>/shelfwright-lite
/plugin install shelfwright-lite@shelfwright
```
Plugin skills get the plugin name as a prefix, for example `/shelfwright-lite:product-qa`.

**Check it worked:** ask your agent "which skills do you have?" and look for `listing-writer`, `product-qa` and `launch-checklist`.

## Example: QA a product before you upload it
Open your agent in the folder above your product (say `weekly-planner/`) and ask:

> QA the weekly-planner folder before I upload it.

The agent loads `product-qa` and runs:
```
python <skills folder>/product-qa/scripts/qa_check.py weekly-planner --out qa-report.md
```
On a deliberately flawed sample (an empty file, a README linking to a missing file, a leftover TODO) it wrote:
```
Verdict (script only): NOT READY - 3 blocker(s), 1 warning(s)

Blockers
- No LICENSE/LICENCE file. State what the buyer may and may not do.
- Empty file: `notes.txt`
- Broken local link in `README.md`: `guide.pdf`

Warnings
- Placeholder `TODO` in `README.md` line 5
```
The agent then walks `checklists/manual-qa.md` for what a script can't judge (does the PDF open, do the screenshots match) and adds that to `qa-report.md`. It never deletes or edits your files unless you ask.

Then ask "write my listing" (`listing-writer`) and "give me a launch checklist" (`launch-checklist`).

More: [`examples/`](examples/) has two before/after pairs. They are our own work, made by running these skills on Shelfwright's own listing and files, not customer results.

## What the skills will not do
- They never publish, upload, send or pay for anything. You click the buttons.
- They don't invent numbers, reviews, testimonials or results. Anything they can't confirm from your files is marked `[ASK USER]`.
- They don't promise sales, and nothing here predicts income.

## Shelfwright Pro
Lite is complete on its own. If you want more of the same workflow, **Shelfwright Pro** ($24, Gumroad) has these three plus five more skills:

- `listing-audit`: score an existing listing against a checklist and suggest fixes
- `cover-builder`: cover and thumbnail PNGs from an HTML template
- `pricing-tiers`: a free/paid/bundle tier plan with a fee calculator
- `launch-packet`: everything (copy, files, cover, price, tags) in one click-ordered folder
- `sales-review`: a short weekly review from your exported numbers

Pro: https://markusgjesdal.gumroad.com/l/shelfwright-pro?utm_source=github&utm_medium=readme

The same Lite pack, with a PDF quick-start, is also a free download on Gumroad (it asks for an email at checkout): https://markusgjesdal.gumroad.com/l/shelfwright-lite?utm_source=github&utm_medium=readme

## Licence
Free to use for your own personal or business work, and to modify for your own use. You may share it unchanged and complete, with the [LICENSE](LICENSE), at no charge. You may not sell it. It is not an OSI open-source licence; see [LICENSE](LICENSE) for the full terms. Anything you make with the skills is yours.

## Feedback
Found a wrong check or a broken step? Open an issue in this repository with your agent tool, the skill, and what it printed.
