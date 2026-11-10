# Reel "Overtrade: a curva das decisões" (TYU-62). Motion 1080x1920, ~25 s, sem narração (texto na tela + trilha).
# Teste de retenção (relatório 02–08/11): o erro no 1º segundo (o 6º trade entrando com pressa), depois a curva dos 6 trades.
# Base visual: ../caixa-preta1-v2/cp2.py. Uso: python3 ot.py <saida.mp4> [fps] | python3 ot.py stills t1 t2 ...
import os, sys, json, asyncio, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
INTER = "/usr/share/fonts/opentype/inter"
LOGO = os.path.join(HERE, "tpl", "logo.png")
END = 25.0
TR = [  # trades: hora, nota, qualidade da decisão (0..1), pressa (0..1)
    ["9h41", "plano completo", 0.95, 0.10],
    ["10h12", "quase no setup", 0.78, 0.25],
    ["10h40", "“pra recuperar”", 0.55, 0.45],
    ["11h05", "sem esperar o candle", 0.38, 0.62],
    ["11h31", "mão maior", 0.22, 0.80],
    ["11h52", "pressa", 0.06, 0.96],
]
T0, DT = 4.9, 1.6
M = dict(slam=0.12, t1=0.35, t2=1.35, rew=3.2, cIn=4.2, ev=[T0 + i * DT for i in range(6)], curve=T0 + 6 * DT + 0.1,
         dIn=15.3, d2=16.7, eIn=18.9, e2=19.9, fIn=21.6)

HTML = r"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'InterD';src:url('file://__INTER__/InterDisplay-Black.otf');font-weight:900}
@font-face{font-family:'InterD';src:url('file://__INTER__/InterDisplay-Bold.otf');font-weight:700}
@font-face{font-family:'Inter';src:url('file://__INTER__/Inter-SemiBold.otf');font-weight:600}
@font-face{font-family:'Inter';src:url('file://__INTER__/Inter-Medium.otf');font-weight:500}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#EEF1F7;font-family:'InterD',sans-serif;color:#0B1533}
#bg{position:absolute;inset:-200px;background:radial-gradient(900px 900px at 82% 8%,rgba(37,99,235,.17),transparent 62%),
  radial-gradient(800px 800px at 8% 92%,rgba(229,72,77,.10),transparent 60%),linear-gradient(180deg,#F7F8FC 0%,#ECEFF6 100%)}
#floor{position:absolute;left:-1200px;width:3480px;top:980px;height:2600px;transform-origin:50% 0;
  background-image:linear-gradient(rgba(11,21,51,.07) 2px,transparent 2px),linear-gradient(90deg,rgba(11,21,51,.07) 2px,transparent 2px);
  background-size:120px 120px;-webkit-mask-image:linear-gradient(180deg,transparent 0%,#000 18%,#000 55%,transparent 100%)}
#world{position:absolute;inset:0}
.scene{position:absolute;inset:0;opacity:0;visibility:hidden}
#vig{position:absolute;inset:0;pointer-events:none;background:radial-gradient(1300px 1700px at 50% 45%,transparent 55%,rgba(11,21,51,.16) 100%)}
#grain{position:absolute;inset:0;width:1080px;height:1920px;mix-blend-mode:overlay;opacity:.10}
#red{position:absolute;inset:0;background:radial-gradient(900px 1200px at 50% 40%,rgba(229,72,77,0),rgba(229,72,77,.22));opacity:0;pointer-events:none}
#top{position:absolute;left:64px;top:232px;display:flex;align-items:center;gap:14px;opacity:0}
.tag{font-family:'Inter';font-weight:600;font-size:26px;letter-spacing:4px;background:rgba(255,255,255,.85);border:2px solid rgba(11,21,51,.08);padding:12px 20px;border-radius:999px;display:flex;align-items:center;gap:12px;box-shadow:0 8px 24px rgba(11,21,51,.06)}
.tag i{width:12px;height:12px;border-radius:50%;background:#E5484D;box-shadow:0 0 0 6px rgba(229,72,77,.18)}
#note{position:absolute;left:64px;top:1236px;font:500 24px 'Inter';color:#7A8499;opacity:0}
.card{position:absolute;background:rgba(255,255,255,.97);border:2px solid rgba(11,21,51,.06);border-radius:44px;box-shadow:0 40px 90px rgba(11,21,51,.14)}
/* A: trade #6 */
#t6{left:90px;width:900px;top:430px;height:560px;border:6px solid #E5484D}
#t6 .hd{position:absolute;left:50px;top:44px;font:600 26px 'Inter';letter-spacing:5px;color:#E5484D}
#t6 .n{position:absolute;left:46px;top:96px;font:900 150px 'InterD';letter-spacing:-6px;line-height:1}
#t6 .clk{position:absolute;right:50px;top:50px;font:900 64px 'InterD';color:#E5484D;letter-spacing:-2px}
#t6 .tags{position:absolute;left:50px;right:50px;top:330px;display:flex;flex-wrap:wrap;gap:16px}
#t6 .tags b{font:900 44px 'InterD';color:#fff;padding:12px 24px 16px;border-radius:18px;opacity:0}
#hA{position:absolute;left:0;width:1080px;top:1100px;text-align:center}
#hA .a{font:900 110px 'InterD';letter-spacing:-4px;opacity:0;line-height:1}
#hA .b{font:900 64px 'InterD';letter-spacing:-2px;opacity:0;margin-top:20px}
#hA .b i{font-style:normal;background:#FFD43B;padding:2px 16px 8px;border-radius:18px}
/* rebobinar */
#rw{position:absolute;left:0;width:1080px;top:760px;text-align:center}
#rw b{display:inline-block;font:900 150px 'InterD';letter-spacing:-5px;color:#0B1533}
#rw small{display:block;font:600 30px 'Inter';letter-spacing:6px;color:#7A8499;margin-top:10px}
/* C: curva */
#cc{left:40px;width:1000px;top:330px;height:900px}
#cc .hd{position:absolute;left:46px;top:40px;font:600 24px 'Inter';letter-spacing:4px;color:#7A8499}
#cc .tt{position:absolute;left:44px;top:76px;font:900 60px 'InterD';letter-spacing:-2px}
#svg{position:absolute;left:20px;top:170px;width:960px;height:700px}
.lbl{font-family:'InterD';font-weight:900}
#cap{position:absolute;left:60px;width:960px;top:1300px;text-align:center;font:900 68px 'InterD';letter-spacing:-1px;line-height:1.12}
#cap .h{color:#2563EB}
/* D, E */
.big{position:absolute;left:70px;width:940px;text-align:center;font:900 96px 'InterD';letter-spacing:-3px;line-height:1.02;opacity:0}
.big i{font-style:normal;background:#FFD43B;padding:0 18px 8px;border-radius:24px}
.big.r i{background:#E5484D;color:#fff}
#E .lim{position:absolute;left:190px;width:700px;top:900px;height:200px;display:flex;gap:16px;justify-content:center;align-items:center}
#E .lim b{width:96px;height:150px;border-radius:22px;background:#2563EB;opacity:0;display:flex;align-items:center;justify-content:center;color:#fff;font:900 54px 'InterD'}
#E .lim b.x{background:#DDE3EE;color:#9AA3B5}
/* F */
#F{background:#fff}
#F .logo{position:absolute;left:180px;top:540px;width:720px;height:270px;overflow:hidden}
#F .logo img{width:720px;display:block}
#F .q{position:absolute;left:90px;width:900px;top:900px;text-align:center;font:900 72px 'InterD';line-height:1.05;letter-spacing:-2px}
#F .u{position:absolute;left:0;width:1080px;top:1110px;text-align:center;font:700 36px 'InterD';color:#2563EB}
#F .d{position:absolute;left:0;width:1080px;top:1166px;text-align:center;font:500 24px 'Inter';color:#8A93A6;line-height:1.5}
</style></head><body>
<div id="bg"></div><div id="floor"></div>
<div id="world">
 <div class="scene" id="A">
  <div class="card" id="t6"><div class="hd">O DIA DO TRADER</div><div class="clk">11h52</div><div class="n">Trade #6</div>
   <div class="tags"><b id="g1" style="background:#E5484D">sem setup</b><b id="g2" style="background:#F59E0B">entrou com pressa</b><b id="g3" style="background:#0B1533">mão 2×</b></div></div>
  <div id="hA"><div class="a" id="a1">6 trades.</div><div class="b" id="a2">Só o <i>primeiro</i> tinha plano.</div></div>
 </div>
 <div class="scene" id="R"><div id="rw"><b id="rwc">11:52</b><small>VOLTANDO NO TEMPO</small></div></div>
 <div class="scene" id="C">
  <div class="card" id="cc"><div class="hd">A CURVA DAS DECISÕES</div><div class="tt" id="ctt">6 trades, 1 dia</div>
   <svg id="svg" viewBox="0 0 960 700">
    <line x1="60" x2="920" y1="560" y2="560" stroke="#DDE3EE" stroke-width="4"/>
    <g id="leg"><circle cx="70" cy="22" r="10" fill="#2563EB"/><text x="90" y="31" class="lbl" font-size="26" fill="#2563EB">QUALIDADE DA DECISÃO</text>
     <line x1="520" x2="560" y1="22" y2="22" stroke="#E5484D" stroke-width="6" stroke-dasharray="10 7"/><text x="572" y="31" class="lbl" font-size="26" fill="#E5484D">PRESSA</text></g>
    <polyline id="pq" fill="none" stroke="#2563EB" stroke-width="9" stroke-linejoin="round" stroke-linecap="round"/>
    <polyline id="pp" fill="none" stroke="#E5484D" stroke-width="6" stroke-dasharray="14 10" stroke-linejoin="round"/>
    <g id="dots"></g><g id="xl"></g>
    <path id="arr" d="" fill="none" stroke="#FFD43B" stroke-width="14" stroke-linecap="round" opacity="0"/>
   </svg>
  </div>
 </div>
 <div class="scene" id="D"><div class="big" id="q1" style="top:560px">O problema não foi o <i>6º trade</i>.</div><div class="big r" id="q2" style="top:880px">Foi a <i>curva</i> até ele.</div></div>
 <div class="scene" id="E"><div class="big" id="e1" style="top:470px;font-size:84px">Antes do pregão, defina: <i>quantos trades</i> cabem no seu plano.</div>
  <div class="lim"><b>1</b><b>2</b><b>3</b><b class="x">4</b><b class="x">5</b><b class="x">6</b></div></div>
 <div class="scene" id="F">
  <div class="logo" id="logo"><img src="file://__LOGO__"></div>
  <div class="q" id="eq">O overtrade começa antes do 6º trade.</div>
  <div class="u" id="eu">tradeyouup.net</div>
  <div class="d" id="ed">Exemplo ilustrativo · conta demo · sem ativo e sem resultados.<br>Conteúdo educativo. Não é recomendação de investimento.</div>
 </div>
</div>
<div id="red"></div><div id="vig"></div>
<div id="top"><div class="tag"><i></i>OVERTRADE</div></div>
<div id="note">Exemplo ilustrativo · conta demo</div>
<div id="cap"></div>
<canvas id="grain" width="360" height="640"></canvas>
<script>
const M=__M__, TR=__TR__, END=__END__;
const $=id=>document.getElementById(id);
const cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)), lerp=(a,b,k)=>a+(b-a)*k, seg=(t,a,b)=>cl((t-a)/(b-a));
const eo=x=>1-Math.pow(1-cl(x),3), eio=x=>{x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2};
const eexp=x=>{x=cl(x);return x===1?1:1-Math.pow(2,-10*x)};
const spring=(x,f=1)=>{x=Math.max(0,x);return 1-Math.exp(-7*x)*Math.cos(10*f*x)};
const pop=(t,a,d=.5)=>t<a?0:Math.min(1.08,spring((t-a)/d));
function vis(el,o){el.style.opacity=o;el.style.visibility=o<=0.001?'hidden':'visible'}
function inScene(id,a,b,t){const S=$(id),on=t>a&&t<b;vis(S,on?1:0);return on}
const gc=$('grain').getContext('2d'), gimg=gc.createImageData(360,640);
function grain(f){let s=f*7919+1;const d=gimg.data;for(let i=0;i<d.length;i+=4){s=(s*16807)%2147483647;const v=s%255;d[i]=d[i+1]=d[i+2]=v;d[i+3]=255}gc.putImageData(gimg,0,0)}
const HITS=[[M.slam,22],[M.t1,8],[M.ev[5],14],[M.dIn+1.4,10],[M.d2,12]];
function shake(t){let x=0,y=0;HITS.forEach(([h,a],j)=>{const d=t-h;if(d>=0&&d<.5){const k=a*Math.exp(-9*d);x+=k*Math.sin(d*90+j);y+=k*Math.cos(d*77+j*2)}});return [x,y]}
const X=i=>120+i*150, YQ=q=>540-q*420;
{let h='',x='';TR.forEach((r,i)=>{h+=`<g id="d${i}" opacity="0"><circle cx="${X(i)}" cy="${YQ(r[2])}" r="20" fill="#fff" stroke="#2563EB" stroke-width="8"/></g>`;
 x+=`<g id="x${i}" opacity="0"><text x="${X(i)}" y="600" text-anchor="middle" class="lbl" font-size="30" fill="#0B1533">#${i+1}</text><text x="${X(i)}" y="636" text-anchor="middle" class="lbl" font-size="24" fill="#7A8499">${r[0]}</text></g>`});
 $('dots').innerHTML=h; $('xl').innerHTML=x;}
const capEl=$('cap');
window.render=function(t,f){
 grain(Math.floor(f/2));
 const [sx,sy]=shake(t); $('world').style.transform=`translate(${sx}px,${sy}px)`;
 $('bg').style.transform=`translate(${Math.sin(t*.25)*30}px,${Math.cos(t*.2)*24}px) scale(${1.05+.03*Math.sin(t*.15)})`;
 $('floor').style.transform=`perspective(900px) rotateX(74deg) translateY(${(t*40)%120}px)`;
 vis($('top'),seg(t,M.rew,M.rew+.4)*(1-seg(t,M.fIn-.2,M.fIn+.1)));
 vis($('note'),seg(t,M.cIn+.3,M.cIn+.7)*(1-seg(t,M.dIn-.3,M.dIn)));
 $('red').style.opacity=(t<M.rew?.9*eo(seg(t,M.slam,M.slam+.2))*(1-seg(t,M.rew-.3,M.rew)):0)+(t>M.ev[5]&&t<M.dIn?.6*Math.exp(-3*(t-M.ev[5])):0);
 let cap='';
 // A: trade #6 no 1º segundo
 if(inScene('A',-1,M.rew+.2,t)){const S=$('A'); const out=seg(t,M.rew-.15,M.rew+.15);
  S.style.transform=`scale(${1-.35*eio(out)})`; S.style.filter=`blur(${10*out}px)`; S.style.opacity=1-eo(out);
  const k=t<M.slam?0:Math.min(1.04,spring((t-M.slam)/.45)); $('t6').style.transform=`scale(${2.2-1.2*k}) rotate(${-3*(1-Math.min(1,k))}deg)`; $('t6').style.opacity=cl((t-M.slam)/.06);
  [['g1',.45],['g2',.75],['g3',1.05]].forEach(([id,a])=>{$(id).style.opacity=cl((t-a)/.08);$(id).style.transform=`scale(${pop(t,a,.4)})`});
  $('a1').style.opacity=cl((t-M.t1)/.1); $('a1').style.transform=`scale(${t<M.t1?1.6:1.6-.6*Math.min(1.03,spring((t-M.t1)/.5))})`;
  $('a2').style.opacity=cl((t-M.t2)/.12); $('a2').style.transform=`translateY(${(1-eo(seg(t,M.t2,M.t2+.4)))*40}px)`;}
 // rebobinar 11:52 -> 09:41
 if(inScene('R',M.rew-.05,M.cIn+.2,t)){const k=eio(seg(t,M.rew,M.cIn-.15)); const m0=11*60+52, m1=9*60+41, m=Math.round(lerp(m0,m1,k));
  $('rwc').textContent=String(Math.floor(m/60)).padStart(2,'0')+':'+String(m%60).padStart(2,'0');
  $('R').style.opacity=seg(t,M.rew-.05,M.rew+.15)*(1-seg(t,M.cIn-.1,M.cIn+.2)); $('rw').style.transform=`rotate(${Math.sin(t*40)*1.2}deg)`;}
 // C: a curva
 if(inScene('C',M.cIn-.1,M.dIn+.2,t)){const S=$('C'); const ik=eexp(seg(t,M.cIn-.1,M.cIn+.35)), out=seg(t,M.dIn-.2,M.dIn+.15);
  S.style.transform=`translateY(${(1-ik)*1500-eio(out)*1600}px)`; S.style.filter=`blur(${Math.sin(Math.PI*out)*14}px)`;
  let cur=-1; M.ev.forEach((a,i)=>{if(t>=a)cur=i});
  const qp=[],pp=[];
  TR.forEach((r,i)=>{const a=M.ev[i]; $('d'+i).setAttribute('opacity',t>=a?1:0); $('x'+i).setAttribute('opacity',cl((t-a)/.15));
   const c=$('d'+i).querySelector('circle'); const s=t<a?0:Math.min(1.2,spring((t-a)/.5)); c.setAttribute('r',20*s); c.setAttribute('stroke',r[2]<.4?'#E5484D':(r[2]<.7?'#F59E0B':'#2563EB'));
   if(t>=a-.6){const k=i==0?1:eo(seg(t,a-.6,a)); const px=i==0?X(0):lerp(X(i-1),X(i),k);
    qp.push(px+','+(i==0?YQ(r[2]):lerp(YQ(TR[i-1][2]),YQ(r[2]),k)).toFixed(1)); pp.push(px+','+(i==0?YQ(r[3]):lerp(YQ(TR[i-1][3]),YQ(r[3]),k)).toFixed(1));}});
  $('pq').setAttribute('points',qp.join(' ')); $('pp').setAttribute('points',pp.join(' '));
  $('ctt').textContent=cur<0?'6 trades, 1 dia':('#'+(cur+1)+' · '+TR[cur][0]);
  $('ctt').style.color=cur>=0&&TR[cur][2]<.4?'#E5484D':'#0B1533';
  const ak=eio(seg(t,M.curve,M.curve+.7)); $('arr').setAttribute('opacity',t>M.curve?.85:0);
  const x0=X(0)+10,y0=YQ(TR[0][2])-40,x1=lerp(x0,X(5)-10,ak),y1=lerp(y0,YQ(TR[5][2])-40,ak); $('arr').setAttribute('d',`M${x0},${y0} L${x1},${y1}`);
  if(cur>=0) cap=TR[cur][1]; if(t>M.curve) cap='a curva das decisões';
  if(t<M.ev[0]) cap='';}
 // D
 if(inScene('D',M.dIn-.1,M.eIn+.2,t)){const S=$('D'); const out=seg(t,M.eIn-.2,M.eIn+.15); S.style.opacity=1-out;
  $('q1').style.opacity=cl((t-M.dIn)/.12); $('q1').style.transform=`translateY(${(1-eo(seg(t,M.dIn,M.dIn+.45)))*50}px)`;
  $('q2').style.opacity=cl((t-M.d2)/.1); $('q2').style.transform=`scale(${t<M.d2?1.5:1.5-.5*Math.min(1.03,spring((t-M.d2)/.6))})`;}
 // E
 if(inScene('E',M.eIn-.1,M.fIn+.2,t)){const S=$('E'); const out=seg(t,M.fIn-.15,M.fIn+.15); S.style.opacity=1-out;
  $('e1').style.opacity=cl((t-M.eIn)/.12); $('e1').style.transform=`translateY(${(1-eo(seg(t,M.eIn,M.eIn+.45)))*50}px)`;
  [...document.querySelectorAll('#E .lim b')].forEach((b,i)=>{const a=M.e2+i*.18; b.style.opacity=cl((t-a)/.1)*(i>=3?.9:1); b.style.transform=`translateY(${(1-Math.min(1,spring((t-a)/.5)))*80}px)`});}
 // F
 {const k=seg(t,M.fIn-.05,M.fIn+.35); vis($('F'),t>M.fIn-.06?eo(k):0);
  $('logo').style.transform=`scale(${t<M.fIn?0.8:0.8+.2*Math.min(1.02,spring((t-M.fIn-.05)/0.9))})`; $('logo').style.opacity=seg(t,M.fIn,M.fIn+.25);
  [['eq',M.fIn+.5],['eu',M.fIn+.85],['ed',M.fIn+1.0]].forEach(([id,a])=>{const kk=eo(seg(t,a,a+.45));$(id).style.opacity=kk;$(id).style.transform=`translateY(${(1-kk)*30}px)`});}
 if(capEl.dataset.v!==cap){capEl.dataset.v=cap; capEl.textContent=cap; capEl.dataset.t=t}
 const ct=parseFloat(capEl.dataset.t||0); capEl.style.opacity=cap?eo(seg(t,ct,ct+.2)):0; capEl.style.transform=`translateY(${(1-eo(seg(t,ct,ct+.2)))*24}px)`;
 capEl.style.color=(cap&&TR.findIndex(r=>r[1]===cap)>=2)?'#E5484D':'#0B1533';
};
</script></body></html>"""


def build():
    rep = {"__INTER__": INTER, "__LOGO__": LOGO, "__M__": json.dumps(M), "__TR__": json.dumps(TR, ensure_ascii=False), "__END__": str(END)}
    h = HTML
    for k, v in rep.items(): h = h.replace(k, v)
    return h


async def render(out, fps, stills=None):
    from playwright.async_api import async_playwright
    hp = os.path.join(HERE, "ot.html"); open(hp, "w").write(build())
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto("file://" + hp); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(600)
        if stills:
            os.makedirs(os.path.join(HERE, "stills"), exist_ok=True)
            for t in stills:
                await pg.evaluate("render(%f,%d)" % (t, int(t * fps)))
                await pg.screenshot(path=os.path.join(HERE, "stills", "st_%05.2f.jpg" % t), type="jpeg", quality=80)
            print("errors:", errs); await b.close(); return
        ff = subprocess.Popen(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(fps), "-c:v", "mjpeg", "-i", "-",
                               "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        for f in range(0, int(round(END * fps))):
            await pg.evaluate("render(%f,%d)" % (f / fps, f))
            ff.stdin.write(await pg.screenshot(type="jpeg", quality=93))
        print("errors:", errs); await b.close()
    ff.stdin.close(); ff.wait()


if __name__ == "__main__":
    if sys.argv[1] == "stills":
        asyncio.run(render(None, 30, [float(x) for x in sys.argv[2:]]))
    else:
        fps = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        asyncio.run(render(sys.argv[1], fps)); print("ok", sys.argv[1])
