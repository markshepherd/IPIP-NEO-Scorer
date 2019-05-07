const puppeteer = require('puppeteer');
// const { getTemplate, getDomain } = require('@alheimsins/b5-result-text');
// const $domain = getDomain({language: 'en', domain: 'A'});

/* eslint-disable no-console */

(async () => {
  console.log("1");
  const browser = await puppeteer.launch();
  console.log("2");
  const page = await browser.newPage();
  console.log("3");
  await page.goto('file:///Users/markshepherd/Temp/Figure0425_l.jpg', {waitUntil: 'networkidle2'});
  console.log("4");
  await page.pdf({path: 'hn.pdf', format: 'A4'});
  console.log("5");
  await browser.close();
  console.log("6");
})();


