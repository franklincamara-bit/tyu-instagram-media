# Short "Acerta 60% e a conta cai? Faça a conta" (VID-39) — motion design 1080x1920.
# Base visual: short81_v2.py. Tempos vêm de phrases.json ([[ini, fim], ...] por frase da narração).
# Uso: python3 short60.py <saida_sem_audio.mp4> [fps] [t0 t1]  |  python3 short60.py stills t1 t2 ...
import os, sys, json, asyncio, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(HERE, "tpl")
FONT = os.path.join(TPL, "Archivo.ttf")
INTER = "/usr/share/fonts/opentype/inter"
LOGO = os.path.join(TPL, "logo.png")

# Frases: (legenda com algarismos, texto falado para pesar a duração de cada palavra)
PHRASES = [
    ("Você acerta 60% dos trades e mesmo assim a conta cai?", "Você acerta sessenta por cento dos trades e mesmo assim a conta cai?"),
    ("Faz a conta.", "Faz a conta."),
    ("Ganha 10 pontos quando acerta.", "Ganha dez pontos quando acerta."),
    ("Perde 20 quando erra.", "Perde vinte quando erra."),
    ("Em 100 trades: +600, −800.", "Em cem trades: mais seiscentos, menos oitocentos."),
    ("−200 pontos.", "Menos duzentos pontos."),
    ("Agora outro trader.", "Agora outro trader."),
    ("Acerta só 40%, mas ganha 30 e perde 10.", "Acerta só quarenta por cento, mas ganha trinta e perde dez."),
    ("+1.200, −600.", "Mais mil e duzentos, menos seiscentos."),
    ("+600 pontos.", "Mais seiscentos pontos."),
    ("Ganhando metade do que perde, você precisa acertar 67% só para empatar.", "Ganhando metade do que perde, você precisa acertar sessenta e sete por cento só para empatar."),
    ("Antes de olhar o acerto, olhe quanto você ganha e quanto perde.", "Antes de olhar o acerto, olhe quanto você ganha e quanto perde."),
]
SPOKEN = {"60%": "sessenta por cento", "10": "dez", "20": "vinte", "100": "cem", "+600,": "mais seiscentos", "−800.": "menos oitocentos",
          "−200": "menos duzentos", "40%,": "quarenta por cento", "30": "trinta", "10.": "dez", "+1.200,": "mais mil e duzentos",
          "−600.": "menos seiscentos", "+600": "mais seiscentos", "67%": "sessenta e sete por cento"}
KEY_RED = ["cai?", "20", "−800.", "−200", "67%"]
KEY_GREEN = ["10", "+600,", "40%,", "30", "+1.200,", "+600"]
KEY_BLUE = ["empatar.", "ganha", "perde."]
TAIL = 3.6  # tela final depois da fala


def load_phrases():
    p = os.path.join(HERE, "phrases.json")
    if os.path.exists(p):
        return json.load(open(p))
    # estimativa provisória (~14 caracteres/s, pausas de 0,35 s) até chegar a narração real
    t, out = 0.0, []
    for _, sp in PHRASES:
        d = max(0.7, len(sp) / 14.0)
        out.append([round(t, 2), round(t + d, 2)]); t += d + 0.35
    return out


def words_and_groups(ph):
    words, groups = [], []
    for (cap, _), seg in zip(PHRASES, ph):
        toks = cap.split()
        wts = [len(SPOKEN.get(w, w)) + 1 for w in toks]
        idx0 = len(words)
        # seg = [ini, fim] ou [ini, fim, k, fim1, ini2]: palavras < k em [ini, fim1], resto em [ini2, fim]
        parts_t = [(0, len(toks), seg[0], seg[1])] if len(seg) == 2 else [(0, seg[2], seg[0], seg[3]), (seg[2], len(toks), seg[4], seg[1])]
        for i0, i1, a, b in parts_t:
            tot, acc = sum(wts[i0:i1]), 0
            for w, k in zip(toks[i0:i1], wts[i0:i1]):
                words.append([w, round(a + (b - a) * acc / tot, 3)]); acc += k
        # quebra frases longas em grupos de até 6 palavras
        n = len(toks)
        if len(seg) > 2:
            groups.append([idx0, idx0 + seg[2] - 1]); groups.append([idx0 + seg[2], idx0 + n - 1]); continue
        parts = 1 if n <= 6 else (2 if n <= 12 else 3)
        size = -(-n // parts)
        for s in range(0, n, size):
            groups.append([idx0 + s, idx0 + min(n, s + size) - 1])
    return words, groups


HTML = r"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'Archivo';src:url('file://__FONT__') format('truetype');font-weight:100 900;font-stretch:62% 125%}
@font-face{font-family:'InterD';src:url('file://__INTER__/InterDisplay-Black.otf');font-weight:900}
@font-face{font-family:'InterD';src:url('file://__INTER__/InterDisplay-Bold.otf');font-weight:700}
@font-face{font-family:'Inter';src:url('file://__INTER__/Inter-SemiBold.otf');font-weight:600}
@font-face{font-family:'Inter';src:url('file://__INTER__/Inter-Medium.otf');font-weight:500}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#EEF1F7;font-family:'InterD',sans-serif;color:#0B1533}
#bg{position:absolute;inset:-200px;background:
  radial-gradient(900px 900px at 78% 12%,rgba(37,99,235,.16),transparent 62%),
  radial-gradient(800px 800px at 10% 92%,rgba(22,163,74,.10),transparent 60%),
  linear-gradient(180deg,#F7F8FC 0%,#ECEFF6 100%)}
#floor{position:absolute;left:-1200px;width:3480px;top:980px;height:2600px;transform-origin:50% 0;
  background-image:linear-gradient(rgba(11,21,51,.07) 2px,transparent 2px),linear-gradient(90deg,rgba(11,21,51,.07) 2px,transparent 2px);
  background-size:120px 120px;-webkit-mask-image:linear-gradient(180deg,transparent 0%,#000 18%,#000 55%,transparent 100%)}
#world{position:absolute;inset:0;transform-origin:540px 860px}
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
.card{position:absolute;background:rgba(255,255,255,.94);border:2px solid rgba(11,21,51,.06);border-radius:44px;box-shadow:0 40px 90px rgba(11,21,51,.14)}
.hd{font:600 24px 'Inter';letter-spacing:4px;color:#7A8499}
/* A: gancho */
#score{left:90px;width:900px;top:380px;height:430px}
#score .hd{position:absolute;left:52px;top:46px}
#score .n{position:absolute;left:48px;top:96px;font:900 300px 'InterD';letter-spacing:-16px;line-height:.9;color:#0B1533}
#score .n small{font-size:170px;letter-spacing:-6px;margin-left:4px}
#chk{position:absolute;right:60px;top:120px;width:190px;height:190px;border-radius:50%;background:linear-gradient(160deg,#34C77B,#169A55);
  box-shadow:0 24px 50px rgba(22,154,85,.35);display:flex;align-items:center;justify-content:center}
#chk svg{width:110px;height:110px}
#mini{left:90px;width:900px;top:840px;height:340px;overflow:hidden}
#mini .hd{position:absolute;left:52px;top:36px}
#mini .q{position:absolute;right:48px;top:24px;font:900 54px 'InterD';color:#E5484D;letter-spacing:-1px;opacity:0}
#faz{position:absolute;left:0;width:1080px;top:600px;text-align:center;opacity:0;visibility:hidden}
#faz b{display:inline-block;font:900 120px 'InterD';color:#fff;background:#0B1533;padding:20px 50px 28px;border-radius:32px;letter-spacing:-3px;box-shadow:0 30px 70px rgba(11,21,51,.35)}
/* B/C: traders */
.thd{position:absolute;left:70px;top:372px;display:flex;align-items:center;gap:18px}
.thd b{font:900 40px 'InterD';color:#fff;background:#0B1533;padding:10px 22px 12px;border-radius:16px;letter-spacing:-.5px}
.thd span{font:700 34px 'InterD';color:#0B1533}
.thd span em{font-style:normal;color:#7A8499}
.pile{position:absolute;top:500px;width:400px;height:520px}
.pl{position:absolute;left:0;width:400px;bottom:-48px;text-align:center;font:600 22px 'Inter';letter-spacing:4px;color:#7A8499}
.tl{position:absolute;width:46px;height:46px;border-radius:11px;display:flex;align-items:center;justify-content:center;font:900 15px 'InterD';color:#fff;letter-spacing:-.5px}
.tl.g{background:linear-gradient(160deg,#34C77B,#169A55);box-shadow:0 5px 10px rgba(22,154,85,.22)}
.tl.r{background:linear-gradient(160deg,#F2676B,#D93A40);box-shadow:0 5px 10px rgba(217,58,64,.25)}
.cnt{position:absolute;top:1060px;width:400px;text-align:center;font:900 76px 'InterD';letter-spacing:-2px}
.tot{position:absolute;left:0;width:1080px;top:690px;text-align:center;opacity:0;visibility:hidden}
.tot b{display:inline-block;font:900 92px 'InterD';color:#fff;padding:8px 36px 14px;border-radius:26px;letter-spacing:-2px;box-shadow:0 26px 60px rgba(11,21,51,.28)}
#cmp{position:absolute;left:70px;width:940px;top:520px;display:flex;gap:28px;opacity:0;visibility:hidden}
#cmp .c{flex:1;background:#fff;border-radius:36px;padding:34px 34px 40px;border:2px solid rgba(11,21,51,.06);box-shadow:0 30px 70px rgba(11,21,51,.14)}
#cmp .c .k{font:600 22px 'Inter';letter-spacing:4px;color:#7A8499}
#cmp .c .a{font:900 110px 'InterD';letter-spacing:-5px;margin-top:10px}
#cmp .c .ar{font:700 34px 'InterD';color:#7A8499;margin-top:2px}
#cmp .c .v{font:900 96px 'InterD';letter-spacing:-4px;margin-top:6px}
/* D: fórmula */
#fcard{left:54px;width:972px;top:380px;height:840px}
#fcard .hd{position:absolute;left:52px;top:46px}
#ftx{position:absolute;left:52px;top:110px;width:870px;display:flex;align-items:center;gap:26px;font:900 54px 'InterD';letter-spacing:-1px}
.fr{display:inline-flex;flex-direction:column;align-items:center}
.fr .t{padding:0 10px 10px;color:#E5484D}
.fr .b{padding:10px 10px 0;border-top:6px solid #0B1533}
#fnum{position:absolute;left:52px;top:330px;font:900 64px 'InterD';letter-spacing:-1.5px;opacity:0}
#fnum .r{color:#E5484D}
#bar{position:absolute;left:52px;top:500px;width:868px;height:86px;border-radius:24px;background:#EEF1F6;overflow:visible}
#bfill{position:absolute;left:0;top:0;height:86px;border-radius:24px;background:linear-gradient(90deg,#3B82F6,#2563EB);width:0}
#bpct{position:absolute;left:24px;top:16px;font:900 52px 'InterD';color:#fff}
.mk{position:absolute;top:-30px;width:6px;height:146px;border-radius:3px;opacity:0}
.mk span{position:absolute;left:50%;transform:translateX(-50%);white-space:nowrap;font:700 28px 'InterD'}
#mkE{background:#0B1533}#mkE span{top:150px;color:#0B1533}
#mkA{background:#E5484D}#mkA span{top:-44px;color:#E5484D}
#fax{position:absolute;left:52px;top:720px;width:868px;display:flex;justify-content:space-between;font:500 24px 'Inter';color:#9AA2B4}
/* E: fecho */
#dq{position:absolute;left:64px;width:950px;top:380px;font:900 92px 'InterD';line-height:1.02;letter-spacing:-3px}
#dq span{display:inline-block;opacity:0;margin-right:20px}
#plan{position:absolute;left:64px;width:900px;top:720px;perspective:1600px}
#plan .in{background:#fff;border-radius:40px;padding:44px 48px 30px;border:2px solid rgba(11,21,51,.06);box-shadow:0 40px 90px rgba(11,21,51,.14);transform-origin:50% 100%}
#plan h3{font:600 24px 'Inter';letter-spacing:5px;color:#2563EB;margin-bottom:12px}
.pr{display:flex;justify-content:space-between;align-items:center;padding:24px 0;border-top:2px solid #EEF1F6;font:700 40px 'InterD';opacity:0}
.pr .f{position:relative;width:180px;height:62px;border-radius:16px;background:#F3F5FA;border:2px dashed #C9D2E3}
.pr .f i{position:absolute;left:22px;top:13px;width:4px;height:36px;background:#2563EB;border-radius:2px;opacity:0}
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
  <div class="card" id="score"><div class="hd">TAXA DE ACERTO</div><div class="n">60<small>%</small></div>
   <div id="chk"><svg viewBox="0 0 24 24"><path id="chkp" d="M5 12.5l4.2 4.2L19 7" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="22" stroke-dashoffset="22"/></svg></div></div>
  <div class="card" id="mini"><div class="hd">SALDO DA CONTA</div><div class="q" id="miniq">E A CONTA CAI?</div>
   <svg width="900" height="340" style="position:absolute;left:0;top:0"><defs><linearGradient id="ag" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E5484D" stop-opacity=".22"/><stop offset="1" stop-color="#E5484D" stop-opacity="0"/></linearGradient></defs>
   <path id="miniA" fill="url(#ag)"/><path id="miniL" fill="none" stroke="#E5484D" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/><circle id="miniD" r="12" fill="#fff" stroke="#E5484D" stroke-width="7"/></svg></div>
  <div id="faz"><b>FAZ A CONTA.</b></div>
 </div>
 __TRADERS__
 <div class="scene" id="CMP"><div id="cmp">
  <div class="c"><div class="k">TRADER A</div><div class="a">60%</div><div class="ar">de acerto ↓</div><div class="v" style="color:#E5484D">−200</div><div class="ar">pontos</div></div>
  <div class="c"><div class="k">TRADER B</div><div class="a">40%</div><div class="ar">de acerto ↓</div><div class="v" style="color:#16A34A">+600</div><div class="ar">pontos</div></div>
 </div></div>
 <div class="scene" id="D">
  <div class="card" id="fcard"><div class="hd">ACERTO MÍNIMO PARA EMPATAR</div>
   <div id="ftx"><span>acerto mínimo =</span><span class="fr"><span class="t">perda</span><span class="b">ganho + perda</span></span></div>
   <div id="fnum"><span class="r">20</span> ÷ (10 + <span class="r">20</span>) = <span style="color:#2563EB">67%</span></div>
   <div id="bar"><div id="bfill"><span id="bpct">0%</span></div>
    <div class="mk" id="mkA" style="left:calc(60% - 3px)"><span>Trader A · 60%</span></div>
    <div class="mk" id="mkE" style="left:calc(66.7% - 3px)"><span>EMPATE · 67%</span></div></div>
   <div id="fax"><span>0%</span><span>50%</span><span>100%</span></div>
  </div>
 </div>
 <div class="scene" id="E">
  <div id="dq"><span>Antes</span><span>do</span><span>acerto,</span><span style="color:#16A34A">quanto</span><span style="color:#16A34A">ganha</span><span>e</span><span style="color:#E5484D">quanto</span><span style="color:#E5484D">perde?</span></div>
  <div id="plan"><div class="in" id="planin"><h3>NO SEU PLANO</h3>
   <div class="pr" id="p1">Ganho médio<span class="f"><i id="cur"></i></span></div>
   <div class="pr" id="p2">Perda média<span class="f"></span></div>
   <div class="pr" id="p3">Acerto mínimo<span class="f"></span></div>
  </div></div>
 </div>
 <div class="scene" id="F">
  <div class="logo" id="logo"><img src="file://__LOGO__"><div class="sh" id="shine"></div></div>
  <div class="q" id="eq">Qual é o seu acerto mínimo?</div>
  <div class="u" id="eu">tradeyouup.net</div>
  <div class="d" id="ed">Exemplo ilustrativo, sem custos operacionais.<br>Conteúdo educativo. Não é recomendação de investimento.</div>
 </div>
</div>
<div id="vig"></div>
<div id="top"><div class="tag"><i></i>A CONTA DO RISCO</div></div>
<div id="prog"><b><i></i></b><b><i></i></b><b><i></i></b><b><i></i></b></div>
<div id="note">Exemplo ilustrativo · valor esperado, sem custos operacionais</div>
<div id="cap"></div>
<canvas id="grain" width="360" height="640"></canvas>
<script>
const W=__WORDS__, G=__GROUPS__, P=__PH__, KR=new Set(__KR__), KG=new Set(__KG__), KB=new Set(__KB__);
const SP=P[P.length-1][1]+0.1, END=SP+__TAIL__;
const $=id=>document.getElementById(id);
const cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)), lerp=(a,b,k)=>a+(b-a)*k, seg=(t,a,b)=>cl((t-a)/(b-a));
const eo=x=>1-Math.pow(1-cl(x),3), eio=x=>{x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2};
const eexp=x=>{x=cl(x);return x===1?1:1-Math.pow(2,-10*x)};
const spring=(x,f=1)=>{x=Math.max(0,x);return 1-Math.exp(-7*x)*Math.cos(10*f*x)};
function vis(el,o){el.style.opacity=o;el.style.visibility=o<=0.001?'hidden':'visible'}
function wt(i){return W[i][1]}           // tempo da palavra i
function ph(i){return P[i]}               // [ini,fim] da frase i
// índice da primeira palavra de cada frase
const PW=[];{let k=0;__PWC__.forEach(n=>{PW.push(k);k+=n})}
function wordAt(p,j){return wt(PW[p]+j)}
// ---- marcos (derivados da narração)
const M={
 a0:0, cai:wordAt(0,10), faz:ph(1)[0], bIn:ph(1)[1]+0.15,
 gIn:ph(2)[0]+0.1, rIn:ph(3)[0]+0.05, cnt:ph(4)[0], tot:ph(5)[0],
 cIn:ph(6)[0]-0.1, cgIn:ph(7)[0]+0.15, crIn:wordAt(7,7), ccnt:ph(8)[0], ctot:ph(9)[0],
 cmp:ph(9)[1]+0.1, dIn:ph(10)[0]+1.1, n67:wordAt(10,8), eIn:ph(11)[0]-0.15
};
// ---- grão
const gc=$('grain').getContext('2d'), gimg=gc.createImageData(360,640);
function grain(f){let s=f*7919+1;const d=gimg.data;for(let i=0;i<d.length;i+=4){s=(s*16807)%2147483647;const v=s%255;d[i]=d[i+1]=d[i+2]=v;d[i+3]=255}gc.putImageData(gimg,0,0)}
const HITS=[[M.faz+0.05,16],[M.tot+0.05,22],[M.ctot+0.05,22],[M.n67,18]];
function shake(t){let x=0,y=0;HITS.forEach(([h,a],j)=>{const d=t-h;if(d>=0&&d<.5){const k=a*Math.exp(-9*d);x+=k*Math.sin(d*90+j);y+=k*Math.cos(d*77+j*2)}});return [x,y]}
// ---- mini gráfico da conta caindo
// 25 trades: 15 acertos (+10) e 10 erros (−20) — a curva desce mesmo com 60% de acerto
const PAT='WWLWWLWLWWLWWLWLWWLWWLWLW', MP=[[60,0]];{let v=0;for(let i=0;i<PAT.length;i++){v+=PAT[i]==='W'?10:-20;MP.push([60+(i+1)*31,v])}}
const mny=Math.min(...MP.map(p=>p[1])), mxy=Math.max(...MP.map(p=>p[1]));
function my(v){return 110+ (mxy-v)/(mxy-mny)*190}
// ---- traders: posições das peças
function tilePos(i,base){const r=Math.floor(i/8),c=i%8;return [c*50+2, 520-46-r*50]}
const TR={B:{gStart:'gIn',rStart:'rIn'},C:{gStart:'cgIn',rStart:'crIn'}};
// ---- legendas
const capEl=$('cap');let capG=-1,capSpans=[];
function buildCap(gi){capEl.innerHTML='';capSpans=[];const [a,b]=G[gi];for(let i=a;i<=b;i++){const s=document.createElement('span');s.textContent=W[i][0];capEl.appendChild(s);capSpans.push([i,s])}}

function trader(id,t,o){
 const S=$(id), g=[...S.querySelectorAll('.tl.g')], r=[...S.querySelectorAll('.tl.r')];
 const gs=M[o.g], rs=M[o.r], gd=Math.max(0.9,Math.min(1.8,(rs-gs)-0.25)), rd=Math.max(0.9,Math.min(1.8,o.rEnd-rs));
 let gl=0, rl=0;
 const fall=(el,i,st,n,dur)=>{const s=st+dur*i/n; const k=cl((t-s)/0.32); const y=-(1-k*k)*380; const land=t>=s+0.32;
   el.style.opacity=cl((t-s)/0.16); el.style.transform=`translateY(${y}px) scale(${land?1+0.12*Math.exp(-12*(t-s-0.32)):1})`; return land};
 g.forEach((el,i)=>{if(fall(el,i,gs,g.length,gd))gl++});
 r.forEach((el,i)=>{if(fall(el,i,rs,r.length,rd))rl++});
 S.querySelector('.cg').textContent='+'+(gl*o.gv).toLocaleString('pt-BR');
 S.querySelector('.cr').textContent=(rl? '−':'')+(rl*o.rv).toLocaleString('pt-BR');
 const ck=seg(t,M[o.cnt],M[o.cnt]+0.4); [S.querySelector('.cg'),S.querySelector('.cr')].forEach(e=>{e.style.opacity=.35+.65*(gl>0?1:0); e.style.transform=`scale(${1+0.12*Math.sin(Math.PI*ck)})`});
 const tt=M[o.tot], tk=spring((t-tt)/0.6), tot=S.querySelector('.tot'); vis(tot,t>=tt?1:0);
 tot.style.transform=`rotate(-3deg) scale(${t<tt?2:2-Math.min(1.03,tk)})`; tot.style.filter=`blur(${cl(1-(t-tt)/0.1)*10}px)`;
}

window.render=function(t,f){
 grain(Math.floor(f/2));
 const [sx,sy]=shake(t); $('world').style.transform=`translate(${sx}px,${sy}px)`;
 $('bg').style.transform=`translate(${Math.sin(t*.25)*30}px,${Math.cos(t*.2)*24}px) scale(${1.05+.03*Math.sin(t*.15)})`;
 $('floor').style.transform=`perspective(900px) rotateX(74deg) translateY(${(t*60)%120}px)`;
 const topO=seg(t,.15,.55)*(1-seg(t,SP-.2,SP+.1)); vis($('top'),topO); vis($('prog'),topO);
 const sc=[[0,M.bIn],[M.bIn,M.cmp],[M.cmp,M.eIn],[M.eIn,SP]];
 document.querySelectorAll('#prog b i').forEach((el,i)=>{el.style.width=(seg(t,sc[i][0],sc[i][1])*100)+'%'});
 vis($('note'),seg(t,M.bIn+.3,M.bIn+.7)*(1-seg(t,M.eIn-.3,M.eIn)));
 // ---------- A: gancho
 {const A=$('A'), out=seg(t,M.bIn-.25,M.bIn+.1); vis(A,t<M.bIn+.15?1:0);
  A.style.transform=`translateX(${-1300*eio(out)}px) scale(${1+0.05*seg(t,0,M.bIn)})`; A.style.filter=`blur(${Math.sin(Math.PI*out)*14}px)`;
  const k1=spring((t-0.1)/0.9); $('score').style.transform=`translateY(${(1-Math.min(1,k1))*-160}px) rotateX(${(1-Math.min(1,k1))*-40}deg)`; $('score').style.opacity=cl((t-.1)/.15);
  const ck=spring((t-0.55)/0.6); $('chk').style.transform=`scale(${t<0.55?0:Math.min(1.08,ck)})`; $('chkp').setAttribute('stroke-dashoffset',22*(1-eo(seg(t,0.7,1.05))));
  const k2=spring((t-0.9)/0.9); $('mini').style.transform=`translateY(${(1-Math.min(1,k2))*200}px)`; $('mini').style.opacity=cl((t-.9)/.15);
  const dk=eio(seg(t,1.2,M.cai+0.2)), n=Math.max(1,dk*(MP.length-1)); let d=`M${MP[0][0]},${my(MP[0][1])}`, last=[MP[0][0],my(MP[0][1])];
  for(let i=1;i<=Math.floor(n);i++){d+=` L${MP[i][0]},${my(MP[i][1])}`;last=[MP[i][0],my(MP[i][1])]}
  const fr=n-Math.floor(n); if(Math.floor(n)<MP.length-1){const a=MP[Math.floor(n)],b=MP[Math.floor(n)+1];last=[lerp(a[0],b[0],fr),my(lerp(a[1],b[1],fr))];d+=` L${last[0]},${last[1]}`}
  $('miniL').setAttribute('d',d); $('miniA').setAttribute('d',d+` L${last[0]},340 L${MP[0][0]},340 Z`); $('miniD').setAttribute('cx',last[0]); $('miniD').setAttribute('cy',last[1]);
  const qk=spring((t-M.cai)/0.6); vis($('miniq'),t>=M.cai?1:0); $('miniq').style.transform=`scale(${t<M.cai?1.6:1.6-.6*Math.min(1.03,qk)})`;$('miniq').style.transformOrigin='100% 50%';
  const fk=spring((t-M.faz)/0.6); vis($('faz'),t>=M.faz?1:0); $('faz').style.transform=`rotate(-3deg) scale(${t<M.faz?2:2-Math.min(1.03,fk)})`; $('faz').style.filter=`blur(${cl(1-(t-M.faz)/0.1)*10}px)`;
  ['score','mini'].forEach(id=>{$(id).style.filter=t>M.faz?`blur(${4*eo(seg(t,M.faz,M.faz+.2))}px)`:''});
 }
 // ---------- B: trader A
 {const S=$('B'), inK=eexp(seg(t,M.bIn-.1,M.bIn+.35)), out=seg(t,M.cIn-.2,M.cIn+.15); vis(S,(t>M.bIn-.1&&t<M.cIn+.2)?1:0);
  S.style.transform=`translateX(${1300*(1-inK)-1300*eio(out)}px)`; S.style.filter=`blur(${Math.sin(Math.PI*seg(t,M.bIn-.1,M.bIn+.35))*14+Math.sin(Math.PI*out)*14}px)`;
  trader('B',t,{g:'gIn',r:'rIn',rEnd:M.cnt+0.3,gv:10,rv:20,cnt:'cnt',tot:'tot'});}
 // ---------- C: trader B
 {const S=$('C'), inK=eexp(seg(t,M.cIn-.1,M.cIn+.35)), out=seg(t,M.cmp-.2,M.cmp+.15); vis(S,(t>M.cIn-.1&&t<M.cmp+.2)?1:0);
  S.style.transform=`translateX(${1300*(1-inK)}px) scale(${1-0.3*eio(out)})`; S.style.opacity=(t>M.cIn-.1&&t<M.cmp+.2)?1-eo(out):0;
  S.style.filter=`blur(${Math.sin(Math.PI*seg(t,M.cIn-.1,M.cIn+.35))*14+eio(out)*12}px)`;
  trader('C',t,{g:'cgIn',r:'crIn',rEnd:M.ccnt+0.3,gv:30,rv:10,cnt:'ccnt',tot:'ctot'});}
 // ---------- comparação
 {const S=$('CMP'), out=seg(t,M.dIn-.25,M.dIn+.1); vis(S,(t>M.cmp-.05&&t<M.dIn+.15)?1:0);
  const k=spring((t-M.cmp)/0.8); $('cmp').style.opacity=cl((t-M.cmp)/.12); $('cmp').style.visibility=t>M.cmp?'visible':'hidden';
  $('cmp').style.transform=`translateY(${(1-Math.min(1,k))*120}px) scale(${.9+.1*Math.min(1,k)})`;
  S.style.transform=`translateY(${-1400*eio(out)}px)`; S.style.filter=`blur(${Math.sin(Math.PI*out)*14}px)`;}
 // ---------- D: fórmula
 {const S=$('D'), inK=eexp(seg(t,M.dIn-.1,M.dIn+.35)), out=seg(t,M.eIn-.2,M.eIn+.15); vis(S,(t>M.dIn-.1&&t<M.eIn+.2)?1:0);
  S.style.transform=`translateY(${(1-inK)*1400-eio(out)*1600}px)`; S.style.filter=`blur(${Math.sin(Math.PI*seg(t,M.dIn-.1,M.dIn+.35))*12+Math.sin(Math.PI*out)*14}px)`;
  const a=M.dIn+0.35; $('ftx').style.opacity=seg(t,a,a+.3); $('ftx').style.transform=`translateY(${(1-eo(seg(t,a,a+.4)))*30}px)`;
  const nb=M.n67-0.9; $('fnum').style.opacity=eo(seg(t,nb,nb+.3)); $('fnum').style.transform=`translateY(${(1-eo(seg(t,nb,nb+.4)))*30}px)`;
  const fk=eio(seg(t,nb+.1,M.n67+0.25)); const pct=fk*66.7; $('bfill').style.width=pct+'%'; $('bpct').textContent=Math.round(pct)+'%'; $('bpct').style.opacity=pct>14?1:0;
  $('mkA').style.opacity=eo(seg(t,nb+.4,nb+.7)); const ek=spring((t-M.n67-0.2)/0.6); $('mkE').style.opacity=t>M.n67+0.2?1:0; $('mkE').style.transform=`scaleY(${Math.min(1.05,ek)})`;
 }
 // ---------- E: fecho
 {const S=$('E'), inK=eexp(seg(t,M.eIn-.1,M.eIn+.35)), out=seg(t,SP-.12,SP+.15); vis(S,(t>M.eIn-.1&&t<SP+.2)?1:0);
  S.style.transform=`translateY(${(1-inK)*1500}px) scale(${1+.04*seg(t,M.eIn,SP)})`; S.style.opacity=(t>M.eIn-.1&&t<SP+.2)?1-out:0;
  const e0=M.eIn+0.15, L=SP-e0; const wts=[0,1,4,6,8,9,10,11].map(j=>wordAt(11,j));
  [...$('dq').children].forEach((s,i)=>{const k=spring((t-wts[i])/0.6);s.style.opacity=cl((t-wts[i])/.08);s.style.transform=`translateY(${(1-Math.min(1,k))*50}px)`});
  const pa=e0+L*0.45, pk=spring((t-pa)/0.9); $('planin').style.transform=`rotateX(${t<pa?50:(1-Math.min(1,pk))*50}deg) translateY(${t<pa?120:(1-Math.min(1,pk))*120}px)`; $('plan').style.opacity=seg(t,pa,pa+.2);
  [['p1',pa+.3],['p2',pa+.65],['p3',pa+1.0]].forEach(([id,a])=>{const k=eo(seg(t,a,a+.35));$(id).style.opacity=k;$(id).style.transform=`translateX(${(1-k)*40}px)`});
  $('cur').style.opacity=(t>pa+1.3&&Math.floor((t-pa-1.3)*2.4)%2===0)?1:0;
 }
 // ---------- F: final
 {const S=$('F'), k=seg(t,SP-.05,SP+.35); vis(S,t>SP-.06?eo(k):0);
  const lk=spring((t-SP-.05)/0.9); $('logo').style.transform=`scale(${t<SP?0.8:0.8+.2*Math.min(1.02,lk)})`; $('logo').style.opacity=seg(t,SP,SP+.25);
  $('shine').style.left=(-200+1100*eio(seg(t,SP+.6,SP+1.5)))+'px';
  [['eq',SP+.5],['eu',SP+.85],['ed',SP+1.0]].forEach(([id,a])=>{const kk=eo(seg(t,a,a+.45));$(id).style.opacity=kk;$(id).style.transform=`translateY(${(1-kk)*30}px)`});}
 // ---------- legendas
 let gi=-1; for(let i=0;i<G.length;i++){const s=wt(G[i][0])-0.12; const e=(i+1<G.length)?wt(G[i+1][0])-0.12:SP+0.05; if(t>=s&&t<e)gi=i}
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


def trader_html(sid, name, desc, ng, gl, nr, rl, total, tcol):
    def tiles(n, cls, lab):
        out = []
        for i in range(n):
            r, c = divmod(i, 8)
            out.append('<div class="tl %s" style="left:%dpx;top:%dpx">%s</div>' % (cls, c * 50 + 2, 520 - 46 - r * 50, lab))
        return "".join(out)
    return ('<div class="scene" id="%s"><div class="thd"><b>%s</b><span>%s</span></div>'
            '<div class="pile" style="left:70px">%s<div class="pl">ACERTOS · %d</div></div>'
            '<div class="pile" style="left:530px">%s<div class="pl">ERROS · %d</div></div>'
            '<div class="cnt cg" style="left:70px;color:#16A34A">+0</div><div class="cnt cr" style="left:530px;color:#E5484D">0</div>'
            '<div class="tot"><b style="background:%s">= %s pontos</b></div></div>') % (
        sid, name, desc, tiles(ng, "g", gl), ng, tiles(nr, "r", rl), nr, tcol, total)


def build():
    ph = load_phrases()
    words, groups = words_and_groups(ph)
    tr = (trader_html("B", "TRADER A", "60% de acerto <em>·</em> ganha 10 <em>·</em> perde 20", 60, "+10", 40, "−20", "−200", "#E5484D") +
          trader_html("C", "TRADER B", "40% de acerto <em>·</em> ganha 30 <em>·</em> perde 10", 40, "+30", 60, "−10", "+600", "#16A34A"))
    pwc = [len(c.split()) for c, _ in PHRASES]
    rep = {"__FONT__": FONT, "__INTER__": INTER, "__LOGO__": LOGO, "__TRADERS__": tr,
           "__WORDS__": json.dumps(words, ensure_ascii=False), "__GROUPS__": json.dumps(groups), "__PH__": json.dumps([p[:2] for p in ph]),
           "__KR__": json.dumps(KEY_RED, ensure_ascii=False), "__KG__": json.dumps(KEY_GREEN, ensure_ascii=False),
           "__KB__": json.dumps(KEY_BLUE, ensure_ascii=False), "__TAIL__": str(TAIL), "__PWC__": json.dumps(pwc)}
    h = HTML
    for k, v in rep.items():
        h = h.replace(k, v)
    return h, ph[-1][1] + 0.1 + TAIL


async def render(out, fps, t0, t1, stills=None):
    from playwright.async_api import async_playwright
    html, end = build()
    hp = os.path.join(HERE, "short60.html"); open(hp, "w").write(html)
    if t1 is None: t1 = end
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
        for f in range(int(round(t0 * fps)), int(round(t1 * fps))):
            await pg.evaluate("render(%f,%d)" % (f / fps, f))
            ff.stdin.write(await pg.screenshot(type="jpeg", quality=95))
        print("errors:", errs); await b.close()
    ff.stdin.close(); ff.wait()


if __name__ == "__main__":
    if sys.argv[1] == "stills":
        asyncio.run(render(None, 60, 0, 0, [float(x) for x in sys.argv[2:]]))
    elif sys.argv[1] == "info":
        _, end = build(); print(json.dumps(load_phrases()), end)
    else:
        fps = int(sys.argv[2]) if len(sys.argv) > 2 else 60
        t0 = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
        t1 = float(sys.argv[4]) if len(sys.argv) > 4 else None
        asyncio.run(render(sys.argv[1], fps, t0, t1))
        print("ok", sys.argv[1])
