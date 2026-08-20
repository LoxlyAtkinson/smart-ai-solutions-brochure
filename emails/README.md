# Client Emails

Four drafts for sending the brochure, plus one HTML version.

| File | Send to | Attach the PDF? |
|---|---|---|
| `01-existing-client.txt` | People you already work with | Yes |
| `02-new-enquiry.txt` | Someone you have just spoken to | Yes |
| `03-cold-intro.txt` | First contact, no prior conversation | **No.** Link only |
| `04-education-hr.txt` | HR, L&D, department heads, training coordinators | Yes if warm |
| `brochure-email.html` | HTML version of 01, for a mail platform | Yes |

**Link in every email:** https://loxlyatkinson.github.io/smart-ai-solutions-brochure/
**Attachment:** `smart-ai-solutions-brochure.pdf` (5.3 MB)

## Before you send

1. **Replace every square bracket.** `[First name]`, `[Company]`, `[their specific problem]`. Email 02 is weak without the specific problem filled in.
2. **Pick one subject line.** Three options at the top of each file. Delete the others.
3. **Set the preview text** if your platform supports it. It is the second thing people read after the subject.
4. **Check the attachment size.** 5.3 MB clears most limits but some corporate gateways cap at 5 MB. If in doubt, send the link only.

## Rules baked into these drafts

- **No pricing.** Not in the brochure, not in the emails. Rates are quoted on request. If you put a number in an email you have undone the reason the brochure has none.
- **No em dashes or en dashes.** House rule, applied throughout.
- **NAPTOSA is described as a 56,000-member union**, never as 56,000 users. The figure is union membership, not platform users.
- **No certification claim.** Session 10 signposts recognised international certification. Smart AI Solutions does not issue a certificate.
- **Cold sends carry an opt-out** and no attachment.

## Sending the HTML version

`brochure-email.html` is built for email clients, not browsers: table layout, every style inline, no `<style>` block, no gradients, no background images, solid hex fills with `bgcolor` fallbacks. Outlook strips all four of those things, which is why none of them are used.

Contrast is above WCAG AA 4.5:1 on every text colour. The measurements are in a comment at the top of the file.

**Always send a plain-text alternative alongside it.** Use `01-existing-client.txt` as the text part. Emails with only an HTML part get filtered more aggressively, and some readers only ever see the text part.

To use it in Gmail: open the file in a browser, select all, copy, paste into the compose window. Gmail preserves inline styles on paste.

## Timing

Tuesday to Thursday, 08:00 to 10:00 South African time. Avoid Monday morning and Friday afternoon.

For email 02, send within 24 hours of the call. After that it reads as an afterthought.

## POPIA

Cold B2B email to a business address is permitted under POPIA, with conditions: honour an opt-out immediately, and be able to show where the address came from. Keep a note of the source against each address you add.
