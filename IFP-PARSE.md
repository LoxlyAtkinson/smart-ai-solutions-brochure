# IFP Parse Artifact — Smart AI Solutions Brochure PDF

**Date:** 2026-08-20
**Protocol:** IFP v1.6.2 (`~/.claude/skills/ifp`) + CLAUDE.md RULE 9
**Thinking mechanism:** `mcp__sequential-thinking__sequentialthinking`, 10 thoughts (no fallback needed)
**Instruction units parsed:** 8 / 8 — coverage 100%

---

## Verbatim source instruction

> Next I need a biz detail or url for our services in pdf form in our colorschema. It must 1x be a Profile on me, 2. Be a Profile on the Business and our business Services. Business Services Can be found https://www.smartaisolutions.co.za/ but not all of them, I want to include our Education Services and Subjects we cover, for that you can go through https://futureai.co.za/ - we offer the exact same packages just exclude the prices. For the pdf creation use the official skill and find a skill that can assist us in finding and structuring the content for the Brochure. Preferrably a Skill that also interviews me

---

## Outcome Statement (4 elements)

| Element | Value |
|---|---|
| **Actor** | Loxly, owner of Smart AI Solutions |
| **Action** | Opens and sends the generated brochure PDF to a prospect |
| **Object** | A single A4 PDF business-detail brochure rendered in Smart AI Solutions' exact brand colour scheme |
| **Result** | The prospect sees, in order: (1) a profile of Loxly personally, (2) a profile of the business, (3) the complete business services catalogue **including services not on the website**, (4) education services with every package tier reproduced faithfully, (5) an explicit list of every subject covered — with **zero prices anywhere** |

---

## Sentence-to-Task Coverage Map

| # | Verbatim instruction unit | Derived task | Scope words | Status |
|---|---|---|---|---|
| 1 | "Next I need a biz detail **or url** for our services **in pdf form** in **our colorschema**." | T1 — Produce an A4 PDF brochure of our services in the exact SAS brand colours. "or url" is a genuine ambiguity → escalate to AskUserQuestion. | `our` (all services), `our colorschema` (hard constraint) | Parsed |
| 2 | "It **must** 1x be a **Profile on me**," | T2 — Brochure Section 1 = personal profile of the owner. Requires local bio mining + user interview. | `must` (mandatory) | Parsed |
| 3 | "2. Be a **Profile on the Business** **and** our **business Services**." | T3 — Section 2 = Business Profile. T4 — Section 3 = Services catalogue. Compound clause: **two** distinct blocks, not one. | `and` (compound) | Parsed |
| 4 | "Business Services Can be found https://www.smartaisolutions.co.za/ **but not all of them**," | T5 — Scrape the site for services. T6 — Present the found list to the user and ask what is missing. **Do not invent** the gap. | `not all` (explicit incompleteness warning) | Parsed |
| 5 | "I want to include our **Education Services** **and Subjects we cover**, for that you can go through https://futureai.co.za/" | T7 — Section 4 = Education Services. T8 — Section 5 = explicit enumerated Subjects list. Source is futureai.co.za; ownership is presented as *ours*. | `include` (mandatory), `Subjects we cover` (enumerable) | Parsed |
| 6 | "we offer the **exact same packages** just **exclude the prices**." | T9 — Reproduce package tiers verbatim (names, tiers, inclusions). T10 — **Hard negative constraint: zero price figures**, currency symbols, rates or "from R…" anywhere in the PDF. | `exact same`, `exclude` (negative scope) | Parsed |
| 7 | "For the pdf creation **use the official skill**" | T11 — Invoke `Skill(pdf)`, follow `references/html-to-pdf-brochures.md` (HTML + Puppeteer Node API, the skill's own routing for brochures). Inherits the mandatory **verify-by-PNG** discipline. | Named-tool mandate (no substitution) | Parsed |
| 8 | "and **find a skill** that can assist us in **finding and structuring** the content for the Brochure. **Preferrably a Skill that also interviews me**" | T12 — Search the skill library, select, and actually invoke. Chain chosen: `product-marketing` (interview + structured context) → `sales-enablement` (brochure structure) → `copywriting` (section copy) → `humanizer-loxly` → `fact-checker-loxly` → `pdf` (render). | `find a skill` (search + invoke), 3 capabilities required | Parsed |

**Coverage check (both directions):** 8 instruction units → 12 tasks. Every task traces back to a quoted unit. No orphan tasks, no unmapped units.

---

## Skill selection rationale (unit 8)

Surveyed `~/.claude/skills` for skills that **find** + **structure** + **interview**:

| Skill | Finds | Structures | Interviews | Verdict |
|---|---|---|---|---|
| **product-marketing** | ✓ | ✓ (`.agents/product-marketing.md`) | ✓ (explicitly interviews for product, audience, positioning, ICP) | **SELECTED — primary** |
| **sales-enablement** | ✓ | ✓ (explicitly covers one-pagers / leave-behinds / brochure collateral) | partial (asks questions before starting) | **SELECTED — structure** |
| copywriting | — | ✓ | partial | Selected — section copy |
| case-study | ✓ | ✓ | ✓ | Rejected: PPTX-bound |
| brainstorming | — | ✓ | ✓ (one question at a time) | Rejected: design-discovery, not content |
| /interview (command) | — | — | ✓ (customer interviews, Mom Test) | Rejected: aimed at *customers*, not the owner |

---

## Verification Plan (every item testable)

| ID | Check | Proof artefact |
|---|---|---|
| **V1** | All 5 content pillars render as visible sections | PNG extraction + multimodal Read of **every** page |
| **V2** | Brochure hex values match hexes extracted from smartaisolutions.co.za CSS | Side-by-side hex diff + visual PNG read |
| **V3** | **Zero prices.** `pdftotext` the final PDF, grep for `R\d`, `ZAR`, `\$`, `price`, `pricing`, `cost`, `fee`, `/mo`, `p/m` | The grep output showing 0 hits |
| **V4** | Services list = scraped set **∪** user-supplied additions | Interview answers recorded in the content brief |
| **V5** | Subject count in PDF == subjects captured from futureai.co.za + user additions | Counted list |
| **V6** | No fabrication — every personal-profile fact traces to a local source file or a user answer | Source column in the content brief |
| **V7** | Layout integrity — no text overflow, no dark-card/footer overlap | PNG read of every page (skill's 12-item pre-flight checklist) |

Also binding: the `pdf` skill's own 12-item pre-flight checklist, and CLAUDE.md **RULE 19** (proof is what the eye sees — here, the PNG read).

---

## Ambiguity triage

**Decided without asking** (self-answerable): PDF engine (skill-mandated Puppeteer), skill chain (unit 8 delegated the choice to me), page order (follows the user's own 1/2 numbering), A4 portrait (SA business standard), verification method (skill-mandated).

**Escalated to `AskUserQuestion`** (different answers → materially different work):

1. **Q1 — "or url":** shareable hosted link alongside the PDF, or PDF only? *(changes deliverable count)*
2. **Q2 — Education-arm branding:** "Smart AI Solutions Education", co-branded with FutureAI, or FutureAI-branded section? *(changes every education page's header, logo, colour treatment)*
3. **Q3 — Primary audience:** corporate/B2B, schools, or parents/individuals? *(changes tone, section order, lead proof points)*
4. **Q4 — Length:** tight one-pager, standard 6–8 page brochure, or full capability document? *(changes the whole layout budget)*

**Sequencing decision:** these are blocking at *design* time but not at *research* time. So research runs first, then Q1–Q4 fold into the **first round of the product-marketing interview** — the user answers once, with the scraped facts already in front of them, and no phase blocks with nothing delivered.

---

## Prior art discovered

`Loxly - Personal Projects/SMART-AI-SOLUTIONS - Company Profile.pdf` (3 October 2025, 16:9 slide format, navy + electric blue). Contains executive summary, company snapshot, 6 service groups, use cases, delivery framework, differentiators, governance, tech stack, engagement options, metrics, brand promise, contact.

**Gaps vs. this request:** no personal profile on Loxly, no education services, no subjects list, landscape not A4, and its colours are a slide-deck palette rather than the live site's scheme. The new brochure supersedes it on all five counts.

