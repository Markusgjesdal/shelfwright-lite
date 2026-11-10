---
name: listing-writer
description: Write a complete, honest product listing (title options, one-line summary, description, what's inside, who it's for, FAQ, tags) for a digital product by reading the product's own files. Use when someone says "write my listing", "product description for my template/guide/pack", or is about to put a digital product on a store page.
---

# Listing writer

Turns a folder of product files into a store listing that says plainly what the buyer gets. The listing is built from facts found in the files, not from hype. Output: `listing.md` next to the product folder.

## When to use
- A digital product (template, PDF guide, printable, code pack, prompt or skill pack, spreadsheet) is built and needs store copy.
- An old listing should be rewritten from scratch. (To score and patch an existing listing instead, use `listing-audit` if you have it.)

## When not to use
- The product isn't built yet. Write the listing after the files exist, so every claim can be checked against them.

## Inputs
- **Required:** path to the product folder or zip.
- **Ask once if not found in the files:** who it's for (one sentence), price or price range, the store it goes on, and anything the buyer must already have (software, account, skill level).
- **Optional:** the user's own notes, an older listing, a screenshot list, real customer feedback the user can show you (only use feedback the user confirms is real and allowed to quote).

## Steps
1. **Inventory the product.** List every file the buyer will receive (recurse into folders and zips). Count pages, sheets, templates, skills, or whatever the unit is. Note formats and any required software. Write this list down first: it is the source of truth for the rest.
2. **Find the job.** In one sentence, state the task the buyer finishes faster or better with this product. If you can't, ask the user before writing anything else.
3. **Fill `templates/listing-template.md`** section by section:
   - **Title options (3):** under 70 characters, lead with the outcome or the thing, include the format (e.g. "Notion template", "PDF", "skill pack"). No ALL CAPS, no emoji walls, no "ultimate/best/#1" unless the user can prove it.
   - **Summary:** one sentence, under 160 characters, usable as the store's short description and the search snippet.
   - **Description:** 3 short paragraphs: the problem in the buyer's words, what this product does about it, how it is used (steps or a short example).
   - **What's inside:** bullet list made only from the inventory in step 1, with real counts.
   - **Who it's for / not for:** 2-4 bullets each. "Not for" builds trust and cuts refunds.
   - **Requirements:** software, versions, accounts, skill level.
   - **FAQ:** 4-6 questions a buyer would really ask (format, refunds, updates, compatibility, licence, support). Answer only with facts the user confirmed; otherwise mark `[ASK USER]`.
   - **Tags:** 8-12 lowercase search phrases people would type, no competitor or brand names unless as compatibility.
4. **Run `checklists/claims-check.md`** over the draft and fix every hit.
5. **Mark gaps.** Any fact you could not verify stays as `[ASK USER: ...]` in the text. Do not fill it with a guess.
6. **Write `listing.md`**, then give the user a 3-line chat summary: chosen title, number of `[ASK USER]` items, anything from the claims check you were unsure about.

## Output
`listing.md` with sections: Title options, Summary, Description, What's inside, Who it's for, Who it's not for, Requirements, FAQ, Tags, Open questions.

## Rules
- Every number in the listing must come from the inventory or from the user.
- No income or results promises ("make $X", "guaranteed", "go viral"). Describe what the product does, not what the buyer will earn.
- No invented reviews, testimonials, buyer counts, "limited time" or "only N left".
- Other companies' product names appear only as compatibility facts ("works with ..."), never in a way that suggests endorsement.
- Write for people skimming on a phone: short paragraphs, plain words, no wall of bold.
- Never publish or paste into the store yourself. The user does that.

## Files in this skill
- `templates/listing-template.md` — the fill-in structure for `listing.md`.
- `checklists/claims-check.md` — lines to search for and fix before handing over.
