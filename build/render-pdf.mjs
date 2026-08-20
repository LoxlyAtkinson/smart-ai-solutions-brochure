// Render the brochure HTML to A4 PDF via the Puppeteer Node API.
// Source of truth: ~/.claude/skills/pdf/references/html-to-pdf-brochures.md
// Usage: node build/render-pdf.mjs [screen|print]
import puppeteer from "puppeteer";
import { pathToFileURL } from "url";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, "..");
const mode = process.argv[2] === "print" ? "print" : "screen";

const HTML = resolve(ROOT, "brochure.html");
const PDF = resolve(
  ROOT,
  mode === "print"
    ? "smart-ai-solutions-brochure-PRINT.pdf"
    : "smart-ai-solutions-brochure.pdf"
);

const browser = await puppeteer.launch({
  headless: "new",
  args: ["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"],
});
try {
  const page = await browser.newPage();
  await page.emulateMediaType("print");
  await page.goto(pathToFileURL(HTML).href, {
    waitUntil: "networkidle0",
    timeout: 60000,
  });

  // Belt-and-braces: wait for web fonts explicitly
  await page.evaluate(async () => {
    if (document.fonts?.ready) await document.fonts.ready;
  });

  await page.pdf({
    path: PDF,
    format: "A4",
    printBackground: true,
    preferCSSPageSize: true,
    margin: { top: "0", right: "0", bottom: "0", left: "0" },
    displayHeaderFooter: false,
  });
  console.log(`Rendered [${mode}] -> ${PDF}`);
} finally {
  await browser.close();
}
