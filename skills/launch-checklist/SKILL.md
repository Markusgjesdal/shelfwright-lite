---
name: launch-checklist
description: Make a step-by-step launch checklist for a digital product - before launch, launch day, and the first week - including the exact clicks the seller must do themselves on their store. Use when someone says "help me launch my product", "what do I need before I publish", "launch plan for my template/guide/pack", or is about to put a product on sale for the first time.
---

# Launch checklist

Turns "I think it's ready" into a short list of concrete, tickable steps, so nothing is forgotten on launch day: files checked, listing ready, images in the right sizes, price set, and a small, honest plan for the first week. Steps the seller must do by hand (clicking publish, posting, paying) are written as numbered click steps. Output: `launch-checklist.md` next to the product folder.

## When to use
- A product is built and the seller wants to launch within days.
- A relaunch or a new version needs the same care as the first launch.

## When not to use
- The product isn't built yet. Finish it first; a checklist can't fix missing content.
- Long-term marketing strategy. This covers launch and the first week only.

## Inputs
- **Required:** the product folder (or a list of the files the buyer gets) and the store it will sell on.
- **Ask once if unknown:** the planned launch date, the price (or "free"), whether there will be a free and a paid version, and where the seller already has an audience (newsletter, community, social account), if anywhere.
- **Optional:** the listing draft, cover images, any outputs from other Shelfwright skills (`qa-report.md`, `listing.md`, `pricing.md`).
If a required input is missing, ask for it once, in one message, then continue.

## Steps
1. **Take stock.** List what exists already: product files, README/instructions, licence, listing text, cover and thumbnail, price. Mark each as done / missing / needs check.
2. **Copy `templates/checklist-template.md`** and fill each section for this product and store. Delete lines that don't apply, add ones that do. Every line must be a single action someone can tick off.
3. **Before launch**: make sure it includes a package check (run `product-qa` if you have it), a listing check (every claim backed by the files), cover images in the store's sizes, price and any discount decided, licence text matching the listing, and a test download of the final file by the seller.
4. **Launch day: write the click steps.** For the store's create-product flow, write numbered steps in the order the seller will meet them on screen ("1. Click New product. 2. Choose Digital product. 3. Paste the title from listing.md, line 1..."). Say exactly which file or text goes where. If you aren't sure what the store's screen looks like today, say so and keep the step general ("find the price field") rather than inventing button names.
5. **First week**: a small plan the seller can really do: share the link where they already have an audience, one helpful post per community that allows it (check the community's self-promotion rules first), answer every buyer question, check the numbers once mid-week and once at the end (use `sales-review` if you have it). No spam, no buying followers or reviews, no repeated posts.
6. **Add time estimates** to each block (e.g. "~20 min") so the seller can plan.
7. Write `launch-checklist.md` and give the user a 3-line chat summary: what's still missing, total time for launch day, the first unticked step.

## Output
`launch-checklist.md` with sections: Status (what exists), Before launch, Launch day (click steps), First week, After week 1 (when to review and decide), Open questions.

## Rules
- Only the seller publishes, posts, pays or emails. The checklist prepares; it never does those steps for them.
- No growth hacks that break store or community rules: no fake reviews, no bulk messages, no comment spam, no fake urgency.
- Don't promise results. A launch checklist makes the launch tidy; it can't guarantee sales.
- Name stores and tools only as plain facts.

## Files in this skill
- `templates/checklist-template.md` — the fill-in checklist with before / launch day / first week sections.
