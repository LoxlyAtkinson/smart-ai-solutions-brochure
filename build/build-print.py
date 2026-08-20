"""Generate the press-ready variant of the brochure.

Screen PDF : 210 x 297 mm, trim size, no marks. For email and WhatsApp.
Print PDF  : 226 x 313 mm media box built as

    +---------------------------------------+  media 226 x 313
    |   +-------------------------------+   |  <- 5mm marks/slug margin
    |   |  +-------------------------+  |   |  <- 3mm bleed (5mm..8mm)
    |   |  |      TRIM 210 x 297     |  |   |  <- trim starts 8mm in
    |   |  +-------------------------+  |   |
    |   +-------------------------------+   |
    +---------------------------------------+

Crop marks are hairlines drawn at the trim line, inside the outer 5mm margin,
so they sit clear of the bleed. Anything that bleeds (the cover gradient band)
is pushed out to the bleed edge at 5mm.
"""
import io
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "brochure.html")
OUT = os.path.join(ROOT, "brochure-print.html")

# 8mm = 5mm marks margin + 3mm bleed
OFFSET = 8

PRINT_CSS = """
<style>
/* ================= PRESS-READY OVERRIDES =================
   media 226 x 313 mm | trim 210 x 297 mm at 8mm inset | bleed 3mm | crop marks
   ========================================================= */
@page { size: 226mm 313mm; margin: 0; }

.page {
  width: 226mm;
  height: 312mm;
  padding: 22mm 26mm 30mm;          /* original 14/18/22 + 8mm offset */
}

/* crop marks: 8 hairlines at the trim boundary, drawn in the outer 5mm margin */
.page, .page.cover {
  background-color: #ffffff;
  background-repeat: no-repeat;
  background-image:
    linear-gradient(#111,#111), linear-gradient(#111,#111),
    linear-gradient(#111,#111), linear-gradient(#111,#111),
    linear-gradient(#111,#111), linear-gradient(#111,#111),
    linear-gradient(#111,#111), linear-gradient(#111,#111);
  background-size:
    0.25pt 5mm, 5mm 0.25pt,
    0.25pt 5mm, 5mm 0.25pt,
    0.25pt 5mm, 5mm 0.25pt,
    0.25pt 5mm, 5mm 0.25pt;
  background-position:
    8mm 0,                  0 8mm,
    calc(100% - 8mm) 0,     100% 8mm,
    8mm 100%,               0 calc(100% - 8mm),
    calc(100% - 8mm) 100%,  100% calc(100% - 8mm);
}

/* absolutely-positioned furniture shifts by the 8mm offset */
.page-foot { left: 26mm; right: 26mm; bottom: 18mm; }

/* cover: the gradient band is the only element that bleeds -> out to 5mm */
.cover-band  { top: 5mm; left: 5mm; right: 5mm; height: 116mm; }
.cover-logo    { top: 24mm; left: 26mm; }
.cover-eyebrow { top: 67mm; left: 26mm; }
.cover-title   { top: 75mm; left: 26mm; right: 32mm; }
.cover-body    { top: 132mm; left: 26mm; right: 44mm; }
.cover-facts   { left: 26mm; right: 26mm; top: 166mm; }
.cover-split   { left: 26mm; right: 26mm; top: 210mm; }
.cover-foot    { left: 26mm; right: 26mm; bottom: 22mm; }

@media print { html, body { background: #fff; } }
</style>
"""


def main():
    with io.open(SRC, encoding="utf-8") as fh:
        html = fh.read()

    html = html.replace(
        "<title>Smart AI Solutions",
        "<title>Smart AI Solutions (PRESS)",
        1,
    )
    html = html.replace("</head>", PRINT_CSS + "</head>", 1)

    with io.open(OUT, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
