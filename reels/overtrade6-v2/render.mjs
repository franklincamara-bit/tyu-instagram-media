// Uso (nesta pasta): node render.mjs meta42.html 36.8 video.mp4  (precisa do playwright); python3 mix42.py lê ../narr.mp3 e ../pen.json — ajuste os caminhos se rodar daqui.
// Renderiza uma página animada (window.renderAt(t)) quadro a quadro direto no ffmpeg.
// Uso: node render.mjs pagina.html duracao saida.mp4 [t_inicio] [t_fim]
//      node render.mjs pagina.html stills pasta t1,t2,t3   (quadros de conferência)
import { chromium } from 'playwright';
import { spawn } from 'child_process';
import fs from 'fs';
import path from 'path';

const [, , html, dur, out, a4, a5] = process.argv;
const FPS = 30, W = 1080, H = 1920;
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: W, height: H } });
await page.goto('file://' + path.resolve(html));
await page.evaluate(() => document.fonts.ready);
await page.waitForFunction(() => window.READY === true, null, { timeout: 30000 });

if (dur === 'stills') {
  fs.mkdirSync(out, { recursive: true });
  for (const t of a4.split(',').map(Number)) {
    await page.evaluate(t => window.renderAt(t), t);
    await page.screenshot({ path: `${out}/f_${t.toFixed(2)}.jpg`, type: 'jpeg', quality: 90 });
  }
  await browser.close();
  process.exit(0);
}

const D = Number(dur);
const t0 = a4 ? Number(a4) : 0, t1 = a5 ? Number(a5) : D;
const tmp = out.replace(/\.mp4$/, '.part.mp4');
const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-c:v', 'mjpeg', '-framerate', String(FPS), '-i', '-',
  '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-pix_fmt', 'yuv420p', '-r', String(FPS), tmp], { stdio: ['pipe', 'inherit', 'inherit'] });
const n0 = Math.round(t0 * FPS), n1 = Math.round(t1 * FPS);
for (let i = n0; i < n1; i++) {
  await page.evaluate(t => window.renderAt(t), i / FPS);
  const buf = await page.screenshot({ type: 'jpeg', quality: 92 });
  if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  if (i % 150 === 0) process.stdout.write(`${(i / FPS).toFixed(1)}s `);
}
ff.stdin.end();
const code = await new Promise(r => ff.on('close', r));
await browser.close();
if (code === 0) { fs.renameSync(tmp, out); console.log('\nok', out); } else { console.error('ffmpeg falhou', code); process.exit(1); }
