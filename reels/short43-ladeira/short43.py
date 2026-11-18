# Short "Perdeu 20%? Agora precisa de 25%" (VID-43) — motion design 1080x1920, série A CONTA DO RISCO.
# Base visual: short60.py / short81_v2.py. Tempos das palavras vêm de whisper_words.json (faster-whisper sobre narr.mp3).
# Uso: python3 short43.py <saida_sem_audio.mp4> [fps]  |  python3 short43.py stills t1 t2 ...  |  python3 short43.py info
import os, sys, json, asyncio, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
INTER = "/usr/share/fonts/opentype/inter"
LOGO = os.path.join(ROOT, "assets", "logo.png")
AV = {k: os.path.join(ROOT, "assets", k + ".png") for k in ("pensativo", "cansado", "explicando", "pare")}
TAIL = 3.6

# legenda com algarismos: correções sobre o texto do whisper (índice -> texto)
FIX = {"Perdeu 10 %": None}
KEY_RED = {"10%", "20%?", "30%?", "metade?", "escada.", "desce", "degrau.", "dobra", "−20%"}
KEY_GREEN = {"11%.", "25%.", "43%.", "dobrar", "ladeira."}
KEY_BLUE = {"antes:", "dia", "semana,", "plano.", "Proteger"}


def load_words():
    raw = json.load(open(os.path.join(HERE, "whisper_words.json")))
    out = []
    i = 0
    while i < len(raw):
        w, a, b = raw[i]
        if w == "10" and i + 1 < len(raw) and raw[i + 1][0] == "%":
            out.append(["10%", a, raw[i + 1][2]]); i += 2; continue
        rep = {"11.": "11%.", "20?": "20%?", "25.": "25%.", "30?": "30%?", "43.": "43%.", "antes.": "antes:", "Limite": "limite",
               "rápido": "rápido,"}
        out.append([rep.get(w, w), a, b]); i += 1
    return out


def groups(words):
    # quebra por frase (pontuação final) e no máximo 6 palavras
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
#top .tag i{width:12px;height:12px;border-radius:50%;background:#E5484D;box-shadow:0 0 0 6px rgba(229,72,77,.15)}
#prog{position:absolute;left:64px;top:300px;display:flex;gap:8px;opacity:0}
#prog b{display:block;width:70px;height:6px;border-radius:6px;background:rgba(11,21,51,.10);overflow:hidden}
#prog b i{display:block;height:100%;width:0;background:#0B1533;border-radius:6px}
#note{position:absolute;left:64px;top:1236px;font:500 24px 'Inter';color:#7A8499;opacity:0}
#cap{position:absolute;left:60px;width:880px;top:1300px;display:flex;flex-wrap:wrap;justify-content:center;align-items:baseline;gap:6px 14px;
  font-family:'InterD';font-weight:900;font-size:68px;line-height:1.12;letter-spacing:-1px}
#cap span{position:relative;display:inline-block;padding:2px 10px;border-radius:16px;color:#0B1533;text-shadow:0 2px 0 rgba(255,255,255,.9),0 0 18px rgba(255,255,255,.9)}
.card{position:absolute;background:rgba(255,255,255,.95);border:2px solid rgba(11,21,51,.06);border-radius:44px;box-shadow:0 40px 90px rgba(11,21,51,.14)}
.hd{font:600 24px 'Inter';letter-spacing:4px;color:#7A8499}
/* A: conta + escada */
#acc{left:70px;width:940px;top:370px;height:230px}
#acc .hd{position:absolute;left:46px;top:34px}
#accn{position:absolute;left:42px;top:70px;font:900 130px 'InterD';letter-spacing:-6px;line-height:1}
#accbar{position:absolute;left:330px;top:100px;width:560px;height:70px;border-radius:20px;background:#EEF1F6;overflow:hidden}
#accfill{position:absolute;left:0;top:0;height:70px;border-radius:20px;background:linear-gradient(90deg,#3B82F6,#2563EB);width:100%}
#accgap{position:absolute;top:0;height:70px;background:repeating-linear-gradient(135deg,rgba(229,72,77,.85) 0 14px,rgba(229,72,77,.55) 14px 28px)}
#stamp{position:absolute;right:40px;top:-38px;font:900 64px 'InterD';color:#fff;background:#E5484D;padding:6px 26px 10px;border-radius:18px;transform:rotate(-6deg);box-shadow:0 18px 40px rgba(229,72,77,.4);opacity:0}
#tbl{left:70px;width:940px;top:640px;height:600px}
#tbl .hdr{position:absolute;left:46px;right:46px;top:34px;display:flex;justify-content:space-between}
#tbl .hdr span{font:600 24px 'Inter';letter-spacing:4px}
.row{position:absolute;left:46px;width:848px;height:110px;opacity:0}
.row .l{position:absolute;left:0;top:18px;width:180px;font:900 64px 'InterD';color:#E5484D;letter-spacing:-2px}
.row .rb{position:absolute;left:190px;top:34px;height:40px;border-radius:12px;background:linear-gradient(90deg,#F2676B,#D93A40)}
.row .gb{position:absolute;right:170px;top:34px;height:40px;border-radius:12px;background:linear-gradient(90deg,#34C77B,#169A55)}
.row .g{position:absolute;right:0;top:14px;width:170px;text-align:right;font:900 72px 'InterD';color:#16A34A;letter-spacing:-2px}
.row .mid{position:absolute;left:50%;top:44px;width:2px;height:24px;background:#C9D2E3}
/* B: escada x ladeira */
#hill{position:absolute;left:40px;top:360px;width:1000px;height:820px}
#B .lab{position:absolute;font:900 54px 'InterD';letter-spacing:-1px;padding:8px 22px 12px;border-radius:18px;color:#fff;opacity:0}
/* C: replay */
#rep{position:absolute;left:70px;top:380px;font:900 46px 'InterD';color:#fff;background:#0B1533;padding:10px 24px 14px;border-radius:14px;letter-spacing:4px;display:flex;align-items:center;gap:14px}
#rep i{width:18px;height:18px;border-radius:50%;background:#E5484D}
#size{left:70px;width:940px;top:480px;height:300px}
#size .hd{position:absolute;left:46px;top:34px}
#sizebars{position:absolute;left:46px;top:96px;display:flex;align-items:flex-end;gap:16px;height:160px}
#sizebars b{display:block;width:70px;border-radius:14px;background:linear-gradient(180deg,#3B82F6,#2563EB)}
#sizex{position:absolute;right:50px;top:96px;font:900 150px 'InterD';letter-spacing:-6px;color:#0B1533;line-height:1}
#acc2{left:70px;width:940px;top:810px;height:330px}
#acc2 .hd{position:absolute;left:46px;top:34px}
#c2n{position:absolute;left:42px;top:80px;font:900 150px 'InterD';letter-spacing:-6px;line-height:1}
#c2r{position:absolute;right:46px;top:66px;text-align:right}
#c2r .k{font:600 24px 'Inter';letter-spacing:4px;color:#7A8499}
#c2r .v{font:900 120px 'InterD';letter-spacing:-5px;color:#16A34A;line-height:1.05}
#lbl{position:absolute;left:46px;right:46px;top:252px;font:700 34px 'InterD';color:#E5484D;opacity:0}
/* D: freio */
#brk{left:64px;width:952px;top:370px;height:860px}
#brk h2{position:absolute;left:52px;top:56px;width:840px;font:900 92px 'InterD';line-height:1.0;letter-spacing:-3px}
#brk h2 em{font-style:normal;color:#2563EB}
.it{position:absolute;left:52px;width:848px;height:130px;border-radius:30px;background:#F3F5FA;border:3px solid #E2E8F0;display:flex;align-items:center;gap:28px;padding:0 34px;font:900 52px 'InterD';letter-spacing:-1px;color:#9AA2B4}
.it .ck{width:70px;height:70px;border-radius:50%;background:#DDE3EE;display:flex;align-items:center;justify-content:center;flex:none}
.it .ck svg{width:42px;height:42px;opacity:0}
#wr{position:absolute;left:52px;top:700px;font:900 64px 'InterD';color:#fff;background:#0B1533;padding:12px 30px 18px;border-radius:22px;transform:rotate(-2deg);opacity:0}
#avD{position:absolute;left:640px;top:860px;width:300px;opacity:0}
/* E: frase */
#dq{position:absolute;left:70px;width:940px;top:470px;font:900 110px 'InterD';line-height:1.02;letter-spacing:-4px}
#dq span{display:inline-block;opacity:0;margin-right:24px}
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
 <div class="scene" id="A">
  <div class="card" id="acc"><div class="hd">SALDO DA CONTA</div><div id="accn">100%</div>
   <div id="accbar"><div id="accfill"></div><div id="accgap"></div></div><div id="stamp">−10%</div></div>
  <div class="card" id="tbl"><div class="hdr"><span style="color:#E5484D">PERDEU</span><span style="color:#16A34A">PARA VOLTAR</span></div>
   __ROWS__
  </div>
 </div>
 <div class="scene" id="B">
  <svg id="hill" viewBox="0 0 1000 820">
   <defs><linearGradient id="rg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F2676B"/><stop offset="1" stop-color="#C8262D"/></linearGradient>
   <linearGradient id="gg" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#34C77B"/><stop offset="1" stop-color="#169A55"/></linearGradient></defs>
   <line x1="20" y1="120" x2="980" y2="120" stroke="#0B1533" stroke-width="4" stroke-dasharray="14 12" opacity=".35"/>
   <text x="24" y="100" font-family="Inter" font-weight="600" font-size="24" letter-spacing="4" fill="#7A8499">100% DA CONTA</text>
   <path id="stairs" d="" fill="url(#rg)"/>
   <path id="ramp" d="" fill="url(#gg)" opacity=".95"/>
   <path id="rampL" d="" fill="none" stroke="#0E7A40" stroke-width="8" stroke-linecap="round"/>
  </svg>
  <div class="lab" id="labD" style="left:70px;top:1150px;background:#E5484D">A DESCIDA: ESCADA</div>
  <div class="lab" id="labV" style="left:560px;top:420px;background:#16A34A">A VOLTA: LADEIRA</div>
  <img id="avB" src="file://__AVB__" style="position:absolute;left:350px;top:620px;width:170px;opacity:0;filter:drop-shadow(0 26px 30px rgba(11,21,51,.25))">
 </div>
 <div class="scene" id="C">
  <div id="rep"><i></i>REPLAY</div>
  <div class="card" id="size"><div class="hd">TAMANHO DA MÃO</div><div id="sizebars"><b id="s1"></b><b id="s2"></b></div><div id="sizex">1×</div></div>
  <div class="card" id="acc2"><div class="hd">SALDO DA CONTA</div><div id="c2n">80%</div>
   <div id="c2r"><div class="k">PARA VOLTAR</div><div class="v" id="c2v">+25%</div></div>
   <div id="lbl">mão maior para recuperar = degrau mais fundo</div></div>
 </div>
 <div class="scene" id="D">
  <div class="card" id="brk"><h2>O freio vem <em>antes</em> da ladeira.</h2>
   <div class="it" id="i1" style="top:340px"><span class="ck"><svg viewBox="0 0 24 24"><path d="M5 12.5l4.2 4.2L19 7" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg></span>Limite de perda no dia</div>
   <div class="it" id="i2" style="top:500px"><span class="ck"><svg viewBox="0 0 24 24"><path d="M5 12.5l4.2 4.2L19 7" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg></span>Limite de perda na semana</div>
   <div id="wr">Escreva no plano.</div>
  </div>
  </div>
 <div class="scene" id="E">
  <div id="dq"><span>Proteger</span><span>a</span><span>conta</span><span>é</span><span>mais</span><span style="color:#16A34A">fácil</span><span>do</span><span>que</span><span style="color:#E5484D">recuperar.</span></div>
  <img id="avD" src="file://__AVD__" style="filter:drop-shadow(0 26px 30px rgba(11,21,51,.25))">
 </div>
 <div class="scene" id="F">
  <div class="logo" id="logo"><img src="file://__LOGO__"><div class="sh" id="shine"></div></div>
  <div class="q" id="eq">Qual é o seu limite de perda no dia?</div>
  <div class="u" id="eu">tradeyouup.net</div>
  <div class="d" id="ed">Exemplo ilustrativo · valores em %, sem custos operacionais.<br>Conteúdo educativo. Não é recomendação de investimento.</div>
 </div>
</div>
<div id="vig"></div>
<div id="top"><div class="tag"><i></i>A CONTA DO RISCO</div></div>
<div id="prog"><b><i></i></b><b><i></i></b><b><i></i></b><b><i></i></b><b><i></i></b></div>
<div id="note">Exemplo ilustrativo · valores em %, sem custos operacionais</div>
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
// ---- marcos
const iP2=wi('Perdeu',1), iP3=wi('Perdeu',iP2+1), iP4=wi('Perdeu',iP3+1), iDesc=wi('descida'), iE=wi('E'), iO=wi('O'), iPr=wi('Proteger');
const M={ l1:wt(wi('10%')), g1:wt(wi('11%.')), l2:wt(iP2+1), g2:wt(wi('25%.')), l3:wt(iP3+1), g3:wt(wi('43%.')), l4:wt(iP4+1), g4:wt(wi('dobrar')),
 bIn:wt(iDesc-1)-0.15, esc:wt(wi('escada.')), lad:wt(wi('ladeira.')), cIn:wt(iE)-0.2, dob:wt(wi('dobra')), des:wt(wi('desce')), deg:wt(wi('degrau.')),
 dIn:wt(iO)-0.2, dia:wt(wi('dia')), sem:wt(wi('semana,')), esc2:wt(wi('escrito')), eIn:wt(iPr)-0.2 };
const ROWS=[[10,11.1,'l1','g1'],[20,25,'l2','g2'],[30,42.9,'l3','g3'],[50,100,'l4','g4']];
// ---- grão
const gc=$('grain').getContext('2d'), gimg=gc.createImageData(360,640);
function grain(f){let s=f*7919+1;const d=gimg.data;for(let i=0;i<d.length;i+=4){s=(s*16807)%2147483647;const v=s%255;d[i]=d[i+1]=d[i+2]=v;d[i+3]=255}gc.putImageData(gimg,0,0)}
const HITS=[[M.l1,10],[M.l2,12],[M.l3,14],[M.l4,20],[M.g4,14],[M.des,22],[M.esc2,10]];
function shake(t){let x=0,y=0;HITS.forEach(([h,a],j)=>{const d=t-h;if(d>=0&&d<.5){const k=a*Math.exp(-9*d);x+=k*Math.sin(d*90+j);y+=k*Math.cos(d*77+j*2)}});return [x,y]}
// ---- legendas
const capEl=$('cap');let capG=-1,capSpans=[];
function buildCap(gi){capEl.innerHTML='';capSpans=[];const [a,b]=G[gi];for(let i=a;i<=b;i++){const s=document.createElement('span');s.textContent=W[i][0];capEl.appendChild(s);capSpans.push([i,s])}}
// ---- escada x ladeira (SVG)
function stairsPath(k){ // 4 degraus descendo de x=40 a x=470, base y=120 -> 720
 const steps=[[40,120],[150,220],[260,340],[360,480],[470,720]]; let d=`M40,120`; const n=k*4;
 for(let i=0;i<4;i++){const f=cl(n-i); if(f<=0)break; const [x0,y0]=steps[i],[x1,y1]=steps[i+1]; const yy=lerp(y0,y1,f); d+=` L${x0},${yy} L${lerp(x0,x1,f)},${yy}`; if(f<1){d+=` L${lerp(x0,x1,f)},780 L40,780 Z`;return d}}
 d+=` L470,780 L40,780 Z`; return d}
function rampPath(k){const x0=470,y0=720,x1=980,y1=120; const x=lerp(x0,x1,k), y=lerp(y0,y1,Math.pow(k,1.6));
 let d=`M${x0},780 L${x0},${y0}`; for(let i=1;i<=24;i++){const kk=k*i/24; d+=` L${lerp(x0,x1,kk)},${lerp(y0,y1,Math.pow(kk,1.6))}`} d+=` L${x},780 Z`; return d}
function rampLine(k){const x0=470,y0=720,x1=980,y1=120; let d=`M${x0},${y0}`; for(let i=1;i<=24;i++){const kk=k*i/24; d+=` L${lerp(x0,x1,kk)},${lerp(y0,y1,Math.pow(kk,1.6))}`} return d}

window.render=function(t,f){
 grain(Math.floor(f/2));
 const [sx,sy]=shake(t); $('world').style.transform=`translate(${sx}px,${sy}px)`;
 $('bg').style.transform=`translate(${Math.sin(t*.25)*30}px,${Math.cos(t*.2)*24}px) scale(${1.05+.03*Math.sin(t*.15)})`;
 $('floor').style.transform=`perspective(900px) rotateX(74deg) translateY(${(t*60)%120}px)`;
 const topO=seg(t,.1,.45)*(1-seg(t,SP-.2,SP+.1)); vis($('top'),topO); vis($('prog'),topO);
 const sc=[[0,M.bIn],[M.bIn,M.cIn],[M.cIn,M.dIn],[M.dIn,M.eIn],[M.eIn,SP]];
 document.querySelectorAll('#prog b i').forEach((el,i)=>{el.style.width=(seg(t,sc[i][0],sc[i][1])*100)+'%'});
 vis($('note'),seg(t,.4,.8)*(1-seg(t,M.eIn-.3,M.eIn)));
 // ---------- A: conta + escada de recuperação
 {const A=$('A'), out=seg(t,M.bIn-.25,M.bIn+.1); vis(A,t<M.bIn+.15?1:0);
  A.style.transform=`translateX(${-1300*eio(out)}px)`; A.style.filter=`blur(${Math.sin(Math.PI*out)*14}px)`;
  const k1=spring((t-0.0)/0.8); $('acc').style.transform=`translateY(${(1-Math.min(1,k1))*-160}px)`; $('acc').style.opacity=cl(t/.12);
  const k2=spring((t-0.25)/0.8); $('tbl').style.transform=`translateY(${(1-Math.min(1,k2))*220}px)`; $('tbl').style.opacity=cl((t-.25)/.15);
  // nível da conta
  let lv=100, lab='−10%', st=-1; ROWS.forEach(([l,g,lk],i)=>{const k=eio(seg(t,M[lk],M[lk]+0.35)); if(t>=M[lk]){st=i;lab='−'+l+'%'} lv=lerp(lv,100-l,k)});
  $('accn').textContent=Math.round(lv)+'%'; $('accn').style.color=lv<99.5?'#E5484D':'#0B1533';
  $('accfill').style.width=lv+'%'; $('accgap').style.left=lv+'%'; $('accgap').style.width=(100-lv)+'%';
  if(st>=0){const sk=spring((t-M[ROWS[st][2]])/0.5); $('stamp').textContent=lab; $('stamp').style.opacity=1; $('stamp').style.transform=`rotate(-6deg) scale(${1.8-0.8*Math.min(1.04,sk)})`}
  else $('stamp').style.opacity=0;
  ROWS.forEach(([l,g,lk,gk],i)=>{const r=$('r'+i), a=M[lk]; const k=eo(seg(t,a-.05,a+.3)); r.style.opacity=k; r.style.transform=`translateX(${(1-k)*-60}px)`;
   r.querySelector('.rb').style.width=(lerp(0,l*4,eio(seg(t,a,a+.45))))+'px';
   const gb=M[gk], gkk=eio(seg(t,gb-.1,gb+.5)); r.querySelector('.gb').style.width=(g*2.8*gkk)+'px';
   const gv=r.querySelector('.g'); gv.style.opacity=seg(t,gb-.1,gb+.1); gv.textContent='+'+Math.round(g*gkk)+'%';
   gv.style.transform=`scale(${1+0.18*Math.exp(-6*Math.max(0,t-gb-.4))*(t>gb+.4?1:0)})`;});
 }
 // ---------- B: escada x ladeira
 {const S=$('B'), inK=eexp(seg(t,M.bIn-.1,M.bIn+.35)), out=seg(t,M.cIn-.2,M.cIn+.15); vis(S,(t>M.bIn-.1&&t<M.cIn+.2)?1:0);
  S.style.transform=`translateX(${1300*(1-inK)-1300*eio(out)}px)`; S.style.filter=`blur(${Math.sin(Math.PI*seg(t,M.bIn-.1,M.bIn+.35))*14+Math.sin(Math.PI*out)*14}px)`;
  const sk=eio(seg(t,M.bIn+.2,M.esc+.2)); $('stairs').setAttribute('d',stairsPath(sk));
  const rk=eio(seg(t,M.esc+.5,M.lad+.4)); $('ramp').setAttribute('d',rampPath(Math.max(0.001,rk))); $('rampL').setAttribute('d',rampLine(Math.max(0.001,rk)));
  [['labD',M.esc-.3],['labV',M.lad-.3]].forEach(([id,a])=>{const k=spring((t-a)/.6); $(id).style.opacity=t>a?1:0; $(id).style.transform=`rotate(-3deg) scale(${t<a?1.5:1.5-.5*Math.min(1.03,k)})`});
  const ak=spring((t-M.esc)/.8); $('avB').style.opacity=seg(t,M.esc,M.esc+.2); $('avB').style.transform=`translateY(${(1-Math.min(1,ak))*120}px)`;
 }
 // ---------- C: replay (mão dobrada)
 {const S=$('C'), inK=eexp(seg(t,M.cIn-.1,M.cIn+.35)), out=seg(t,M.dIn-.2,M.dIn+.15); vis(S,(t>M.cIn-.1&&t<M.dIn+.2)?1:0);
  S.style.transform=`translateY(${(1-inK)*1400-eio(out)*1600}px)`; S.style.filter=`blur(${Math.sin(Math.PI*seg(t,M.cIn-.1,M.cIn+.35))*12+Math.sin(Math.PI*out)*14}px)`;
  $('rep').style.opacity=(Math.floor(t*2.5)%2===0||t>M.cIn+1.2)?1:.35;
  const dk=spring((t-M.dob)/0.7); const sz=t<M.dob?1:1+Math.min(1.04,dk); $('s1').style.height='80px'; $('s2').style.height=(80*sz)+'px';
  $('s2').style.background=t>M.dob?'linear-gradient(180deg,#F2676B,#D93A40)':''; $('sizex').textContent=(t<M.dob+.2?'1×':'2×'); $('sizex').style.color=t>M.dob+.2?'#E5484D':'#0B1533';
  const fk=eio(seg(t,M.des,M.des+.45)); const lv=lerp(80,60,fk), rec=(100/lv-1)*100; $('c2n').textContent=Math.round(lv)+'%'; $('c2n').style.color='#E5484D';
  $('c2v').textContent='+'+Math.round(rec)+'%'; $('c2v').style.transform=`scale(${1+0.15*Math.sin(Math.PI*fk)})`; $('c2v').style.transformOrigin='100% 50%';
  $('acc2').style.transform=`translateY(${fk>0&&fk<1?Math.sin(fk*Math.PI)*30:0}px)`;
  const lk=eo(seg(t,M.deg-.1,M.deg+.3)); $('lbl').style.opacity=lk; $('lbl').style.transform=`translateY(${(1-lk)*20}px)`;
 }
 // ---------- D: freio
 {const S=$('D'), inK=eexp(seg(t,M.dIn-.1,M.dIn+.35)), out=seg(t,M.eIn-.2,M.eIn+.15); vis(S,(t>M.dIn-.1&&t<M.eIn+.2)?1:0);
  S.style.transform=`translateY(${(1-inK)*1500}px)`; S.style.opacity=(t>M.dIn-.1&&t<M.eIn+.2)?1-eo(out):0;
  [['i1',M.dia],['i2',M.sem]].forEach(([id,a])=>{const e=$(id), on=t>=a, k=spring((t-a)/.5);
   e.style.color=on?'#0B1533':'#9AA2B4'; e.style.borderColor=on?'#2563EB':'#E2E8F0'; e.style.background=on?'#EEF4FF':'#F3F5FA';
   e.querySelector('.ck').style.background=on?'#2563EB':'#DDE3EE'; e.querySelector('svg').style.opacity=on?1:0;
   e.style.transform=`scale(${on?1+0.04*Math.exp(-5*(t-a)):1})`;});
  const wk=spring((t-M.esc2)/.6); $('wr').style.opacity=t>M.esc2?1:0; $('wr').style.transform=`rotate(-2deg) scale(${t<M.esc2?1.6:1.6-.6*Math.min(1.03,wk)})`;
  
 }
 // ---------- E: frase final
 {const S=$('E'), inK=eexp(seg(t,M.eIn-.1,M.eIn+.35)), out=seg(t,SP-.12,SP+.15); vis(S,(t>M.eIn-.1&&t<SP+.2)?1:0);
  S.style.transform=`translateY(${(1-inK)*1500}px) scale(${1+.04*seg(t,M.eIn,SP)})`; S.style.opacity=(t>M.eIn-.1&&t<SP+.2)?1-out:0;
  const ak=spring((t-M.eIn-.2)/.9); $('avD').style.opacity=seg(t,M.eIn+.2,M.eIn+.4); $('avD').style.transform=`translateY(${(1-Math.min(1,ak))*200}px)`;
  [...$('dq').children].forEach((s,i)=>{const a=wt(iPr+i)-.05, k=spring((t-a)/0.6);s.style.opacity=cl((t-a)/.08);s.style.transform=`translateY(${(1-Math.min(1,k))*50}px)`});
 }
 // ---------- F: final
 {const S=$('F'), k=seg(t,SP-.05,SP+.35); vis(S,t>SP-.06?eo(k):0);
  const lk=spring((t-SP-.05)/0.9); $('logo').style.transform=`scale(${t<SP?0.8:0.8+.2*Math.min(1.02,lk)})`; $('logo').style.opacity=seg(t,SP,SP+.25);
  $('shine').style.left=(-200+1100*eio(seg(t,SP+.6,SP+1.5)))+'px';
  [['eq',SP+.5],['eu',SP+.85],['ed',SP+1.0]].forEach(([id,a])=>{const kk=eo(seg(t,a,a+.45));$(id).style.opacity=kk;$(id).style.transform=`translateY(${(1-kk)*30}px)`});}
 // ---------- legendas (somem na frase final, que já está na tela)
 let gi=-1; for(let i=0;i<G.length;i++){const s=wt(G[i][0])-0.12; const e=(i+1<G.length)?wt(G[i+1][0])-0.12:SP+0.05; if(t>=s&&t<e)gi=i}
 if(gi>=0&&G[gi][0]>=iPr)gi=-1;
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
    rows = "".join('<div class="row" id="r%d" style="top:%dpx"><div class="l">−%d%%</div><div class="rb"></div><div class="mid"></div>'
                   '<div class="gb"></div><div class="g">+0%%</div></div>' % (i, 96 + i * 122, l) for i, l in enumerate([10, 20, 30, 50]))
    rep = {"__INTER__": INTER, "__LOGO__": LOGO, "__ROWS__": rows, "__AVB__": AV["pensativo"], "__AVD__": AV["pare"],
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
    hp = os.path.join(HERE, "short43.html"); open(hp, "w").write(html)
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
