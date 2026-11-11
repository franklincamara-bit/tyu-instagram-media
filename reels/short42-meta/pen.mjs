import { chromium } from 'playwright'; import path from 'path'; import fs from 'fs';
const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+path.resolve(process.argv[2])); await p.waitForFunction(()=>window.READY===true);
fs.writeFileSync(process.argv[3], JSON.stringify(await p.evaluate(()=>window.penIntervals()))); await b.close();
