import puppeteer from "puppeteer";
const url = process.argv[2];
const out = process.argv[3];
const b = await puppeteer.launch({ headless: "new", args: ["--no-sandbox","--disable-setuid-sandbox"] });
try {
  const p = await b.newPage();
  await p.setViewport({ width: 1440, height: 1200, deviceScaleFactor: 1 });
  await p.goto(url, { waitUntil: "networkidle2", timeout: 90000 });
  await new Promise(r => setTimeout(r, 3500));
  const data = await p.evaluate(() => {
    const seen = new Map();
    const bump = (k, w) => { if (!k || k === "rgba(0, 0, 0, 0)" || k === "transparent") return; seen.set(k, (seen.get(k)||0) + w); };
    for (const el of document.querySelectorAll("body *")) {
      const r = el.getBoundingClientRect();
      if (r.width < 4 || r.height < 4) continue;
      const cs = getComputedStyle(el);
      bump("BG " + cs.backgroundColor, Math.round(r.width * r.height / 1000));
      if (el.children.length === 0 && el.textContent.trim()) bump("TEXT " + cs.color, 40);
      if (cs.backgroundImage && cs.backgroundImage.includes("gradient")) bump("GRAD " + cs.backgroundImage.slice(0,160), 60);
    }
    const btn = [...document.querySelectorAll("a,button")].filter(e => /book|call|contact|start|get|quote/i.test(e.textContent)).slice(0,6)
      .map(e => ({ text: e.textContent.trim().slice(0,40), bg: getComputedStyle(e).backgroundColor, color: getComputedStyle(e).color, bgImage: getComputedStyle(e).backgroundImage.slice(0,120) }));
    const h = [...document.querySelectorAll("h1,h2")].slice(0,8).map(e => ({ tag: e.tagName, text: e.textContent.trim().slice(0,90), color: getComputedStyle(e).color, font: getComputedStyle(e).fontFamily.slice(0,60), weight: getComputedStyle(e).fontWeight }));
    const nav = [...document.querySelectorAll("nav a, header a")].map(e => e.textContent.trim()).filter(Boolean).slice(0,40);
    const links = [...new Set([...document.querySelectorAll("a[href^='/'], a[href*='smartaisolutions']")].map(a => a.getAttribute("href")))].slice(0,80);
    return {
      bodyBg: getComputedStyle(document.body).backgroundColor,
      bodyColor: getComputedStyle(document.body).color,
      bodyFont: getComputedStyle(document.body).fontFamily,
      top: [...seen.entries()].sort((a,b) => b[1]-a[1]).slice(0,28),
      ctas: btn, headings: h, nav, links,
      title: document.title,
    };
  });
  await p.screenshot({ path: out + ".png", fullPage: false });
  await p.screenshot({ path: out + "-full.png", fullPage: true });
  console.log(JSON.stringify(data, null, 1));
} finally { await b.close(); }
