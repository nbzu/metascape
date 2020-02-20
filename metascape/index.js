const puppeteer = require('puppeteer');
 
(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto('http://metascape.org/gp/index.html#/main/step1');
  await page.pdf({path: 'output/hn.pdf', format: 'A4'});
 
  await browser.close();
})();