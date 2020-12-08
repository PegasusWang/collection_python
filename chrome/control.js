// npm i puppeteer
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto('https://www.qq.com');
  await page.screenshot({path: 'qq.png'});

  await browser.close();
})();
