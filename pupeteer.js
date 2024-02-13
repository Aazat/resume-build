import puppeteer from  "puppeteer"

const  browser  = await puppeteer.launch({
headless:  false
});
const  page  = await browser.newPage();
await  page.goto('file:///E:/My%20Files/htmltopdf/exported_template.html');

// await  page.goto('file:///media/aazar/Ashu/My%20Files/htmltopdf/test.html');
//generate pdf
// await page.pdf({ path: 'page.pdf' });

//format pdf options
await  page.pdf({
	path: 'formatted.pdf',
	format: 'letter',
});

//close the browser
await browser.close()

// Chromium extracted to: C:\Users\Aazar\AppData\Local\pyppeteer\pyppeteer\local-chromium\588429


