const puppeteer = require('puppeteer');

let page = null;
let input = null;
(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto('http://metascape.org/gp/index.html#/main/step1');

  await page.waitForSelector('#eq1').then(
        async el=>{
            await page.evaluate(() => {
                document.querySelector("#eq1").click();
            })
        }
    );

  await page.waitForXPath('//input[@type="file"]').then(
        async input=>{
            await input.uploadFile('input/metascape.csv')
            await input.evaluate(upload => {
                upload.dispatchEvent(new Event('change', { bubbles: true }))
            });
        }
    );

  await page.waitFor(60*1000)

  await page.waitForSelector('body > div:nth-child(3) > div > div:nth-child(1) > div.col-md-7.ng-scope > div > table > tbody > tr:nth-child(2) > td.info > div > table > tbody > tr:nth-child(1) > td:nth-child(2)',{visible: true}).then(
        async select=>{
            await select.click()
        }
    );
  await page.waitForSelector('body > div.k-animation-container > div > div.k-list-scroller > ul > li:nth-child(2)').then(
        async select=>{
            await select.click()
        }
    );
  await page.waitForSelector('#button-div > button:nth-child(1)').then(
        async select=>{
            await select.click()
        }
    );

  await page.waitFor(60*20*1000)
  await page.waitForSelector('body > div:nth-child(3) > div > div:nth-child(1) > div.col-md-7.ng-scope > div > table > tbody > tr:nth-child(3) > td.info > div:nth-child(2) > div:nth-child(2) > button',{visible: true}).then(
        async select=>{
            await select.click()
        }
    );
  await page.waitFor(10*1*1000)
  const pages = await browser.pages()
  const reportfinal = pages[pages.length - 1];

  await reportfinal._client.send('Page.setDownloadBehavior', {
        behavior: 'allow', 
        downloadPath: 'output'
    })

    await (await reportfinal.waitForSelector('body > div:nth-child(3) > div > div > div > div:nth-child(3) > a:nth-child(3)')).click();
    await reportfinal.waitFor(10*1000)
  
    await browser.close()
})();
