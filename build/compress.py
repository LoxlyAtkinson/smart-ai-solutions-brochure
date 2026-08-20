"""Apply the pdf-skill compression recipe to brochure.html.

Source of the recipe: ~/.claude/skills/pdf/references/html-to-pdf-brochures.md
                      section "Compression recipe (apply when overflow detected)".
Measured overflows before this pass (build/measure.mjs):
  p2 +21.3mm  p3 +30.5mm  p4 +22.0mm  p5 +12.6mm
  p6 +52.1mm  p7 +2.1mm   p8 +15.5mm  (p9, p10 fit)
"""
import io
import os

HTML = os.path.join(os.path.dirname(__file__), "..", "brochure.html")

SUBS = [
    # ---- page furniture ----
    ("padding-bottom: 3mm;\n  border-bottom: 0.5pt solid var(--slate-200);\n  margin-bottom: 7mm;",
     "padding-bottom: 2.4mm;\n  border-bottom: 0.5pt solid var(--slate-200);\n  margin-bottom: 5mm;"),

    # ---- titles / ledes ----
    (".section-title {\n  font-size: 21pt;\n  line-height: 1.14;\n  margin-bottom: 3mm;\n}",
     ".section-title {\n  font-size: 18.5pt;\n  line-height: 1.13;\n  margin-bottom: 2.4mm;\n}"),
    ("  font-size: 10.5pt;\n  line-height: 1.52;\n  color: var(--slate-600);\n  max-width: 152mm;\n  margin-bottom: 6mm;",
     "  font-size: 9.6pt;\n  line-height: 1.48;\n  color: var(--slate-600);\n  max-width: 150mm;\n  margin-bottom: 4.6mm;"),
    ("  width: 16mm;\n  height: 1.2mm;\n  background: linear-gradient(90deg, var(--cyan-600), var(--cyan-400));\n  border-radius: 1mm;\n  margin-bottom: 4mm;",
     "  width: 15mm;\n  height: 1.1mm;\n  background: linear-gradient(90deg, var(--cyan-600), var(--cyan-400));\n  border-radius: 1mm;\n  margin-bottom: 3.2mm;"),
    (".eyebrow {\n  font-size: 7.5pt;\n  font-weight: 600;\n  letter-spacing: 0.16em;\n  text-transform: uppercase;\n  color: var(--cyan-600);\n  margin-bottom: 3mm;\n}",
     ".eyebrow {\n  font-size: 7.2pt;\n  font-weight: 600;\n  letter-spacing: 0.16em;\n  text-transform: uppercase;\n  color: var(--cyan-600);\n  margin-bottom: 2.4mm;\n}"),

    # ---- prose / bullet lists ----
    (".prose p { margin-bottom: 3mm; font-size: 9.3pt; line-height: 1.56; }",
     ".prose p { margin-bottom: 2.4mm; font-size: 8.9pt; line-height: 1.5; }"),
    ("ul.ticks li {\n  position: relative;\n  padding-left: 5mm;\n  margin-bottom: 2mm;\n  font-size: 8.8pt;\n  line-height: 1.45;\n}",
     "ul.ticks li {\n  position: relative;\n  padding-left: 4.4mm;\n  margin-bottom: 1.5mm;\n  font-size: 8.3pt;\n  line-height: 1.4;\n}"),
    (".mini-h {\n  font-size: 9.5pt;\n  font-weight: 600;\n  color: var(--slate-900);\n  margin-bottom: 2.5mm;\n  padding-bottom: 1.5mm;",
     ".mini-h {\n  font-size: 9.2pt;\n  font-weight: 600;\n  color: var(--slate-900);\n  margin-bottom: 2mm;\n  padding-bottom: 1.2mm;"),

    # ---- callout ----
    (".callout {\n  margin-top: 5mm;\n  padding: 4.5mm 5.5mm;\n  background: var(--cyan-50);\n  border-left: 1mm solid var(--cyan-600);\n  border-radius: 2mm;\n  font-size: 9.2pt;\n  line-height: 1.5;",
     ".callout {\n  margin-top: 4mm;\n  padding: 3.4mm 4.4mm;\n  background: var(--cyan-50);\n  border-left: 1mm solid var(--cyan-600);\n  border-radius: 2mm;\n  font-size: 8.5pt;\n  line-height: 1.44;"),

    # ---- profile page ----
    (".profile-top {\n  display: grid;\n  grid-template-columns: 52mm 1fr;\n  gap: 8mm;\n  align-items: start;\n  margin-bottom: 6mm;\n}",
     ".profile-top {\n  display: grid;\n  grid-template-columns: 50mm 1fr;\n  gap: 7mm;\n  align-items: start;\n  margin-bottom: 4.5mm;\n}"),
    (".portrait {\n  width: 52mm;\n  height: 62mm;",
     ".portrait {\n  width: 50mm;\n  height: 57mm;"),
    (".profile-name {\n  font-size: 22pt;", ".profile-name {\n  font-size: 20pt;"),
    (".profile-role {\n  font-size: 9pt;\n  font-weight: 600;\n  letter-spacing: 0.1em;\n  text-transform: uppercase;\n  color: var(--cyan-700);\n  margin-bottom: 4mm;\n}",
     ".profile-role {\n  font-size: 8.4pt;\n  font-weight: 600;\n  letter-spacing: 0.1em;\n  text-transform: uppercase;\n  color: var(--cyan-700);\n  margin-bottom: 3.2mm;\n}"),
    (".profile-hook {\n  font-size: 11pt;\n  line-height: 1.5;", ".profile-hook {\n  font-size: 10pt;\n  line-height: 1.45;"),
    ("  gap: 4mm;\n  margin: 5mm 0;\n}", "  gap: 3.4mm;\n  margin: 4mm 0;\n}"),
    (".tl {\n  background: var(--slate-50);\n  border-radius: 2.5mm;\n  border-left: 1mm solid var(--cyan-600);\n  padding: 4mm 4.5mm;\n}",
     ".tl {\n  background: var(--slate-50);\n  border-radius: 2.5mm;\n  border-left: 1mm solid var(--cyan-600);\n  padding: 3.2mm 3.8mm;\n}"),
    (".tl .org { font-size: 8pt; color: var(--slate-500); line-height: 1.4; }",
     ".tl .org { font-size: 7.6pt; color: var(--slate-500); line-height: 1.35; }"),

    # ---- service cards ----
    (".svc-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 4.5mm; }",
     ".svc-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 3.4mm; align-items: start; }"),
    ("  border-radius: 2.5mm;\n  padding: 4.5mm 5mm 5mm;\n  position: relative;\n  overflow: hidden;\n}",
     "  border-radius: 2.5mm;\n  padding: 3.4mm 4mm 3.8mm;\n  position: relative;\n  overflow: hidden;\n}"),
    (".svc h3 {\n  font-size: 10.5pt;\n  line-height: 1.22;\n  margin-bottom: 2mm;\n}",
     ".svc h3 {\n  font-size: 9.9pt;\n  line-height: 1.2;\n  margin-bottom: 1.5mm;\n}"),
    (".svc p { font-size: 8.4pt; line-height: 1.45; margin-bottom: 2.5mm; }",
     ".svc p { font-size: 8pt; line-height: 1.4; margin-bottom: 2mm; }"),
    ("  font-size: 7.9pt;\n  line-height: 1.4;\n  margin-bottom: 1.2mm;\n  color: var(--slate-600);\n}",
     "  font-size: 7.5pt;\n  line-height: 1.37;\n  margin-bottom: 0.9mm;\n  color: var(--slate-600);\n}"),

    # ---- tiers ----
    (".tier-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 4mm; }",
     ".tier-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 3.4mm; align-items: start; }"),
    (".tier {\n  border: 0.5pt solid var(--slate-200);\n  border-radius: 2.5mm;\n  padding: 4.5mm 4.5mm 5mm;\n  background: var(--white);\n}",
     ".tier {\n  border: 0.5pt solid var(--slate-200);\n  border-radius: 2.5mm;\n  padding: 3.4mm 3.8mm 3.8mm;\n  background: var(--white);\n}"),
    (".tier .name {\n  font-size: 11pt;", ".tier .name {\n  font-size: 10pt;"),
    ("  font-size: 7.6pt;\n  color: var(--cyan-700);\n  font-weight: 600;\n  letter-spacing: 0.06em;\n  text-transform: uppercase;\n  margin-bottom: 3mm;",
     "  font-size: 7.1pt;\n  color: var(--cyan-700);\n  font-weight: 600;\n  letter-spacing: 0.06em;\n  text-transform: uppercase;\n  margin-bottom: 2.4mm;"),
    (".tier ul li {\n  position: relative;\n  padding-left: 4mm;\n  font-size: 8pt;\n  line-height: 1.42;\n  margin-bottom: 1.8mm;\n}",
     ".tier ul li {\n  position: relative;\n  padding-left: 3.6mm;\n  font-size: 7.5pt;\n  line-height: 1.36;\n  margin-bottom: 1.3mm;\n}"),

    # ---- process strip ----
    (".strip {\n  display: grid;\n  grid-template-columns: repeat(4, 1fr);\n  gap: 3.5mm;\n  margin-top: 4mm;\n}",
     ".strip {\n  display: grid;\n  grid-template-columns: repeat(4, 1fr);\n  gap: 3mm;\n  margin-top: 3mm;\n  align-items: start;\n}"),
    (".step {\n  background: var(--slate-50);\n  border-radius: 2.5mm;\n  padding: 4mm 4mm 4.5mm;\n  border-top: 1mm solid var(--cyan-500);\n}",
     ".step {\n  background: var(--slate-50);\n  border-radius: 2.5mm;\n  padding: 3.2mm 3.4mm 3.6mm;\n  border-top: 1mm solid var(--cyan-500);\n}"),
    (".step .d { font-size: 7.6pt; line-height: 1.4; color: var(--slate-600); }",
     ".step .d { font-size: 7.2pt; line-height: 1.36; color: var(--slate-600); }"),

    # ---- grids that must not stretch ----
    (".two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 7mm; }",
     ".two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 6.5mm; align-items: start; }"),
    (".subj-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 3.5mm 6mm; }",
     ".subj-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 3.2mm 6mm; align-items: start; }"),
    (".work-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 4.5mm; }",
     ".work-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 3.6mm; align-items: start; }"),
    (".work {\n  border: 0.5pt solid var(--slate-200);\n  border-radius: 2.5mm;\n  padding: 4.5mm 5mm 5mm;\n  background: var(--white);\n}",
     ".work {\n  border: 0.5pt solid var(--slate-200);\n  border-radius: 2.5mm;\n  padding: 3.6mm 4.2mm 4mm;\n  background: var(--white);\n}"),
    (".toolbox {\n  margin-top: 5mm;\n  padding: 4.5mm 5mm 5mm;",
     ".toolbox {\n  margin-top: 4mm;\n  padding: 3.6mm 4.2mm 4mm;"),

    # ---- inline per-card overrides used on p3 and p6 ----
    ('style="padding:4mm 4mm 4.5mm;"', 'style="padding:3.2mm 3.4mm 3.6mm;"'),

    # ---- COVER: the 4th headline line was clipped by the band edge ----
    ("  height: 104mm;\n  background:", "  height: 113mm;\n  background:"),
    (".cover-eyebrow {\n  position: absolute;\n  top: 62mm; left: 18mm;",
     ".cover-eyebrow {\n  position: absolute;\n  top: 59mm; left: 18mm;"),
    (".cover-title {\n  position: absolute;\n  top: 70mm; left: 18mm; right: 24mm;\n  font-size: 27pt;",
     ".cover-title {\n  position: absolute;\n  top: 67mm; left: 18mm; right: 24mm;\n  font-size: 23.5pt;"),
    (".cover-body {\n  position: absolute;\n  top: 116mm; left: 18mm; right: 40mm;\n}",
     ".cover-body {\n  position: absolute;\n  top: 124mm; left: 18mm; right: 36mm;\n}"),
    ("  left: 18mm; right: 18mm; top: 168mm;\n  display: grid;",
     "  left: 18mm; right: 18mm; top: 158mm;\n  display: grid;"),
    ("  left: 18mm; right: 18mm; top: 210mm;\n  border-top:",
     "  left: 18mm; right: 18mm; top: 202mm;\n  border-top:"),
]


def main():
    with io.open(HTML, encoding="utf-8") as fh:
        html = fh.read()

    missing = []
    for old, new in SUBS:
        if old in html:
            html = html.replace(old, new, 1)
        else:
            missing.append(old.splitlines()[0][:56])

    with io.open(HTML, "w", encoding="utf-8") as fh:
        fh.write(html)

    print("applied {0} of {1} substitutions".format(len(SUBS) - len(missing), len(SUBS)))
    if missing:
        print("NOT FOUND:")
        for m in missing:
            print("  -", m)


if __name__ == "__main__":
    main()
