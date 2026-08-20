import puppeteer from "puppeteer";
const URL = "https://loxlyatkinson.github.io/smart-ai-solutions-brochure/";
const b = await puppeteer.launch({ headless: "new", args: ["--no-sandbox","--disable-setuid-sandbox"] });
try {
  // ---------- desktop ----------
  const p = await b.newPage();
  await p.setViewport({ width: 1280, height: 1000 });
  const resp = await p.goto(URL, { waitUntil: "networkidle0", timeout: 90000 });
  await p.evaluate(async () => { if (document.fonts?.ready) await document.fonts.ready; });

  const r = await p.evaluate(() => {
    const t = document.body.innerText;
    const grab = (re) => (t.match(re) || []).slice(0, 6);
    return {
      status_title: document.title,
      pages: document.querySelectorAll(".page").length,
      emDashes: (t.match(/—/g) || []).length,
      enDashes: (t.match(/–/g) || []).length,
      emSamples: grab(/.{25}—.{25}/g),
      priceHits: grab(/\bR ?\d[\d ,.]*|\bZAR\b|\$\d|\b\d+%/g),
      hasBar: !!document.querySelector(".webbar"),
      barLinks: [...document.querySelectorAll(".webbar a")].map(a => a.textContent.trim()),
      loxly: t.includes("Loxly Atkinson"),
      barend: t.includes("Barend Geldenhuys"),
      geoColon: t.includes("GEO: AI Search Visibility"),
      imgs: [...document.images].map(i => ({ src: i.src.split("/").pop(), ok: i.naturalWidth > 0 })),
      bodyScrollW: document.body.scrollWidth,
      clientW: document.documentElement.clientWidth,
    };
  });
  console.log("HTTP", resp.status(), JSON.stringify(r, null, 1));
  await p.screenshot({ path: "verify/live-desktop.png", clip: { x: 0, y: 0, width: 1280, height: 1000 } });

  // ---------- mobile ----------
  const m = await b.newPage();
  await m.setViewport({ width: 390, height: 844, isMobile: true, deviceScaleFactor: 2 });
  await m.goto(URL, { waitUntil: "networkidle0", timeout: 90000 });
  await m.evaluate(async () => { if (document.fonts?.ready) await document.fonts.ready; });
  const mm = await m.evaluate(() => ({
    scrollW: document.documentElement.scrollWidth,
    clientW: document.documentElement.clientWidth,
    fit: getComputedStyle(document.documentElement).getPropertyValue("--fit").trim(),
  }));
  console.log("MOBILE", JSON.stringify(mm));
  await m.screenshot({ path: "verify/live-mobile.png" });
} finally { await b.close(); }
