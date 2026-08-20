import puppeteer from "puppeteer";
import { pathToFileURL } from "url";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";
const __dirname = dirname(fileURLToPath(import.meta.url));
const HTML = resolve(__dirname, "..", "emails", "brochure-email.html");
const b = await puppeteer.launch({ headless: "new", args: ["--no-sandbox","--disable-setuid-sandbox"] });
try {
  for (const [w, tag] of [[700, "desktop"], [390, "mobile"]]) {
    const p = await b.newPage();
    await p.setViewport({ width: w, height: 900, deviceScaleFactor: 2 });
    await p.goto(pathToFileURL(HTML).href, { waitUntil: "networkidle0" });
    await p.screenshot({ path: `verify/email-${tag}.png`, fullPage: true });
    const r = await p.evaluate(() => ({
      scrollW: document.documentElement.scrollWidth,
      clientW: document.documentElement.clientWidth,
      btn: document.querySelector('a[href*="github.io"]')?.textContent.trim(),
      links: [...document.querySelectorAll("a")].length,
    }));
    console.log(tag, w + "px", JSON.stringify(r));
    await p.close();
  }
} finally { await b.close(); }
