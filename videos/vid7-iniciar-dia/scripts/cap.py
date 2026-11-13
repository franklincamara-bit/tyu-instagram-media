import json, asyncio, sys
from pathlib import Path
from playwright.async_api import async_playwright
CLEAN = """
document.querySelectorAll('[role=dialog]').forEach(d=>{ d.remove(); });
document.querySelectorAll('div').forEach(e=>{const s=getComputedStyle(e); if(s.position==='fixed' && s.inset==='0px' && (e.className+'').match(/bg-black|backdrop/)) e.remove();});
// esconde e-mail/nome do rodapé do menu
[...document.querySelectorAll('*')].filter(e=>e.children.length===0 && /@|^F$|camara/i.test(e.textContent)).forEach(e=>{e.style.filter='blur(5px)';});
document.querySelectorAll('[data-sonner-toaster]').forEach(e=>e.remove());
"""
BOXJS = """
(args)=>{ const [q, mode] = args;
  const els=[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect(); if(r.width<2||r.height<2) return false;
     const t=((e.tagName==='INPUT'?e.value:e.innerText)||'').trim(); return mode==='exact'? t===q : t.includes(q);});
  els.sort((a,b)=>{const ra=a.getBoundingClientRect(), rb=b.getBoundingClientRect(); return ra.width*ra.height-rb.width*rb.height;});
  const e=els[0]; if(!e) return null; const r=e.getBoundingClientRect(); return [r.left,r.top,r.right,r.bottom]; }
"""
async def main(spec):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width':1280,'height':800}, device_scale_factor=2)
        res = {}
        for name, s in spec.items():
            await pg.goto(Path(f"snaps/{s['snap']}.html").resolve().as_uri(), wait_until='networkidle', timeout=60000)
            await pg.wait_for_timeout(500)
            await pg.evaluate(CLEAN)
            if s.get('js'): await pg.evaluate(s['js'])
            if s.get('scroll'):
                await pg.evaluate("""(q)=>{const els=[...document.querySelectorAll('body *')].filter(e=>(e.innerText||'').trim().startsWith(q)); els.sort((a,b)=>a.innerText.length-b.innerText.length); const e=els[0]; if(e){ const r=e.getBoundingClientRect(); window.scrollTo(0, window.scrollY + r.top - %d);} }""" % s.get('top',90), s['scroll'])
            await pg.evaluate('window.__fix && window.__fix()')
            await pg.wait_for_timeout(300)
            boxes = {}
            for k, q in s.get('boxes', {}).items():
                mode = 'exact'
                if isinstance(q, list): q, mode = q
                boxes[k] = await pg.evaluate(BOXJS, [q, mode])
            await pg.screenshot(path=f"up/{name}.png")
            res[name] = boxes
            print(name, boxes, flush=True)
        await b.close()
    json.dump(res, open('boxes.json','w'), indent=1, ensure_ascii=False)
spec = json.load(open(sys.argv[1]))
asyncio.run(main(spec))
