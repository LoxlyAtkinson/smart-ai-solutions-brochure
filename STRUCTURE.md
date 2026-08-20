# Brochure Architecture — Smart AI Solutions

**Format:** A4 portrait, 10 pages. Business first, education second (Q2). Single brand (Q4). Zero prices.
**Structure method:** `sales-enablement` skill — leave-behind principles (scannable in 30 seconds, bold headers, short bullets, one idea per block, every claim tied to an outcome) applied at brochure length rather than one-pager length.

---

## Page map

| Page | Section | Maps to instruction unit | Content source |
|---|---|---|---|
| **1** | **Cover** — logo, wordmark, "Company & Services Profile", brand-colour field, website + contact strip | Unit 1 (colour scheme) | Live site brand assets |
| **2** | **The person behind it** — Loxly Atkinson profile: photo, headline, the story (POS trade → built the fix), career spine (Corex → IQ Retail → Smart AI Solutions), how he works | **Unit 2 — "a Profile on me"** | `_Bio/loxly-atkinson-bio.md`, `config.json`, owner interview |
| **3** | **The business** — Smart AI Solutions profile: what we do, who we serve, engagement models, outcomes targeted, brand promise | **Unit 3a — "Profile on the Business"** | Live site + Oct 2025 Company Profile PDF |
| **4** | **Business services I** — core AI + automation services (cards) | **Unit 3b + Unit 4** | smartaisolutions.co.za **∪** owner additions |
| **5** | **Business services II** — remaining services + integrations/tech | **Unit 3b + Unit 4** | smartaisolutions.co.za **∪** owner additions |
| **6** | **Smart AI Solutions Education** — the education division: who it is for, formats, delivery modes | **Unit 5a — "Education Services"** | futureai.co.za (rebranded per Q4) |
| **7** | **Education packages** — every tier reproduced faithfully, **prices removed** | **Unit 6 — "exact same packages just exclude the prices"** | futureai.co.za |
| **8** | **Subjects we cover** — the full enumerated subject list | **Unit 5b — "Subjects we cover"** | futureai.co.za **∪** owner additions |
| **9** | **How we work + selected work** — delivery framework, proof points, sectors served | Supporting (credibility) | Oct 2025 profile + `_TechPortfolio/portfolio-content.md` |
| **10** | **Contact** — website, WhatsApp, email, location, QR to the GitHub Pages version | Unit 1 (the "url") | Live site + owner confirmation |

**Flex:** if the subject list is long, page 8 splits into 8a/8b and the document runs to 11 pages. If it is short, pages 7 and 8 merge and the document runs to 9. Both stay inside the "8–10 pages" decision with a note.

---

## Layout rules inherited from the `pdf` skill

Non-negotiable, from `references/html-to-pdf-brochures.md`:

- `.page { width: 210mm; height: 296mm; padding: 14mm 18mm 22mm; overflow: hidden; page-break-after: always; }` — **fixed** height, never `min-height` (the overflow trap doubles the page count).
- `@page { size: 210mm 297mm; margin: 0; }` and Puppeteer `preferCSSPageSize: true`.
- `print-color-adjust: exact` on `*`, `html`, `body` — otherwise Chrome strips the coloured cover to white.
- 22mm bottom padding reserves the footer zone; **no dark card in the last 40mm** of a dense page (footer-overlap anti-pattern). Use light tonal callouts there instead.
- Images: fixed-height wrapper + `object-fit: cover`. Never `height: auto` in a grid cell.
- Intermediate page headings 20–22pt; 30pt+ reserved for the cover.

## Verification gates before delivery

1. `pdfinfo` → page count as expected, page size `595.92 x 841.92 pts` (A4, not Letter).
2. `pdftoppm -r 150 -png` → one PNG per page.
3. Multimodal `Read` on **every** PNG; describe the pixels, not the intent.
4. `pdftotext` + grep for `R\d`, `ZAR`, `\$`, `price`, `pricing`, `cost`, `fee`, `/mo`, `p/m` → **zero hits**.
5. Hex diff: brochure `:root` values vs hexes extracted from smartaisolutions.co.za.
6. Full 12-item pre-flight checklist from the `pdf` skill.
