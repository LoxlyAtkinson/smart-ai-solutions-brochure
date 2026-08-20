import puppeteer from "puppeteer";
import { pathToFileURL } from "url";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";
const __dirname = dirname(fileURLToPath(import.meta.url));
const HTML = resolve(__dirname, "..", "brochure.html");
const b = await puppeteer.launch({ headless: "new", args: ["--no-sandbox","--disable-setuid-sandbox"] });
try {
  const p = await b.newPage();
  await p.emulateMediaType("print");
  await p.goto(pathToFileURL(HTML).href, { waitUntil: "networkidle0", timeout: 60000 });
  await p.evaluate(async () => { if (document.fonts?.ready) await document.fonts.ready; });
  const rows = await p.evaluate(() => {
    const MM = 96 / 25.4;                       // px per mm at 96dpi
    const out = [];
    document.querySelectorAll(".page").forEach((pg, i) => {
      const cs = getComputedStyle(pg);
      const padTop = parseFloat(cs.paddingTop);
      const padBottom = parseFloat(cs.paddingBottom);
      const pageH = pg.getBoundingClientRect().height;
      const budgetPx = pageH - padTop - padBottom;
      const pageTop = pg.getBoundingClientRect().top;
      // lowest bottom edge of any normal-flow child (exclude absolutely positioned furniture)
      let lowest = 0, worst = "";
      const walk = (el) => {
        for (const c of el.children) {
          const s = getComputedStyle(c);
          if (s.position === "absolute" || s.position === "fixed") continue;
          const r = c.getBoundingClientRect();
          const rel = r.bottom - pageTop;
          if (rel > lowest) { lowest = rel; worst = (c.className || c.tagName) + " :: " + (c.textContent||"").trim().slice(0,42); }
          walk(c);
        }
      };
      walk(pg);
      const contentEndMm = (lowest - padTop) / MM;
      const budgetMm = budgetPx / MM;
      out.push({
        page: i + 1,
        usedMm: +contentEndMm.toFixed(1),
        budgetMm: +budgetMm.toFixed(1),
        overMm: +(contentEndMm - budgetMm).toFixed(1),
        worst: worst.slice(0, 60),
      });
    });
    return out;
  });
  console.log("page  used   budget  OVER   offender");
  for (const r of rows) {
    const flag = r.overMm > 0 ? "  *** OVERFLOW" : "";
    console.log(
      String(r.page).padStart(4),
      String(r.usedMm).padStart(6),
      String(r.budgetMm).padStart(7),
      String(r.overMm).padStart(6),
      " ", r.worst + flag
    );
  }
} finally { await b.close(); }
