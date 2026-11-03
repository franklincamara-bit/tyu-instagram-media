# Reel "Duas Realidades #1: o stop respeitado" (TYU-57) — motion design 1080x1920, tela dividida.
# Base visual: cashflow1.py / tribunal1.py (padrão Short 81% v2). Tempos das palavras: words.json (transcrição com
# marcação de tempo da narracao.mp3, conferida com silencedetect).
# Uso: python3 duas1.py <saida_sem_audio.mp4> [fps]  |  python3 duas1.py stills t1 t2 ...
import os, sys, json, asyncio, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
INTER = "/usr/share/fonts/opentype/inter"
LOGO = os.path.join(ROOT, "assets", "logo.png")
RAW = json.load(open(os.path.join(HERE, "words.json")))  # [palavra, ini, fim]
TAIL = 3.2

# Legenda: "menos um R" -> "−1R"; "menos três R's" -> "−3R".
REPL = {("menos", "um", "R,"): "−1R.", ("menos", "três", "R's."): "−3R."}
KEY_RED = ["−3R.", "hábito.", "decisão", "espaço.", "espaço,", "não"]
KEY_BLUE = ["−1R.", "anota.", "plano.", "plataforma,", "disciplina,"]
KEY_GREEN = ["certo."]


def words_and_groups():
    w, i = [], 0
    while i < len(RAW):
        hit = None
        for k, v in REPL.items():
            if tuple(x[0] for x in RAW[i:i + len(k)]) == k:
                hit = (len(k), v)
        if hit:
            w.append([hit[1], RAW[i][1], RAW[i + hit[0] - 1][2]]); i += hit[0]
        else:
            w.append(list(RAW[i])); i += 1
    w[0][1] = max(w[0][1], 0.05)
    groups, cur = [], []
    for j, x in enumerate(w):
        cur.append(j)
        end = x[0][-1] in ".?" or (x[0][-1] == "," and len(cur) >= 2) or len(cur) >= 9
        if end or j == len(w) - 1:
            groups.append([cur[0], cur[-1]]); cur = []
    return w, groups


def T(word, n=1):
    """instante da n-ésima ocorrência da palavra (sem pontuação) na narração."""
    c = 0
    for x in RAW:
        if x[0].strip(".,?!").lower() == word.lower():
            c += 1
            if c == n:
                return x[1]
    raise KeyError(word)


M = dict(
    stop0=T("stop"), duas=T("duas"), lfoc=T("Na"), hitL=T("menos") - 0.3, m1=T("menos"), anota=T("aceita"),
    rfoc=T("direita"), mv1=T("só") , volta=T("volta"), zero=T("zero"), certo=T("parece"), mas=T("Mas"), hab=T("hábito"),
    sem=T("semana"), mv2=T("espaço", 2), nv=T("dessa", 2), m3=T("menos", 2), cmpL=T("esquerda", 2), custo=T("custo"),
    cmpR=T("direita", 2), dec=T("decisão"), plat=T("plataforma"), reg=T("registra"), falha=T("falha"), mesmo=T("quando"),
    em=T("Em"))
M["hitR"] = M["m3"] - 0.25
SP = M["em"] - 0.2
END = RAW[-1][2] + TAIL

HTML = r"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'InterD';src:url('file://__INTER__/InterDisplay-Black.otf');font-weight:900}
@font-face{font-family:'InterD';src:url('file://__INTER__/InterDisplay-Bold.otf');font-weight:700}
@font-face{font-family:'Inter';src:url('file://__INTER__/Inter-SemiBold.otf');font-weight:600}
@font-face{font-family:'Inter';src:url('file://__INTER__/Inter-Medium.otf');font-weight:500}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#EEF1F7;font-family:'InterD',sans-serif;color:#0B1533}
#bg{position:absolute;inset:-200px;background:
  radial-gradient(900px 900px at 12% 12%,rgba(37,99,235,.16),transparent 62%),
  radial-gradient(900px 900px at 92% 30%,rgba(229,72,77,.12),transparent 62%),
  linear-gradient(180deg,#F7F8FC 0%,#ECEFF6 100%)}
#floor{position:absolute;left:-1200px;width:3480px;top:1000px;height:2600px;transform-origin:50% 0;
  background-image:linear-gradient(rgba(11,21,51,.07) 2px,transparent 2px),linear-gradient(90deg,rgba(11,21,51,.07) 2px,transparent 2px);
  background-size:120px 120px;-webkit-mask-image:linear-gradient(180deg,transparent 0%,#000 18%,#000 55%,transparent 100%)}
#world{position:absolute;inset:0;transform-origin:540px 800px}
#vig{position:absolute;inset:0;pointer-events:none;background:radial-gradient(1300px 1700px at 50% 45%,transparent 55%,rgba(11,21,51,.15) 100%)}
#grain{position:absolute;inset:0;width:1080px;height:1920px;mix-blend-mode:overlay;opacity:.10}
#top{position:absolute;left:64px;top:232px;display:flex;align-items:center;gap:18px;opacity:0;z-index:5}
#top .tag{font:600 26px 'Inter';letter-spacing:4px;background:rgba(255,255,255,.85);border:2px solid rgba(11,21,51,.08);padding:12px 20px;border-radius:999px;display:flex;align-items:center;gap:12px;box-shadow:0 8px 24px rgba(11,21,51,.06)}
#top .tag i{width:12px;height:12px;border-radius:50%;background:#2563EB;box-shadow:0 0 0 6px rgba(37,99,235,.15)}
#top .tag i+i{background:#E5484D;box-shadow:0 0 0 6px rgba(229,72,77,.15);margin-left:-4px}
#cap{position:absolute;left:60px;width:880px;top:1310px;display:flex;flex-wrap:wrap;justify-content:center;align-items:baseline;gap:6px 14px;
  font-family:'InterD';font-weight:900;font-size:66px;line-height:1.12;letter-spacing:-1px;z-index:6}
#cap span{position:relative;display:inline-block;padding:2px 10px;border-radius:16px;color:#0B1533;white-space:nowrap;text-shadow:0 2px 0 rgba(255,255,255,.9),0 0 18px rgba(255,255,255,.9)}
.pan{position:absolute;top:340px;width:470px;height:880px;background:rgba(255,255,255,.97);border:2px solid rgba(11,21,51,.06);border-radius:40px;box-shadow:0 40px 90px rgba(11,21,51,.14);overflow:hidden}
#PA{left:50px}#PB{left:560px}
.pan .hd{position:absolute;left:30px;top:30px;display:flex;align-items:center;gap:12px;font:600 22px 'Inter';letter-spacing:4px;color:#7A8499}
.pan .hd i{width:14px;height:14px;border-radius:50%}
#PA .hd i{background:#2563EB}#PB .hd i{background:#E5484D}
.pan .tt{position:absolute;left:30px;top:64px;font:900 40px 'InterD';letter-spacing:-1.5px;white-space:nowrap}
.pan .sub{position:absolute;left:30px;top:124px;font:900 20px 'InterD';letter-spacing:2px;color:#fff;background:#0B1533;border-radius:999px;padding:8px 14px 10px;opacity:0}
.pan svg.ch{position:absolute;left:0;top:150px}
.ring{position:absolute;inset:0;border-radius:40px;pointer-events:none}
.stamp{position:absolute;opacity:0;white-space:nowrap}
.stamp b{display:inline-block;font:900 92px 'InterD';letter-spacing:-2px;border:9px solid;border-radius:24px;padding:0 22px 8px;background:rgba(255,255,255,.88)}
.chip{position:absolute;opacity:0;white-space:nowrap}
.chip b{display:inline-flex;align-items:center;gap:12px;font:900 30px 'InterD';border-radius:999px;padding:12px 22px 14px;color:#fff}
.res{position:absolute;left:24px;right:24px;bottom:20px;height:180px;border-radius:30px;padding:18px 26px;opacity:0}
.res .v{font:900 88px 'InterD';letter-spacing:-3px;line-height:1}
.res .l{font:700 30px 'InterD';letter-spacing:-.5px;margin-top:10px;line-height:1.1}
#resA{background:#E8EFFE}#resA .v{color:#2563EB}
#resB{background:#FDECEC}#resB .v{color:#E5484D}
#selo{position:absolute;left:0;right:0;top:1236px;text-align:center;font:500 22px 'Inter';color:#8A93A6;opacity:0}
/* D: registro de falhas (cartão estilizado) */
#D{position:absolute;inset:0;opacity:0;visibility:hidden}
#reg{position:absolute;left:90px;width:900px;top:360px;height:860px;padding:44px 48px;background:rgba(255,255,255,.97);border:2px solid rgba(11,21,51,.06);border-radius:44px;box-shadow:0 40px 90px rgba(11,21,51,.14)}
#reg .h2{font:600 24px 'Inter';letter-spacing:4px;color:#7A8499}
#reg .ttl{font:900 58px 'InterD';letter-spacing:-1.5px;margin-top:14px}
.rr{position:absolute;left:48px;right:48px;height:190px;border-radius:28px;background:#F6F7FB;border:2px solid #E2E8F0;padding:24px 28px;opacity:0}
.rr .a{display:flex;justify-content:space-between;align-items:center}
.rr .a b{font:900 42px 'InterD';letter-spacing:-1px}
.rr .a span{font:900 40px 'InterD';white-space:nowrap}
.rr .pill{display:inline-block;margin-top:18px;font:600 20px 'Inter';letter-spacing:3px;color:#B45309;background:#FEF3C7;border-radius:999px;padding:8px 16px;opacity:0;transform-origin:0 50%}
.rr .mk{position:absolute;right:26px;bottom:26px;font:900 28px 'InterD';color:#0B1533;background:#FFD43B;border-radius:12px;padding:6px 14px 8px;opacity:0;white-space:nowrap}
#rselo{position:absolute;left:48px;bottom:36px;font:500 22px 'Inter';color:#8A93A6}
/* F */
#F{position:absolute;inset:0;background:#fff;opacity:0;visibility:hidden}
#F .logo{position:absolute;left:180px;top:470px;width:720px;height:270px;overflow:hidden}
#F .logo img{width:720px;display:block}
#F .logo .sh{position:absolute;top:-40px;bottom:-40px;width:160px;background:linear-gradient(100deg,transparent,rgba(255,255,255,.85),transparent);transform:skewX(-18deg)}
#F .q{position:absolute;left:80px;width:920px;top:820px;text-align:center;font:900 78px 'InterD';line-height:1.05;letter-spacing:-2.5px}
#F .q em{font-style:normal;color:#2563EB}#F .q u{text-decoration:none;color:#E5484D}
#F .u{position:absolute;left:0;width:1080px;top:1150px;text-align:center;font:700 36px 'InterD';color:#2563EB}
#F .d{position:absolute;left:0;width:1080px;top:1206px;text-align:center;font:500 24px 'Inter';color:#8A93A6;line-height:1.5}
</style></head><body>
<div id="bg"></div><div id="floor"></div>
<div id="world">
 <div class="pan" id="PA"><div class="hd"><i></i>REALIDADE A</div><div class="tt">Respeitou o stop</div><div class="sub" id="subA">O TRADE</div>
  <svg class="ch" id="chA" width="470" height="560"></svg>
  <div class="chip" id="okA" style="left:30px;top:690px"><b style="background:#2563EB">✓ Aceitou e anotou</b></div>
  <div class="res" id="resA"><div class="v">−1R</div><div class="l" id="lA">custo do plano</div></div>
  <div class="ring" id="ringA"></div></div>
 <div class="pan" id="PB"><div class="hd"><i></i>REALIDADE B</div><div class="tt">"Só mais um espaço"</div><div class="sub" id="subB">O TRADE</div>
  <svg class="ch" id="chB" width="470" height="560"></svg>
  <div class="chip" id="zB" style="left:30px;top:690px"><b style="background:#16A34A">0R · deu certo?</b></div>
  <div class="stamp" id="habB" style="left:34px;top:340px"><b style="color:#B45309;border-color:#F59E0B;font-size:50px;border-width:7px">FICOU O HÁBITO</b></div>
  <div class="res" id="resB"><div class="v">−3R</div><div class="l" id="lB">decisão no meio do trade</div></div>
  <div class="ring" id="ringB"></div></div>
 <div class="stamp" id="m1" style="left:120px;top:760px"><b style="color:#2563EB;border-color:#2563EB">−1R</b></div>
 <div class="stamp" id="m3" style="left:630px;top:760px"><b style="color:#E5484D;border-color:#E5484D">−3R</b></div>
 <div id="selo">Exemplo ilustrativo · conta demo · resultados em R</div>
 <div id="D"><div id="reg"><div class="h2">REGISTRO DO DIA</div><div class="ttl">Falhas de disciplina</div>
  <div class="rr" id="r1" style="top:200px"><div class="a"><b>Moveu o stop</b><span style="color:#16A34A">0R</span></div><div class="pill">FALHA DE DISCIPLINA</div><div class="mk">mesmo no zero</div></div>
  <div class="rr" id="r2" style="top:420px"><div class="a"><b>Moveu o stop</b><span style="color:#E5484D">−3R</span></div><div class="pill">FALHA DE DISCIPLINA</div></div>
  <div class="rr" id="r3" style="top:640px;height:110px"><div class="a"><b style="color:#2563EB">Stop respeitado</b><span style="color:#2563EB">−1R</span></div></div>
  <div id="rselo">Exemplo ilustrativo · conta demo</div></div></div>
 <div id="F">
  <div class="logo" id="logo"><img src="file://__LOGO__"><div class="sh" id="shine"></div></div>
  <div class="q" id="eq">Em qual das <em>duas</em> <u>realidades</u> você operou essa semana?</div>
  <div class="u" id="eu">tradeyouup.net</div>
  <div class="d" id="ed">Exemplo ilustrativo · conta demo.<br>Conteúdo educativo. Não é recomendação de investimento.</div>
 </div>
</div>
<div id="vig"></div>
<div id="top"><div class="tag"><i></i><i></i>DUAS REALIDADES #1</div></div>
<div id="cap"></div>
<canvas id="grain" width="360" height="640"></canvas>
<script>
const W=__WORDS__, G=__GROUPS__, M=__M__, SP=__SP__, END=__END__, KR=new Set(__KR__), KG=new Set(__KG__), KB=new Set(__KB__);
const $=id=>document.getElementById(id);
const cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)), lerp=(a,b,k)=>a+(b-a)*k, seg=(t,a,b)=>cl((t-a)/(b-a));
const eo=x=>1-Math.pow(1-cl(x),3), eio=x=>{x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2};
const spring=(x,f=1)=>{x=Math.max(0,x);return 1-Math.exp(-7*x)*Math.cos(10*f*x)};
function vis(el,o){el.style.opacity=o;el.style.visibility=o<=0.001?'hidden':'visible'}
const gc=$('grain').getContext('2d'), gimg=gc.createImageData(360,640);
function grain(f){let s=f*7919+1;const d=gimg.data;for(let i=0;i<d.length;i+=4){s=(s*16807)%2147483647;const v=s%255;d[i]=d[i+1]=d[i+2]=v;d[i+3]=255}gc.putImageData(gimg,0,0)}
const HITS=[[M.hitL,8],[M.m1,12],[M.zero,5],[M.hab,10],[M.hitR,10],[M.m3,18]];
function shake(t){let x=0,y=0;HITS.forEach(([h,a],j)=>{const d=t-h;if(d>=0&&d<.5){const k=a*Math.exp(-9*d);x+=k*Math.sin(d*90+j);y+=k*Math.cos(d*77+j*2)}});return [x,y]}
// ---------- gráficos (em R): y de +1 a −3.5
const YR=r=>40+(1-r)*(470/4.5), X0=30, X1=440;
const KA=[[0.2,0],[0.9,0.32],[1.7,0.05],[2.5,0.42],[3.4,-0.15],[4.5,0.08],[5.4,-0.55],[M.hitL,-1.0]];
const pre=[[0.2,0],[0.9,0.32],[1.7,0.05],[2.5,0.42],[3.4,-0.15],[4.5,0.08],[5.4,-0.55],[M.hitL-.2,-0.9]];
const KB1=pre.concat([[M.rfoc+.6,-0.93],[M.mv1+1.2,-1.35],[M.volta-.4,-1.7],[M.volta,-1.15],[M.zero-.6,-0.4],[M.zero,0]]);
const KB2=[[M.sem,0],[M.sem+.5,0.25],[M.mv2-.2,-0.55],[M.mv2+.2,-0.95],[M.nv,-1.25],[M.nv+.7,-1.9],[M.hitR-.5,-2.6],[M.hitR,-3.0]];
function pathAt(K,t,ta,tb){const pts=[];const tt=Math.min(t,K[K.length-1][0]);if(tt<K[0][0])return {d:'',x:null,y:null};
 const N=80;for(let i=0;i<=N;i++){const s=K[0][0]+(tt-K[0][0])*i/N;let r=K[0][1];
  for(let j=0;j<K.length-1;j++){if(s>=K[j][0]&&s<=K[j+1][0]){const k=(s-K[j][0])/(K[j+1][0]-K[j][0]);r=lerp(K[j][1],K[j+1][1],k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2)+0.04*Math.sin(s*23)*Math.sin(s*7);break}
   if(s>K[j+1][0])r=K[j+1][1]}
  pts.push([lerp(X0,X1,(s-ta)/(tb-ta)),YR(r)])}
 return {d:'M'+pts.map(p=>p[0].toFixed(1)+' '+p[1].toFixed(1)).join(' L'),x:pts[N][0],y:pts[N][1]}}
function chart(svg,K,t,ta,tb,stopR,stopLbl,stopCol,flash,col){
 const p=pathAt(K,t,ta,tb); let h='';
 for(let r=1;r>=-3.5;r-=.5){h+=`<line x1="${X0}" x2="${X1}" y1="${YR(r)}" y2="${YR(r)}" stroke="rgba(11,21,51,.06)" stroke-width="2"/>`}
 h+=`<line x1="${X0}" x2="${X1}" y1="${YR(0)}" y2="${YR(0)}" stroke="#0B1533" stroke-width="4" stroke-linecap="round"/>`;
 h+=`<text x="${X1}" y="${YR(0)-14}" text-anchor="end" font-family="Inter" font-weight="600" font-size="18" letter-spacing="3" fill="#7A8499">ENTRADA · 0R</text>`;
 h+=`<line x1="${X0}" x2="${X1}" y1="${YR(stopR)}" y2="${YR(stopR)}" stroke="${stopCol}" stroke-width="5" stroke-dasharray="16 12" stroke-linecap="round"/>`;
 h+=`<rect x="${X1-210}" y="${YR(stopR)+10}" width="210" height="40" rx="12" fill="${stopCol}"/><text x="${X1-105}" y="${YR(stopR)+38}" text-anchor="middle" font-family="InterD" font-weight="900" font-size="22" fill="#fff">${stopLbl}</text>`;
 if(p.d){h+=`<path d="${p.d}" fill="none" stroke="${col}" stroke-width="16" stroke-opacity=".12" stroke-linecap="round" stroke-linejoin="round"/>`;
  h+=`<path d="${p.d}" fill="none" stroke="${col}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>`;
  h+=`<circle cx="${p.x}" cy="${p.y}" r="${13+flash*22}" fill="${col}" opacity="${.18+flash*.3}"/><circle cx="${p.x}" cy="${p.y}" r="9" fill="${col}"/>`}
 svg.innerHTML=h}
const capEl=$('cap');let capG=-1,capSpans=[];
function buildCap(gi){capEl.innerHTML='';capSpans=[];const [a,b]=G[gi];for(let i=a;i<=b;i++){const s=document.createElement('span');s.textContent=W[i][0];capEl.appendChild(s);capSpans.push([i,s])}}
function stamp(el,t0,t,s0=2.2){const k=spring((t-t0)/0.6);el.style.opacity=t>=t0?1:0;el.style.transform=`scale(${t<t0?s0:s0-(s0-1)*Math.min(1.03,k)}) rotate(-7deg)`;el.style.filter=`blur(${cl(1-(t-t0)/0.1)*12}px)`}
function chip(el,t0,t){const k=spring((t-t0)/0.6);el.style.opacity=t>=t0?1:0;el.style.transform=`translateY(${(1-Math.min(1,k))*30}px) scale(${Math.min(1.05,.6+.4*k)})`}

window.render=function(t,f){
 grain(Math.floor(f/2));
 const [sx,sy]=shake(t);
 $('world').style.transform=`translate(${sx}px,${sy}px)`;
 $('bg').style.transform=`translate(${Math.sin(t*.25)*30}px,${Math.cos(t*.2)*24}px) scale(${1.05+.03*Math.sin(t*.15)})`;
 $('floor').style.transform=`perspective(900px) rotateX(74deg) translateY(${(t*60)%120}px)`;
 vis($('top'),seg(t,.3,.7)*(1-seg(t,SP-.2,SP+.1)));
 // entrada / saída dos painéis
 const out=seg(t,M.plat-.25,M.plat+.25);
 const inA=spring(t/0.8), inB=spring((t-0.15)/0.8);
 // foco: A em [lfoc, rfoc), B em [rfoc, cmpL), ambos depois
 const focA=t>=M.lfoc&&t<M.rfoc-.1, focB=t>=M.rfoc-.1&&t<M.cmpL-.2;
 const dimA=(t>=M.rfoc-.1&&t<M.cmpL-.2)?.42:1, dimB=(t>=M.lfoc&&t<M.rfoc-.1)?.42:1;
 const sA=1+(focA?.03:0), sB=1+(focB?.03:0);
 $('PA').style.transform=`translateY(${(1-Math.min(1,inA))*900}px) translateX(${-900*eio(out)}px) scale(${sA})`;
 $('PB').style.transform=`translateY(${(1-Math.min(1,inB))*900}px) translateX(${900*eio(out)}px) scale(${sB})`;
 $('PA').style.opacity=lerp(1,dimA,1); $('PB').style.opacity=dimB;
 $('PA').style.filter=dimA<1?'saturate(.4)':''; $('PB').style.filter=dimB<1?'saturate(.4)':'';
 $('ringA').style.boxShadow=focA?'inset 0 0 0 6px rgba(37,99,235,.55)':'none'; $('ringB').style.boxShadow=focB?'inset 0 0 0 6px rgba(229,72,77,.55)':'none';
 vis($('PA'),t<M.plat+.3?(dimA):0); vis($('PB'),t<M.plat+.3?(dimB):0);
 // A
 const flA=t>M.hitL&&t<M.hitL+.5?Math.exp(-6*(t-M.hitL)):0;
 chart($('chA'),KA,t,0.2,M.hitL+.6,-1,'STOP −1R','#2563EB',flA,'#0B1533');
 const sk=eo(seg(t,M.duas,M.duas+.4)); $('subA').style.opacity=sk; $('subB').style.opacity=sk;
 stamp($('m1'),M.m1,t); vis($('m1'),t>=M.m1&&t<M.cmpL-.2?1:0);
 chip($('okA'),M.anota,t); if(t>M.cmpL-.2)$('okA').style.opacity=0;
 // B — episódio 1 e 2
 const ep2=t>=M.sem-.15;
 const wipe=Math.sin(Math.PI*seg(t,M.sem-.35,M.sem+.05));
 $('chB').style.opacity=1-wipe; $('chB').style.transform=`translateX(${-60*wipe}px)`;
 if(!ep2){
  const mv=eio(seg(t,M.mv1,M.mv1+.8)), sr=lerp(-1,-2,mv);
  chart($('chB'),KB1,t,0.2,M.zero+.4,sr,mv>.02?'STOP MOVIDO −2R':'STOP −1R',mv>.02?'#F59E0B':'#E5484D',t>M.zero&&t<M.zero+.5?Math.exp(-6*(t-M.zero)):0,'#0B1533');
  $('subB').textContent='O TRADE';
 } else {
  const mv=eio(seg(t,M.mv2,M.mv2+.8)), sr=lerp(-1,-3,mv);
  const fl=t>M.hitR&&t<M.hitR+.5?Math.exp(-6*(t-M.hitR)):0;
  chart($('chB'),KB2,t,M.sem,M.hitR+.6,sr,mv>.02?'STOP MOVIDO −3R':'STOP −1R',mv>.02?'#F59E0B':'#E5484D',fl,'#0B1533');
  $('subB').textContent='SEMANA SEGUINTE'; $('subB').style.background='#E5484D';
 }
 chip($('zB'),M.zero,t); if(t>M.sem-.3)$('zB').style.opacity=0;
 stamp($('habB'),M.hab,t,2.0); if(t>M.sem-.3)$('habB').style.opacity=0;
 stamp($('m3'),M.m3,t); vis($('m3'),t>=M.m3&&t<M.cmpL-.2?1:0);
 // comparação
 [['resA',M.cmpL,'lA',M.custo],['resB',M.cmpR,'lB',M.dec]].forEach(([id,a,l,b])=>{const k=spring((t-a)/0.7);$(id).style.opacity=t>=a?1:0;$(id).style.transform=`translateY(${(1-Math.min(1,k))*120}px)`;
  const kk=eo(seg(t,b,b+.35));$(l).style.opacity=kk;$(l).style.transform=`translateX(${(1-kk)*-20}px)`});
 vis($('selo'),seg(t,.8,1.2)*(1-seg(t,M.plat-.3,M.plat)));
 // D: registro
 {const S=$('D'), inK=eo(seg(t,M.plat,M.plat+.5)), o2=seg(t,SP-.2,SP+.15); vis(S,(t>M.plat&&t<SP+.2)?1:0);
  $('reg').style.transform=`translateY(${(1-inK)*1300}px) scale(${1-o2*.08})`; $('reg').style.filter=`blur(${Math.sin(Math.PI*seg(t,M.plat,M.plat+.5))*12+o2*8}px)`;
  const RA=[M.reg+.3,M.reg+.75,M.reg+1.2];
  ['r1','r2','r3'].forEach((id,i)=>{const k=spring((t-RA[i])/0.7);$(id).style.opacity=t>RA[i]?1:0;$(id).style.transform=`translateY(${(1-Math.min(1,k))*60}px)`;
   const p=$(id).querySelector('.pill'); if(p){const kk=spring((t-M.falha-i*.15)/0.6);p.style.opacity=t>M.falha+i*.15?1:0;p.style.transform=`scale(${Math.min(1.06,kk)})`}});
  const mk=spring((t-M.mesmo)/0.6); const e=$('r1').querySelector('.mk'); e.style.opacity=t>M.mesmo?1:0; e.style.transform=`scale(${Math.min(1.05,mk)}) rotate(-3deg)`;
  $('r1').style.boxShadow=t>M.mesmo?`0 0 0 ${6*eo(seg(t,M.mesmo,M.mesmo+.3))}px rgba(255,212,59,.7)`:'';}
 // F
 {const S=$('F'), k=seg(t,SP-.05,SP+.35); vis(S,t>SP-.06?eo(k):0);
  const lk=spring((t-SP-.05)/0.9); $('logo').style.transform=`scale(${t<SP?0.8:0.8+.2*Math.min(1.02,lk)})`; $('logo').style.opacity=seg(t,SP,SP+.25);
  $('shine').style.left=(-200+1100*eio(seg(t,SP+.9,SP+1.8)))+'px';
  [['eq',SP+.15],['eu',SP+1.6],['ed',SP+1.8]].forEach(([id,a])=>{const kk=eo(seg(t,a,a+.45));$(id).style.opacity=kk;$(id).style.transform=`translateY(${(1-kk)*30}px)`});}
 // legendas
 let gi=-1; for(let i=0;i<G.length;i++){const s=W[G[i][0]][1]-0.12; const e=(i+1<G.length)?W[G[i+1][0]][1]-0.12:SP; if(t>=s&&t<e)gi=i}
 if(t>=SP)gi=-1;
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


def build():
    words, groups = words_and_groups()
    rep = {"__INTER__": INTER, "__LOGO__": LOGO, "__WORDS__": json.dumps(words, ensure_ascii=False), "__GROUPS__": json.dumps(groups),
           "__M__": json.dumps(M), "__SP__": str(SP), "__END__": str(END), "__KR__": json.dumps(KEY_RED, ensure_ascii=False),
           "__KG__": json.dumps(KEY_GREEN, ensure_ascii=False), "__KB__": json.dumps(KEY_BLUE, ensure_ascii=False)}
    h = HTML
    for k, v in rep.items():
        h = h.replace(k, v)
    return h


async def render(out, fps, stills=None):
    from playwright.async_api import async_playwright
    hp = os.path.join(HERE, "duas1.html"); open(hp, "w").write(build())
    async with async_playwright() as p:
        b = await p.chromium.launch()
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
        for f in range(int(round(END * fps))):
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
