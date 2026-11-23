# Short "No lucro e reprovado? A linha que sobe com o seu pico" (VID-44) — motion design 1080x1920, série MESA PROPRIETÁRIA SEM ROMANCE.
# Base visual: short43.py (padrão Short 81% v2). Tempos das palavras vêm de whisper_words.json (faster-whisper sobre narr.mp3).
# Uso: python3 short44.py <saida_sem_audio.mp4> [fps]  |  python3 short44.py stills t1 t2 ...  |  python3 short44.py info
import os, sys, json, asyncio, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
INTER = "/usr/share/fonts/opentype/inter"
LOGO = os.path.join(ROOT, "assets", "logo.png")
AV = {k: os.path.join(ROOT, "assets", k + ".png") for k in ("pensativo", "explicando", "joinha", "cansado")}
TAIL = 3.6

KEY_RED = {"limite", "linha", "encerrada.", "devolução", "desce", "Limite", "perda", "volta."}
KEY_GREEN = {"lucro.", "53", "bem"}
KEY_BLUE = {"pico.", "pico", "Pico", "conta:", "espaço", "regras", "verdade"}


def load_words():
    raw = json.load(open(os.path.join(HERE, "whisper_words.json")))
    rep = {"que": "que,", "mesas": "mesas,", "parado.": "parado:", "normal.": "normal:", "Saldo,": "Saldo:",
           "conta.": "conta:", "Pico": "Pico", "limite.": "limite."}
    out = []
    for i, (w, a, b) in enumerate(raw):
        x = w
        if w == "seu" and raw[i - 1][0] != "com": x = w
        elif w in rep: x = rep[w]
        out.append([x, a, b])
    return out


def groups(words):
    gs, cur = [], []
    for i, (w, a, b) in enumerate(words):
        cur.append(i)
        end = w.endswith((".", "?", ":")) or (w.endswith(",") and len(cur) >= 4)
        if end or len(cur) >= 6:
            gs.append([cur[0], cur[-1]]); cur = []
    if cur: gs.append([cur[0], cur[-1]])
    return gs


HTML = r"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'InterD';src:url('file://__INTER__/InterDisplay-Black.otf');font-weight:900}
@font-face{font-family:'InterD';src:url('file://__INTER__/InterDisplay-Bold.otf');font-weight:700}
@font-face{font-family:'Inter';src:url('file://__INTER__/Inter-SemiBold.otf');font-weight:600}
@font-face{font-family:'Inter';src:url('file://__INTER__/Inter-Medium.otf');font-weight:500}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#EEF1F7;font-family:'InterD',sans-serif;color:#0B1533}
#bg{position:absolute;inset:-200px;background:
  radial-gradient(900px 900px at 78% 12%,rgba(37,99,235,.16),transparent 62%),
  radial-gradient(800px 800px at 10% 92%,rgba(229,72,77,.08),transparent 60%),
  linear-gradient(180deg,#F7F8FC 0%,#ECEFF6 100%)}
#floor{position:absolute;left:-1200px;width:3480px;top:980px;height:2600px;transform-origin:50% 0;
  background-image:linear-gradient(rgba(11,21,51,.07) 2px,transparent 2px),linear-gradient(90deg,rgba(11,21,51,.07) 2px,transparent 2px);
  background-size:120px 120px;-webkit-mask-image:linear-gradient(180deg,transparent 0%,#000 18%,#000 55%,transparent 100%)}
#world{position:absolute;inset:0}
.scene{position:absolute;inset:0;opacity:0;visibility:hidden;transform-origin:540px 860px}
#vig{position:absolute;inset:0;pointer-events:none;background:radial-gradient(1300px 1700px at 50% 45%,transparent 55%,rgba(11,21,51,.16) 100%)}
#grain{position:absolute;inset:0;width:1080px;height:1920px;mix-blend-mode:overlay;opacity:.10}
#top{position:absolute;left:64px;top:232px;display:flex;align-items:center;gap:18px;opacity:0}
#top .tag{font-family:'Inter';font-weight:600;font-size:26px;letter-spacing:4px;background:rgba(255,255,255,.75);border:2px solid rgba(11,21,51,.08);padding:12px 20px;border-radius:999px;display:flex;align-items:center;gap:12px;box-shadow:0 8px 24px rgba(11,21,51,.06)}
#top .tag i{width:12px;height:12px;border-radius:50%;background:#2563EB;box-shadow:0 0 0 6px rgba(37,99,235,.15)}
#prog{position:absolute;left:64px;top:300px;display:flex;gap:8px;opacity:0}
#prog b{display:block;width:70px;height:6px;border-radius:6px;background:rgba(11,21,51,.10);overflow:hidden}
#prog b i{display:block;height:100%;width:0;background:#0B1533;border-radius:6px}
#note{position:absolute;left:64px;top:1236px;font:500 24px 'Inter';color:#7A8499;opacity:0}
#cap{position:absolute;left:60px;width:880px;top:1300px;display:flex;flex-wrap:wrap;justify-content:center;align-items:baseline;gap:6px 14px;
  font-family:'InterD';font-weight:900;font-size:68px;line-height:1.12;letter-spacing:-1px}
#cap span{position:relative;display:inline-block;padding:2px 10px;border-radius:16px;color:#0B1533;text-shadow:0 2px 0 rgba(255,255,255,.9),0 0 18px rgba(255,255,255,.9)}
.card{position:absolute;background:rgba(255,255,255,.95);border:2px solid rgba(11,21,51,.06);border-radius:44px;box-shadow:0 40px 90px rgba(11,21,51,.14)}
.hd{font:600 24px 'Inter';letter-spacing:4px;color:#7A8499}
/* HOOK */
#H{z-index:5}
#Hs{position:absolute;inset:0;background:rgba(7,17,52,.82)}
#Hq{position:absolute;left:0;right:0;top:470px;text-align:center;font:900 104px 'InterD';color:#fff;letter-spacing:-3px;line-height:1}
#Hq em{font-style:normal;color:#FFD43B}
#Hst{position:absolute;left:150px;top:640px;font:900 92px 'InterD';color:#fff;background:#E5484D;padding:10px 34px 16px;border-radius:22px;transform:rotate(-5deg);box-shadow:0 24px 50px rgba(229,72,77,.5);letter-spacing:-2px}
#Hg{position:absolute;left:0;right:0;top:880px;text-align:center;font:900 170px 'InterD';color:#22C26A;letter-spacing:-6px;line-height:1}
#Hr{position:absolute;left:0;right:0;top:1090px;text-align:center;font:700 34px 'InterD';color:#9FB4E8;letter-spacing:6px}
/* A-C: gráfico */
#S1 .card{left:70px;width:940px}
#nums{top:370px;height:200px}
.nb{position:absolute;top:30px}
.nb .k{font:600 22px 'Inter';letter-spacing:4px;color:#7A8499}
.nb .v{font:900 76px 'InterD';letter-spacing:-3px;line-height:1.05;margin-top:6px}
#nDist{position:absolute;right:30px;top:24px;width:250px;height:150px;border-radius:30px;background:#F3F5FA;text-align:center;padding-top:14px}
#nDist .v{font:900 72px 'InterD';letter-spacing:-3px}
#chart{top:600px;height:640px;overflow:hidden}
#chart svg{position:absolute;left:0;top:0}
.tip{position:absolute;font:900 34px 'InterD';color:#fff;padding:6px 14px 9px;border-radius:12px;white-space:nowrap;letter-spacing:-.5px}
#tipB{background:#2563EB}#tipL{background:#E5484D}
#accTag{position:absolute;font:900 38px 'InterD';background:#FFD43B;color:#0B1533;padding:8px 20px 12px;border-radius:14px;transform:rotate(-3deg);box-shadow:0 14px 30px rgba(11,21,51,.18);opacity:0;white-space:nowrap}
#lock{position:absolute;font:900 36px 'InterD';background:#0B1533;color:#fff;padding:8px 20px 12px;border-radius:14px;opacity:0;white-space:nowrap}
#rep{position:absolute;left:100px;top:630px;font:900 40px 'InterD';color:#fff;background:#0B1533;padding:8px 20px 12px;border-radius:12px;letter-spacing:4px;display:flex;align-items:center;gap:12px;opacity:0}
#rep i{width:16px;height:16px;border-radius:50%;background:#E5484D}
#flash{position:absolute;inset:0;background:#E5484D;opacity:0;pointer-events:none}
#stamp{position:absolute;left:170px;top:760px;font:900 84px 'InterD';color:#fff;background:#E5484D;padding:8px 30px 14px;border-radius:20px;transform:rotate(-6deg);box-shadow:0 22px 50px rgba(229,72,77,.45);opacity:0;letter-spacing:-2px;white-space:nowrap}
#profit{position:absolute;left:330px;top:900px;font:900 46px 'InterD';color:#fff;background:#16A34A;padding:8px 24px 12px;border-radius:16px;opacity:0;white-space:nowrap;box-shadow:0 16px 36px rgba(22,163,74,.35)}
/* D: regra */
#rule{left:64px;width:952px;top:370px;height:880px}
#rule h2{position:absolute;left:52px;top:52px;width:850px;font:900 84px 'InterD';line-height:1.0;letter-spacing:-3px}
#rule h2 em{font-style:normal;color:#2563EB}
.eq{position:absolute;left:52px;width:600px;height:120px;display:flex;justify-content:space-between;align-items:center;opacity:0}
.eq .k{font:600 26px 'Inter';letter-spacing:4px;color:#7A8499}
.eq .v{font:900 88px 'InterD';letter-spacing:-3px}
#eqLine{position:absolute;left:52px;top:615px;width:600px;height:6px;border-radius:6px;background:#0B1533;transform-origin:0 50%}
#eqR{position:absolute;left:52px;top:640px;width:600px;height:160px;border-radius:30px;background:#EEF4FF;border:4px solid #2563EB;display:flex;justify-content:space-between;align-items:center;padding:0 30px;opacity:0}
#eqR .k{font:700 30px 'InterD';color:#2563EB;line-height:1.1}
#eqR .v{font:900 100px 'InterD';letter-spacing:-4px;color:#0B1533}
#avR{position:absolute;left:690px;top:520px;width:260px;opacity:0;filter:drop-shadow(0 26px 30px rgba(11,21,51,.25))}
/* E: frase */
#dq{position:absolute;left:70px;width:940px;top:460px;font:900 120px 'InterD';line-height:1.02;letter-spacing:-4px}
#dq span{display:inline-block;opacity:0;margin-right:26px}
#dn{position:absolute;left:70px;width:600px;top:1010px;font:600 30px 'Inter';color:#5B6478;line-height:1.4;opacity:0}
#avE{position:absolute;left:700px;top:820px;width:290px;opacity:0;filter:drop-shadow(0 26px 30px rgba(11,21,51,.25))}
/* F: final */
#F{background:#fff}
#F .logo{position:absolute;left:180px;top:540px;width:720px;height:270px;overflow:hidden}
#F .logo img{width:720px;display:block}
#F .logo .sh{position:absolute;top:-40px;bottom:-40px;width:160px;background:linear-gradient(100deg,transparent,rgba(255,255,255,.85),transparent);transform:skewX(-18deg)}
#F .q{position:absolute;left:90px;width:900px;top:900px;text-align:center;font:900 80px 'InterD';line-height:1.05;letter-spacing:-2px}
#F .u{position:absolute;left:0;width:1080px;top:1150px;text-align:center;font:700 36px 'InterD';color:#2563EB}
#F .d{position:absolute;left:0;width:1080px;top:1206px;text-align:center;font:500 24px 'Inter';color:#8A93A6;line-height:1.5}
</style></head><body>
<div id="bg"></div><div id="floor"></div>
<div id="world">
 <div class="scene" id="S1">
  <div class="card" id="nums">
   <div class="nb" style="left:44px"><div class="k">SALDO</div><div class="v" id="nB" style="color:#2563EB">50.000</div></div>
   <div class="nb" style="left:350px"><div class="k">LIMITE</div><div class="v" id="nL" style="color:#E5484D">48.000</div></div>
   <div id="nDist"><div class="k" style="font:600 22px 'Inter';letter-spacing:4px;color:#7A8499">DISTÂNCIA</div><div class="v" id="nD">2.000</div></div>
  </div>
  <div class="card" id="chart">
   <svg width="940" height="640" viewBox="0 0 940 640">
    <defs><linearGradient id="ga" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2563EB" stop-opacity=".22"/><stop offset="1" stop-color="#2563EB" stop-opacity="0"/></linearGradient></defs>
    <g id="grid"></g>
    <line id="base" x1="40" x2="900" stroke="#94A3B8" stroke-width="3" stroke-dasharray="4 10"/>
    <text id="baseT" x="48" font-family="Inter" font-weight="600" font-size="22" letter-spacing="3" fill="#94A3B8">SALDO INICIAL 50.000</text>
    <path id="area" fill="url(#ga)"/>
    <path id="lim" fill="none" stroke="#E5484D" stroke-width="7" stroke-dasharray="20 14" stroke-linecap="round"/>
    <path id="bal" fill="none" stroke="#2563EB" stroke-width="9" stroke-linejoin="round" stroke-linecap="round"/>
    <circle id="dot" r="14" fill="#2563EB" stroke="#fff" stroke-width="5"/>
    <circle id="hit" r="20" fill="none" stroke="#E5484D" stroke-width="6" opacity="0"/>
   </svg>
   <div class="tip" id="tipB">50.000</div><div class="tip" id="tipL">48.000</div>
   <div id="accTag">o limite acompanha o pico</div>
   <div id="lock">não desce mais</div>
  </div>
  <div id="rep"><i></i>REPLAY</div>
  <div id="flash"></div>
  <div id="stamp">CONTA ENCERRADA</div>
  <div id="profit">+1.000 sobre o inicial</div>
 </div>
 <div class="scene" id="D">
  <div class="card" id="rule"><h2>Seu espaço <em>real</em> hoje</h2>
   <div class="eq" id="e1" style="top:300px"><span class="k">PICO</span><span class="v" style="color:#2563EB">53.000</span></div>
   <div class="eq" id="e2" style="top:450px"><span class="k">− LIMITE</span><span class="v" style="color:#E5484D">51.000</span></div>
   <div id="eqLine"></div>
   <div id="eqR"><span class="k">ESPAÇO<br>REAL</span><span class="v">2.000</span></div>
   <img id="avR" src="file://__AVR__">
  </div>
 </div>
 <div class="scene" id="E">
  <div id="dq"><span>Confira</span><span>as</span><span style="color:#2563EB">regras</span><span>da</span><span>sua</span><span>mesa.</span></div>
  <div id="dn">Há mesas com limite fixo, que trava no saldo inicial ou que só atualiza no fim do dia.</div>
  <img id="avE" src="file://__AVE__">
 </div>
 <div class="scene" id="F">
  <div class="logo" id="logo"><img src="file://__LOGO__"><div class="sh" id="shine"></div></div>
  <div class="q" id="eq">Quanto espaço você tem hoje, de verdade?</div>
  <div class="u" id="eu">tradeyouup.net</div>
  <div class="d" id="ed">Exemplo ilustrativo · valores fictícios · regras variam por mesa.<br>Conteúdo educativo. Não é recomendação de investimento.</div>
 </div>
 <div class="scene" id="H"><div id="Hs"></div>
  <div id="Hq">No lucro e <em>reprovado?</em></div>
  <div id="Hst">CONTA ENCERRADA</div>
  <div id="Hg">+1.000</div>
  <div id="Hr">◀◀ VOLTA DO COMEÇO</div>
 </div>
</div>
<div id="vig"></div>
<div id="top"><div class="tag"><i></i>MESA SEM ROMANCE</div></div>
<div id="prog"><b><i></i></b><b><i></i></b><b><i></i></b><b><i></i></b><b><i></i></b></div>
<div id="note">Exemplo ilustrativo · valores fictícios · regras variam por mesa</div>
<div id="cap"></div>
<canvas id="grain" width="360" height="640"></canvas>
<script>
const W=__WORDS__, G=__GROUPS__, KR=new Set(__KR__), KG=new Set(__KG__), KB=new Set(__KB__);
const SP=W[W.length-1][2]+0.15, END=SP+__TAIL__;
const $=id=>document.getElementById(id);
const cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)), lerp=(a,b,k)=>a+(b-a)*k, seg=(t,a,b)=>cl((t-a)/(b-a));
const eo=x=>1-Math.pow(1-cl(x),3), eio=x=>{x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2};
const eexp=x=>{x=cl(x);return x===1?1:1-Math.pow(2,-10*x)};
const spring=(x,f=1)=>{x=Math.max(0,x);return 1-Math.exp(-7*x)*Math.cos(10*f*x)};
function vis(el,o){el.style.opacity=o;el.style.visibility=o<=0.001?'hidden':'visible'}
function wi(txt,from){for(let i=from||0;i<W.length;i++)if(W[i][0]===txt)return i;throw txt}
const wt=i=>W[i][1];
const fmt=v=>(Math.round(v/100)*100).toString().replace(/\B(?=(\d{3})+(?!\d))/g,'.');
// ---- marcos
const iSo=wi('Só'), iAg=wi('Agora'), iAi=wi('Aí'), iO=wi('O',60), iAn=wi('Antes'), iE=wi('E',80), iL2=wi('limite',iAg-8);
const M={ m53:wt(wi('53')), m2:wt(wi('2')), sob:wt(wi('sobe')), m51:wt(wi('51')), dev:wt(wi('devolução')), vol:wt(wi('volta.')),
 sal:wt(wi('Saldo:')), enc:wt(wi('encerrada.')), luc:wt(wi('lucro.')), des:wt(wi('desce')),
 dIn:wt(iAn)-0.2, pico:wt(wi('Pico')), lim:wt(wi('limite.')), esp:wt(wi('espaço')), eIn:wt(iE)-0.2, aIn:wt(iSo)-0.2, bIn:wt(iAi)-0.2, cIn:wt(iO)-0.15 };
// ---- caminho do saldo (milhares) e limite = pico - 2
const KP=[[0,50],[.07,50.6],[.12,50.3],[.21,51.4],[.27,51.05],[.37,52.2],[.43,51.85],[.55,53],[.61,52.55],[.67,52.8],[.72,53.0],[.77,52.2],[.8,52.45],[.9,51.0]];
function balAt(u){for(let i=1;i<KP.length;i++){if(u<=KP[i][0]){const [a,va]=KP[i-1],[b,vb]=KP[i];return lerp(va,vb,(u-a)/(b-a))}}return KP[KP.length-1][1]}
const N=360, U=[...Array(N+1)].map((_,i)=>.9*i/N), BV=U.map(balAt); const PK=[]; BV.reduce((m,v,i)=>{m=Math.max(m,v);PK[i]=m;return m},0);
const X=u=>40+u/.9*800, Y=v=>600-(v-47.2)/(54-47.2)*560;
function reveal(t){ // u revelado
 if(t<0.35)return 0; if(t<M.m53+.3)return .55*eio(seg(t,.35,M.m53+.3));
 if(t<M.dev)return lerp(.55,.72,seg(t,M.m53+.3,M.dev)); return lerp(.72,.9,eio(seg(t,M.dev+.2,M.vol+.15)));}
// ---- grão
const gc=$('grain').getContext('2d'), gimg=gc.createImageData(360,640);
function grain(f){let s=f*7919+1;const d=gimg.data;for(let i=0;i<d.length;i+=4){s=(s*16807)%2147483647;const v=s%255;d[i]=d[i+1]=d[i+2]=v;d[i+3]=255}gc.putImageData(gimg,0,0)}
const HITS=[[1.45,12],[M.vol+.15,22],[M.enc,16],[M.esp,10]];
function shake(t){let x=0,y=0;HITS.forEach(([h,a],j)=>{const d=t-h;if(d>=0&&d<.5){const k=a*Math.exp(-9*d);x+=k*Math.sin(d*90+j);y+=k*Math.cos(d*77+j*2)}});return [x,y]}
// grade
(function(){let g='';[48,49,50,51,52,53].forEach(v=>{g+=`<line x1="40" x2="900" y1="${Y(v)}" y2="${Y(v)}" stroke="#0B1533" stroke-opacity=".06" stroke-width="2"/>`});$('grid').innerHTML=g;
 $('base').setAttribute('y1',Y(50));$('base').setAttribute('y2',Y(50));$('baseT').setAttribute('y',Y(50)+34)})();
// ---- legendas
const capEl=$('cap');let capG=-1,capSpans=[];
function buildCap(gi){capEl.innerHTML='';capSpans=[];const [a,b]=G[gi];for(let i=a;i<=b;i++){const s=document.createElement('span');s.textContent=W[i][0];capEl.appendChild(s);capSpans.push([i,s])}}

window.render=function(t,f){
 grain(Math.floor(f/2));
 const [sx,sy]=shake(t); $('world').style.transform=`translate(${sx}px,${sy}px)`;
 $('bg').style.transform=`translate(${Math.sin(t*.25)*30}px,${Math.cos(t*.2)*24}px) scale(${1.05+.03*Math.sin(t*.15)})`;
 $('floor').style.transform=`perspective(900px) rotateX(74deg) translateY(${(t*60)%120}px)`;
 const topO=seg(t,1.5,1.8)*(1-seg(t,SP-.2,SP+.1)); vis($('top'),topO); vis($('prog'),topO);
 const sc=[[0,M.aIn],[M.aIn,M.bIn],[M.bIn,M.dIn],[M.dIn,M.eIn],[M.eIn,SP]];
 document.querySelectorAll('#prog b i').forEach((el,i)=>{el.style.width=(seg(t,sc[i][0],sc[i][1])*100)+'%'});
 vis($('note'),seg(t,1.7,2.1)*(1-seg(t,M.eIn-.3,M.eIn)));
 // ---------- HOOK (0–1,5 s)
 {const H=$('H'), out=seg(t,1.25,1.6); vis(H,t<1.6?1-eo(out):0);
  const k1=spring(t/.5); $('Hq').style.transform=`scale(${1.4-.4*Math.min(1.03,k1)})`;
  const k2=spring((t-.25)/.5); $('Hst').style.opacity=t>.25?1:0; $('Hst').style.transform=`rotate(-5deg) scale(${t<.25?1.8:1.8-.8*Math.min(1.04,k2)})`;
  const k3=spring((t-.5)/.5); $('Hg').style.opacity=t>.5?1:0; $('Hg').style.transform=`scale(${t<.5?.6:.6+.4*Math.min(1.03,k3)})`;
  $('Hr').style.opacity=seg(t,.85,1.0)*((Math.floor(t*6)%2)?1:.5);
  H.style.filter=`blur(${out*16}px)`; H.style.transform=`scale(${1+out*.15})`;}
 // ---------- S1: gráfico (até D)
 {const S=$('S1'), inK=eexp(seg(t,1.2,1.6)), out=seg(t,M.dIn-.2,M.dIn+.15); vis(S,(t>1.2&&t<M.dIn+.2)?1:0);
  S.style.transform=`translateY(${(1-inK)*300-eio(out)*1600}px)`; S.style.opacity=inK; S.style.filter=`blur(${Math.sin(Math.PI*out)*14}px)`;
  const u=reveal(t), n=Math.max(1,Math.round(u/.9*N)); let d='',dl='',da='';
  for(let i=0;i<=n;i++){const x=X(U[i]).toFixed(1), y=Y(BV[i]).toFixed(1), yl=Y(PK[i]-2).toFixed(1); d+=(i?' L':'M')+x+','+y; dl+=(i?' L':'M')+x+','+yl;}
  da=d+` L${X(U[n]).toFixed(1)},640 L40,640 Z`;
  $('bal').setAttribute('d',d); $('lim').setAttribute('d',dl); $('area').setAttribute('d',da);
  const bx=X(U[n]), by=Y(BV[n]), ly=Y(PK[n]-2); $('dot').setAttribute('cx',bx); $('dot').setAttribute('cy',by);
  const b=BV[n], l=PK[n]-2;
  $('tipB').textContent=fmt(b*1000); $('tipL').textContent=fmt(l*1000);
  $('tipB').style.left=Math.min(760,bx+20)+'px'; $('tipB').style.top=(by-70)+'px';
  $('tipL').style.left=Math.min(760,bx+20)+'px'; $('tipL').style.top=(ly+16)+'px';
  $('nB').textContent=fmt(b*1000); $('nL').textContent=fmt(l*1000);
  const dist=Math.max(0,(b-l)*1000); $('nD').textContent=fmt(dist); $('nD').style.color=dist<400?'#E5484D':'#0B1533';
  $('nL').style.transform=`scale(${1+0.14*Math.exp(-5*Math.max(0,t-M.m51))*(t>M.m51?1:0)})`; $('nL').style.transformOrigin='0 50%';
  const ak=spring((t-M.sob)/.6); $('accTag').style.opacity=t>M.sob&&t<M.dev?1:0; $('accTag').style.left='60px'; $('accTag').style.top='34px';
  $('accTag').style.transform=`rotate(-3deg) scale(${t<M.sob?1.4:1.4-.4*Math.min(1.03,ak)})`;
  const lk=spring((t-M.des)/.6); $('lock').style.opacity=t>M.des?1:0; $('lock').style.left='470px'; $('lock').style.top=(Y(51)+30)+'px';
  $('lock').style.transform=`scale(${t<M.des?1.4:1.4-.4*Math.min(1.03,lk)})`;
  $('rep').style.opacity=(t>M.dev-.1&&t<M.sal)?((Math.floor(t*2.5)%2===0)?1:.4):0;
  const touch=M.vol+.15; const hk=seg(t,touch,touch+.6); $('hit').setAttribute('cx',bx); $('hit').setAttribute('cy',by);
  $('hit').setAttribute('r',20+hk*60); $('hit').setAttribute('opacity',t>touch?(1-hk):0);
  $('flash').style.opacity=t>touch?0.35*Math.exp(-6*(t-touch)):0;
  const sk=spring((t-M.enc)/.5); $('stamp').style.opacity=t>M.enc?1:0; $('stamp').style.transform=`rotate(-6deg) scale(${t<M.enc?1.8:1.8-.8*Math.min(1.04,sk)})`;
  const pk=eo(seg(t,M.luc-.15,M.luc+.25)); $('profit').style.opacity=pk; $('profit').style.transform=`translateY(${(1-pk)*30}px)`;
  $('chart').style.borderColor=t>touch?'rgba(229,72,77,.5)':'rgba(11,21,51,.06)';
 }
 // ---------- D: regra
 {const S=$('D'), inK=eexp(seg(t,M.dIn-.1,M.dIn+.35)), out=seg(t,M.eIn-.2,M.eIn+.15); vis(S,(t>M.dIn-.1&&t<M.eIn+.2)?1:0);
  S.style.transform=`translateY(${(1-inK)*1500}px)`; S.style.opacity=(t>M.dIn-.1&&t<M.eIn+.2)?1-eo(out):0;
  [['e1',M.pico-.1],['e2',M.lim-.25]].forEach(([id,a])=>{const k=eo(seg(t,a,a+.3)); $(id).style.opacity=k; $(id).style.transform=`translateX(${(1-k)*-80}px)`});
  $('eqLine').style.transform=`scaleX(${eio(seg(t,M.lim+.2,M.lim+.6))})`;
  const rk=spring((t-M.esp)/.6); $('eqR').style.opacity=t>M.esp-.05?1:0; $('eqR').style.transform=`scale(${t<M.esp?1.3:1.3-.3*Math.min(1.03,rk)})`;
  const ak=spring((t-M.dIn-.3)/.9); $('avR').style.opacity=seg(t,M.dIn+.3,M.dIn+.5); $('avR').style.transform=`translateY(${(1-Math.min(1,ak))*200}px)`;}
 // ---------- E: frase final
 {const S=$('E'), inK=eexp(seg(t,M.eIn-.1,M.eIn+.35)), out=seg(t,SP-.12,SP+.15); vis(S,(t>M.eIn-.1&&t<SP+.2)?1:0);
  S.style.transform=`translateY(${(1-inK)*1500}px) scale(${1+.04*seg(t,M.eIn,SP)})`; S.style.opacity=(t>M.eIn-.1&&t<SP+.2)?1-out:0;
  const ak=spring((t-M.eIn-.2)/.9); $('avE').style.opacity=seg(t,M.eIn+.2,M.eIn+.4); $('avE').style.transform=`translateY(${(1-Math.min(1,ak))*200}px)`;
  const iC=wi('confira'); [...$('dq').children].forEach((s,i)=>{const a=wt(iC+i)-.05, k=spring((t-a)/0.6);s.style.opacity=cl((t-a)/.08);s.style.transform=`translateY(${(1-Math.min(1,k))*50}px)`});
  $('dn').style.opacity=eo(seg(t,wt(iC)+.6,wt(iC)+1.0));}
 // ---------- F: final
 {const S=$('F'), k=seg(t,SP-.05,SP+.35); vis(S,t>SP-.06?eo(k):0);
  const lk=spring((t-SP-.05)/0.9); $('logo').style.transform=`scale(${t<SP?0.8:0.8+.2*Math.min(1.02,lk)})`; $('logo').style.opacity=seg(t,SP,SP+.25);
  $('shine').style.left=(-200+1100*eio(seg(t,SP+.6,SP+1.5)))+'px';
  [['eq',SP+.5],['eu',SP+.85],['ed',SP+1.0]].forEach(([id,a])=>{const kk=eo(seg(t,a,a+.45));$(id).style.opacity=kk;$(id).style.transform=`translateY(${(1-kk)*30}px)`});}
 // ---------- legendas (somem na frase final)
 let gi=-1; for(let i=0;i<G.length;i++){const s=wt(G[i][0])-0.12; const e=(i+1<G.length)?wt(G[i+1][0])-0.12:SP+0.05; if(t>=s&&t<e)gi=i}
 if(gi>=0&&G[gi][0]>=iE)gi=-1;
 if(gi!==capG){capG=gi; if(gi>=0)buildCap(gi); else capEl.innerHTML=''}
 if(gi>=0){const gs=wt(G[gi][0])-0.12, gk=eo(seg(t,gs,gs+.18)); capEl.style.opacity=gk; capEl.style.transform=`translateY(${(1-gk)*24}px)`;
  capSpans.forEach(([i,s])=>{const w=W[i], on=t>=w[1]-0.04, act=on&&(i+1>G[gi][1]||t<W[i+1][1]-0.04);
   s.style.opacity=on?1:.22; const c=KR.has(w[0])?'#E5484D':KG.has(w[0])?'#16A34A':KB.has(w[0])?'#2563EB':null;
   if(act){const pk=spring((t-w[1]+0.04)/0.45); s.style.background=c||'#0B1533'; s.style.color='#fff'; s.style.textShadow='none';
    s.style.transform=`scale(${1+.08*Math.max(0,1-(t-w[1])/0.35)}) translateY(${-4*Math.min(1,pk)}px)`; s.style.boxShadow='0 10px 24px rgba(11,21,51,.22)';}
   else{s.style.background='transparent'; s.style.color=c||'#0B1533'; s.style.textShadow=''; s.style.transform='none'; s.style.boxShadow='none';}});}
 else capEl.style.opacity=0;
};
</script></body></html>"""


def build():
    words = load_words()
    gs = groups(words)
    rep = {"__INTER__": INTER, "__LOGO__": LOGO, "__AVR__": AV["explicando"], "__AVE__": AV["joinha"],
           "__WORDS__": json.dumps(words, ensure_ascii=False), "__GROUPS__": json.dumps(gs),
           "__KR__": json.dumps(sorted(KEY_RED), ensure_ascii=False), "__KG__": json.dumps(sorted(KEY_GREEN), ensure_ascii=False),
           "__KB__": json.dumps(sorted(KEY_BLUE), ensure_ascii=False), "__TAIL__": str(TAIL)}
    h = HTML
    for k, v in rep.items():
        h = h.replace(k, v)
    return h, words[-1][2] + 0.15 + TAIL


async def render(out, fps, stills=None):
    from playwright.async_api import async_playwright
    html, end = build()
    hp = os.path.join(HERE, "short44.html"); open(hp, "w").write(html)
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--enable-gpu-rasterization", "--ignore-gpu-blocklist"])
        pg = await b.new_page(viewport={"width": 1080, "height": 1920})
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
        for f in range(int(round(end * fps))):
            await pg.evaluate("render(%f,%d)" % (f / fps, f))
            ff.stdin.write(await pg.screenshot(type="jpeg", quality=93))
        print("errors:", errs); await b.close()
    ff.stdin.close(); ff.wait()


if __name__ == "__main__":
    if sys.argv[1] == "stills":
        asyncio.run(render(None, 60, [float(x) for x in sys.argv[2:]]))
    elif sys.argv[1] == "info":
        _, end = build(); print(end)
    else:
        fps = int(sys.argv[2]) if len(sys.argv) > 2 else 60
        asyncio.run(render(sys.argv[1], fps))
        print("ok", sys.argv[1])
