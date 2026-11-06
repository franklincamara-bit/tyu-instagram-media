# Short "Mover o stop 'só um pouquinho': quanto custa" (VID-40) — série Erro em câmera lenta. Motion 1080x1920.
# Base visual: short60.py / short81_v2.py. Palavras com tempo da transcrição (whisper_words.json, deslocadas para narr.mp3).
# Uso: python3 stop40.py <saida_sem_audio.mp4> [fps]  |  python3 stop40.py stills t1 t2 ...
import os, sys, json, asyncio, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
INTER = "/usr/share/fonts/opentype/inter"
LOGO = os.path.join(HERE, "tpl", "logo.png")
SHIFT = 0.90           # narr.mp3 = bruto a partir de 0,98 s; whisper adianta ~0,08 s
TAIL = 3.6

# (legenda, índice da palavra na transcrição, cor) — cor: r vermelho, g verde, b azul, None
CAP = [
    [("Mover", 0, None), ("o", 1, None), ("stop", 2, "r"), ("“só", 3, None), ("um", 4, None), ("pouquinho”.", 5, None)],
    [("Parece", 6, None), ("inofensivo.", 7, None)],
    [("Faz", 8, None), ("a", 9, None), ("conta.", 10, "b")],
    [("Stop", 11, "r"), ("de", 12, None), ("20", 13, "r"), ("pontos", 14, None), ("e", 15, None), ("alvo", 16, "g"), ("de", 17, None), ("30:", 18, "g")],
    [("você", 19, None), ("precisa", 20, None), ("acertar", 21, None), ("40%", 22, "b"), ("para", 24, None), ("empatar.", 25, None)],
    [("Moveu", 26, None), ("o", 27, None), ("stop", 28, "r"), ("para", 29, None), ("30?", 30, "r")],
    [("Agora", 31, None), ("precisa", 32, None), ("de", 33, None), ("50%.", 34, "r")],
    [("Para", 35, None), ("40?", 36, "r")],
    [("57%.", 37, "r")],
    [("Com", 38, None), ("o", 39, None), ("mesmo", 40, None), ("acerto", 41, None), ("de", 42, None), ("45%,", 43, "b")],
    [("a", 44, None), ("estratégia", 45, None), ("passa", 46, None), ("de", 47, None), ("+2,5", 48, "g"), ("para", 51, None), ("−3", 52, "r"), ("pontos", 54, None), ("por", 55, None), ("trade.", 56, None)],
    [("Às", 57, None), ("vezes", 58, None), ("o", 59, None), ("preço", 60, None), ("volta.", 61, "g")],
    [("Mas", 62, None), ("o", 63, None), ("stop", 64, None), ("que", 65, None), ("você", 66, None), ("move", 67, None), ("vira", 68, None), ("o", 69, None), ("seu", 70, None), ("stop", 71, "r"), ("de", 72, "r"), ("verdade.", 73, "r")],
    [("Escreva", 74, None), ("no", 75, None), ("plano:", 76, None), ("stop", 77, "b"), ("só", 78, "b"), ("anda", 79, "b"), ("a", 80, "b"), ("favor.", 81, "b")],
]
# limites de cada frase na narração (silencedetect), em segundos de narr.mp3
PH = [[0.10, 1.73], [2.28, 3.27], [3.69, 4.30], [4.78, 7.10], [7.49, 10.17], [10.75, 11.87], [12.28, 13.59], [14.03, 14.64],
      [14.94, 16.08], [16.58, 18.30], [18.98, 23.24], [23.74, 25.20], [25.63, 28.80], [29.32, 32.34]]


def words_and_groups():
    ww = json.load(open(os.path.join(HERE, "whisper_words.json")))
    words, groups, pw = [], [], []
    for p, toks in enumerate(CAP):
        a, b = PH[p]
        i0 = len(words); pw.append(i0)
        for j, (txt, wi, col) in enumerate(toks):
            t = ww[wi][1] - SHIFT
            t = min(max(t, a), b - 0.05)
            if j == 0: t = a
            if words and words[-1][1] >= t: t = words[-1][1] + 0.04
            words.append([txt, round(t, 3), col])
        n = len(toks); parts = 1 if n <= 6 else 2
        size = -(-n // parts)
        for s in range(0, n, size): groups.append([i0 + s, i0 + min(n, s + size) - 1])
    return words, groups, pw


HTML = r"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'InterD';src:url('file://__INTER__/InterDisplay-Black.otf');font-weight:900}
@font-face{font-family:'InterD';src:url('file://__INTER__/InterDisplay-Bold.otf');font-weight:700}
@font-face{font-family:'Inter';src:url('file://__INTER__/Inter-SemiBold.otf');font-weight:600}
@font-face{font-family:'Inter';src:url('file://__INTER__/Inter-Medium.otf');font-weight:500}
@font-face{font-family:'Mono';src:local('DejaVu Sans Mono'),local('Liberation Mono')}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#EEF1F7;font-family:'InterD',sans-serif;color:#0B1533}
#bg{position:absolute;inset:-200px;background:radial-gradient(900px 900px at 80% 10%,rgba(37,99,235,.16),transparent 62%),
  radial-gradient(800px 800px at 10% 92%,rgba(229,72,77,.10),transparent 60%),linear-gradient(180deg,#F7F8FC 0%,#ECEFF6 100%)}
#floor{position:absolute;left:-1200px;width:3480px;top:980px;height:2600px;transform-origin:50% 0;
  background-image:linear-gradient(rgba(11,21,51,.07) 2px,transparent 2px),linear-gradient(90deg,rgba(11,21,51,.07) 2px,transparent 2px);
  background-size:120px 120px;-webkit-mask-image:linear-gradient(180deg,transparent 0%,#000 18%,#000 55%,transparent 100%)}
#world{position:absolute;inset:0;transform-origin:540px 860px}
.scene{position:absolute;inset:0;opacity:0;visibility:hidden}
#vig{position:absolute;inset:0;pointer-events:none;background:radial-gradient(1300px 1700px at 50% 45%,transparent 55%,rgba(11,21,51,.16) 100%)}
#slow{position:absolute;inset:0;pointer-events:none;background:linear-gradient(180deg,rgba(11,21,51,.10),transparent 18%,transparent 82%,rgba(11,21,51,.10));opacity:0}
#grain{position:absolute;inset:0;width:1080px;height:1920px;mix-blend-mode:overlay;opacity:.10}
#top{position:absolute;left:64px;top:232px;display:flex;align-items:center;gap:14px;opacity:0}
.tag{font-family:'Inter';font-weight:600;font-size:26px;letter-spacing:4px;background:rgba(255,255,255,.8);border:2px solid rgba(11,21,51,.08);padding:12px 20px;border-radius:999px;display:flex;align-items:center;gap:12px;box-shadow:0 8px 24px rgba(11,21,51,.06)}
.tag i{width:12px;height:12px;border-radius:50%;background:#E5484D;box-shadow:0 0 0 6px rgba(229,72,77,.15)}
#rp{background:#0B1533;color:#fff;border-color:#0B1533}
#rp i{background:#FFD43B;box-shadow:0 0 0 6px rgba(255,212,59,.25)}
#tc{position:absolute;right:64px;top:244px;font:500 26px 'Mono',monospace;color:#0B1533;opacity:0;background:rgba(255,255,255,.8);padding:8px 14px;border-radius:10px}
#prog{position:absolute;left:64px;top:300px;display:flex;gap:8px;opacity:0}
#prog b{display:block;width:70px;height:6px;border-radius:6px;background:rgba(11,21,51,.10);overflow:hidden}
#prog b i{display:block;height:100%;width:0;background:#0B1533;border-radius:6px}
#note{position:absolute;left:64px;top:1236px;font:500 24px 'Inter';color:#7A8499;opacity:0}
#cap{position:absolute;left:60px;width:880px;top:1300px;display:flex;flex-wrap:wrap;justify-content:center;align-items:baseline;gap:6px 14px;
  font-family:'InterD';font-weight:900;font-size:68px;line-height:1.12;letter-spacing:-1px}
#cap span{position:relative;display:inline-block;padding:2px 10px;border-radius:16px;color:#0B1533;text-shadow:0 2px 0 rgba(255,255,255,.9),0 0 18px rgba(255,255,255,.9)}
.card{position:absolute;background:rgba(255,255,255,.95);border:2px solid rgba(11,21,51,.06);border-radius:44px;box-shadow:0 40px 90px rgba(11,21,51,.14)}
.hd{font:600 24px 'Inter';letter-spacing:4px;color:#7A8499}
/* A: gráfico */
#chart{left:54px;width:972px;top:370px;height:840px;overflow:hidden}
#chart .hd{position:absolute;left:48px;top:40px}
#chart svg{position:absolute;left:0;top:0}
.lbl{position:absolute;font:900 34px 'InterD';padding:8px 16px;border-radius:12px;color:#fff;white-space:nowrap}
#stopL{background:#E5484D}
#stopG{background:rgba(229,72,77,.18);color:#E5484D;border:2px dashed #E5484D}
#hand{position:absolute;width:86px;height:86px;opacity:0}
#faz{position:absolute;left:0;width:1080px;top:600px;text-align:center;opacity:0;visibility:hidden}
#faz b{display:inline-block;font:900 120px 'InterD';color:#fff;background:#0B1533;padding:20px 50px 28px;border-radius:32px;letter-spacing:-3px;box-shadow:0 30px 70px rgba(11,21,51,.35)}
#sr{position:absolute;left:0;width:1080px;top:520px;text-align:center;opacity:0;visibility:hidden}
#sr b{display:inline-block;font:900 104px 'InterD';color:#fff;background:#E5484D;padding:16px 44px 24px;border-radius:28px;letter-spacing:-2px;box-shadow:0 30px 70px rgba(229,72,77,.35);border:8px solid #fff}
#volta{position:absolute;opacity:0;font:700 30px 'InterD';color:#16A34A;background:#E2F6EE;padding:8px 16px;border-radius:12px}
/* B: régua + medidor */
#rul{left:54px;width:440px;top:370px;height:840px}
#rul .hd{position:absolute;left:40px;top:40px}
#axis{position:absolute;left:210px;top:110px;width:8px;height:690px;border-radius:4px;background:#E7EBF3}
.mark{position:absolute;left:96px;width:300px;height:8px;border-radius:4px}
.mark span{position:absolute;right:0;top:-58px;font:900 52px 'InterD';letter-spacing:-1px}
#mT{background:#16A34A}#mT span{color:#16A34A}
#mE{background:#0B1533;height:6px}#mE span{color:#0B1533;font-size:30px;top:-44px;font-weight:700}
#mS{background:#E5484D}#mS span{color:#E5484D;top:14px}
#mS0{background:repeating-linear-gradient(90deg,#E5484D 0 14px,transparent 14px 24px);opacity:0;height:6px}
#zr{position:absolute;left:96px;width:300px;background:rgba(229,72,77,.10);border-radius:8px}
#zg{position:absolute;left:96px;width:300px;background:rgba(22,163,74,.10);border-radius:8px}
#gau{left:518px;width:508px;top:370px;height:840px}
#gau .hd{position:absolute;left:40px;top:40px;width:430px;line-height:1.35}
#gsv{position:absolute;left:24px;top:150px}
#gnum{position:absolute;left:0;width:508px;top:300px;text-align:center;font:900 150px 'InterD';letter-spacing:-7px}
#gsub{position:absolute;left:0;width:508px;top:470px;text-align:center;font:700 30px 'InterD';color:#7A8499}
#hist{position:absolute;left:40px;top:560px;width:430px;font:700 34px 'InterD';line-height:1.6}
#hist div{display:flex;justify-content:space-between;opacity:0;border-top:2px solid #EEF1F6;padding-top:6px}
#hist em{font-style:normal;color:#7A8499;font-weight:700}
/* D: contadores */
#dh{position:absolute;left:0;width:1080px;top:380px;text-align:center}
#dh b{display:inline-block;font:900 52px 'InterD';color:#fff;background:#2563EB;padding:12px 30px 16px;border-radius:20px;letter-spacing:-1px}
#cols{position:absolute;left:54px;width:972px;top:520px;display:flex;gap:28px}
#cols .c{flex:1;min-height:640px;background:#fff;border-radius:40px;padding:44px 38px 40px;border:2px solid rgba(11,21,51,.06);box-shadow:0 30px 70px rgba(11,21,51,.14);opacity:0}
#cols .k{font:600 24px 'Inter';letter-spacing:4px;color:#7A8499}
#cols .s{font:900 70px 'InterD';letter-spacing:-2px;margin-top:8px}
#cols .v{font:900 176px 'InterD';letter-spacing:-6px;margin-top:20px;line-height:1}
#cols .u{font:700 30px 'InterD';color:#7A8499;margin-top:8px}
#cols .f{font:500 25px 'Inter';color:#7A8499;margin-top:22px;border-top:2px solid #EEF1F6;padding-top:16px;line-height:1.45}
#arr{position:absolute;left:504px;top:820px;width:72px;height:72px;border-radius:50%;background:#0B1533;color:#fff;font:900 44px 'InterD';display:flex;align-items:center;justify-content:center;opacity:0;box-shadow:0 12px 30px rgba(11,21,51,.3)}
/* F: plano */
#dq{position:absolute;left:64px;width:950px;top:380px;font:900 92px 'InterD';line-height:1.02;letter-spacing:-3px}
#dq span{display:inline-block;opacity:0;margin-right:20px}
#plan{position:absolute;left:64px;width:950px;top:720px;perspective:1600px}
#plan .in{background:#fff;border-radius:40px;padding:44px 48px 40px;border:2px solid rgba(11,21,51,.06);box-shadow:0 40px 90px rgba(11,21,51,.14);transform-origin:50% 100%}
#plan h3{font:600 24px 'Inter';letter-spacing:5px;color:#2563EB;margin-bottom:20px}
.pr{display:flex;align-items:center;gap:24px;padding:22px 0;border-top:2px solid #EEF1F6;font:700 44px 'InterD';opacity:0}
.pr .bx{width:64px;height:64px;border-radius:16px;border:4px solid #C9D2E3;display:flex;align-items:center;justify-content:center;flex:none}
.pr .bx svg{width:44px;height:44px}
/* G: final */
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
 <div class="scene" id="A">
  <div class="card" id="chart"><div class="hd" id="chd">O TRADE</div>
   <svg width="972" height="840" id="csv"><g id="cg"></g>
    <line id="tgt" x1="40" x2="932" stroke="#16A34A" stroke-width="5" stroke-dasharray="16 12"/>
    <line id="sl0" x1="40" x2="932" stroke="#E5484D" stroke-width="5" stroke-dasharray="14 10" opacity="0"/>
    <line id="sl" x1="40" x2="932" stroke="#E5484D" stroke-width="7"/>
    <line id="entry" x1="40" x2="932" stroke="#0B1533" stroke-width="3" opacity=".35"/>
   </svg>
   <div class="lbl" id="tgtL" style="background:#16A34A">ALVO +30</div>
   <div class="lbl" id="stopL">STOP −20</div>
   <div class="lbl" id="entL" style="background:#0B1533;font-size:26px">ENTRADA</div>
   <svg id="hand" viewBox="0 0 24 24"><path d="M9 11V5.5a1.5 1.5 0 0 1 3 0V10m0-.5V4a1.5 1.5 0 0 1 3 0v6m0-1a1.5 1.5 0 0 1 3 0v4.5a6.5 6.5 0 0 1-6.5 6.5h-.6a6 6 0 0 1-4.6-2.2L4.2 14a1.6 1.6 0 0 1 2.4-2.1L9 14" fill="#fff" stroke="#0B1533" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"/></svg>
   <div id="volta">às vezes volta</div>
  </div>
  <div id="faz"><b>FAZ A CONTA.</b></div>
  <div id="sr"><b>STOP REAL</b></div>
 </div>
 <div class="scene" id="B">
  <div class="card" id="rul"><div class="hd">O PLANO</div><div id="axis"></div><div id="zg"></div><div id="zr"></div>
   <div class="mark" id="mT"><span>+30</span></div><div class="mark" id="mE"><span>entrada</span></div>
   <div class="mark" id="mS0"></div><div class="mark" id="mS"><span id="mSt">−20</span></div></div>
  <div class="card" id="gau"><div class="hd">ACERTO MÍNIMO PARA EMPATAR</div>
   <svg id="gsv" width="460" height="260" viewBox="0 0 460 260"><path d="M30 230 A200 200 0 0 1 430 230" fill="none" stroke="#EEF1F6" stroke-width="40" stroke-linecap="round"/>
    <path id="garc" d="M30 230 A200 200 0 0 1 430 230" fill="none" stroke="#2563EB" stroke-width="40" stroke-linecap="round" pathLength="100" stroke-dasharray="0 100"/></svg>
   <div id="gnum">0%</div><div id="gsub">stop ÷ (alvo + stop)</div>
   <div id="hist"><div id="h1"><span>stop 20</span><em>→</em><span style="color:#2563EB">40%</span></div>
    <div id="h2"><span>stop 30</span><em>→</em><span style="color:#E5484D">50%</span></div>
    <div id="h3"><span>stop 40</span><em>→</em><span style="color:#E5484D">57%</span></div></div>
  </div>
 </div>
 <div class="scene" id="D">
  <div id="dh"><b>MESMO ACERTO: 45%</b></div>
  <div id="cols">
   <div class="c" id="c1"><div class="k">ALVO 30 · STOP</div><div class="s">20 pontos</div><div class="v" id="v1" style="color:#16A34A">+2,5</div><div class="u">pontos por trade</div>
    <div class="f">0,45 × 30 − 0,55 × 20</div></div>
   <div class="c" id="c2"><div class="k">ALVO 30 · STOP</div><div class="s" style="color:#E5484D">30 pontos</div><div class="v" id="v2" style="color:#E5484D">−3</div><div class="u">pontos por trade</div>
    <div class="f">0,45 × 30 − 0,55 × 30</div></div>
  </div>
  <div id="arr">→</div>
 </div>
 <div class="scene" id="E">
  <div id="dq"><span>O</span><span>stop</span><span>que</span><span>você</span><span>move</span><span style="color:#E5484D">é</span><span style="color:#E5484D">o</span><span style="color:#E5484D">seu</span><span style="color:#E5484D">stop.</span></div>
  <div id="plan"><div class="in" id="planin"><h3>NO SEU PLANO</h3>
   <div class="pr" id="p1"><span class="bx" id="b1"></span>Stop definido antes da entrada</div>
   <div class="pr" id="p2"><span class="bx" id="b2"></span>Stop só anda a favor</div>
   <div class="pr" id="p3"><span class="bx" id="b3"></span>Nunca para mais longe</div>
  </div></div>
 </div>
 <div class="scene" id="F">
  <div class="logo" id="logo"><img src="file://__LOGO__"><div class="sh" id="shine"></div></div>
  <div class="q" id="eq">O seu stop só anda a favor?</div>
  <div class="u" id="eu">tradeyouup.net</div>
  <div class="d" id="ed">Exemplo ilustrativo, sem custos operacionais.<br>Conteúdo educativo. Não é recomendação de investimento.</div>
 </div>
</div>
<div id="slow"></div><div id="vig"></div>
<div id="top"><div class="tag"><i></i>ERRO EM CÂMERA LENTA</div><div class="tag" id="rp"><i></i>REPLAY</div></div>
<div id="tc">00:00:00</div>
<div id="prog"><b><i></i></b><b><i></i></b><b><i></i></b><b><i></i></b></div>
<div id="note">Exemplo ilustrativo · em pontos, sem ativo · sem custos operacionais</div>
<div id="cap"></div>
<canvas id="grain" width="360" height="640"></canvas>
<script>
const W=__WORDS__, G=__GROUPS__, P=__PH__, PW=__PW__;
const SP=P[P.length-1][1]+0.1, END=SP+__TAIL__;
const $=id=>document.getElementById(id);
const cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)), lerp=(a,b,k)=>a+(b-a)*k, seg=(t,a,b)=>cl((t-a)/(b-a));
const eo=x=>1-Math.pow(1-cl(x),3), eio=x=>{x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2};
const eexp=x=>{x=cl(x);return x===1?1:1-Math.pow(2,-10*x)};
const spring=(x,f=1)=>{x=Math.max(0,x);return 1-Math.exp(-7*x)*Math.cos(10*f*x)};
function vis(el,o){el.style.opacity=o;el.style.visibility=o<=0.001?'hidden':'visible'}
const wa=(p,j)=>W[PW[p]+j][1], ph=i=>P[i];
const M={drag:wa(0,2), faz:ph(2)[0], bIn:ph(2)[1]+0.2, b40:wa(4,3), m30:wa(5,4), g50:wa(6,3), m40:wa(7,1), g57:ph(8)[0],
 dIn:ph(9)[0]-0.15, v1:wa(9,5), v2:wa(10,6), eA:ph(11)[0]-0.15, volta:wa(11,4), sr:wa(12,9), fIn:ph(13)[0]-0.15, plan:wa(13,3)};
// grão
const gc=$('grain').getContext('2d'), gimg=gc.createImageData(360,640);
function grain(f){let s=f*7919+1;const d=gimg.data;for(let i=0;i<d.length;i+=4){s=(s*16807)%2147483647;const v=s%255;d[i]=d[i+1]=d[i+2]=v;d[i+3]=255}gc.putImageData(gimg,0,0)}
const HITS=[[M.faz+0.05,16],[M.g50,12],[M.g57,16],[M.v2+0.05,18],[M.sr,20]];
function shake(t){let x=0,y=0;HITS.forEach(([h,a],j)=>{const d=t-h;if(d>=0&&d<.5){const k=a*Math.exp(-9*d);x+=k*Math.sin(d*90+j);y+=k*Math.cos(d*77+j*2)}});return [x,y]}
// ---- velas (preço em pontos relativos à entrada; y = 420 - v*9)
const Y=v=>430-v*8.2;
const C=[];{let v=6;const seq=[-2,3,-4,2,-5,-3,4,-6,1,-4,-3,2,-5,-4];
 seq.forEach((d,i)=>{const o=v,c=v+d;C.push({o,c,h:Math.max(o,c)+2.2,l:Math.min(o,c)-2.2});v=c});}
// trajetória do preço após o arrasto (cenário A: volta e vai ao alvo; usado em E)
const PATH=[-17,-21,-24,-19,-12,-6,2,9,17,24,31];
function drawCandles(n,partial,dx){let h='';const x0=70;const bw=dx*0.6;
 for(let i=0;i<n;i++){const k=C[i],x=x0+i*dx;const up=k.c>=k.o;const col=up?'#16A34A':'#E5484D';
  let c=k.c; if(i===n-1&&partial<1){c=lerp(k.o,k.c,partial)}
  h+=`<line x1="${x}" x2="${x}" y1="${Y(Math.max(k.h,c))}" y2="${Y(Math.min(k.l,c))}" stroke="${col}" stroke-width="4"/>`;
  h+=`<rect x="${x-bw/2}" y="${Y(Math.max(k.o,c))}" width="${bw}" height="${Math.max(6,Math.abs(Y(k.o)-Y(c)))}" rx="5" fill="${col}"/>`}
 return h}
function setLine(id,v){const e=$(id);e.setAttribute('y1',Y(v));e.setAttribute('y2',Y(v))}
function labelAt(id,v,x){const e=$(id);e.style.left=x+'px';e.style.top=(Y(v)-30)+'px'}
// ---- legendas
const capEl=$('cap');let capG=-1,capSpans=[];
const COL={r:'#E5484D',g:'#16A34A',b:'#2563EB'};
function buildCap(gi){capEl.innerHTML='';capSpans=[];const [a,b]=G[gi];for(let i=a;i<=b;i++){const s=document.createElement('span');s.textContent=W[i][0];capEl.appendChild(s);capSpans.push([i,s])}}
const CHK='<svg viewBox="0 0 24 24"><path d="M5 12.5l4.2 4.2L19 7" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg>';
['b1','b2','b3'].forEach(id=>$(id).innerHTML=CHK);
function tcode(t){const f=Math.floor(t*30)%30, s=Math.floor(t)%60;return '00:00:'+String(s).padStart(2,'0')+':'+String(f).padStart(2,'0')}

window.render=function(t,f){
 grain(Math.floor(f/2));
 const [sx,sy]=shake(t); $('world').style.transform=`translate(${sx}px,${sy}px)`;
 $('bg').style.transform=`translate(${Math.sin(t*.25)*30}px,${Math.cos(t*.2)*24}px) scale(${1.05+.03*Math.sin(t*.15)})`;
 const slowK=(t<M.bIn?seg(t,M.drag-.6,M.drag):0)+(t>M.eA&&t<M.fIn?1:0);
 $('floor').style.transform=`perspective(900px) rotateX(74deg) translateY(${(t*(slowK>0.5?15:60))%120}px)`;
 $('slow').style.opacity=cl(slowK)*.9;
 const topO=seg(t,.15,.55)*(1-seg(t,SP-.2,SP+.1)); vis($('top'),topO); vis($('prog'),topO);
 const rpO=(t<M.bIn?seg(t,M.drag-.5,M.drag-.2):0)+((t>M.eA&&t<M.fIn)?seg(t,M.eA,M.eA+.3):0);
 vis($('rp'),cl(rpO)); vis($('tc'),cl(rpO)*topO); $('tc').textContent=tcode(t<M.bIn?(t-M.drag+2)*0.25+10:(t-M.eA)*0.25+12);
 const sc=[[0,M.bIn],[M.bIn,M.dIn],[M.dIn,M.eA],[M.eA,SP]];
 document.querySelectorAll('#prog b i').forEach((el,i)=>{el.style.width=(seg(t,sc[i][0],sc[i][1])*100)+'%'});
 vis($('note'),seg(t,M.bIn+.3,M.bIn+.7)*(1-seg(t,M.fIn-.3,M.fIn)));
 // ---------- A: gráfico (gancho) e E (volta + STOP REAL)
 {const A=$('A'); const inA=t<M.bIn+.15, inE=t>M.eA-.1&&t<M.fIn+.2; vis(A,(inA||inE)?1:0);
  let tr='',bl=0;
  if(inA){const out=seg(t,M.bIn-.25,M.bIn+.1); tr=`translateX(${-1300*eio(out)}px)`; bl=Math.sin(Math.PI*out)*14;}
  else if(inE){const ik=eexp(seg(t,M.eA-.1,M.eA+.35)), out=seg(t,M.fIn-.2,M.fIn+.15); tr=`translateX(${1300*(1-ik)}px) translateY(${-1500*eio(out)}px)`; bl=Math.sin(Math.PI*seg(t,M.eA-.1,M.eA+.35))*14+Math.sin(Math.PI*out)*14;}
  A.style.transform=tr; A.style.filter=`blur(${bl}px)`;
  const k1=spring((t-0.05)/0.9); $('chart').style.transform=inA?`translateY(${(1-Math.min(1,k1))*-160}px)`:''; $('chart').style.opacity=inA?cl((t-.05)/.15):1;
  // velas
  let n, part=1, stop=-20, ghost=0;
  if(inA){const nk=seg(t,0.1,M.drag-0.2)*C.length; n=Math.max(1,Math.ceil(nk)); part=nk-Math.floor(nk)||1;
   const dk=eio(seg(t,M.drag,M.drag+1.1)); stop=-20-10*dk; ghost=dk>0?1:0;}
  else{n=C.length; stop=-30; ghost=1;}
  const DX=inA?56:36; let svg=drawCandles(n,part,DX);
  // E: trajetória pós-arrasto
  if(inE){const pk=seg(t,M.eA+.3,M.volta+.2)*(PATH.length-1); const xl=70+(C.length-1)*DX; let d=`M${xl},${Y(C[C.length-1].c)}`;
   for(let i=0;i<=Math.floor(pk);i++){d+=` L${xl+(i+1)*DX},${Y(PATH[i])}`}
   svg+=`<path d="${d}" fill="none" stroke="#0B1533" stroke-width="6" stroke-linejoin="round" stroke-linecap="round" opacity=".85"/>`;}
  $('cg').innerHTML=svg;
  setLine('tgt',30); setLine('entry',0); setLine('sl',stop); setLine('sl0',-20); $('sl0').setAttribute('opacity',ghost*.9);
  labelAt('tgtL',30,700); labelAt('entL',0,inA?760:44); labelAt('stopL',stop,700);
  $('stopL').textContent='STOP '+(stop>-20.5?'−20':'−'+Math.round(-stop));
  const hx=inA?(t>M.drag-.5&&t<M.drag+1.6):false; $('hand').style.opacity=hx?1:0; $('hand').style.left='640px'; $('hand').style.top=(Y(stop)-10)+'px';
  $('chd').textContent=inA?'O TRADE':'O STOP MOVIDO';
  if(inA){const fk=spring((t-M.faz)/0.6); vis($('faz'),t>=M.faz?1:0); $('faz').style.transform=`rotate(-3deg) scale(${t<M.faz?2:2-Math.min(1.03,fk)})`; $('faz').style.filter=`blur(${cl(1-(t-M.faz)/0.1)*10}px)`;
   $('chart').style.filter=t>M.faz?`blur(${4*eo(seg(t,M.faz,M.faz+.2))}px)`:'';} else {vis($('faz'),0); $('chart').style.filter='';}
  const vk=inE?eo(seg(t,M.volta-.3,M.volta+.1)):0; $('volta').style.opacity=vk; $('volta').style.left='600px'; $('volta').style.top=(Y(8)-20)+'px';
  const sk=spring((t-M.sr)/0.6); vis($('sr'),inE&&t>=M.sr?1:0); $('sr').style.top=(370+Y(-30)-70)+'px'; $('sr').style.transform=`rotate(-4deg) scale(${t<M.sr?2.2:2.2-1.2*Math.min(1.03,sk)})`; $('sr').style.filter=`blur(${cl(1-(t-M.sr)/0.1)*10}px)`;
 }
 // ---------- B: régua + medidor
 {const S=$('B'), ik=eexp(seg(t,M.bIn-.1,M.bIn+.35)), out=seg(t,M.dIn-.2,M.dIn+.15); vis(S,(t>M.bIn-.1&&t<M.dIn+.2)?1:0);
  S.style.transform=`translateX(${1300*(1-ik)}px) translateY(${-1500*eio(out)}px)`; S.style.filter=`blur(${Math.sin(Math.PI*seg(t,M.bIn-.1,M.bIn+.35))*14+Math.sin(Math.PI*out)*14}px)`;
  // escala da régua: +30 em y=150, 0 em y=150+30*u, u=9px/ponto
  const yv=v=>150+(30-v)*9.0;
  const s1=spring((t-M.m30)/0.7), s2=spring((t-M.m40)/0.7);
  const stop=20+(t>=M.m30?10*Math.min(1.04,s1):0)+(t>=M.m40?10*Math.min(1.04,s2):0);
  $('mT').style.top=yv(30)+'px'; $('mE').style.top=yv(0)+'px'; $('mS').style.top=yv(-stop)+'px'; $('mS0').style.top=yv(-20)+'px'; $('mS0').style.opacity=t>M.m30?.9:0;
  $('mSt').textContent='−'+Math.round(Math.min(40,stop));
  $('zg').style.top=yv(30)+'px'; $('zg').style.height=(yv(0)-yv(30))+'px'; $('zr').style.top=yv(0)+'px'; $('zr').style.height=(yv(-stop)-yv(0))+'px';
  const s=Math.min(40,stop), pct=s/(30+s)*100; const gk=eio(seg(t,M.bIn+.3,M.b40));
  const show=t<M.b40?pct*gk:pct; $('garc').setAttribute('stroke-dasharray',`${show} 100`); $('garc').setAttribute('stroke',show>45?'#E5484D':'#2563EB');
  $('gnum').textContent=Math.round(show)+'%'; $('gnum').style.color=show>45?'#E5484D':'#2563EB';
  const pk=[M.b40,M.g50,M.g57].reduce((a,h)=>{const d=t-h;return a+(d>=0&&d<.4?Math.sin(Math.PI*d/.4)*.12:0)},0); $('gnum').style.transform=`scale(${1+pk})`;
  [['h1',M.b40],['h2',M.g50],['h3',M.g57]].forEach(([id,a])=>{const k=eo(seg(t,a,a+.35));$(id).style.opacity=k;$(id).style.transform=`translateX(${(1-k)*40}px)`});
 }
 // ---------- D: contadores
 {const S=$('D'), ik=eexp(seg(t,M.dIn-.1,M.dIn+.35)), out=seg(t,M.eA-.2,M.eA+.15); vis(S,(t>M.dIn-.1&&t<M.eA+.2)?1:0);
  S.style.transform=`translateY(${(1-ik)*1500-eio(out)*1600}px)`; S.style.filter=`blur(${Math.sin(Math.PI*seg(t,M.dIn-.1,M.dIn+.35))*12+Math.sin(Math.PI*out)*14}px)`;
  const a1=M.v1+.2, a2=M.v2-.9;
  [['c1',a1],['c2',a2]].forEach(([id,a])=>{const k=spring((t-a)/0.8);$(id).style.opacity=cl((t-a)/.12);$(id).style.transform=`translateY(${(1-Math.min(1,k))*120}px)`});
  const k1=eio(seg(t,a1+.2,a1+1.0)); $('v1').textContent='+'+(2.5*k1).toFixed(1).replace('.',',');
  const k2=eio(seg(t,a2+.2,M.v2+.1)); const v=-3*k2; $('v2').textContent=(v<-0.05?'−':'')+Math.abs(v).toFixed(v<-2.95?0:1).replace('.',',');
  const ak=spring((t-a2)/0.6); $('arr').style.opacity=cl((t-a2)/.1); $('arr').style.transform=`scale(${t<a2?0:Math.min(1.1,ak)})`;
 }
 // ---------- E2: plano (fecho)
 {const S=$('E'), ik=eexp(seg(t,M.fIn-.1,M.fIn+.35)), out=seg(t,SP-.12,SP+.15); vis(S,(t>M.fIn-.1&&t<SP+.2)?1:0);
  S.style.transform=`translateY(${(1-ik)*1500}px) scale(${1+.04*seg(t,M.fIn,SP)})`; S.style.opacity=(t>M.fIn-.1&&t<SP+.2)?1-out:0;
  [...$('dq').children].forEach((s,i)=>{const a=M.fIn+.15+i*.09, k=spring((t-a)/0.6);s.style.opacity=cl((t-a)/.08);s.style.transform=`translateY(${(1-Math.min(1,k))*50}px)`});
  const pa=M.fIn+.6, pk=spring((t-pa)/0.9); $('planin').style.transform=`rotateX(${t<pa?50:(1-Math.min(1,pk))*50}deg) translateY(${t<pa?120:(1-Math.min(1,pk))*120}px)`; $('plan').style.opacity=seg(t,pa,pa+.2);
  [['p1',pa+.3,'b1',pa+.6],['p2',M.plan,'b2',M.plan+.35],['p3',M.plan+.5,'b3',M.plan+.85]].forEach(([id,a,bx,ba])=>{const k=eo(seg(t,a,a+.35));$(id).style.opacity=k;$(id).style.transform=`translateX(${(1-k)*40}px)`;
   const on=t>=ba, bk=spring((t-ba)/0.5); $(bx).style.background=on?'#16A34A':'transparent'; $(bx).style.borderColor=on?'#16A34A':'#C9D2E3'; $(bx).style.transform=`scale(${on?Math.min(1.12,bk):1})`; $(bx).firstChild.style.opacity=on?1:0});
  $('p2').style.color=t>=M.plan+.35?'#16A34A':'#0B1533';
 }
 // ---------- F: final
 {const S=$('F'), k=seg(t,SP-.05,SP+.35); vis(S,t>SP-.06?eo(k):0);
  const lk=spring((t-SP-.05)/0.9); $('logo').style.transform=`scale(${t<SP?0.8:0.8+.2*Math.min(1.02,lk)})`; $('logo').style.opacity=seg(t,SP,SP+.25);
  $('shine').style.left=(-200+1100*eio(seg(t,SP+.6,SP+1.5)))+'px';
  [['eq',SP+.5],['eu',SP+.85],['ed',SP+1.0]].forEach(([id,a])=>{const kk=eo(seg(t,a,a+.45));$(id).style.opacity=kk;$(id).style.transform=`translateY(${(1-kk)*30}px)`});}
 // ---------- legendas
 let gi=-1; for(let i=0;i<G.length;i++){const s=W[G[i][0]][1]-0.12; const e=(i+1<G.length)?W[G[i+1][0]][1]-0.12:SP+0.05; if(t>=s&&t<e)gi=i}
 if(gi!==capG){capG=gi; if(gi>=0)buildCap(gi); else capEl.innerHTML=''}
 if(gi>=0){const gs=W[G[gi][0]][1]-0.12, gk=eo(seg(t,gs,gs+.18)); capEl.style.opacity=gk; capEl.style.transform=`translateY(${(1-gk)*24}px)`;
  capSpans.forEach(([i,s])=>{const w=W[i], on=t>=w[1]-0.04, act=on&&(i+1>G[gi][1]||t<W[i+1][1]-0.04);
   s.style.opacity=on?1:.22; const c=w[2]?COL[w[2]]:null;
   if(act){const pk=spring((t-w[1]+0.04)/0.45); s.style.background=c||'#0B1533'; s.style.color='#fff'; s.style.textShadow='none';
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
    return h, PH[-1][1] + 0.1 + TAIL


async def render(out, fps, stills=None):
    from playwright.async_api import async_playwright
    html, end = build()
    hp = os.path.join(HERE, "stop40.html"); open(hp, "w").write(html)
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
