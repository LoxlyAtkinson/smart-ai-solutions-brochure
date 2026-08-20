# Smart AI Solutions — Company & Services Profile

The source and build pipeline for the Smart AI Solutions 10-page A4 brochure.

**Live version:** https://loxlyatkinson.github.io/smart-ai-solutions-brochure/

## Outputs

| File | Purpose |
|---|---|
| `smart-ai-solutions-brochure.pdf` | 210 × 297 mm, trim size. Email, WhatsApp, screen. |
| `smart-ai-solutions-brochure-PRINT.pdf` | 226 × 313 mm media box — 210 × 297 trim, 3 mm bleed, crop marks. Hand this to a printer. |
| `docs/` | The GitHub Pages site. |

## Build

```bash
npm install
node build/render-pdf.mjs        # screen PDF
python build/build-print.py      # press HTML (bleed + crop marks)
node build/render-print.mjs      # press PDF
python build/build-web.py        # docs/ for GitHub Pages
node build/measure.mjs           # per-page overflow check against the 260mm content zone
```

`brochure.html` is the single source of truth. Everything else is generated from it.

## Design

Palette sampled from the Smart AI Solutions logo artwork: cyan `#0891b2` primary,
`#22d3ee` bright accent, `#083344` deep, wordmark ink `#15232c`, on the site's own
light-theme neutrals. Typeface Inter, matching the website.

A4 layout follows the fixed-height page system (`height: 296mm`, never `min-height`)
to avoid the Chrome print-engine overflow trap that silently doubles page count.
