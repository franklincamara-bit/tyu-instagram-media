# Reel "Cash Flow: o custo invisível da mesa" (TYU-52) — motion design 1080x1920.
# Base visual: tribunal1.py / short60.py / short81_v2.py. Tempos das frases medidos com silencedetect na narração (narracao.mp3).
# Uso: python3 cashflow1.py <saida_sem_audio.mp4> [fps]  |  python3 cashflow1.py stills t1 t2 ...
import os, sys, json, asyncio, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
INTER = "/usr/share/fonts/opentype/inter"
LOGO = os.path.join(ROOT, "assets", "logo.png")

# (legenda com algarismos, falado, [ini, fim] medido). Tokens separados por espaço comum; NBSP mantém "US$ 450" junto.
N = " "
PHRASES = [
    ("Passou na avaliação.", "Passou na avaliação.", [0.05, 1.06]),
    ("Parabéns.", "Parabéns.", [1.29, 2.01]),
    ("Agora faz a conta que quase ninguém faz.", "Agora faz a conta que quase ninguém faz.", [2.46, 4.96]),
    ("3 tentativas de avaliação:", "Três tentativas de avaliação:", [5.40, 6.83]),
    (f"US${N}450.", "quatrocentos e cinquenta dólares.", [7.19, 8.89]),
    ("2 resets:", "Dois resets:", [9.19, 10.04]),
    (f"US${N}160.", "cento e sessenta.", [10.24, 11.18]),
    (f"Ativação da conta: US${N}130.", "Ativação da conta: cento e trinta.", [11.56, 13.56]),
    (f"3 meses de dados e plataforma: US${N}135.", "Três meses de dados e plataforma: cento e trinta e cinco.", [14.04, 17.20]),
    ("Total:", "Total:", [17.64, 18.09]),
    (f"US${N}875.", "oitocentos e setenta e cinco dólares.", [18.46, 20.53]),
    ("Antes do 1º saque.", "Antes do primeiro saque.", [20.88, 22.12]),
    ("Esse é o seu ponto de partida.", "Esse é o seu ponto de partida.", [22.59, 24.33]),
    ("Não é o zero.", "Não é o zero.", [24.72, 25.41]),
    ("Anota cada custo da mesa, inclusive o que se repete todo mês.", "Anota cada custo da mesa, inclusive o que se repete todo mês.", [25.73, 29.46]),
    ("Na plataforma, o Cash Flow guarda tudo isso num lugar só.", "Na plataforma, o Cash Flow guarda tudo isso num lugar só.", [29.94, 32.97]),
    ("Quanto a sua mesa já te custou?", "Quanto a sua mesa já te custou?", [33.38, 34.77]),
]
GROUPS = [[0, 1], [2], [3, 4], [5, 6], [7], [8], [9, 10], [11], [12], [13], [14], [15]]  # a 16 vira a tela final
SPLIT = {14: 5, 15: 5}
KEY_RED = [f"US${N}450.", f"US${N}160.", f"US${N}130.", f"US${N}135.", f"US${N}875.", "saque.", "Não", "zero."]
KEY_GREEN = ["avaliação.", "Parabéns."]
KEY_BLUE = ["partida.", "Cash", "Flow", "repete", "mês."]
TAIL = 3.4


def words_and_groups():
    words, pw = [], []
    for cap, sp, (a, b) in PHRASES:
        toks, stoks = cap.split(" "), sp.split(" ")
        pw.append(len(words))
        if len(toks) == len(stoks):
            wts = [len(s) + 1 for s in stoks]
        elif len(toks) == 1:
            wts = [len(sp)]
        else:  # pesa cada token da legenda pelo trecho falado equivalente quando possível
            wts = [len(t) + 1 for t in toks]
            if toks[-1].startswith("US$"):
                head = " ".join(toks[:-1]); spoken_tail = sp[len(head):] if sp.startswith(head) else sp
                wts[-1] = len(spoken_tail)
        tot, acc = sum(wts), 0
        for w, k in zip(toks, wts):
            words.append([w, round(a + (b - a) * acc / tot, 3)]); acc += k
    groups = []
    for g in GROUPS:
        i0 = pw[g[0]]; i1 = pw[g[-1]] + len(PHRASES[g[-1]][0].split(" ")) - 1
        if len(g) == 1 and g[0] in SPLIT:
            groups.append([i0, i0 + SPLIT[g[0]] - 1]); groups.append([i0 + SPLIT[g[0]], i1])
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
  radial-gradient(900px 900px at 80% 10%,rgba(37,99,235,.15),transparent 62%),
  radial-gradient(800px 800px at 8% 90%,rgba(22,163,74,.08),transparent 60%),
  linear-gradient(180deg,#F7F8FC 0%,#ECEFF6 100%)}
#floor{position:absolute;left:-1200px;width:3480px;top:980px;height:2600px;transform-origin:50% 0;
  background-image:linear-gradient(rgba(11,21,51,.07) 2px,transparent 2px),linear-gradient(90deg,rgba(11,21,51,.07) 2px,transparent 2px);
  background-size:120px 120px;-webkit-mask-image:linear-gradient(180deg,transparent 0%,#000 18%,#000 55%,transparent 100%)}
#world{position:absolute;inset:0;transform-origin:540px 760px}
.scene{position:absolute;inset:0;opacity:0;visibility:hidden}
#vig{position:absolute;inset:0;pointer-events:none;background:radial-gradient(1300px 1700px at 50% 45%,transparent 55%,rgba(11,21,51,.15) 100%)}
#grain{position:absolute;inset:0;width:1080px;height:1920px;mix-blend-mode:overlay;opacity:.10}
#top{position:absolute;left:64px;top:232px;display:flex;align-items:center;gap:18px;opacity:0;z-index:5}
#top .tag{font:600 26px 'Inter';letter-spacing:4px;background:rgba(255,255,255,.82);border:2px solid rgba(11,21,51,.08);padding:12px 20px;border-radius:999px;display:flex;align-items:center;gap:12px;box-shadow:0 8px 24px rgba(11,21,51,.06)}
#top .tag i{width:12px;height:12px;border-radius:50%;background:#E5484D;box-shadow:0 0 0 6px rgba(229,72,77,.15)}
#cap{position:absolute;left:60px;width:880px;top:1300px;display:flex;flex-wrap:wrap;justify-content:center;align-items:baseline;gap:6px 14px;
  font-family:'InterD';font-weight:900;font-size:66px;line-height:1.12;letter-spacing:-1px;z-index:6}
#cap span{position:relative;display:inline-block;padding:2px 10px;border-radius:16px;color:#0B1533;white-space:nowrap;text-shadow:0 2px 0 rgba(255,255,255,.9),0 0 18px rgba(255,255,255,.9)}
.card{position:absolute;background:rgba(255,255,255,.96);border:2px solid rgba(11,21,51,.06);border-radius:44px;box-shadow:0 40px 90px rgba(11,21,51,.14)}
.hd{font:600 24px 'Inter';letter-spacing:4px;color:#7A8499}
/* A: avaliação aprovada */
#eval{left:150px;width:780px;top:420px;height:600px;padding:52px 56px}
#eval .ttl{font:900 64px 'InterD';letter-spacing:-2px;margin-top:14px}
#eval .row{display:flex;align-items:center;gap:22px;margin-top:34px;font:700 38px 'InterD';color:#0B1533}
#eval .ck{width:56px;height:56px;border-radius:50%;background:#16A34A;display:flex;align-items:center;justify-content:center;flex:none}
#eval .ck svg{width:32px;height:32px}
#ok{position:absolute;left:330px;top:300px;opacity:0}
#ok b{display:inline-block;font:900 92px 'InterD';letter-spacing:4px;color:#16A34A;border:10px solid #16A34A;border-radius:26px;padding:0 30px 8px;background:rgba(255,255,255,.75);transform:rotate(-8deg)}
.conf{position:absolute;width:18px;height:30px;border-radius:4px;opacity:0}
/* B: impressora + recibo */
#printer{position:absolute;left:120px;width:840px;top:330px;height:70px;border-radius:24px;background:linear-gradient(180deg,#1A2754,#0B1533);box-shadow:0 26px 50px rgba(11,21,51,.35);opacity:0;z-index:3}
#printer:after{content:'';position:absolute;left:120px;right:120px;bottom:16px;height:10px;border-radius:5px;background:#050A1C}
#printer .led{position:absolute;right:40px;top:28px;width:14px;height:14px;border-radius:50%;background:#16A34A;box-shadow:0 0 12px #16A34A}
#printer .lbl{position:absolute;left:40px;top:22px;font:600 20px 'Inter';letter-spacing:5px;color:rgba(255,255,255,.7)}
#paperwrap{position:absolute;left:170px;width:740px;top:384px;height:900px;overflow:hidden;z-index:2}
#paper{position:absolute;left:0;top:0;width:740px;height:900px;background:#FFFEFA;box-shadow:0 30px 60px rgba(11,21,51,.16)}
#paper .ph{position:absolute;left:44px;right:44px;top:34px}
#paper .ph .t{font:900 44px 'InterD';letter-spacing:6px;text-align:center}
#paper .ph .s{font:500 22px 'Inter';color:#8A93A6;text-align:center;margin-top:6px}
.ln{position:absolute;left:44px;right:44px;height:110px;border-bottom:2px dashed rgba(11,21,51,.12);display:flex;align-items:center;justify-content:space-between}
.ln .l{font:700 36px 'InterD';color:#0B1533;letter-spacing:-.5px;white-space:nowrap}
.ln .l small{display:block;font:500 22px 'Inter';color:#8A93A6;letter-spacing:0;margin-top:2px}
.ln .v{font:900 46px 'InterD';color:#E5484D;letter-spacing:-1px;opacity:0;white-space:nowrap}
#sep{position:absolute;left:44px;right:44px;top:650px;height:0;border-top:5px dashed #0B1533;opacity:0}
#tot{position:absolute;left:44px;right:44px;top:676px;display:flex;align-items:baseline;justify-content:space-between;opacity:0}
#tot .l{font:900 44px 'InterD';letter-spacing:6px}
#tot .v{font:900 96px 'InterD';letter-spacing:-3px;color:#E5484D}
#selo{position:absolute;left:0;right:0;top:812px;text-align:center;font:500 22px 'Inter';color:#8A93A6}
#stamp2{position:absolute;left:320px;top:860px;opacity:0;z-index:4}
#stamp2 b{display:inline-block;font:900 50px 'InterD';letter-spacing:3px;color:#E5484D;border:8px solid #E5484D;border-radius:20px;padding:4px 22px 10px;background:rgba(255,255,255,.85);transform:rotate(-7deg);white-space:nowrap}
/* C: régua do saldo */
#ruler{left:70px;width:940px;top:420px;height:700px}
#ruler .hd{position:absolute;left:52px;top:48px}
#ruler .big{position:absolute;left:52px;top:92px;font:900 60px 'InterD';letter-spacing:-2px}
#axis{position:absolute;left:0;top:0}
#pin{position:absolute;top:0;left:0}
#pin .bb{position:absolute;left:-150px;width:300px;top:-150px;text-align:center}
#pin .bb b{display:inline-block;font:900 52px 'InterD';color:#fff;background:#E5484D;padding:10px 22px 14px;border-radius:20px;letter-spacing:-1px;white-space:nowrap;box-shadow:0 14px 30px rgba(229,72,77,.3)}
#pin .bb b.z{background:#0B1533;box-shadow:0 14px 30px rgba(11,21,51,.25)}
#nz{position:absolute;opacity:0}
#nz b{display:inline-block;font:900 40px 'InterD';color:#0B1533;background:#FFD43B;padding:10px 22px 14px;border-radius:16px;letter-spacing:-.5px;white-space:nowrap}
#rnote{position:absolute;left:52px;bottom:40px;font:500 22px 'Inter';color:#8A93A6}
/* D: registro (cartão estilizado) */
#reg{left:90px;width:900px;top:330px;height:940px;padding:44px 48px}
#reg .top{display:flex;justify-content:space-between;align-items:center}
#cfpill{font:900 30px 'InterD';color:#fff;background:#2563EB;padding:10px 22px 12px;border-radius:999px;opacity:0;white-space:nowrap}
#reg .ttl{font:900 54px 'InterD';letter-spacing:-1.5px;margin-top:16px}
.rr{position:absolute;left:48px;right:48px;height:100px;border-radius:24px;background:#F6F7FB;border:2px solid #E2E8F0;display:flex;align-items:center;padding:0 26px;gap:20px;opacity:0}
.rr .ic{width:58px;height:58px;border-radius:16px;background:#FDECEC;display:flex;align-items:center;justify-content:center;flex:none;font:900 34px 'InterD';color:#E5484D}
.rr .tx{flex:1;min-width:0}
.rr .tx b{display:block;font:700 33px 'InterD';letter-spacing:-.5px;white-space:nowrap}
.rr .tx span{font:600 18px 'Inter';letter-spacing:3px;color:#7A8499}
.rr .rc{display:inline-block;font:600 18px 'Inter';letter-spacing:2px;color:#2563EB;background:#E8EFFE;border-radius:999px;padding:5px 12px;margin-left:10px;opacity:0;transform-origin:0 50%}
.rr .vv{font:900 38px 'InterD';color:#E5484D;white-space:nowrap}
#rsum{position:absolute;left:48px;right:48px;bottom:76px;display:flex;justify-content:space-between;align-items:baseline;border-top:4px solid #0B1533;padding-top:18px;opacity:0}
#rsum .l{font:900 34px 'InterD';letter-spacing:4px}
#rsum .v{font:900 64px 'InterD';color:#E5484D;letter-spacing:-2px}
#rselo{position:absolute;left:48px;bottom:34px;font:500 22px 'Inter';color:#8A93A6}
/* F: final */
#F{background:#fff}
#F .logo{position:absolute;left:180px;top:500px;width:720px;height:270px;overflow:hidden}
#F .logo img{width:720px;display:block}
#F .logo .sh{position:absolute;top:-40px;bottom:-40px;width:160px;background:linear-gradient(100deg,transparent,rgba(255,255,255,.85),transparent);transform:skewX(-18deg)}
#F .q{position:absolute;left:90px;width:900px;top:860px;text-align:center;font:900 82px 'InterD';line-height:1.04;letter-spacing:-2.5px}
#F .q em{font-style:normal;color:#E5484D}
#F .u{position:absolute;left:0;width:1080px;top:1150px;text-align:center;font:700 36px 'InterD';color:#2563EB}
#F .d{position:absolute;left:0;width:1080px;top:1206px;text-align:center;font:500 24px 'Inter';color:#8A93A6;line-height:1.5}
</style></head><body>
<div id="bg"></div><div id="floor"></div>
<div id="world">
 <div class="scene" id="A">
  <div class="card" id="eval"><div class="hd">CONTA DE AVALIAÇÃO</div><div class="ttl">Resultado final</div>
   <div class="row" id="r1"><div class="ck">__CK__</div>Meta da avaliação</div>
   <div class="row" id="r2"><div class="ck">__CK__</div>Limite de perda respeitado</div>
   <div class="row" id="r3"><div class="ck">__CK__</div>Dias mínimos cumpridos</div>
  </div>
  <div id="ok"><b>APROVADO</b></div>
  __CONF__
 </div>
 <div class="scene" id="B">
  <div id="printer"><div class="lbl">CUSTOS DA MESA</div><div class="led" id="led"></div></div>
  <div id="paperwrap"><div id="paper">
   <div class="ph"><div class="t">RECIBO DA MESA</div><div class="s">exemplo ilustrativo · valores fictícios</div></div>
   <div class="ln" id="L0" style="top:150px"><div class="l" data-t="3 × avaliação"></div><div class="v">US$ 450</div></div>
   <div class="ln" id="L1" style="top:260px"><div class="l" data-t="2 × reset"></div><div class="v">US$ 160</div></div>
   <div class="ln" id="L2" style="top:370px"><div class="l" data-t="Ativação da conta"></div><div class="v">US$ 130</div></div>
   <div class="ln" id="L3" style="top:480px"><div class="l" data-t="Dados + plataforma" data-s="3 meses · US$ 15 + US$ 30 por mês"></div><div class="v">US$ 135</div></div>
   <div id="sep"></div>
   <div id="tot"><div class="l">TOTAL</div><div class="v" id="totv">US$ 0</div></div>
   <div id="selo">Exemplo ilustrativo · valores fictícios · antes de impostos</div>
  </div></div>
  <div id="stamp2"><b>ANTES DO 1º SAQUE</b></div>
 </div>
 <div class="scene" id="C">
  <div class="card" id="ruler"><div class="hd">SEU SALDO REAL</div><div class="big">Onde a conta começa</div>
   <svg id="axis" width="940" height="700">
    <rect id="redbar" x="0" y="452" height="16" rx="8" fill="#E5484D" opacity=".85"/>
    <line x1="80" x2="860" y1="460" y2="460" stroke="#0B1533" stroke-width="6" stroke-linecap="round"/>
    __TICKS__
    <g id="zx" opacity="0"><line x1="__ZX0__" y1="500" x2="__ZX1__" y2="560" stroke="#E5484D" stroke-width="8" stroke-linecap="round"/><line x1="__ZX1__" y1="500" x2="__ZX0__" y2="560" stroke="#E5484D" stroke-width="8" stroke-linecap="round"/></g>
   </svg>
   <div id="pin"><svg width="40" height="40" style="position:absolute;left:-20px;top:-40px"><path d="M0 0h40L20 34z" fill="#0B1533"/></svg><div class="bb"><b id="pinv" class="z">US$ 0</b></div></div>
   <div id="nz"><b>NÃO É O ZERO</b></div>
   <div id="rnote">Exemplo ilustrativo · valores fictícios</div>
  </div>
 </div>
 <div class="scene" id="D">
  <div class="card" id="reg"><div class="top"><div class="hd">REGISTRO DE CUSTOS</div><div id="cfpill">Cash Flow</div></div><div class="ttl">Cada custo, anotado</div>
   __ROWS__
   <div id="rsum"><div class="l">TOTAL</div><div class="v">−US$ 875</div></div>
   <div id="rselo">Exemplo ilustrativo · conta demo</div>
  </div>
 </div>
 <div class="scene" id="F">
  <div class="logo" id="logo"><img src="file://__LOGO__"><div class="sh" id="shine"></div></div>
  <div class="q" id="eq">Quanto a sua mesa <em>já te custou?</em></div>
  <div class="u" id="eu">tradeyouup.net</div>
  <div class="d" id="ed">Exemplo ilustrativo, valores fictícios.<br>Conteúdo educativo. Não é recomendação de investimento.</div>
 </div>
</div>
<div id="vig"></div>
<div id="top"><div class="tag"><i></i>QUANTO CUSTOU OPERAR</div></div>
<div id="cap"></div>
<canvas id="grain" width="360" height="640"></canvas>
<script>
const W=__WORDS__, G=__GROUPS__, P=__PH__, PW=__PW__, KR=new Set(__KR__), KG=new Set(__KG__), KB=new Set(__KB__);
const SP=P[16][0]-0.15, END=P[16][1]+__TAIL__;
const $=id=>document.getElementById(id);
const cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)), lerp=(a,b,k)=>a+(b-a)*k, seg=(t,a,b)=>cl((t-a)/(b-a));
const eo=x=>1-Math.pow(1-cl(x),3), eio=x=>{x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2};
const eexp=x=>{x=cl(x);return x===1?1:1-Math.pow(2,-10*x)};
const spring=(x,f=1)=>{x=Math.max(0,x);return 1-Math.exp(-7*x)*Math.cos(10*f*x)};
function vis(el,o){el.style.opacity=o;el.style.visibility=o<=0.001?'hidden':'visible'}
const ph=i=>P[i], wa=(p,j)=>W[PW[p]+j][1];
const M={ok:0.55, conf:ph(1)[0], prIn:ph(2)[0]+0.6, bIn:ph(2)[1]-0.35,
 l0:ph(3)[0], v0:ph(4)[0], l1:ph(5)[0], v1:ph(6)[0], l2:ph(7)[0], v2:wa(7,3), l3:ph(8)[0], v3:wa(8,6),
 sep:ph(9)[0], tot:ph(10)[0], st:ph(11)[0], cIn:ph(12)[0]-0.2, slide:ph(12)[0]+0.2, nz:ph(13)[0],
 dIn:ph(14)[0]-0.2, rec:wa(14,9), cf:wa(15,3)};
const LT=[[M.l0,M.v0],[M.l1,M.v1],[M.l2,M.v2],[M.l3,M.v3]];
window.M=M;
const gc=$('grain').getContext('2d'), gimg=gc.createImageData(360,640);
function grain(f){let s=f*7919+1;const d=gimg.data;for(let i=0;i<d.length;i+=4){s=(s*16807)%2147483647;const v=s%255;d[i]=d[i+1]=d[i+2]=v;d[i+3]=255}gc.putImageData(gimg,0,0)}
const HITS=[[M.ok,16],[M.v0,6],[M.v1,6],[M.v2,6],[M.v3,6],[M.st,20],[M.nz,8]];
function shake(t){let x=0,y=0;HITS.forEach(([h,a],j)=>{const d=t-h;if(d>=0&&d<.5){const k=a*Math.exp(-9*d);x+=k*Math.sin(d*90+j);y+=k*Math.cos(d*77+j*2)}});return [x,y]}
const capEl=$('cap');let capG=-1,capSpans=[];
function buildCap(gi){capEl.innerHTML='';capSpans=[];const [a,b]=G[gi];for(let i=a;i<=b;i++){const s=document.createElement('span');s.textContent=W[i][0];capEl.appendChild(s);capSpans.push([i,s])}}
const fmt=v=>Math.round(v).toString().replace(/\B(?=(\d{3})+(?!\d))/g,'.');
const CONF=[...document.querySelectorAll('.conf')];
// régua: −1000..+500 -> x 80..860
const AX=v=>80+780*(v+1000)/1500;

window.render=function(t,f){
 grain(Math.floor(f/2));
 const [sx,sy]=shake(t);
 // câmera: aproxima no total do recibo
 const zt=eio(seg(t,M.tot-.2,M.tot+.6))*(1-eio(seg(t,M.cIn-.3,M.cIn)));
 $('world').style.transform=`translate(${sx}px,${sy}px) scale(${1+zt*.04})`; $('world').style.transformOrigin='540px 1100px';
 $('bg').style.transform=`translate(${Math.sin(t*.25)*30}px,${Math.cos(t*.2)*24}px) scale(${1.05+.03*Math.sin(t*.15)})`;
 $('floor').style.transform=`perspective(900px) rotateX(74deg) translateY(${(t*60)%120}px)`;
 vis($('top'),seg(t,.5,.9)*(1-seg(t,SP-.2,SP+.1)));
 // ---------- A
 {const S=$('A'), out=seg(t,M.bIn-.1,M.bIn+.35); vis(S,t<M.bIn+.4?1:0);
  const ik=spring(t/0.8); $('eval').style.transform=`translateY(${(1-Math.min(1,ik))*500+eio(out)*1400}px) rotate(${eio(out)*-8}deg)`;
  $('eval').style.filter=`blur(${Math.sin(Math.PI*out)*10}px)`;
  ['r1','r2','r3'].forEach((id,i)=>{const k=eo(seg(t,.12+i*.1,.4+i*.1));$(id).style.opacity=k;$(id).style.transform=`translateX(${(1-k)*-40}px)`});
  const ok=spring((t-M.ok)/0.6); vis($('ok'),t>=M.ok?1-seg(t,M.prIn-.25,M.prIn+.05):0);
  $('ok').style.transform=`translateY(${eio(out)*1400}px) scale(${t<M.ok?2.4:2.4-1.4*Math.min(1.03,ok)})`; $('ok').style.filter=`blur(${cl(1-(t-M.ok)/0.1)*12}px)`;
  CONF.forEach((c,i)=>{const d=t-M.conf-(i%5)*0.03; if(d<0||d>2.6){c.style.opacity=0;return}
   const a=(i*137.5)%360*Math.PI/180, v=520+(i*53)%380; const x=540+Math.cos(a)*v*d, y=560+Math.sin(a)*v*d*0.7+650*d*d;
   c.style.opacity=1-seg(d,1.8,2.6); c.style.transform=`translate(${x}px,${y}px) rotate(${d*(300+i*40)}deg)`;});
 }
 // ---------- B
 {const S=$('B'); vis(S,(t>M.prIn-.1&&t<M.cIn+.4)?1:0);
  const pk=spring((t-M.prIn)/0.7), out=seg(t,M.cIn-.15,M.cIn+.3);
  const flyUp=-1500*eio(out);
  vis($('printer'),t>M.prIn?1:0); $('printer').style.transform=`translateY(${(1-Math.min(1,pk))*-420+flyUp}px)`;
  // altura do papel
  let h=0; if(t>M.bIn)h=lerp(0,150,eo(seg(t,M.bIn,M.bIn+.5)));
  LT.forEach(([a,b],i)=>{if(t>a)h=Math.max(h,lerp(150+i*110,150+(i+1)*110,eo(seg(t,a,a+.6))))});
  if(t>M.sep)h=Math.max(h,lerp(590,800,eo(seg(t,M.sep,M.sep+.5)))); if(t>M.tot)h=Math.max(h,lerp(800,860,eo(seg(t,M.tot,M.tot+.4))));
  const z=[];for(let x=0;x<=740;x+=20){z.push(`${x}px ${h-(x/20%2?0:14)}px`)}
  $('paper').style.clipPath=`polygon(0 0,740px 0,${z.reverse().join(',')})`;
  $('paper').style.transform=`translateY(${flyUp}px)`; $('paperwrap').style.height='900px';
  // jitter da impressora enquanto imprime
  const printing=LT.some(([a])=>t>a&&t<a+.6)||(t>M.bIn&&t<M.bIn+.5)||(t>M.sep&&t<M.sep+.5);
  $('led').style.background=printing&&(Math.floor(t*12)%2)?'#FFD43B':'#16A34A';
  if(printing&&t<M.cIn)$('printer').style.transform+=` translateX(${Math.sin(t*90)*2}px)`;
  LT.forEach(([a,b],i)=>{const L=$('L'+i), l=L.querySelector('.l'), v=L.querySelector('.v'); const txt=l.dataset.t, sub=l.dataset.s;
   const n=Math.floor(cl((t-a)/0.5)*txt.length); l.innerHTML=(t>a?txt.slice(0,n):'')+(sub&&t>a+.4?`<small style="opacity:${eo(seg(t,a+.4,a+.8))}">${sub}</small>`:'');
   const vk=spring((t-b)/0.5); v.style.opacity=t>=b?1:0; v.style.transform=`scale(${t<b?1.6:1.6-.6*Math.min(1.04,vk)})`; v.style.transformOrigin='100% 50%';});
  $('sep').style.opacity=t>M.sep?1:0; $('sep').style.clipPath=`inset(0 ${100-100*eo(seg(t,M.sep,M.sep+.4))}% 0 0)`;
  vis($('tot'),eo(seg(t,M.sep+.1,M.sep+.4)));
  const cv=875*eo(seg(t,M.tot,M.tot+1.3)); $('totv').textContent='US$ '+fmt(cv);
  const tp=t>M.tot+1.3&&t<M.tot+1.8?Math.exp(-8*(t-M.tot-1.3)):0; $('totv').style.transform=`scale(${1+.12*tp})`; $('totv').style.transformOrigin='100% 80%';
  const sk=spring((t-M.st)/0.6); vis($('stamp2'),t>=M.st?1:0); $('stamp2').style.transform=`translateY(${flyUp}px) scale(${t<M.st?2.2:2.2-1.2*Math.min(1.03,sk)})`;
  $('stamp2').style.filter=`blur(${cl(1-(t-M.st)/0.1)*12}px)`;
 }
 // ---------- C
 {const S=$('C'), inK=eexp(seg(t,M.cIn,M.cIn+.45)), out=seg(t,M.dIn-.15,M.dIn+.3); vis(S,(t>M.cIn&&t<M.dIn+.35)?1:0);
  S.style.transform=`translateY(${(1-inK)*1400}px) translateX(${-1300*eio(out)}px)`; S.style.filter=`blur(${Math.sin(Math.PI*out)*12}px)`;
  const sk=eio(seg(t,M.slide,M.slide+1.4)), v=-875*sk, px=AX(v);
  $('pin').style.left=(px)+'px'; $('pin').style.top='452px';
  $('pinv').textContent=v>-1?'US$ 0':'−US$ '+fmt(-v); $('pinv').className=v>-1?'z':'';
  $('pinv').style.transform=`scale(${1+.1*(t>M.slide+1.4&&t<M.slide+1.9?Math.exp(-8*(t-M.slide-1.4)):0)})`;
  $('redbar').setAttribute('x',px); $('redbar').setAttribute('width',Math.max(0,AX(0)-px));
  const nk=spring((t-M.nz)/0.6); $('zx').setAttribute('opacity',eo(seg(t,M.nz,M.nz+.25)));
  vis($('nz'),t>M.nz?1:0); $('nz').style.left=(AX(0)-150)+'px'; $('nz').style.top='330px'; $('nz').style.transform=`scale(${Math.min(1.04,nk)})`;
 }
 // ---------- D
 {const S=$('D'), inK=eexp(seg(t,M.dIn,M.dIn+.45)), out=seg(t,SP-.2,SP+.15); vis(S,(t>M.dIn&&t<SP+.2)?1:0);
  S.style.transform=`translateX(${(1-inK)*1300}px) scale(${1-out*.08})`; S.style.filter=`blur(${Math.sin(Math.PI*seg(t,M.dIn,M.dIn+.45))*12+out*8}px)`;
  const RA=[0,.45,.9,1.35,1.8].map(d=>M.dIn+.5+d);
  document.querySelectorAll('.rr').forEach((r,i)=>{const k=spring((t-RA[i])/0.7); r.style.opacity=t>RA[i]?1:0; r.style.transform=`translateY(${(1-Math.min(1,k))*60}px)`;
   const rc=r.querySelector('.rc'); if(rc){const kk=spring((t-M.rec-i*.12)/0.6); rc.style.opacity=t>M.rec+i*.12?1:0; rc.style.transform=`scale(${Math.min(1.06,kk)})`}});
  const sk=eo(seg(t,RA[4]+.5,RA[4]+.9)); vis($('rsum'),sk); $('rsum').style.transform=`translateY(${(1-sk)*20}px)`;
  const ck=spring((t-M.cf)/0.6); vis($('cfpill'),t>M.cf?1:0); $('cfpill').style.transform=`scale(${Math.min(1.05,ck)})`;
  $('reg').style.boxShadow=t>M.cf?`0 40px 90px rgba(11,21,51,.14),0 0 0 ${6*eo(seg(t,M.cf,M.cf+.3))}px rgba(37,99,235,.35)`:'';
 }
 // ---------- F
 {const S=$('F'), k=seg(t,SP-.05,SP+.35); vis(S,t>SP-.06?eo(k):0);
  const lk=spring((t-SP-.05)/0.9); $('logo').style.transform=`scale(${t<SP?0.8:0.8+.2*Math.min(1.02,lk)})`; $('logo').style.opacity=seg(t,SP,SP+.25);
  $('shine').style.left=(-200+1100*eio(seg(t,SP+.9,SP+1.8)))+'px';
  [['eq',SP+.15],['eu',SP+1.6],['ed',SP+1.8]].forEach(([id,a])=>{const kk=eo(seg(t,a,a+.45));$(id).style.opacity=kk;$(id).style.transform=`translateY(${(1-kk)*30}px)`});}
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

CK = '<svg viewBox="0 0 32 32"><path d="M6 17l7 7 13-15" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CONF_COLORS = ["#2563EB", "#16A34A", "#FFD43B", "#0B1533", "#93B4F8"]
ROWS = [("3 × avaliação", "DESPESA", "−US$ 450", False), ("2 × reset", "DESPESA", "−US$ 160", False),
        ("Ativação da conta", "DESPESA", "−US$ 130", False), ("Dados de mercado", "DESPESA · 3 MESES", "−US$ 45", True),
        ("Plataforma", "DESPESA · 3 MESES", "−US$ 90", True)]


def build():
    words, groups, pw = words_and_groups()
    ax = lambda v: 80 + 780 * (v + 1000) / 1500
    ticks = ""
    for v, lab in [(-1000, "−1.000"), (-500, "−500"), (0, "0"), (500, "+500")]:
        x = ax(v); big = v == 0
        ticks += (f'<line x1="{x}" x2="{x}" y1="{440 if not big else 425}" y2="{480 if not big else 495}" stroke="#0B1533" stroke-width="{4 if not big else 7}" stroke-linecap="round"/>'
                  f'<text x="{x}" y="{545}" text-anchor="middle" font-family="InterD" font-weight="{900 if big else 700}" font-size="{40 if big else 30}" fill="{"#0B1533" if big else "#7A8499"}">{lab}</text>')
    ticks += '<text x="860" y="610" text-anchor="end" font-family="Inter" font-weight="600" font-size="20" letter-spacing="3" fill="#7A8499">SALDO EM US$</text>'
    conf = "".join(f'<div class="conf" style="background:{CONF_COLORS[i % 5]};left:0;top:0"></div>' for i in range(34))
    rows = ""
    for i, (t, tag, v, rec) in enumerate(ROWS):
        rows += (f'<div class="rr" style="top:{190 + i * 116}px"><div class="ic">$</div><div class="tx"><b>{t}</b><span>{tag}</span>'
                 + ('<i class="rc">RECORRENTE · MENSAL</i>' if rec else '') + f'</div><div class="vv">{v}</div></div>')
    rep = {"__INTER__": INTER, "__LOGO__": LOGO, "__CK__": CK, "__CONF__": conf, "__TICKS__": ticks, "__ROWS__": rows,
           "__ZX0__": str(ax(0) - 26), "__ZX1__": str(ax(0) + 26),
           "__WORDS__": json.dumps(words, ensure_ascii=False), "__GROUPS__": json.dumps(groups), "__PW__": json.dumps(pw),
           "__PH__": json.dumps([p[2] for p in PHRASES]), "__KR__": json.dumps(KEY_RED, ensure_ascii=False),
           "__KG__": json.dumps(KEY_GREEN, ensure_ascii=False), "__KB__": json.dumps(KEY_BLUE, ensure_ascii=False), "__TAIL__": str(TAIL)}
    h = HTML
    for k, v in rep.items():
        h = h.replace(k, v)
    return h, PHRASES[-1][2][1] + TAIL


async def render(out, fps, stills=None):
    from playwright.async_api import async_playwright
    html, end = build()
    hp = os.path.join(HERE, "cashflow1.html"); open(hp, "w").write(html)
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
