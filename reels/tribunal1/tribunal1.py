# Trial Reel "Tribunal do Trade #1: o stop móvel" (TYU-49) — motion design 1080x1920.
# Base visual: short60.py / short81_v2.py. Tempos das frases medidos com silencedetect na narração (narracao.mp3).
# Uso: python3 tribunal1.py <saida_sem_audio.mp4> [fps]  |  python3 tribunal1.py stills t1 t2 ...
import os, sys, json, asyncio, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
INTER = "/usr/share/fonts/opentype/inter"
LOGO = os.path.join(ROOT, "assets", "logo.png")
JUIZ = os.path.join(ROOT, "assets", "explicando.png")

# (legenda com algarismos, falado para pesar palavras, [ini, fim] medido)
PHRASES = [
    ("Tribunal do Trade.", "Tribunal do Trade.", [0.03, 1.15]),
    ("Réu:", "Réu:", [1.48, 1.79]),
    ("o stop que andou sozinho.", "o stop que andou sozinho.", [2.20, 3.78]),
    ("9h45:", "Nove e quarenta e cinco:", [4.33, 5.43]),
    ("o preço chega perto.", "o preço chega perto.", [5.70, 6.77]),
    ("O stop desce.", "O stop desce.", [7.09, 7.90]),
    ("9h50:", "Nove e cinquenta:", [8.34, 9.12]),
    ("desce de novo.", "desce de novo.", [9.38, 10.15]),
    ("10h00:", "Dez horas:", [10.57, 11.25]),
    ("desce mais uma vez.", "desce mais uma vez.", [11.51, 12.70]),
    ("Mas o trade voltou, Excelência.", "Mas o trade voltou, Excelência.", [12.97, 14.50]),
    ("Fechei no 0 a 0.", "Fechei no zero a zero.", [14.71, 15.67]),
    ("E na vez em que não voltar?", "E na vez em que não voltar?", [16.06, 17.22]),
    ("Culpado.", "Culpado.", [17.69, 18.27]),
    ("Mesmo quando dá certo.", "Mesmo quando dá certo.", [18.67, 19.89]),
    ("O stop é a decisão que você tomou com a cabeça fria.", "O stop é a decisão que você tomou com a cabeça fria.", [20.29, 22.99]),
    ("Próximo réu?", "Próximo réu?", [23.46, 24.11]),
    ("Comenta aí.", "Comenta aí.", [24.48, 25.09]),
]
# grupos de legenda (frases exibidas juntas); a frase 15 é dividida em duas linhas de leitura
GROUPS = [[0], [1, 2], [3, 4], [5], [6, 7], [8, 9], [10], [11], [12], [13], [14], [15], [16, 17]]
SPLIT15 = 6
KEY_RED = ["desce.", "desce", "Culpado.", "não", "sozinho."]
KEY_BLUE = ["cabeça", "fria.", "decisão"]
KEY_GREEN = ["voltou,"]
TAIL = 3.7


def words_and_groups():
    words, pw = [], []
    for cap, sp, (a, b) in PHRASES:
        toks, stoks = cap.split(), sp.split()
        pw.append(len(words))
        if len(toks) == len(stoks):
            wts = [len(s) + 1 for s in stoks]
        else:
            wts = [len(sp)] if len(toks) == 1 else [len(t) + 1 for t in toks]
        tot, acc = sum(wts), 0
        for w, k in zip(toks, wts):
            words.append([w, round(a + (b - a) * acc / tot, 3)]); acc += k
    groups = []
    for g in GROUPS:
        i0 = pw[g[0]]; i1 = pw[g[-1]] + len(PHRASES[g[-1]][0].split()) - 1
        if g == [15]:
            groups.append([i0, i0 + SPLIT15 - 1]); groups.append([i0 + SPLIT15, i1])
        else:
            groups.append([i0, i1])
    return words, groups, pw


HTML = r"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'InterD';src:url('file://__INTER__/InterDisplay-Black.otf');font-weight:900}
@font-face{font-family:'InterD';src:url('file://__INTER__/InterDisplay-Bold.otf');font-weight:700}
@font-face{font-family:'Inter';src:url('file://__INTER__/Inter-SemiBold.otf');font-weight:600}
@font-face{font-family:'Inter';src:url('file://__INTER__/Inter-Medium.otf');font-weight:500}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#EEF1F7;font-family:'InterD',sans-serif;color:#0B1533}
#bg{position:absolute;inset:-200px;background:
  radial-gradient(900px 900px at 78% 12%,rgba(37,99,235,.16),transparent 62%),
  radial-gradient(800px 800px at 10% 92%,rgba(229,72,77,.09),transparent 60%),
  linear-gradient(180deg,#F7F8FC 0%,#ECEFF6 100%)}
#floor{position:absolute;left:-1200px;width:3480px;top:980px;height:2600px;transform-origin:50% 0;
  background-image:linear-gradient(rgba(11,21,51,.07) 2px,transparent 2px),linear-gradient(90deg,rgba(11,21,51,.07) 2px,transparent 2px);
  background-size:120px 120px;-webkit-mask-image:linear-gradient(180deg,transparent 0%,#000 18%,#000 55%,transparent 100%)}
#world{position:absolute;inset:0;transform-origin:540px 860px}
.scene{position:absolute;inset:0;opacity:0;visibility:hidden;transform-origin:540px 860px}
#vig{position:absolute;inset:0;pointer-events:none;background:radial-gradient(1300px 1700px at 50% 45%,transparent 55%,rgba(11,21,51,.16) 100%)}
#grain{position:absolute;inset:0;width:1080px;height:1920px;mix-blend-mode:overlay;opacity:.10}
#top{position:absolute;left:64px;top:232px;display:flex;align-items:center;gap:18px;opacity:0}
#top .tag{font:600 26px 'Inter';letter-spacing:4px;background:rgba(255,255,255,.78);border:2px solid rgba(11,21,51,.08);padding:12px 20px;border-radius:999px;display:flex;align-items:center;gap:12px;box-shadow:0 8px 24px rgba(11,21,51,.06)}
#top .tag i{width:12px;height:12px;border-radius:50%;background:#E5484D;box-shadow:0 0 0 6px rgba(229,72,77,.15)}
#cap{position:absolute;left:60px;width:880px;top:1300px;display:flex;flex-wrap:wrap;justify-content:center;align-items:baseline;gap:6px 14px;
  font-family:'InterD';font-weight:900;font-size:66px;line-height:1.12;letter-spacing:-1px}
#cap span{position:relative;display:inline-block;padding:2px 10px;border-radius:16px;color:#0B1533;text-shadow:0 2px 0 rgba(255,255,255,.9),0 0 18px rgba(255,255,255,.9)}
.card{position:absolute;background:rgba(255,255,255,.95);border:2px solid rgba(11,21,51,.06);border-radius:44px;box-shadow:0 40px 90px rgba(11,21,51,.14)}
.hd{font:600 24px 'Inter';letter-spacing:4px;color:#7A8499}
/* tribunal: juiz + bancada (fixos em A, D, E) */
#court{position:absolute;inset:0;opacity:0;visibility:hidden}
#judge{position:absolute;left:310px;top:700px;width:460px;height:400px;overflow:hidden;transform-origin:230px 400px}
#judge img{position:absolute;left:0;top:0;width:460px;filter:drop-shadow(0 26px 30px rgba(11,21,51,.22))}
#bench{position:absolute;left:120px;top:1080px;width:840px;height:200px;border-radius:26px 26px 10px 10px;
  background:linear-gradient(180deg,#16224A 0%,#0B1533 60%,#081029 100%);box-shadow:0 40px 80px rgba(11,21,51,.35)}
#bench:before{content:'';position:absolute;left:0;right:0;top:0;height:18px;border-radius:26px 26px 0 0;background:linear-gradient(180deg,#2B3B6E,#16224A)}
#bench .pl{position:absolute;left:50%;top:70px;transform:translateX(-50%);font:600 22px 'Inter';letter-spacing:8px;color:rgba(255,255,255,.75);
  border:2px solid rgba(255,255,255,.22);border-radius:12px;padding:10px 22px;white-space:nowrap}
#bench .ln{position:absolute;left:40px;right:40px;top:44px;height:3px;background:#2563EB;opacity:.8;border-radius:3px}
#gavel{position:absolute;left:700px;top:880px;width:300px;height:196px;filter:drop-shadow(0 14px 18px rgba(11,21,51,.25))}
#block{position:absolute;left:760px;top:1062px;width:150px;height:26px;border-radius:10px;background:linear-gradient(180deg,#475569,#334155);box-shadow:0 10px 18px rgba(11,21,51,.3)}
#title{position:absolute;left:0;width:1080px;top:330px;text-align:center}
#title .l1{font:900 132px 'InterD';letter-spacing:-6px;line-height:.92;color:#0B1533;text-transform:uppercase;display:block}
#title .l2{font:900 132px 'InterD';letter-spacing:-6px;line-height:.92;color:#2563EB;text-transform:uppercase;display:block}
#sess{position:absolute;left:0;width:1080px;top:600px;text-align:center}
#sess b{display:inline-block;font:600 24px 'Inter';letter-spacing:6px;color:#fff;background:#0B1533;padding:12px 24px;border-radius:999px}
/* réu: o stop */
.reu{position:absolute;width:300px;height:140px}
.reu .body{position:absolute;inset:0;border-radius:70px;background:linear-gradient(180deg,#F05A5F,#D93A40);box-shadow:0 26px 44px rgba(217,58,64,.35), inset 0 -10px 0 rgba(0,0,0,.08)}
.reu .txt{position:absolute;left:0;right:0;bottom:16px;text-align:center;font:900 40px 'InterD';letter-spacing:4px;color:#fff}
.reu .eye{position:absolute;top:26px;width:44px;height:44px;border-radius:50%;background:#fff}
.reu .eye i{position:absolute;left:13px;top:13px;width:18px;height:18px;border-radius:50%;background:#0B1533}
.reu .lid{position:absolute;left:-2px;right:-2px;top:-2px;height:0;background:#E44A50;border-radius:22px 22px 0 0}
.reu .brow{position:absolute;top:14px;width:46px;height:8px;border-radius:6px;background:#7A1D21}
.reu .sweat{position:absolute;right:30px;top:-6px;width:22px;height:30px;border-radius:50% 50% 50% 50%/60% 60% 40% 40%;background:#9CC3FF;opacity:0}
.reu .leg{position:absolute;bottom:-34px;width:12px;height:38px;border-radius:6px;background:#0B1533}
.reu .tagn{position:absolute;left:50%;top:-58px;transform:translateX(-50%);font:600 22px 'Inter';letter-spacing:5px;color:#fff;background:#E5484D;padding:8px 16px;border-radius:999px;white-space:nowrap}
/* B: acusação (gráfico) */
#chart{left:70px;width:940px;top:360px;height:860px}
#chart .hd{position:absolute;left:48px;top:40px}
#risk{position:absolute;right:44px;top:26px;text-align:right}
#risk .k{font:600 20px 'Inter';letter-spacing:4px;color:#7A8499}
#risk .v{font:900 86px 'InterD';letter-spacing:-3px;color:#0B1533;line-height:1}
#clock{position:absolute;left:44px;top:84px;font:900 72px 'InterD';letter-spacing:-2px;color:#0B1533}
#clock small{font:600 22px 'Inter';letter-spacing:4px;color:#7A8499;margin-left:12px}
#selo{position:absolute;left:48px;bottom:30px;font:500 22px 'Inter';color:#8A93A6}
#ghostlbl{position:absolute;left:520px;top:700px;text-align:right;width:280px;font:900 52px 'InterD';color:#E5484D;opacity:0;white-space:nowrap}
#ghostlbl small{display:block;font:600 20px 'Inter';letter-spacing:4px;color:#E5484D;opacity:.8}
#jb{position:absolute;right:40px;top:150px;display:flex;align-items:center;gap:14px;opacity:0}
#jb .av{width:110px;height:110px;border-radius:50%;overflow:hidden;background:#E8EEFB;border:4px solid #fff;box-shadow:0 12px 28px rgba(11,21,51,.2);position:relative}
#jb .av img{position:absolute;width:330px;left:-105px;top:-8px}
#jb .bl{background:#0B1533;color:#fff;font:700 30px 'InterD';padding:16px 22px;border-radius:22px 22px 6px 22px;white-space:nowrap}
#rb{position:absolute;opacity:0;background:#fff;border:3px solid #E5484D;color:#E5484D;font:900 34px 'InterD';padding:12px 20px;border-radius:22px 22px 22px 6px;white-space:nowrap;box-shadow:0 14px 30px rgba(229,72,77,.18)}
#zero{position:absolute;opacity:0;font:900 30px 'InterD';color:#fff;background:#0B1533;padding:8px 16px;border-radius:14px;white-space:nowrap}
/* D: veredito */
#stamp{position:absolute;left:0;width:1080px;top:290px;text-align:center;opacity:0}
#stamp b{display:inline-block;font:900 128px 'InterD';letter-spacing:4px;color:#E5484D;border:12px solid #E5484D;border-radius:30px;padding:0 40px 10px;background:rgba(255,255,255,.7);transform:rotate(-6deg)}
#mesmo{position:absolute;left:0;width:1080px;top:520px;text-align:center;opacity:0}
#mesmo b{display:inline-block;font:900 44px 'InterD';color:#fff;background:#0B1533;padding:12px 26px 16px;border-radius:18px;letter-spacing:-.5px}
#rule{left:90px;width:900px;top:490px;height:170px;opacity:0;display:flex;flex-direction:column;justify-content:center;padding:0 46px}
#rule .a{font:700 36px 'InterD';color:#0B1533;letter-spacing:-.5px}
#rule .b{font:900 58px 'InterD';color:#E5484D;letter-spacing:-1.5px;margin-top:4px}
/* E: próximo réu */
#next{position:absolute;left:290px;top:380px;width:500px;height:230px;border-radius:115px;border:6px dashed #94A3B8;opacity:0;display:flex;align-items:center;justify-content:center}
#next b{font:900 180px 'InterD';color:#94A3B8;line-height:1}
#nexttag{position:absolute;left:0;width:1080px;top:640px;text-align:center;opacity:0}
#nexttag b{display:inline-block;font:900 52px 'InterD';color:#0B1533;letter-spacing:-1px}
#cbub{position:absolute;left:770px;top:330px;width:150px;height:110px;opacity:0}
/* F: final */
#F{background:#fff}
#F .logo{position:absolute;left:180px;top:540px;width:720px;height:270px;overflow:hidden}
#F .logo img{width:720px;display:block}
#F .logo .sh{position:absolute;top:-40px;bottom:-40px;width:160px;background:linear-gradient(100deg,transparent,rgba(255,255,255,.85),transparent);transform:skewX(-18deg)}
#F .q{position:absolute;left:90px;width:900px;top:900px;text-align:center;font:900 76px 'InterD';line-height:1.05;letter-spacing:-2px}
#F .u{position:absolute;left:0;width:1080px;top:1150px;text-align:center;font:700 36px 'InterD';color:#2563EB}
#F .d{position:absolute;left:0;width:1080px;top:1206px;text-align:center;font:500 24px 'Inter';color:#8A93A6;line-height:1.5}
</style></head><body>
<div id="bg"></div><div id="floor"></div>
<div id="world">
 <div id="court">
  <div id="title"><span class="l1">Tribunal</span><span class="l2">do Trade</span></div>
  <div id="sess"><b>SESSÃO Nº 1</b></div>
  <div id="stamp"><b>CULPADO</b></div>
  <div id="mesmo"><b>MESMO QUANDO DÁ CERTO</b></div>
  <div class="card" id="rule"><div class="a">Mover o stop contra a posição</div><div class="b">= falha de disciplina</div></div>
  <div id="next"><b>?</b></div>
  <div id="nexttag"><b>Próximo réu?</b></div>
  <svg id="cbub" viewBox="0 0 150 110"><path d="M20 6h110a16 16 0 0 1 16 16v50a16 16 0 0 1-16 16H62l-28 20 6-20H20A16 16 0 0 1 4 72V22A16 16 0 0 1 20 6z" fill="#2563EB"/>
   <circle id="d1" cx="48" cy="47" r="9" fill="#fff"/><circle id="d2" cx="75" cy="47" r="9" fill="#fff"/><circle id="d3" cx="102" cy="47" r="9" fill="#fff"/></svg>
  <div id="judge"><img src="file://__JUIZ__"></div>
  <div id="block"></div>
  <svg id="gavel" viewBox="0 0 260 170"><g id="gv" transform="rotate(0 230 120)">
   <rect x="96" y="108" width="140" height="16" rx="8" fill="#475569"/>
   <rect x="30" y="70" width="80" height="96" rx="16" fill="#334155"/>
   <rect x="30" y="86" width="80" height="10" fill="#2563EB"/><rect x="30" y="140" width="80" height="10" fill="#2563EB"/></g></svg>
  <div id="bench"><div class="ln"></div><div class="pl">EXCELENTÍSSIMO JUIZ</div></div>
 </div>
 <div class="reu" id="reuA">__REU__<div class="tagn">RÉU</div></div>
 <div class="scene" id="B">
  <div class="card" id="chart"><div class="hd">A ACUSAÇÃO</div>
   <div id="risk"><div class="k">RISCO DO TRADE</div><div class="v" id="riskv">1,0R</div></div>
   <div id="clock">9h45<small>HORÁRIO</small></div>
   <svg id="plot" width="940" height="860" style="position:absolute;left:0;top:0">
    <line x1="48" x2="892" y1="330" y2="330" stroke="#2563EB" stroke-width="4" stroke-dasharray="14 12"/>
    <text x="52" y="316" font-family="Inter" font-weight="600" font-size="20" letter-spacing="4" fill="#2563EB">ENTRADA</text>
    <line id="sl0" x1="48" x2="892" y1="460" y2="460" stroke="#E5484D" stroke-width="3" stroke-dasharray="6 10" opacity="0"/>
    <text id="sl0t" x="52" y="492" font-family="Inter" font-weight="600" font-size="20" letter-spacing="4" fill="#E5484D" opacity="0">STOP PLANEJADO · 1R</text>
    <rect id="zone" x="48" width="844" fill="#E5484D" opacity=".07"/>
    <line id="sl" x1="48" x2="700" y1="430" y2="430" stroke="#E5484D" stroke-width="7" stroke-linecap="round"/>
    <path id="gpath" fill="none" stroke="#E5484D" stroke-width="6" stroke-dasharray="4 14" stroke-linecap="round"/>
    <path id="parea" fill="url(#pg)"/>
    <defs><linearGradient id="pg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0B1533" stop-opacity=".10"/><stop offset="1" stop-color="#0B1533" stop-opacity="0"/></linearGradient></defs>
    <path id="pline" fill="none" stroke="#0B1533" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>
    <circle id="pdot" r="13" fill="#fff" stroke="#0B1533" stroke-width="7"/>
   </svg>
   <div class="reu" id="reuS" style="transform-origin:0 0">__REU__</div>
   <div id="rb">Voltou, Excelência!</div>
   <div id="zero">0 A 0</div>
   <div id="ghostlbl">−2,8R<small>E SE NÃO VOLTASSE?</small></div>
   <div id="jb"><div class="av"><img src="file://__JUIZ__"></div><div class="bl">E na vez em que não voltar?</div></div>
   <div id="selo">Exemplo ilustrativo · gráfico sem ativo · em R (múltiplos do risco)</div>
  </div>
 </div>
 <div class="scene" id="F">
  <div class="logo" id="logo"><img src="file://__LOGO__"><div class="sh" id="shine"></div></div>
  <div class="q" id="eq">Qual hábito vai a julgamento?</div>
  <div class="u" id="eu">tradeyouup.net</div>
  <div class="d" id="ed">Exemplo ilustrativo.<br>Conteúdo educativo. Não é recomendação de investimento.</div>
 </div>
</div>
<div id="vig"></div>
<div id="top"><div class="tag"><i></i>TRIBUNAL DO TRADE · Nº 1</div></div>
<div id="cap"></div>
<canvas id="grain" width="360" height="640"></canvas>
<script>
const W=__WORDS__, G=__GROUPS__, P=__PH__, PW=__PW__, KR=new Set(__KR__), KG=new Set(__KG__), KB=new Set(__KB__);
const SP=P[P.length-1][1]+0.2, END=SP+__TAIL__;
const $=id=>document.getElementById(id);
const cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)), lerp=(a,b,k)=>a+(b-a)*k, seg=(t,a,b)=>cl((t-a)/(b-a));
const eo=x=>1-Math.pow(1-cl(x),3), eio=x=>{x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2};
const eexp=x=>{x=cl(x);return x===1?1:1-Math.pow(2,-10*x)};
const spring=(x,f=1)=>{x=Math.max(0,x);return 1-Math.exp(-7*x)*Math.cos(10*f*x)};
function vis(el,o){el.style.opacity=o;el.style.visibility=o<=0.001?'hidden':'visible'}
const ph=i=>P[i], wa=(p,j)=>W[PW[p]+j][1];
const M={slam1:0.30, reu:ph(1)[0], reuIn:ph(1)[0]+0.05, bIn:ph(3)[0]-0.15, m1:ph(5)[0]+0.25, m2:ph(7)[0]+0.05, m3:ph(9)[0]+0.05,
 c945:ph(3)[0], c950:ph(6)[0], c1000:ph(8)[0], back:ph(10)[0], zero:ph(11)[0], ghost:ph(12)[0], dIn:ph(13)[0]-0.12, slam2:ph(13)[0],
 mesmo:ph(14)[0], rule:ph(15)[0], eIn:ph(16)[0]-0.1, com:ph(17)[0]};
window.M=M;
// grão
const gc=$('grain').getContext('2d'), gimg=gc.createImageData(360,640);
function grain(f){let s=f*7919+1;const d=gimg.data;for(let i=0;i<d.length;i+=4){s=(s*16807)%2147483647;const v=s%255;d[i]=d[i+1]=d[i+2]=v;d[i+3]=255}gc.putImageData(gimg,0,0)}
const HITS=[[M.slam1,18],[M.m1,10],[M.m2,10],[M.m3,12],[M.slam2,26]];
function shake(t){let x=0,y=0;HITS.forEach(([h,a],j)=>{const d=t-h;if(d>=0&&d<.5){const k=a*Math.exp(-9*d);x+=k*Math.sin(d*90+j);y+=k*Math.cos(d*77+j*2)}});return [x,y]}
// martelo: levanta e bate em h
function gavel(t){let a=0;[[M.slam1,0.35],[M.slam2,0.45]].forEach(([h,up])=>{if(t>h-up&&t<h){a=-38*Math.sin(Math.PI/2*seg(t,h-up,h-up*0.35))*(t<h-0.07?1:(h-t)/0.07)}
 else if(t>=h&&t<h+0.5){a=4*Math.exp(-10*(t-h))*Math.sin((t-h)*40)}});return a}
// réu (stop com rosto)
function face(root,t,mood){const eyes=root.querySelectorAll('.eye i'), lids=root.querySelectorAll('.lid'), brows=root.querySelectorAll('.brow');
 const lookX=mood.look??(Math.sin(t*1.3)*5), lookY=mood.lookY??0;
 eyes.forEach(e=>e.style.transform=`translate(${lookX}px,${lookY}px)`);
 const bl=((t*1.0)%3.1)<0.12?1:0; lids.forEach(l=>l.style.height=(bl?48:(mood.lid??0))+'px');
 brows.forEach((b,i)=>b.style.transform=`translateY(${mood.browY??0}px) rotate(${(i?-1:1)*(mood.brow??0)}deg)`);
 const sw=root.querySelector('.sweat'); sw.style.opacity=mood.sweat??0; sw.style.transform=`translateY(${((t*40)%30)}px)`;}
// gráfico: preço (y em px a partir da entrada; 1R = 100 px)
const ENT=330, X0=60, X1=700;
const RK=1.3;
function stopY(t){let y=100; if(t>=M.m1)y=lerp(100,160,eo(seg(t,M.m1,M.m1+.3))); if(t>=M.m2)y=lerp(160,220,eo(seg(t,M.m2,M.m2+.3))); if(t>=M.m3)y=lerp(220,280,eo(seg(t,M.m3,M.m3+.3))); return y*RK}
// trajetória do preço por tempo (pontos-chave), ruído determinístico por cima
const KP=[[ph(3)[0],-10],[ph(4)[1],88],[M.m1,92],[ph(6)[0],70],[ph(7)[0],148],[M.m2,150],[ph(8)[0],128],[ph(9)[0],210],[M.m3,212],[ph(9)[1],196],[ph(10)[0],200],[ph(10)[1]-.1,40],[ph(11)[0]+.2,0],[ph(11)[1]+2,0]];
function priceAt(t){if(t<=KP[0][0])return RK*KP[0][1];for(let i=1;i<KP.length;i++){if(t<=KP[i][0]){const k=eio((t-KP[i-1][0])/(KP[i][0]-KP[i-1][0]));return RK*lerp(KP[i-1][1],KP[i][1],k)}}return RK*KP[KP.length-1][1]}
const noise=t=>6*Math.sin(t*23.1)+4*Math.sin(t*41.7+1)+3*Math.sin(t*67.3+2);
const T0=ph(3)[0], T1=ph(11)[1];
const xAt=t=>X0+(X1-X0)*cl((t-T0)/(T1-T0));
function pathTo(t){let d='',last=null;const n=Math.max(2,Math.floor((Math.min(t,T1)-T0)/0.04));for(let i=0;i<=n;i++){const tt=T0+(Math.min(t,T1)-T0)*i/n;const y=ENT+priceAt(tt)+noise(tt)*(1-seg(tt,ph(11)[0],ph(11)[0]+.3));const x=xAt(tt);d+=(i?' L':'M')+x.toFixed(1)+','+y.toFixed(1);last=[x,y]}return [d,last]}
// legendas
const capEl=$('cap');let capG=-1,capSpans=[];
function buildCap(gi){capEl.innerHTML='';capSpans=[];const [a,b]=G[gi];for(let i=a;i<=b;i++){const s=document.createElement('span');s.textContent=W[i][0];capEl.appendChild(s);capSpans.push([i,s])}}
const fmtR=v=>v.toFixed(1).replace('.',',')+'R';

window.render=function(t,f){
 grain(Math.floor(f/2));
 const [sx,sy]=shake(t); $('world').style.transform=`translate(${sx}px,${sy}px)`;
 $('bg').style.transform=`translate(${Math.sin(t*.25)*30}px,${Math.cos(t*.2)*24}px) scale(${1.05+.03*Math.sin(t*.15)})`;
 $('floor').style.transform=`perspective(900px) rotateX(74deg) translateY(${(t*60)%120}px)`;
 vis($('top'),seg(t,.5,.9)*(1-seg(t,SP-.2,SP+.1)));
 // ---------- tribunal (A, D, E)
 const courtO=(1-seg(t,M.bIn-.15,M.bIn+.2))+seg(t,M.dIn-.1,M.dIn+.25)*(1-seg(t,SP-.1,SP+.2));
 vis($('court'),cl(courtO));
 {const outA=seg(t,M.bIn-.2,M.bIn+.2), inD=1-eexp(seg(t,M.dIn-.1,M.dIn+.4));
  $('court').style.transform=t<M.ghost?`translateX(${-1200*eio(outA)}px)`:`translateY(${inD*1300}px)`;
  $('court').style.filter=t<M.ghost?`blur(${Math.sin(Math.PI*outA)*12}px)`:`blur(${inD*10}px)`;
  // juiz: respira, balança; afunda no golpe; inclina no veredito
  const dip=[M.slam1,M.slam2].reduce((s,h)=>s+(t>h&&t<h+.5?10*Math.exp(-8*(t-h)):0),0);
  const lean=t>M.rule?eo(seg(t,M.rule,M.rule+.5))*(1-seg(t,M.eIn,M.eIn+.4)):0;
  const jin=spring((t-0.05)/0.9);
  $('judge').style.transform=`translateY(${(1-Math.min(1,jin))*260+Math.sin(t*1.7)*4+dip-lean*10}px) rotate(${Math.sin(t*.9)*1.1+(t>M.com?Math.sin((t-M.com)*6)*1.5*(1-seg(t,M.com+1,M.com+1.5)):0)}deg) scale(${1+.008*Math.sin(t*2.1)+lean*.04})`;
  $('gv').setAttribute('transform',`rotate(${gavel(t)} 230 116)`);
  $('bench').style.transform=`translateY(${(1-eexp(seg(t,0,.4)))*300}px)`;
  // título
  const tk=spring((t-0.1)/0.7); $('title').style.transform=`scale(${t<0.1?1.8:1.8-.8*Math.min(1.02,tk)})`; vis($('title'),(t>0.1?1:0)*(1-seg(t,M.dIn-.2,M.dIn)));
  $('title').style.filter=`blur(${cl(1-(t-0.1)/0.12)*10}px)`;
  const sk=eo(seg(t,0.7,1.0)); vis($('sess'),sk*(t<M.dIn?1:0)); $('sess').style.transform=`translateY(${(1-sk)*24}px)`;
  // veredito
  const st=spring((t-M.slam2)/0.6); vis($('stamp'),t>=M.slam2&&t<M.eIn?1:0); $('stamp').style.transform=`scale(${t<M.slam2?2.2:2.2-1.2*Math.min(1.02,st)})`;
  $('stamp').style.filter=`blur(${cl(1-(t-M.slam2)/0.1)*12}px)`;
  const mk=eo(seg(t,M.mesmo,M.mesmo+.35)); vis($('mesmo'),mk*(1-seg(t,M.rule-.25,M.rule))); $('mesmo').style.transform=`translateY(${(1-mk)*30}px)`;
  const rk=spring((t-M.rule)/0.8); vis($('rule'),seg(t,M.rule,M.rule+.15)*(1-seg(t,M.eIn-.2,M.eIn+.1))); $('rule').style.transform=`translateY(${(1-Math.min(1,rk))*80}px) rotateX(${(1-Math.min(1,rk))*30}deg)`;
  // próximo réu
  const nk=spring((t-M.eIn)/0.8); vis($('next'),t>M.eIn?1:0); $('next').style.transform=`scale(${Math.min(1.03,nk)}) rotate(${Math.sin(t*3)*2}deg)`;
  $('next').querySelector('b').style.transform=`translateY(${Math.sin(t*4)*8}px)`;
  const ntk=eo(seg(t,M.eIn+.2,M.eIn+.5)); vis($('nexttag'),ntk); $('nexttag').style.transform=`translateY(${(1-ntk)*24}px)`;
  const ck=spring((t-M.com)/0.6); vis($('cbub'),t>M.com?1:0); $('cbub').style.transform=`scale(${Math.min(1.05,ck)}) rotate(6deg)`;
  ['d1','d2','d3'].forEach((id,i)=>$(id).setAttribute('cy',47-6*Math.max(0,Math.sin((t-M.com)*8-i*0.9))));
 }
 // ---------- réu na abertura (entra em "Réu:")
 {const R=$('reuA'); const k=cl((t-M.reuIn)/0.45); const land=t>=M.reuIn+0.45; const out=seg(t,M.bIn-.25,M.bIn+.15);
  vis(R,(t>M.reuIn&&t<M.bIn+.2)?1:0);
  const y=-(1-k*k)*900, sq=land?1+0.18*Math.exp(-10*(t-M.reuIn-.45))*Math.cos((t-M.reuIn-.45)*20):1;
  R.style.left='90px'; R.style.top='900px'; R.style.transform=`translate(${-1200*eio(out)}px,${y}px) scale(${sq},${2-sq})`; R.style.transformOrigin='150px 140px';
  face(R,t,{look:land?Math.sin(t*2)*7:0, lookY:land?0:-6, brow:land?10:-6, sweat:land?seg(t,M.reuIn+1,M.reuIn+1.4):0});}
 // ---------- B: gráfico da acusação + defesa
 {const S=$('B'), inK=eexp(seg(t,M.bIn-.05,M.bIn+.4)), out=seg(t,M.dIn-.25,M.dIn+.1); vis(S,(t>M.bIn-.05&&t<M.dIn+.15)?1:0);
  S.style.transform=`translateX(${1300*(1-inK)}px) translateY(${-1500*eio(out)}px)`; S.style.filter=`blur(${Math.sin(Math.PI*seg(t,M.bIn-.05,M.bIn+.4))*14+Math.sin(Math.PI*out)*14}px)`;
  const sy=stopY(t), SY=ENT+sy;
  $('sl').setAttribute('y1',SY); $('sl').setAttribute('y2',SY);
  $('zone').setAttribute('y',ENT); $('zone').setAttribute('height',sy);
  const g0=seg(t,M.m1,M.m1+.3); $('sl0').setAttribute('opacity',g0); $('sl0t').setAttribute('opacity',g0);
  const [d,last]=pathTo(t); $('pline').setAttribute('d',d); $('parea').setAttribute('d',d+` L${last[0]},800 L${X0},760 Z`);
  $('pdot').setAttribute('cx',last[0]); $('pdot').setAttribute('cy',last[1]);
  // risco em R acompanha o stop
  const rv=sy/100/RK; $('riskv').textContent=fmtR(rv); $('riskv').style.color=rv>1.05?'#E5484D':'#0B1533';
  const rp=[M.m1,M.m2,M.m3].reduce((s,h)=>s+(t>h&&t<h+.5?Math.exp(-7*(t-h)):0),0); $('riskv').style.transform=`scale(${1+.18*rp})`; $('riskv').style.transformOrigin='100% 50%';
  // relógio
  const cv=t<M.c950?'9h45':t<M.c1000?'9h50':'10h00'; const ch=[M.c945,M.c950,M.c1000].reduce((s,h)=>s+(t>h&&t<h+.4?Math.exp(-9*(t-h)):0),0);
  $('clock').firstChild.textContent=cv; $('clock').style.transform=`translateY(${-ch*14}px)`; $('clock').style.opacity=t>M.back-.2?1-seg(t,M.back-.2,M.back+.1):1;
  // réu = rótulo do stop (anda junto com a linha)
  const R=$('reuS'); const walk=[M.m1,M.m2,M.m3].reduce((s,h)=>s+(t>h&&t<h+.3?Math.sin(Math.PI*(t-h)/.3):0),0);
  R.style.left='712px'; R.style.top=(SY-38)+'px'; R.style.transform=`scale(.55) rotate(${walk*8*Math.sin(t*30)}deg)`;
  const defense=t>M.back&&t<M.ghost, scared=t>=M.ghost;
  face(R,t,{look:defense?-8:(scared?-6:Math.sin(t*1.6)*6), lookY:scared?6:-4, brow:defense?-12:(scared?14:6), browY:defense?-4:0, sweat:(t>M.m2&&t<M.back)||scared?1:0, lid:scared?14:0});
  // balão do réu e 0 a 0
  const rbk=spring((t-M.back)/0.6); vis($('rb'),t>M.back&&t<M.ghost+.1?Math.min(1,rbk):0); $('rb').style.left='520px'; $('rb').style.top=(SY-110)+'px';
  $('rb').style.transform=`scale(${Math.min(1.03,rbk)})`; $('rb').style.transformOrigin='0 100%';
  const zk=spring((t-M.zero)/0.6); vis($('zero'),t>M.zero?1:0); $('zero').style.left=(X1-60)+'px'; $('zero').style.top=(ENT-96)+'px'; $('zero').style.transform=`scale(${Math.min(1.05,zk)})`;
  // E se não voltasse? caminho fantasma do ponto mais baixo atravessando o stop
  const gk=eio(seg(t,M.ghost+.1,M.ghost+.9)); const gx0=xAt(ph(10)[0]), gy0=ENT+200*RK;
  const gx1=lerp(gx0,gx0+220,gk), gy1=lerp(gy0,ENT+345*RK,gk);
  $('gpath').setAttribute('d',t>M.ghost?`M${gx0},${gy0} Q${gx0+60},${gy0+30} ${gx1},${gy1}`:'');
  const gl=eo(seg(t,M.ghost+.7,M.ghost+1.0)); $('ghostlbl').style.opacity=gl; $('ghostlbl').style.left=(gx0-300)+'px'; $('ghostlbl').style.top=(ENT+292*RK)+'px';
  $('ghostlbl').style.transform=`scale(${1+.06*Math.sin(t*9)*gl})`;
  const jk=spring((t-M.ghost)/0.7); vis($('jb'),t>M.ghost?Math.min(1,jk):0); $('jb').style.transform=`translateX(${(1-Math.min(1,jk))*200}px)`;
 }
 // ---------- F: final
 {const S=$('F'), k=seg(t,SP-.05,SP+.35); vis(S,t>SP-.06?eo(k):0);
  const lk=spring((t-SP-.05)/0.9); $('logo').style.transform=`scale(${t<SP?0.8:0.8+.2*Math.min(1.02,lk)})`; $('logo').style.opacity=seg(t,SP,SP+.25);
  $('shine').style.left=(-200+1100*eio(seg(t,SP+.6,SP+1.5)))+'px';
  [['eq',SP+.5],['eu',SP+.85],['ed',SP+1.0]].forEach(([id,a])=>{const kk=eo(seg(t,a,a+.45));$(id).style.opacity=kk;$(id).style.transform=`translateY(${(1-kk)*30}px)`});}
 // ---------- legendas
 let gi=-1; for(let i=0;i<G.length;i++){const s=W[G[i][0]][1]-0.12; const e=(i+1<G.length)?W[G[i+1][0]][1]-0.12:SP; if(t>=s&&t<e)gi=i}
 if(gi!==capG){capG=gi; if(gi>=0)buildCap(gi); else capEl.innerHTML=''}
 if(gi>=0){const gs=W[G[gi][0]][1]-0.12, gk=eo(seg(t,gs,gs+.18)); capEl.style.opacity=gk; capEl.style.transform=`translateY(${(1-gk)*24}px)`;
  capSpans.forEach(([i,s])=>{const w=W[i], on=t>=w[1]-0.04, act=on&&(i+1>G[gi][1]||t<W[i+1][1]-0.04);
   s.style.opacity=on?1:.22; const c=KR.has(w[0])?'#E5484D':KG.has(w[0])?'#16A34A':KB.has(w[0])?'#2563EB':null;
   if(act){const pk=spring((t-w[1]+0.04)/0.45); s.style.background=c||'#0B1533'; s.style.color='#fff'; s.style.textShadow='none';
    s.style.transform=`scale(${1+.08*Math.max(0,1-(t-w[1])/0.35)}) translateY(${-4*Math.min(1,pk)}px)`; s.style.boxShadow='0 10px 24px rgba(11,21,51,.22)';}
   else{s.style.background='transparent'; s.style.color=c||'#0B1533'; s.style.textShadow=''; s.style.transform='none'; s.style.boxShadow='none';}});}
 else capEl.style.opacity=0;
};
</script></body></html>"""

REU = ('<div class="body"></div><div class="leg" style="left:100px"></div><div class="leg" style="left:188px"></div>'
       '<div class="eye" style="left:90px"><i></i><div class="lid"></div></div><div class="eye" style="left:166px"><i></i><div class="lid"></div></div>'
       '<div class="brow" style="left:88px"></div><div class="brow" style="left:166px"></div><div class="sweat"></div><div class="txt">STOP</div>')


def build():
    words, groups, pw = words_and_groups()
    rep = {"__INTER__": INTER, "__LOGO__": LOGO, "__JUIZ__": JUIZ, "__REU__": REU,
           "__WORDS__": json.dumps(words, ensure_ascii=False), "__GROUPS__": json.dumps(groups), "__PW__": json.dumps(pw),
           "__PH__": json.dumps([p[2] for p in PHRASES]), "__KR__": json.dumps(KEY_RED, ensure_ascii=False),
           "__KG__": json.dumps(KEY_GREEN, ensure_ascii=False), "__KB__": json.dumps(KEY_BLUE, ensure_ascii=False), "__TAIL__": str(TAIL)}
    h = HTML
    for k, v in rep.items():
        h = h.replace(k, v)
    return h, PHRASES[-1][2][1] + 0.2 + TAIL


async def render(out, fps, stills=None):
    from playwright.async_api import async_playwright
    html, end = build()
    hp = os.path.join(HERE, "tribunal1.html"); open(hp, "w").write(html)
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--enable-gpu-rasterization", "--ignore-gpu-blocklist"])
        pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto("file://" + hp); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(600)
        if stills:
            os.makedirs(os.path.join(HERE, "stills"), exist_ok=True)
            for t in stills:
                await pg.evaluate("render(%f,%d)" % (t, int(t * fps)))
                await pg.screenshot(path=os.path.join(HERE, "stills", "st_%05.2f.jpg" % t), type="jpeg", quality=70)
            print("errors:", errs); await b.close(); return
        ff = subprocess.Popen(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(fps), "-c:v", "mjpeg", "-i", "-",
                               "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        for f in range(int(round(end * fps))):
            await pg.evaluate("render(%f,%d)" % (f / fps, f))
            ff.stdin.write(await pg.screenshot(type="jpeg", quality=95))
        print("errors:", errs); await b.close()
    ff.stdin.close(); ff.wait()


if __name__ == "__main__":
    if sys.argv[1] == "stills":
        asyncio.run(render(None, 60, [float(x) for x in sys.argv[2:]]))
    else:
        asyncio.run(render(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 60))
        print("ok", sys.argv[1])
