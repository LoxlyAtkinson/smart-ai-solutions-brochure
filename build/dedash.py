"""Remove every em dash and en dash from the brochure copy.

Owner's cardinal rule (auto-memory: feedback_no_long_dashes / feedback_no_em_dashes,
and the header of _Bio/loxly-atkinson-bio.md: "Rules applied: ... no em dashes"):
NEVER use em or en dashes in any content.

Each replacement below picks the punctuation the sentence actually wants, rather
than a blanket swap: a colon where the clause enumerates, a comma where it
qualifies, a full stop where it is really two sentences, "to" for ranges.
"""
import io
import os
import sys

HTML = os.path.join(os.path.dirname(__file__), "..", "brochure.html")

REPLACEMENTS = [
    # --- document furniture ---
    ("<title>Smart AI Solutions — Company", "<title>Smart AI Solutions: Company"),
    ("   Smart AI Solutions — Company & Services Profile",
     "   Smart AI Solutions: Company & Services Profile"),
    ("/* Brand cyan — sampled from the logo mark */",
     "/* Brand cyan: sampled from the logo mark */"),
    ("/* Neutrals — the site's own light-theme tokens */",
     "/* Neutrals: the site's own light-theme tokens */"),

    # --- page 1 cover ---
    ("works — and the <em>skills</em>", "works, and the <em>skills</em>"),

    # --- page 2 profile ---
    ("<div class=\"yr\">2013 — 2017</div>", "<div class=\"yr\">2013 to 2017</div>"),
    ("<div class=\"yr\">2017 — 2020</div>", "<div class=\"yr\">2017 to 2020</div>"),
    ("<div class=\"yr\">2020 — now</div>", "<div class=\"yr\">2020 to now</div>"),
    ("Same job, new tools — your staff using AI properly",
     "Same job, new tools. Your staff using AI properly"),
    ("deployed and maintained personally — including a WhatsApp platform",
     "deployed and maintained personally, including a WhatsApp platform"),

    # --- page 3 business ---
    ("We start with the business system — your SOPs",
     "We start with the business system: your SOPs"),
    ("<strong>Loxly Atkinson — Founder.</strong>", "<strong>Loxly Atkinson, Founder.</strong>"),
    ("<strong>Barend Geldenhuys — Chief Operating Officer.</strong>",
     "<strong>Barend Geldenhuys, Chief Operating Officer.</strong>"),

    # --- page 4 services I ---
    ("flexible monthly basis — someone who learns your business",
     "flexible monthly basis. Someone who learns your business"),
    ("<li>No rip-and-replace — existing systems stay intact</li>",
     "<li>No rip-and-replace: existing systems stay intact</li>"),

    # --- page 5 services II ---
    ("<li>Pipeline intelligence — deal health, stalled opportunities, forecasts</li>",
     "<li>Pipeline intelligence: deal health, stalled opportunities, forecasts</li>"),
    ("customers already message you — because in South Africa",
     "customers already message you, because in South Africa"),
    ("<h3>GEO — AI Search Visibility</h3>", "<h3>GEO: AI Search Visibility</h3>"),
    ("gets you <em>cited</em> — named as the answer",
     "gets you <em>cited</em>, named as the answer"),
    ("<li>AI crawler configuration — robots.txt for ChatGPT",
     "<li>AI crawler configuration: robots.txt for ChatGPT"),
    ("<li>Content citability — answer-block formatting and expertise signals</li>",
     "<li>Content citability: answer-block formatting and expertise signals</li>"),

    # --- page 6 tools ---
    ("get a 0–100 GEO score", "get a 0 to 100 GEO score"),

    # --- page 7 education overview ---
    ("take people from cautious to capable — and give organisations",
     "take people from cautious to capable, and give organisations"),
    ("on their own real tasks — not on a case study",
     "on their own real tasks, not on a case study"),
    ("sense it can do far more — you just do not know",
     "sense it can do far more. You just do not know"),
    ("what AI can do end to end — one idea turned into research",
     "what AI can do end to end: one idea turned into research"),

    # --- page 8 programmes ---
    ("fits how your people actually learn — plus two organisation-wide",
     "fits how your people actually learn, plus two organisation-wide"),
    ("Two-Day AI Intensive<br />— Online", "Two-Day AI Intensive<br />Online"),
    ("Two-Day AI Intensive<br />— In Person", "Two-Day AI Intensive<br />In Person"),
    ("<li>Part one: discovering AI — sessions one to five</li>",
     "<li>Part one, discovering AI: sessions one to five</li>"),
    ("<li>Part two: building with AI — sessions six to ten</li>",
     "<li>Part two, building with AI: sessions six to ten</li>"),
    ("<li>We begin by listening — leadership discussions",
     "<li>We begin by listening: leadership discussions"),
    ("<li>Flexible formats — recurring weekly sessions",
     "<li>Flexible formats: recurring weekly sessions"),

    # --- page 9 subjects ---
    ("a presentation and an infographic — in front of you, in real time",
     "a presentation and an infographic, in front of you, in real time"),

    # --- page 10 contact ---
    ("<div class=\"lab\">WhatsApp — fastest route</div>",
     "<div class=\"lab\">WhatsApp, fastest route</div>"),
    ("Mon–Fri 08:00–18:00 &middot; Sat 09:00–14:00",
     "Mon to Fri 08:00 to 18:00 &middot; Sat 09:00 to 14:00"),
    ("Mon–Fri 08:00–18:00 · Sat 09:00–14:00",
     "Mon to Fri 08:00 to 18:00 · Sat 09:00 to 14:00"),
]


def main():
    with io.open(HTML, encoding="utf-8") as fh:
        html = fh.read()

    missing = []
    for old, new in REPLACEMENTS:
        if old in html:
            html = html.replace(old, new)
        else:
            missing.append(old[:64])

    with io.open(HTML, "w", encoding="utf-8") as fh:
        fh.write(html)

    # section-divider comments still carry a dash; harmless but tidy them too
    with io.open(HTML, encoding="utf-8") as fh:
        html = fh.read()
    remaining_em = html.count("—")
    remaining_en = html.count("–")

    print("applied {0} of {1}".format(len(REPLACEMENTS) - len(missing), len(REPLACEMENTS)))
    if missing:
        print("NOT FOUND:")
        for m in missing:
            print("  -", m)
    print("remaining em dashes:", remaining_em)
    print("remaining en dashes:", remaining_en)
    if remaining_em or remaining_en:
        for i, line in enumerate(html.splitlines(), 1):
            if "—" in line or "–" in line:
                print("  line {0}: {1}".format(i, line.strip()[:110]))
        sys.exit(1)


if __name__ == "__main__":
    main()
