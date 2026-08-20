"""Build the GitHub Pages version of the brochure into docs/.

Takes brochure.html (the A4 print source) and wraps it for the web:
  - a sticky brand bar with a Download-PDF button
  - JS-driven zoom so a 210mm page fits any viewport, phones included
  - SEO/Open Graph metadata so the shared link previews properly
The page content itself is byte-identical to the printed PDF.
"""
import io
import os
import re
import shutil

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "brochure.html")
DOCS = os.path.join(ROOT, "docs")

PAGES_URL = "https://loxlyatkinson.github.io/smart-ai-solutions-brochure/"

HEAD_EXTRA = """
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="description" content="Smart AI Solutions company and services profile: AI developer rental, automation, chatbots, integrations, analytics and AI search visibility, plus the Smart AI Solutions Education programme. Cape Town, serving South Africa." />
<link rel="canonical" href="{url}" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="Smart AI Solutions" />
<meta property="og:title" content="Smart AI Solutions - Company &amp; Services Profile" />
<meta property="og:description" content="AI systems built around how your business actually works, and the skills to run them yourself." />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="{url}assets/logo-smartai.png" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="icon" href="assets/logo-smartai.png" />
<style>
/* ---------- web-only chrome (does not affect the printed PDF) ---------- */
@media screen {{
  body {{ background: #eef2f5; padding: 0 0 14mm; }}
  .page {{ zoom: var(--fit, 1); }}
  .webbar {{
    position: sticky; top: 0; z-index: 50;
    display: flex; align-items: center; justify-content: space-between;
    gap: 12px; padding: 10px 18px; margin-bottom: 14px;
    background: linear-gradient(135deg, #083344 0%, #155e75 55%, #0891b2 100%);
    color: #fff; font-family: "Inter", system-ui, sans-serif;
  }}
  .webbar .wb-name {{ font-size: 15px; font-weight: 600; letter-spacing: -0.01em; }}
  .webbar .wb-sub {{ font-size: 12px; color: #a5f3fc; display: block; font-weight: 400; }}
  .webbar .wb-actions {{ display: flex; gap: 8px; flex-wrap: wrap; }}
  .webbar a {{
    display: inline-block; padding: 8px 14px; border-radius: 8px;
    font-size: 13px; font-weight: 600; text-decoration: none;
    background: #22d3ee; color: #083344; white-space: nowrap;
  }}
  .webbar a.ghost {{ background: rgba(255,255,255,.14); color: #fff; }}
  .webfoot {{
    max-width: 210mm; margin: 18px auto 0; padding: 0 12px;
    font-family: "Inter", system-ui, sans-serif;
    font-size: 12px; color: #64748b; text-align: center;
  }}
  .webfoot a {{ color: #0e7490; }}
  @media (max-width: 640px) {{
    .webbar {{ flex-direction: column; align-items: flex-start; }}
  }}
}}
@media print {{ .webbar, .webfoot {{ display: none !important; }} }}
</style>
""".format(url=PAGES_URL)

BAR = """
<div class="webbar">
  <div>
    <span class="wb-name">Smart AI Solutions</span>
    <span class="wb-sub">Company &amp; Services Profile &middot; 2026</span>
  </div>
  <div class="wb-actions">
    <a href="smart-ai-solutions-brochure.pdf" download>Download PDF</a>
    <a class="ghost" href="https://wa.me/27722831551">WhatsApp us</a>
    <a class="ghost" href="https://www.smartaisolutions.co.za/">Visit the site</a>
  </div>
</div>
"""

FOOT = """
<div class="webfoot">
  Smart AI Solutions (Pty) Ltd &middot; Kuilsriver, Cape Town &middot;
  <a href="https://www.smartaisolutions.co.za/">smartaisolutions.co.za</a>
</div>
<script>
(function () {
  var A4_PX = 794; /* 210mm at 96dpi */
  function fit() {
    var avail = document.documentElement.clientWidth - 12;
    var s = Math.min(1, avail / A4_PX);
    document.documentElement.style.setProperty('--fit', s);
  }
  fit();
  window.addEventListener('resize', fit);
})();
</script>
"""


def main():
    with io.open(SRC, encoding="utf-8") as fh:
        html = fh.read()

    # inject web-only head additions
    html = html.replace("</head>", HEAD_EXTRA + "</head>", 1)
    # sticky bar right after <body>
    html = html.replace("<body>", "<body>" + BAR, 1)
    # footer + fit script before </body>
    html = html.replace("</body>", FOOT + "</body>", 1)

    if os.path.isdir(DOCS):
        shutil.rmtree(DOCS)
    os.makedirs(os.path.join(DOCS, "assets"))

    with io.open(os.path.join(DOCS, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(html)

    for name in ("logo-smartai.png", "logo-smartai.svg", "loxly-headshot.png", "brochure-qr.png"):
        src = os.path.join(ROOT, "assets", name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(DOCS, "assets", name))

    pdf = os.path.join(ROOT, "smart-ai-solutions-brochure.pdf")
    if os.path.exists(pdf):
        shutil.copy2(pdf, os.path.join(DOCS, "smart-ai-solutions-brochure.pdf"))

    # Jekyll would otherwise ignore nothing here, but be explicit
    with io.open(os.path.join(DOCS, ".nojekyll"), "w", encoding="utf-8") as fh:
        fh.write("")

    print("built docs/ ->", DOCS)
    for root, _dirs, files in os.walk(DOCS):
        for f in sorted(files):
            p = os.path.join(root, f)
            print("  {0:>9,} bytes  {1}".format(os.path.getsize(p), os.path.relpath(p, DOCS)))


if __name__ == "__main__":
    main()
