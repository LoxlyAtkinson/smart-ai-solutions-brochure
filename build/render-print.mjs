import puppeteer from "puppeteer";
import { pathToFileURL } from "url";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";
const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, "..");
const HTML = resolve(ROOT, "brochure-print.html");
const PDF = resolve(ROOT, "smart-ai-solutions-brochure-PRINT.pdf");
const browser = await puppeteer.launch({
  headless: "new",
  args: ["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"],
});
try {
  const page = await browser.newPage();
  await page.emulateMediaType("print");
  await page.goto(pathToFileURL(HTML).href, { waitUntil: "networkidle0", timeout: 60000 });
  await page.evaluate(async () => { if (document.fonts?.ready) await document.fonts.ready; });
  await page.pdf({
    path: PDF,
    width: "226mm",
    height: "313mm",
    printBackground: true,
    preferCSSPageSize: true,
    margin: { top: "0", right: "0", bottom: "0", left: "0" },
    displayHeaderFooter: false,
  });
  console.log("Rendered [press] ->", PDF);
} finally { await browser.close(); }
