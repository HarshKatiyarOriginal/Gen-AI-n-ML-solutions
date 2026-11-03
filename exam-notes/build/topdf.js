// Render the notebook HTML to an A4 PDF with page numbers.
// Usage: node topdf.js input.html output.pdf
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const [input, output] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(input), { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({
    path: output,
    format: 'A4',
    printBackground: false,
    displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate:
      '<div style="font-size:8px;width:100%;text-align:center;font-family:serif;">' +
      'Page <span class="pageNumber"></span> of <span class="totalPages"></span></div>',
    margin: { top: '16mm', bottom: '18mm', left: '15mm', right: '15mm' },
  });
  await browser.close();
})();
