# Trial Reel "Caixa-Preta do Trader #1" (TYU-59). Motion 1080x1920, linha do tempo minuto a minuto.
# Base visual: stop40.py / short60.py. Narração Rafael Valente (narr.mp3 = raw.mp3 com OFF s de silêncio no início).
# Uso: python3 cp1.py <saida_sem_audio.mp4> [fps]  |  python3 cp1.py stills t1 t2 ...
import os, sys, json, asyncio, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
INTER = "/usr/share/fonts/opentype/inter"
LOGO = os.path.join(HERE, "tpl", "logo.png")
OFF = 0.35
TAIL = 3.6

# frases da narração (silencedetect em raw.mp3) e legenda (algarismos), cor por palavra: r/g/b/y/None
RAW = [[0.05, 2.01], [2.39, 4.46], [4.99, 6.11], [6.67, 7.70], [7.97, 8.83], [9.19, 9.80], [10.14, 10.73], [11.16, 12.09],
       [12.47, 13.87], [14.23, 15.65], [16.06, 17.22], [17.50, 18.38], [18.68, 19.71], [20.09, 20.94], [21.25, 22.58],
       [22.91, 23.98], [24.23, 24.75], [25.03, 25.97], [26.30, 28.24], [28.69, 30.88], [31.44, 33.22], [33.72, 35.05]]
PH = [[a + OFF, b + OFF] for a, b in RAW]
CAP = [
    [("A", None), ("operação", None), ("durou", None), ("4", "b"), ("minutos.", "b")],
    [("O", None), ("erro", "r"), ("começou", None), ("12", "r"), ("minutos", "r"), ("antes.", None)],
    [("Vamos", None), ("abrir", None), ("a", None), ("caixa-preta.", "y")],
    [("9h38:", "b")], [("um", None), ("stop", None), ("normal.", None)], [("−1R.", "r")], [("Faz", None), ("parte.", None)],
    [("9h41:", "b")], [("o", None), ("preço", None), ("anda", None), ("sem", None), ("você.", None)],
    [("Bate", None), ("a", None), ("vontade", "r"), ("de", "r"), ("devolver.", "r")],
    [("9h46:", "b")], [("você", None), ("dobra", "r"), ("a", "r"), ("mão.", "r")], [("Sem", None), ("anotar", None), ("nada.", None)],
    [("9h50:", "b")], [("entrada", None), ("fora", "r"), ("do", "r"), ("setup.", "r")],
    [("9h54:", "b")], [("stop.", "r")], [("−2R.", "r")],
    [("O", None), ("trade", None), ("ruim", None), ("foi", None), ("só", None), ("o", None), ("último", "b"), ("elo.", "b")],
    [("A", None), ("falha", "r"), ("começou", None), ("na", None), ("decisão", "y"), ("de", "y"), ("recuperar.", "y")],
    [("Registre", "b"), ("o", None), ("que", None), ("veio", None), ("antes", "b"), ("da", None), ("entrada.", None)],
    [("Qual", None), ("foi", None), ("o", None), ("seu", None), ("minuto", "y"), ("zero?", "y")],
]
# frases curtas que se juntam na mesma legenda (hora + frase seguinte)
JOIN = {3: 4, 7: 8, 10: 11, 13: 14, 15: 16}


def words_and_groups():
    words, groups, pw = [], [], []
    for p, toks in enumerate(CAP):
        a, b = PH[p]
        i0 = len(words); pw.append(i0)
        L = sum(len(x) + 1 for x, _ in toks); acc = 0
        for txt, col in toks:
            words.append([txt, round(a + (b - a) * 0.92 * acc / L, 3), col]); acc += len(txt) + 1
    # grupos: por frase, juntando hora + frase seguinte; frases longas em 2 linhas no máximo
    p = 0
    while p < len(CAP):
        if p in JOIN:
            q = JOIN[p]; extra = 1 if q + 1 < len(CAP) and q == 16 else 0
            last = q + extra
            groups.append([pw[p], pw[last] + len(CAP[last]) - 1]); p = last + 1
        else:
            groups.append([pw[p], pw[p] + len(CAP[p]) - 1]); p += 1
    return words, groups, pw


HTML = r"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'InterD';src:url('file://__INTER__/InterDisplay-Black.otf');font-weight:900}
@font-face{font-family:'InterD';src:url('file://__INTER__/InterDisplay-Bold.otf');font-weight:700}
@font-face{font-family:'Inter';src:url('file://__INTER__/Inter-SemiBold.otf');font-weight:600}
@font-face{font-family:'Inter';src:url('file://__INTER__/Inter-Medium.otf');font-weight:500}
@font-face{font-family:'Mono';src:local('DejaVu Sans Mono'),local('Liberation Mono')}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#EEF1F7;font-family:'InterD',sans-serif;color:#0B1533}
#bg{position:absolute;inset:-200px;background:radial-gradient(900px 900px at 82% 8%,rgba(37,99,235,.17),transparent 62%),
  radial-gradient(800px 800px at 8% 92%,rgba(249,115,22,.12),transparent 60%),linear-gradient(180deg,#F7F8FC 0%,#ECEFF6 100%)}
#floor{position:absolute;left:-1200px;width:3480px;top:980px;height:2600px;transform-origin:50% 0;
  background-image:linear-gradient(rgba(11,21,51,.07) 2px,transparent 2px),linear-gradient(90deg,rgba(11,21,51,.07) 2px,transparent 2px);
  background-size:120px 120px;-webkit-mask-image:linear-gradient(180deg,transparent 0%,#000 18%,#000 55%,transparent 100%)}
#world{position:absolute;inset:0}
.scene{position:absolute;inset:0;opacity:0;visibility:hidden}
#vig{position:absolute;inset:0;pointer-events:none;background:radial-gradient(1300px 1700px at 50% 45%,transparent 55%,rgba(11,21,51,.16) 100%)}
#grain{position:absolute;inset:0;width:1080px;height:1920px;mix-blend-mode:overlay;opacity:.10}
#top{position:absolute;left:64px;top:232px;display:flex;align-items:center;gap:14px;opacity:0}
.tag{font-family:'Inter';font-weight:600;font-size:26px;letter-spacing:4px;background:rgba(255,255,255,.85);border:2px solid rgba(11,21,51,.08);padding:12px 20px;border-radius:999px;display:flex;align-items:center;gap:12px;box-shadow:0 8px 24px rgba(11,21,51,.06)}
.tag i{width:12px;height:12px;border-radius:50%;background:#F97316;box-shadow:0 0 0 6px rgba(249,115,22,.18)}
#ep{background:#0B1533;color:#fff;border-color:#0B1533}
#rec{position:absolute;right:64px;top:240px;font:600 26px 'Mono',monospace;color:#0B1533;opacity:0;background:rgba(255,255,255,.85);padding:10px 16px;border-radius:12px;display:flex;align-items:center;gap:10px}
#rec i{width:14px;height:14px;border-radius:50%;background:#E5484D}
#note{position:absolute;left:64px;top:1236px;font:500 24px 'Inter';color:#7A8499;opacity:0}
#cap{position:absolute;left:60px;width:960px;top:1300px;display:flex;flex-wrap:wrap;justify-content:center;align-items:baseline;gap:6px 14px;
  font-family:'InterD';font-weight:900;font-size:68px;line-height:1.12;letter-spacing:-1px}
#cap span{position:relative;display:inline-block;padding:2px 10px;border-radius:16px;color:#0B1533;text-shadow:0 2px 0 rgba(255,255,255,.9),0 0 18px rgba(255,255,255,.9)}
.card{position:absolute;background:rgba(255,255,255,.96);border:2px solid rgba(11,21,51,.06);border-radius:44px;box-shadow:0 40px 90px rgba(11,21,51,.14)}
.hd{font:600 24px 'Inter';letter-spacing:4px;color:#7A8499}
/* A: eixo do tempo (gancho) */
#ax{left:54px;width:972px;top:420px;height:700px}
#ax .hd{position:absolute;left:48px;top:40px}
#axl{position:absolute;left:60px;width:852px;top:430px;height:6px;border-radius:3px;background:#DDE3EE}
.tk{position:absolute;top:410px;width:3px;height:46px;background:#C9D2E3}
.tl{position:absolute;top:470px;width:120px;margin-left:-60px;text-align:center;font:700 28px 'InterD';color:#7A8499}
#opb{position:absolute;top:396px;height:74px;border-radius:16px;background:#2563EB;box-shadow:0 14px 30px rgba(37,99,235,.35)}
#opl{position:absolute;top:250px;font:900 46px 'InterD';color:#2563EB;letter-spacing:-1px;white-space:nowrap;text-align:right;line-height:1.05}
#opl small{display:block;font:700 28px 'InterD';color:#7A8499;letter-spacing:0}
#erb{position:absolute;top:396px;height:74px;border-radius:16px;border:6px dashed #E5484D;background:rgba(229,72,77,.10)}
#erl{position:absolute;top:540px;font:900 52px 'InterD';color:#E5484D;letter-spacing:-1px;white-space:nowrap}
#erl small{display:block;font:700 28px 'InterD';color:#7A8499;letter-spacing:0}
/* B: caixa-preta */
#box{position:absolute;left:190px;top:520px;width:700px;height:560px;perspective:1800px}
#boxb{position:absolute;inset:0;border-radius:48px;background:linear-gradient(160deg,#FF8A3D,#F97316 55%,#D9590B);box-shadow:0 50px 110px rgba(217,89,11,.40),inset 0 -14px 0 rgba(0,0,0,.12)}
#boxb::before{content:'';position:absolute;inset:26px;border-radius:30px;border:4px solid rgba(255,255,255,.35)}
#lid{position:absolute;left:0;right:0;top:0;height:160px;border-radius:48px 48px 18px 18px;background:linear-gradient(180deg,#FFA060,#F97316);transform-origin:50% 0;box-shadow:0 10px 30px rgba(0,0,0,.15)}
#bt1{position:absolute;left:0;width:700px;top:230px;text-align:center;font:900 70px 'InterD';color:#fff;letter-spacing:-2px;line-height:1}
#bt2{position:absolute;left:0;width:700px;top:320px;text-align:center;font:700 34px 'InterD';color:rgba(255,255,255,.9);letter-spacing:6px}
#bstripes{position:absolute;left:60px;right:60px;bottom:60px;height:44px;border-radius:12px;background:repeating-linear-gradient(-45deg,#0B1533 0 22px,#FFD43B 22px 44px);opacity:.9}
#beam{position:absolute;left:190px;top:520px;width:700px;height:560px;border-radius:48px;background:radial-gradient(400px 300px at 50% 10%,rgba(255,212,59,.9),transparent 70%);opacity:0;mix-blend-mode:screen}
/* C: linha do tempo */
#tlc{left:54px;width:972px;top:330px;height:900px}
#clock{position:absolute;left:48px;top:34px;font:900 92px 'InterD';letter-spacing:-3px;color:#0B1533}
#clock small{font:600 24px 'Inter';letter-spacing:4px;color:#7A8499;margin-left:16px;vertical-align:middle}
#rail{position:absolute;left:180px;top:190px;width:8px;height:660px;border-radius:4px;background:#E7EBF3}
#railf{position:absolute;left:180px;top:190px;width:8px;height:0;border-radius:4px;background:linear-gradient(180deg,#7A8499,#F59E0B 45%,#E5484D)}
.ev{position:absolute;left:40px;width:880px;height:120px;opacity:0}
.ev .tm{position:absolute;left:0;top:30px;width:110px;text-align:right;font:900 38px 'InterD';letter-spacing:-1px}
.ev .dot{position:absolute;left:126px;top:28px;width:48px;height:48px;border-radius:50%;background:#fff;border:8px solid #7A8499}
.ev .bx{position:absolute;left:200px;top:0;width:640px;min-height:110px;border-radius:26px;background:#F6F8FC;padding:20px 26px;border:3px solid transparent}
.ev .t1{font:900 40px 'InterD';letter-spacing:-1px;line-height:1.05}
.ev .t2{font:600 26px 'Inter';color:#7A8499;margin-top:8px}
.chip{position:absolute;right:20px;top:20px;font:900 26px 'InterD';padding:8px 14px;border-radius:10px;color:#fff}
#pr{position:absolute;left:880px;top:190px;width:40px;height:660px;border-radius:20px;background:#EEF1F6;overflow:hidden}
#prf{position:absolute;left:0;bottom:0;width:40px;height:0;border-radius:20px;background:linear-gradient(0deg,#F59E0B,#E5484D)}
#prl{position:absolute;left:836px;top:862px;width:130px;text-align:center;font:600 20px 'Inter';letter-spacing:2px;color:#7A8499}
#stamp{position:absolute;left:0;width:1080px;top:1010px;text-align:center;opacity:0;visibility:hidden}
#stamp b{display:inline-block;font:900 96px 'InterD';color:#fff;background:#E5484D;padding:14px 40px 22px;border-radius:26px;letter-spacing:-2px;border:8px solid #fff;box-shadow:0 30px 70px rgba(229,72,77,.35)}
#mz{position:absolute;left:236px;width:664px;height:132px;border-radius:30px;border:7px solid #FFD43B;box-shadow:0 0 0 10px rgba(255,212,59,.25);opacity:0}
#mzc{position:absolute;font:900 30px 'InterD';background:#FFD43B;color:#0B1533;padding:8px 16px;border-radius:12px;opacity:0;white-space:nowrap}
#ue{position:absolute;font:900 26px 'InterD';background:#0B1533;color:#fff;padding:8px 14px;border-radius:10px;opacity:0;white-space:nowrap}
#br{position:absolute;left:204px;width:10px;border-radius:5px;background:#FFD43B;opacity:0}
/* E: registre */
#rh{position:absolute;left:64px;width:950px;top:380px;font:900 88px 'InterD';line-height:1.02;letter-spacing:-3px}
#rh span{display:inline-block;opacity:0;margin-right:18px}
#log{position:absolute;left:64px;width:950px;top:640px;background:#fff;border-radius:40px;padding:40px 46px;border:2px solid rgba(11,21,51,.06);box-shadow:0 40px 90px rgba(11,21,51,.14);opacity:0}
#log h3{font:600 24px 'Inter';letter-spacing:5px;color:#F97316;margin-bottom:16px}
.lr{display:flex;gap:22px;align-items:flex-start;font:700 38px 'InterD';padding:16px 0;border-top:2px solid #EEF1F6;opacity:0}
.lr em{font-style:normal;font:900 34px 'InterD';color:#2563EB;min-width:120px}
.lr span{line-height:1.2}
/* F2: pergunta */
#q{position:absolute;left:0;width:1080px;top:560px;text-align:center}
#q .a{font:900 64px 'InterD';color:#0B1533;letter-spacing:-1px;opacity:0}
#q .b{display:inline-block;margin-top:24px;font:900 150px 'InterD';line-height:.95;letter-spacing:-6px;color:#0B1533;background:#FFD43B;padding:20px 46px 34px;border-radius:40px;opacity:0;box-shadow:0 40px 90px rgba(11,21,51,.18)}
/* G: final */
#F{background:#fff}
#F .logo{position:absolute;left:180px;top:540px;width:720px;height:270px;overflow:hidden}
#F .logo img{width:720px;display:block}
#F .logo .sh{position:absolute;top:-40px;bottom:-40px;width:160px;background:linear-gradient(100deg,transparent,rgba(255,255,255,.85),transparent);transform:skewX(-18deg)}
#F .q{position:absolute;left:90px;width:900px;top:900px;text-align:center;font:900 76px 'InterD';line-height:1.05;letter-spacing:-2px}
#F .u{position:absolute;left:0;width:1080px;top:1130px;text-align:center;font:700 36px 'InterD';color:#2563EB}
#F .d{position:absolute;left:0;width:1080px;top:1186px;text-align:center;font:500 24px 'Inter';color:#8A93A6;line-height:1.5}
</style></head><body>
<div id="bg"></div><div id="floor"></div>
<div id="world">
 <div class="scene" id="A">
  <div class="card" id="ax"><div class="hd">A MANHÃ DO TRADE</div>
   <div id="axl"></div><div id="ticks"></div>
   <div id="erb"></div><div id="opb"></div>
   <div id="opl">A OPERAÇÃO<small>4 minutos</small></div>
   <div id="erl">O ERRO<small>começou 12 minutos antes</small></div>
  </div>
 </div>
 <div class="scene" id="B">
  <div id="box"><div id="boxb"><div id="bt1">CAIXA-PRETA</div><div id="bt2">DO TRADER · #1</div><div id="bstripes"></div></div><div id="lid"></div></div>
  <div id="beam"></div>
 </div>
 <div class="scene" id="C">
  <div class="card" id="tlc">
   <div id="clock">09:38<small>MINUTO A MINUTO</small></div>
   <div id="rail"></div><div id="railf"></div>
   <div class="ev" id="e0"><div class="tm">9h38</div><div class="dot"></div><div class="bx"><div class="t1">Stop normal</div><div class="t2">dentro do plano · faz parte</div><div class="chip" style="background:#7A8499">−1R</div></div></div>
   <div class="ev" id="e1"><div class="tm">9h41</div><div class="dot"></div><div class="bx"><div class="t1">O preço anda sem você</div><div class="t2">vontade de devolver</div></div></div>
   <div class="ev" id="e2"><div class="tm">9h46</div><div class="dot"></div><div class="bx"><div class="t1">Dobra a mão</div><div class="t2">sem anotar nada</div><div class="chip" style="background:#F59E0B">2×</div></div></div>
   <div class="ev" id="e3"><div class="tm">9h50</div><div class="dot"></div><div class="bx"><div class="t1">Entrada fora do setup</div><div class="t2">a operação começa</div></div></div>
   <div class="ev" id="e4"><div class="tm">9h54</div><div class="dot"></div><div class="bx"><div class="t1">Stop</div><div class="t2">a operação termina</div><div class="chip" style="background:#E5484D">−2R</div></div></div>
   <div id="br"></div><div id="mz"></div><div id="mzc">MINUTO ZERO</div><div id="ue">ÚLTIMO ELO</div>
   <div id="pr"><div id="prf"></div></div><div id="prl">PRESSÃO</div>
  </div>
  <div id="stamp"><b>−2R</b></div>
 </div>
 <div class="scene" id="E">
  <div id="rh"><span>Registre</span><span>o</span><span>que</span><span>veio</span><span style="color:#2563EB">antes</span><span>da</span><span>entrada.</span></div>
  <div id="log"><h3>NO SEU DIÁRIO</h3>
   <div class="lr" id="l1"><em>9h38</em><span>Stop dentro do plano</span></div>
   <div class="lr" id="l2"><em>9h41</em><span>Senti: pressa de devolver</span></div>
   <div class="lr" id="l3"><em>9h46</em><span style="color:#E5484D">Falha: aumentou a mão</span></div>
  </div>
 </div>
 <div class="scene" id="Q"><div id="q"><div class="a" id="qa">Qual foi o seu</div><div class="b" id="qb">MINUTO<br>ZERO?</div></div></div>
 <div class="scene" id="F">
  <div class="logo" id="logo"><img src="file://__LOGO__"><div class="sh" id="shine"></div></div>
  <div class="q" id="eq">O erro começa antes da entrada.</div>
  <div class="u" id="eu">tradeyouup.net</div>
  <div class="d" id="ed">Exemplo ilustrativo, sem ativo e sem custos operacionais.<br>Conteúdo educativo. Não é recomendação de investimento.</div>
 </div>
</div>
<div id="vig"></div>
<div id="top"><div class="tag"><i></i>CAIXA-PRETA DO TRADER</div><div class="tag" id="ep">#1</div></div>
<div id="rec"><i></i><span id="rect">REC 09:38</span></div>
<div id="note">Exemplo ilustrativo · conta demo · resultados em R</div>
<div id="cap"></div>
<canvas id="grain" width="360" height="640"></canvas>
<script>
const W=__WORDS__, G=__GROUPS__, P=__PH__, PW=__PW__;
const SP=P[P.length-1][1]+0.15, END=SP+__TAIL__;
const $=id=>document.getElementById(id);
const cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)), lerp=(a,b,k)=>a+(b-a)*k, seg=(t,a,b)=>cl((t-a)/(b-a));
const eo=x=>1-Math.pow(1-cl(x),3), eio=x=>{x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2};
const eexp=x=>{x=cl(x);return x===1?1:1-Math.pow(2,-10*x)};
const spring=(x,f=1)=>{x=Math.max(0,x);return 1-Math.exp(-7*x)*Math.cos(10*f*x)};
function vis(el,o){el.style.opacity=o;el.style.visibility=o<=0.001?'hidden':'visible'}
const ph=i=>P[i];
const M={op:ph(0)[0]+0.5, er:ph(1)[0]+0.3, bIn:ph(2)[0]-0.2, open:ph(2)[0]+0.7, cIn:ph(3)[0]-0.25,
 ev:[ph(3)[0],ph(7)[0],ph(10)[0],ph(13)[0],ph(15)[0]], stamp:ph(17)[0], ue:ph(18)[0]+0.9, mz:ph(19)[0]+0.4,
 eIn:ph(20)[0]-0.2, qIn:ph(21)[0]-0.15};
const MIN=['09:38','09:41','09:46','09:50','09:54'];
// grão
const gc=$('grain').getContext('2d'), gimg=gc.createImageData(360,640);
function grain(f){let s=f*7919+1;const d=gimg.data;for(let i=0;i<d.length;i+=4){s=(s*16807)%2147483647;const v=s%255;d[i]=d[i+1]=d[i+2]=v;d[i+3]=255}gc.putImageData(gimg,0,0)}
const HITS=[[M.er,14],[M.open,10],[M.ev[2],8],[M.ev[4],16],[M.stamp,20],[M.mz,10]];
function shake(t){let x=0,y=0;HITS.forEach(([h,a],j)=>{const d=t-h;if(d>=0&&d<.5){const k=a*Math.exp(-9*d);x+=k*Math.sin(d*90+j);y+=k*Math.cos(d*77+j*2)}});return [x,y]}
// eixo A: 09:34 → 09:58, x = 60 + (m-34)*35.5
const AX=m=>60+(m-34)*35.5;
{let h='';for(let m=34;m<=58;m+=2){h+=`<div class="tk" style="left:${AX(m)}px;${m%4==2?'':'height:30px;top:418px'}"></div>`;if(m%4==2)h+=`<div class="tl" style="left:${AX(m)}px">9h${String(m).padStart(2,'0')}</div>`}$('ticks').innerHTML=h;}
// linha do tempo C
const EY=i=>200+i*134;
['e0','e1','e2','e3','e4'].forEach((id,i)=>{$(id).style.top=EY(i)+'px'});
const DOTC=['#7A8499','#F59E0B','#F59E0B','#E5484D','#E5484D'], PRS=[.16,.42,.66,.84,1];
// legendas
const capEl=$('cap');let capG=-1,capSpans=[];
const COL={r:'#E5484D',g:'#16A34A',b:'#2563EB',y:'#D97706'}, COLBG={y:'#FFD43B'};
function buildCap(gi){capEl.innerHTML='';capSpans=[];const [a,b]=G[gi];for(let i=a;i<=b;i++){const s=document.createElement('span');s.textContent=W[i][0];capEl.appendChild(s);capSpans.push([i,s])}}

window.render=function(t,f){
 grain(Math.floor(f/2));
 const [sx,sy]=shake(t); $('world').style.transform=`translate(${sx}px,${sy}px)`;
 $('bg').style.transform=`translate(${Math.sin(t*.25)*30}px,${Math.cos(t*.2)*24}px) scale(${1.05+.03*Math.sin(t*.15)})`;
 $('floor').style.transform=`perspective(900px) rotateX(74deg) translateY(${(t*40)%120}px)`;
 const topO=seg(t,.15,.55)*(1-seg(t,SP-.2,SP+.1)); vis($('top'),topO);
 // REC + relógio durante C
 const inC=t>M.cIn-.1&&t<M.eIn+.2;
 let cur=-1; M.ev.forEach((a,i)=>{if(t>=a)cur=i});
 vis($('rec'),(inC?seg(t,M.cIn,M.cIn+.3):0)*topO); $('rec').firstChild.style.opacity=(Math.floor(t*2)%2)?1:.25;
 $('rect').textContent='REC '+(cur<0?'09:38':MIN[cur]);
 vis($('note'),seg(t,M.cIn+.3,M.cIn+.7)*(1-seg(t,M.eIn-.3,M.eIn)));
 // ---------- A: eixo
 {const S=$('A'), on=t<M.bIn+.2; vis(S,on?1:0);
  const out=seg(t,M.bIn-.25,M.bIn+.1); S.style.transform=`translateX(${-1300*eio(out)}px)`; S.style.filter=`blur(${Math.sin(Math.PI*out)*14}px)`;
  const k1=spring((t-0.05)/0.9); $('ax').style.transform=`translateY(${(1-Math.min(1,k1))*-160}px)`; $('ax').style.opacity=cl((t-.05)/.15);
  const ok=eexp(seg(t,M.op,M.op+.6)); $('opb').style.left=AX(50)+'px'; $('opb').style.width=(AX(54)-AX(50))*ok+'px';
  $('opl').style.opacity=eo(seg(t,M.op+.1,M.op+.5)); $('opl').style.left=(AX(54)-340)+'px'; $('opl').style.width='340px';
  const ek=eio(seg(t,M.er,M.er+.9)); const x0=lerp(AX(50),AX(38),ek); $('erb').style.left=x0+'px'; $('erb').style.width=(AX(50)-x0+10)+'px'; $('erb').style.opacity=t>=M.er?1:0;
  const lk=spring((t-M.er-.5)/0.6); $('erl').style.left=(AX(38))+'px'; $('erl').style.opacity=cl((t-M.er-.5)/.12); $('erl').style.transform=`translateY(${(1-Math.min(1,lk))*40}px)`;
 }
 // ---------- B: caixa
 {const S=$('B'), on=t>M.bIn-.1&&t<M.cIn+.25; vis(S,on?1:0);
  const ik=spring((t-M.bIn)/0.8), out=seg(t,M.cIn-.2,M.cIn+.2);
  $('box').style.transform=`translateY(${(1-Math.min(1,ik))*900}px) rotate(${(1-Math.min(1,ik))*-8}deg) scale(${1+1.6*eio(out)})`;
  S.style.opacity=on?1-eo(out):0;
  const lid=eio(seg(t,M.open,M.open+.5)); $('lid').style.transform=`rotateX(${lid*-110}deg)`;
  $('beam').style.opacity=eo(seg(t,M.open+.1,M.open+.5))*(1-out);
 }
 // ---------- C: linha do tempo + D (último elo / minuto zero)
 {const S=$('C'), on=inC; vis(S,on?1:0);
  const ik=eexp(seg(t,M.cIn-.1,M.cIn+.35)), out=seg(t,M.eIn-.2,M.eIn+.15);
  S.style.transform=`translateY(${(1-ik)*1500-eio(out)*1600}px)`; S.style.filter=`blur(${Math.sin(Math.PI*seg(t,M.cIn-.1,M.cIn+.35))*12+Math.sin(Math.PI*out)*14}px)`;
  // relógio
  const ck=cur<0?0:spring((t-M.ev[cur])/0.5); $('clock').firstChild.textContent=cur<0?'09:38':MIN[cur];
  $('clock').style.transform=`translateY(${(1-Math.min(1,ck))*-30}px)`; $('clock').style.color=cur>=3?'#E5484D':'#0B1533';
  // eventos
  const dimK=eo(seg(t,M.ue-.3,M.ue+.2));
  ['e0','e1','e2','e3','e4'].forEach((id,i)=>{const a=M.ev[i], k=spring((t-a)/0.7), el=$(id);
   el.style.opacity=cl((t-a)/.12)*(i>0&&t>M.mz?1-.55*eo(seg(t,M.mz,M.mz+.4)):1); el.style.transform=`translateX(${(1-Math.min(1,k))*120}px)`;
   const dot=el.querySelector('.dot'); dot.style.borderColor=DOTC[i]; dot.style.transform=`scale(${t<a?0:Math.min(1.15,spring((t-a)/0.5))})`;
   el.querySelector('.tm').style.color=DOTC[i]==='#7A8499'?'#0B1533':DOTC[i];
   const bx=el.querySelector('.bx'); bx.style.borderColor=(i===4&&t>M.stamp)?'#E5484D':(i===4&&t>M.ue?'#0B1533':'transparent');
   if(i===4)bx.style.background=t>M.stamp?'#FDECEC':'#F6F8FC';});
  // trilho preenchido
  const fh=cur<0?0:(EY(cur)-200+52)*eo(seg(t,M.ev[cur],M.ev[cur]+.5))+(cur>0?(EY(cur-1)-200+52)*(1-eo(seg(t,M.ev[cur],M.ev[cur]+.5))):0);
  $('railf').style.height=Math.max(0,fh)+'px';
  // pressão
  const pv=cur<0?0:lerp(cur>0?PRS[cur-1]:0,PRS[cur],eo(seg(t,M.ev[cur],M.ev[cur]+.6)));
  $('prf').style.height=(660*pv*(1-.0*seg(t,M.mz,M.mz+1)))+'px';
  // carimbo −2R
  const sk=spring((t-M.stamp)/0.6); vis($('stamp'),t>=M.stamp&&t<M.stamp+1.3?1-seg(t,M.stamp+.9,M.stamp+1.2):0);
  $('stamp').style.transform=`rotate(-4deg) scale(${t<M.stamp?2.2:2.2-1.2*Math.min(1.03,sk)})`; $('stamp').style.filter=`blur(${cl(1-(t-M.stamp)/0.1)*10}px)`;
  // último elo
  const uk=spring((t-M.ue)/0.6); $('ue').style.opacity=cl((t-M.ue)/.12)*(1-.6*eo(seg(t,M.mz,M.mz+.4))); $('ue').style.left='560px'; $('ue').style.top=(EY(4)-22)+'px';
  $('ue').style.transform=`scale(${t<M.ue?0:Math.min(1.08,uk)})`;
  // minuto zero
  const mk=spring((t-M.mz)/0.7); $('mz').style.top=(EY(0)-11)+'px'; $('mz').style.opacity=cl((t-M.mz)/.15); $('mz').style.transform=`scale(${t<M.mz?1.3:1.3-.3*Math.min(1.02,mk)})`;
  $('mzc').style.left='600px'; $('mzc').style.top=(EY(0)-30)+'px'; $('mzc').style.opacity=cl((t-M.mz-.25)/.12); $('mzc').style.transform=`rotate(-3deg) scale(${t<M.mz+.25?0:Math.min(1.1,spring((t-M.mz-.25)/0.5))})`;
  const bk=eio(seg(t,M.mz+.5,M.mz+1.6)); $('br').style.top=(EY(0)+122)+'px'; $('br').style.height=((EY(4)+60)-(EY(0)+122))*bk+'px'; $('br').style.opacity=t>M.mz+.5?.9:0;
 }
 // ---------- E: registre
 {const S=$('E'), on=t>M.eIn-.1&&t<M.qIn+.2; vis(S,on?1:0);
  const ik=eexp(seg(t,M.eIn-.1,M.eIn+.35)), out=seg(t,M.qIn-.2,M.qIn+.15);
  S.style.transform=`translateY(${(1-ik)*1500-eio(out)*1600}px)`; S.style.filter=`blur(${Math.sin(Math.PI*out)*14}px)`;
  [...$('rh').children].forEach((s,i)=>{const a=M.eIn+.1+i*.11, k=spring((t-a)/0.6);s.style.opacity=cl((t-a)/.08);s.style.transform=`translateY(${(1-Math.min(1,k))*50}px)`});
  const la=M.eIn+.3; $('log').style.opacity=seg(t,la,la+.2); $('log').style.transform=`translateY(${(1-eo(seg(t,la,la+.4)))*80}px)`;
  ['l1','l2','l3'].forEach((id,i)=>{const a=la+.2+i*.22, k=eo(seg(t,a,a+.3));$(id).style.opacity=k;$(id).style.transform=`translateX(${(1-k)*40}px)`});
 }
 // ---------- Q: pergunta
 {const S=$('Q'), on=t>M.qIn-.1&&t<SP+.2; vis(S,on?1:0);
  const out=seg(t,SP-.12,SP+.15); S.style.opacity=on?1-out:0;
  $('qa').style.opacity=eo(seg(t,M.qIn,M.qIn+.3)); $('qa').style.transform=`translateY(${(1-eo(seg(t,M.qIn,M.qIn+.3)))*40}px)`;
  const bk=spring((t-M.qIn-.6)/0.7); $('qb').style.opacity=cl((t-M.qIn-.6)/.1); $('qb').style.transform=`rotate(-2deg) scale(${t<M.qIn+.6?1.8:1.8-.8*Math.min(1.03,bk)})`;
 }
 // ---------- F: final
 {const S=$('F'), k=seg(t,SP-.05,SP+.35); vis(S,t>SP-.06?eo(k):0);
  const lk=spring((t-SP-.05)/0.9); $('logo').style.transform=`scale(${t<SP?0.8:0.8+.2*Math.min(1.02,lk)})`; $('logo').style.opacity=seg(t,SP,SP+.25);
  $('shine').style.left=(-200+1100*eio(seg(t,SP+.6,SP+1.5)))+'px';
  [['eq',SP+.5],['eu',SP+.85],['ed',SP+1.0]].forEach(([id,a])=>{const kk=eo(seg(t,a,a+.45));$(id).style.opacity=kk;$(id).style.transform=`translateY(${(1-kk)*30}px)`});}
 // ---------- legendas (somem na pergunta final, que já está na tela)
 let gi=-1; for(let i=0;i<G.length;i++){const s=W[G[i][0]][1]-0.12; const e=(i+1<G.length)?W[G[i+1][0]][1]-0.12:SP+0.05; if(t>=s&&t<e)gi=i}
 if(t>=M.qIn)gi=-1;
 if(gi!==capG){capG=gi; if(gi>=0)buildCap(gi); else capEl.innerHTML=''}
 if(gi>=0){const gs=W[G[gi][0]][1]-0.12, gk=eo(seg(t,gs,gs+.18)); capEl.style.opacity=gk; capEl.style.transform=`translateY(${(1-gk)*24}px)`;
  capSpans.forEach(([i,s])=>{const w=W[i], on=t>=w[1]-0.04, act=on&&(i+1>G[gi][1]||t<W[i+1][1]-0.04);
   s.style.opacity=on?1:.22; const c=w[2]?COL[w[2]]:null;
   if(act){const pk=spring((t-w[1]+0.04)/0.45); s.style.background=w[2]?(COLBG[w[2]]||c):'#0B1533'; s.style.color=w[2]==='y'?'#0B1533':'#fff'; s.style.textShadow='none';
    s.style.transform=`scale(${1+.08*Math.max(0,1-(t-w[1])/0.35)}) translateY(${-4*Math.min(1,pk)}px)`; s.style.boxShadow='0 10px 24px rgba(11,21,51,.22)';}
   else{s.style.background='transparent'; s.style.color=c||'#0B1533'; s.style.textShadow=''; s.style.transform='none'; s.style.boxShadow='none';}});}
 else capEl.style.opacity=0;
};
</script></body></html>"""


def build():
    words, groups, pw = words_and_groups()
    rep = {"__INTER__": INTER, "__LOGO__": LOGO, "__WORDS__": json.dumps(words, ensure_ascii=False), "__GROUPS__": json.dumps(groups),
           "__PH__": json.dumps(PH), "__PW__": json.dumps(pw), "__TAIL__": str(TAIL)}
    h = HTML
    for k, v in rep.items(): h = h.replace(k, v)
    return h, PH[-1][1] + 0.15 + TAIL


async def render(out, fps, stills=None):
    from playwright.async_api import async_playwright
    html, end = build()
    hp = os.path.join(HERE, "cp1.html"); open(hp, "w").write(html)
    async with async_playwright() as p:
        b = await p.chromium.launch()
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
        for f in range(0, int(round(end * fps))):
            await pg.evaluate("render(%f,%d)" % (f / fps, f))
            ff.stdin.write(await pg.screenshot(type="jpeg", quality=93))
        print("errors:", errs); await b.close()
    ff.stdin.close(); ff.wait()


if __name__ == "__main__":
    if sys.argv[1] == "stills":
        asyncio.run(render(None, 30, [float(x) for x in sys.argv[2:]]))
    else:
        fps = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        asyncio.run(render(sys.argv[1], fps))
        print("ok", sys.argv[1])
