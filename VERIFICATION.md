# Verification Record

Against the plan in `IFP-PARSE.md`, the layout gates in `STRUCTURE.md`, and the
12-item pre-flight checklist in `~/.claude/skills/pdf/references/html-to-pdf-brochures.md`.

Date: 2026-08-20. All receipts in `verify/` (git-ignored; regenerate with the build commands in `README.md`).

---

## V1 — All five content pillars render

| Pillar | Instruction unit | Page | Result |
|---|---|---|---|
| Profile on the owner | 2 | 2 | PASS |
| Profile on the business | 3a | 3 | PASS |
| Business services | 3b + 4 | 4, 5, 6 | PASS |
| Education services | 5a | 7, 8 | PASS |
| Subjects we cover | 5b | 9 | PASS |

Proof: `pdftoppm -r 150` produced ten PNGs; every page opened and inspected in the multimodal Read tool.

## V2 — Colour fidelity

Palette hex-matched to the logo artwork sampled pixel-by-pixel (`#0891b2`, `#22d3ee`, `#33dfeb`, `#083344`, ink `#15232c`) and the site's own light-theme neutral tokens (`#0f172a`, `#475569`, `#64748b`, `#f8fafc`, `#e2e8f0`). Typeface Inter, the site font.

Owner chose the **logo cyan** over the website's blue chrome (`#3b82f6` / `#2563eb`); both palettes are documented in `.agents/product-marketing.md` so the divergence is a recorded decision rather than an accident. **PASS.**

## V3 — Zero prices

```
pdftotext -layout -enc UTF-8 smart-ai-solutions-brochure.pdf verify/brochure.txt
grep -anioE "\bR ?[0-9][0-9 ,.]*|\bZAR\b|\$[0-9]|\bprice[sd]?\b|\bpricing\b|\bcost[s]?\b|\b[0-9]+%|/month\b|per month\b|excl\.? ?VAT\b"
  -> no matches (exit 1)
```

Confirmed again against the **live DOM**, not just the PDF: `priceHits: []`.

The only money-adjacent words in the document are the deliberate absence statements
"Current rates for every service are quoted on request" and "Programme fees and
scheduled dates are quoted on request". No figure, no currency symbol, no percentage. **PASS.**

> Note: the first scan appeared to pass while `grep` was silently treating the extracted
> text as a binary file. Re-run with `-a` and `-enc UTF-8`, which is when the page-8
> footer collision below was actually caught. A green scan is not a scan.

## V4 — Service completeness

Website crawl found 10 core service lines plus GEO. Owner selected "All 11 plus the free
audits and tools", so the brochure carries 11 service lines, 3 free diagnostics, 4
done-for-you reports and 3 partnership models. Owner added nothing beyond the site. **PASS.**

## V5 — Subject completeness

Ten curriculum sessions and 32 named platforms, reproduced as subject coverage in original
Smart AI Solutions wording. **PASS.**

## V6 — No fabrication

Every fact on page 2 traces to `_Bio/loxly-atkinson-bio.md`, `config.json`, or an owner answer.
Owner ruled the `_Bio` career history over the conflicting website version. Barend Geldenhuys'
details come from the website `/about`. Suppressed on the owner's standing rulings: the
"56,000 users" framing, HubSpot, Ash Electronics, agent runtime line counts, unevidenced
Eden FM engagement figures, and the contested live-systems count. **PASS.**

## V7 — Layout integrity

`build/measure.mjs` compares each page's lowest normal-flow element against the 260mm content zone.

| Page | Before compression | After | Status |
|---|---|---|---|
| 2 | +21.3mm over | 13.4mm spare | fixed |
| 3 | +30.5mm over | 12.2mm spare | fixed |
| 4 | +22.0mm over | 24.0mm spare | fixed |
| 5 | +12.6mm over | 29.8mm spare | fixed |
| 6 | +52.1mm over | 15.8mm spare | fixed (report cards restructured 2x2 to 1x4) |
| 7 | +2.1mm over | 27.5mm spare | fixed |
| 8 | +15.5mm over | 32.8mm spare | fixed |
| 9 | fits | 27.1mm spare | ok |
| 10 | fits | 10.4mm spare | ok |

**Bugs caught and fixed by visual inspection, not by the build succeeding:**
1. Cover headline's fourth line clipped by the gradient band edge. Band 104mm to 113mm, title 27pt to 23.5pt.
2. Page-2, 3, 4 callouts and cards painting over the absolute footer (the documented dark-card/footer-overlap anti-pattern). Fixed by the compression recipe, not by moving the footer.
3. Grid children stretching to row height; `align-items: start` added to every card grid.

**PASS.**

## V8 — House style

Owner's cardinal rule is no em or en dashes in any content. First draft had 44 em dashes
and 4 en dashes. All replaced with the punctuation each sentence wanted.

```
brochure.html          em: 0   en: 0
rendered PDF text      em: 0   en: 0
live DOM               emDashes: 0   enDashes: 0
```

**PASS.**

## V9 — Output integrity

```
smart-ai-solutions-brochure.pdf         Pages: 10   Page size: 594.96 x 841.92 pts (A4)
smart-ai-solutions-brochure-PRINT.pdf   Pages: 10   Page size: 641.04 x 887.04 pts (226 x 313 mm)
```

Neither doubled, neither US Letter. Press file inspected: crop marks visible at all four
corners in the outer margin, cover gradient carried out to the 3mm bleed edge. **PASS.**

Image resolution at print size: headshot 1254px across 50mm is roughly 637dpi; logo 1376px
across 62mm is roughly 564dpi. Both comfortably above the 300dpi press minimum.

## V10 — Deployment smoke test (global RULE 13)

| Route | Status | Bytes |
|---|---|---|
| `/` | 200 | 63,157 |
| `/smart-ai-solutions-brochure.pdf` | 200 | 5,258,361 |
| `/assets/logo-smartai.png` | 200 | 187,914 |
| `/assets/loxly-headshot.png` | 200 | 2,002,051 |
| `/assets/brochure-qr.png` | 200 | 2,323 |

## V11 — Browser-observed result (global RULE 19)

Live site driven in a real browser, not curled.

- HTTP 200, title `Smart AI Solutions: Company & Services Profile`
- 10 `.page` elements present
- 12 of 12 images loaded (`naturalWidth > 0`)
- Sticky bar renders with Download PDF, WhatsApp us, Visit the site
- "Loxly Atkinson" and "Barend Geldenhuys" both present
- Desktop 1280px: `scrollWidth == clientWidth`, no horizontal overflow
- Mobile 390px: `scrollWidth == clientWidth`, fit scale 0.476, whole A4 page visible

Screenshots: `verify/live-desktop.png`, `verify/live-mobile.png`. **PASS.**

---

## Open items for the owner

1. **No print-ready logo master exists.** Everything published is RGB web raster on a white
   ground, plus one SVG. A transparent-background and CMYK version should be produced before
   a commercial print run.
2. **The website's founder bio contradicts the CV corpus** (Chaos Computers / IT architecture
   versus Corex / IQ Retail). The brochure uses the `_Bio` version on the owner's instruction;
   the website still carries the other one.
3. **No client testimonials exist on disk.** Every CV promises them. The brochure therefore
   carries none. Two quotes from NAPTOSA and Eden FM would materially strengthen page 10.
4. **The October 2025 company profile PDF and the 6-page site brochure are now superseded**
   by this document on five counts: owner profile, education arm, subject list, A4 format,
   and palette.
