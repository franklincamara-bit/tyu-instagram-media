# Trial Reel "Caixa-Preta do Trader #1" v2.1 (TYU-59). Motion 1080x1920: linha do tempo + gráfico esquemático.
# Roteiro v2.1 (09/11): entrada arriscada 9h38 "porque o stop era pequeno" -> −1R -> entrada atrasada mão pesada -> fecha na mão −2R -> preço no alvo; dia −3R.
# Narração Rafael Valente (raw.mp3; tempos de whisper_words.json). Base visual: ../caixa-preta1/cp1.py.
# Uso: python3 cp2.py <saida_sem_audio.mp4> [fps]  |  python3 cp2.py stills t1 t2 ...
import os, sys, json, asyncio, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
INTER = "/usr/share/fonts/opentype/inter"
LOGO = os.path.join(HERE, "tpl", "logo.png")
OFF = 0.35
TAIL = 3.8
WW = json.load(open(os.path.join(HERE, "whisper_words.json")))
w = lambda i: WW[i][1] + OFF
END_NARR = WW[-1][2] + OFF

# legenda: frases com (texto, índice da palavra no whisper, cor r/g/b/y/None)
CAP = [
    [("A", 0), ("operação", 1), ("durou", 2), ("4", 3, "b"), ("minutos.", 4, "b")],
    [("O", 5), ("erro", 6, "r"), ("começou", 7), ("12", 8, "r"), ("minutos", 9, "r"), ("antes.", 10)],
    [("Vamos", 11), ("abrir", 12), ("a", 13), ("caixa-preta.", 14, "y")],
    [("9h38:", 16, "b"), ("entrada", 21), ("arriscada,", 22, "r"), ("sem", 23), ("confirmação.", 24)],
    [("O", 25), ("motivo?", 26), ("O", 27), ("stop", 28), ("era", 29), ("pequeno.", 30, "y")],
    [("Stopado.", 31, "r"), ("−1R.", 32, "r")],
    [("Dentro", 35), ("do", 36), ("gerenciamento...", 37, "g")],
    [("...mas", 38), ("o", 39), ("emocional", 40, "r"), ("já", 41), ("saiu", 42), ("do", 43), ("plano.", 44)],
    [("9h43:", 45, "b"), ("o", 50), ("preço", 51), ("anda", 52), ("sem", 53), ("você.", 54)],
    [("Bate", 55), ("a", 56), ("vontade", 57, "r"), ("de", 58, "r"), ("não", 59, "r"), ("ficar", 60, "r"), ("de", 61, "r"), ("fora.", 62, "r")],
    [("9h46:", 63, "b"), ("entra", 68), ("atrasado,", 69, "r"), ("fora", 70, "r"), ("do", 71, "r"), ("setup,", 72, "r")],
    [("com", 73), ("a", 74), ("mão", 75, "r"), ("mais", 76, "r"), ("pesada", 77, "r"), ("pra", 78), ("recuperar", 79), ("o", 80), ("stop.", 81)],
    [("Fora", 82), ("do", 83), ("ponto", 84), ("e", 85), ("pesado,", 86)],
    [("o", 87), ("stop", 88, "r"), ("técnico", 89, "r"), ("ficou", 90), ("caro.", 91, "r")],
    [("O", 92), ("preço", 93), ("começa", 94), ("a", 95), ("voltar.", 96)],
    [("Chega", 97), ("perto", 98), ("do", 99), ("stop.", 100)],
    [("Ele", 101), ("fecha", 102, "r"), ("na", 103, "r"), ("mão:", 104, "r"), ("−2R.", 105, "r")],
    [("E", 108), ("aí", 109), ("o", 110), ("preço", 111), ("vira...", 112), ("e", 113), ("vai", 114), ("no", 115), ("alvo.", 116, "g")],
    [("Sem", 117, "y"), ("ele.", 118, "y")],
    [("Parecia", 119), ("um", 120), ("risco", 121, "y"), ("pequeno.", 122, "y")],
    [("Virou", 123), ("um", 124), ("dia", 125, "r"), ("de", 126, "r"), ("stop", 127, "r"), ("desastroso.", 128, "r")],
]


def words_and_groups():
    words, groups = [], []
    for toks in CAP:
        a = len(words)
        for tk in toks:
            words.append([tk[0], round(w(tk[1]), 3), tk[2] if len(tk) > 2 else None])
        groups.append([a, len(words) - 1])
    return words, groups


M = dict(op=w(3), er=w(6), bIn=w(11) - 0.2, open=w(14), cIn=w(16) - 0.25,
         ev=[w(16), w(31), w(45), w(63)], bub=w(27), seal=w(35), crack=w(38),
         rIn=w(82) - 0.25, stopT=w(88), back=w(92), near=w(97), zerar=w(101), stamp=w(105), vira=w(112), alvo=w(116), sem=w(117),
         xIn=w(119) - 0.2, dia=w(123), qIn=w(129) - 0.15, q2=w(131))

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

/* v2: contador do dia, selo, balão, chips */
#day{position:absolute;right:64px;top:226px;background:#0B1533;color:#fff;border-radius:22px;padding:12px 22px 14px;opacity:0;text-align:right;box-shadow:0 16px 36px rgba(11,21,51,.25)}
#day small{display:block;font:600 18px 'Inter';letter-spacing:3px;color:#9AA6C2}
#dayv{font:900 54px 'InterD';letter-spacing:-1px;line-height:1}
#bub{position:absolute;left:420px;top:60px;background:#fff;border:4px solid #0B1533;border-radius:28px;padding:14px 22px;font:900 34px 'InterD';white-space:nowrap;opacity:0;box-shadow:0 18px 36px rgba(11,21,51,.18)}
#bub::after{content:'';position:absolute;left:40px;bottom:-22px;width:30px;height:30px;background:#fff;border-right:4px solid #0B1533;border-bottom:4px solid #0B1533;transform:rotate(45deg)}
#seal{position:absolute;font:900 30px 'InterD';color:#16A34A;background:#E8F7EE;border:4px solid #16A34A;padding:8px 16px;border-radius:14px;opacity:0;white-space:nowrap}
#crk{position:absolute;font:900 30px 'InterD';color:#fff;background:#E5484D;padding:8px 16px;border-radius:14px;opacity:0;white-space:nowrap}
.tags{margin-top:10px;display:flex;gap:10px;flex-wrap:wrap}
.tags b{font:900 24px 'InterD';padding:6px 12px;border-radius:10px;color:#fff;background:#E5484D;opacity:0}
/* R: gráfico esquemático */
#rc{left:54px;width:972px;top:330px;height:900px}
#rclock{position:absolute;left:48px;top:34px;font:900 92px 'InterD';letter-spacing:-3px}
#rclock small{font:600 24px 'Inter';letter-spacing:4px;color:#7A8499;margin-left:16px;vertical-align:middle}
#svg{position:absolute;left:30px;top:170px;width:912px;height:700px}
.lbl{font-family:'InterD';font-weight:900}
#zer{position:absolute;font:900 34px 'InterD';color:#fff;background:#0B1533;padding:12px 22px;border-radius:16px;opacity:0;box-shadow:0 14px 30px rgba(11,21,51,.35)}
#rstamp{position:absolute;left:0;width:1080px;top:1010px;text-align:center;opacity:0;visibility:hidden}
#rstamp b{display:inline-block;font:900 96px 'InterD';color:#fff;background:#E5484D;padding:14px 40px 22px;border-radius:26px;letter-spacing:-2px;border:8px solid #fff;box-shadow:0 30px 70px rgba(229,72,77,.35)}
#sem{position:absolute;font:900 40px 'InterD';color:#0B1533;background:#FFD43B;padding:10px 20px;border-radius:14px;opacity:0;white-space:nowrap}
/* X: risco pequeno? */
#xa{position:absolute;left:0;width:1080px;top:470px;text-align:center;font:900 110px 'InterD';letter-spacing:-4px;line-height:1}
#xa span{display:inline-block;opacity:0}
#xs{position:absolute;left:250px;top:530px;width:580px;height:16px;border-radius:8px;background:#E5484D;transform-origin:0 50%}
#xd{position:absolute;left:0;width:1080px;top:760px;text-align:center;opacity:0}
#xd small{display:block;font:600 30px 'Inter';letter-spacing:6px;color:#7A8499;margin-bottom:10px}
#xd b{display:inline-block;font:900 210px 'InterD';color:#fff;background:#E5484D;padding:10px 54px 30px;border-radius:44px;letter-spacing:-8px;box-shadow:0 40px 90px rgba(229,72,77,.35)}
/* Q: frase final */
#qq{position:absolute;left:0;width:1080px;top:600px;text-align:center}
#qq .a{font:900 120px 'InterD';letter-spacing:-4px;opacity:0;line-height:1}
#qq .b{font:900 82px 'InterD';letter-spacing:-2px;opacity:0;margin-top:30px}
#qq .b i{font-style:normal;background:#FFD43B;padding:4px 20px 12px;border-radius:24px}
/* F */
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
   <div class="ev" id="e0"><div class="tm">9h38</div><div class="dot"></div><div class="bx"><div class="t1">Entrada arriscada</div><div class="t2">sem confirmação · “o stop é pequeno”</div></div></div>
   <div class="ev" id="e1"><div class="tm">9h40</div><div class="dot"></div><div class="bx"><div class="t1">Stopado</div><div class="t2">dentro do gerenciamento</div><div class="chip" style="background:#7A8499">−1R</div></div></div>
   <div class="ev" id="e2"><div class="tm">9h43</div><div class="dot"></div><div class="bx"><div class="t1">O preço anda sem você</div><div class="t2">vontade de não ficar de fora</div></div></div>
   <div class="ev" id="e3"><div class="tm">9h46</div><div class="dot"></div><div class="bx"><div class="t1">Entra atrasado</div><div class="tags"><b id="g1">fora do setup</b><b id="g2" style="background:#F59E0B">mão 2×</b><b id="g3" style="background:#0B1533">missão: recuperar 1R</b></div></div></div>
   <div id="bub">“se der errado, é só 1R”</div>
   <div id="seal">dentro do plano ✓</div><div id="crk">emocional fora do plano ✗</div>
   <div id="pr"><div id="prf"></div></div><div id="prl">PRESSÃO</div>
  </div>
 </div>
 <div class="scene" id="R">
  <div class="card" id="rc">
   <div id="rclock">09:46<small>A OPERAÇÃO</small></div>
   <svg id="svg" viewBox="0 0 912 700">
    <defs><linearGradient id="rz" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E5484D" stop-opacity=".05"/><stop offset="1" stop-color="#E5484D" stop-opacity=".22"/></linearGradient></defs>
    <g id="gAlvo" opacity="0"><line x1="20" x2="892" y1="90" y2="90" stroke="#16A34A" stroke-width="5" stroke-dasharray="14 10"/>
     <rect x="742" y="40" width="150" height="44" rx="10" fill="#16A34A"/><text x="817" y="72" text-anchor="middle" class="lbl" font-size="28" fill="#fff">ALVO</text></g>
    <g id="gEnt" opacity="0"><line x1="20" x2="892" y1="300" y2="300" stroke="#2563EB" stroke-width="5" stroke-dasharray="14 10"/>
     <text x="24" y="285" class="lbl" font-size="28" fill="#2563EB">ENTRADA ATRASADA · MÃO 2×</text></g>
    <g id="gRisk" opacity="0"><rect id="rzone" x="20" y="300" width="872" height="0" fill="url(#rz)"/>
     <line id="stl" x1="20" x2="892" y1="620" y2="620" stroke="#E5484D" stroke-width="6"/>
     <line id="rul" x1="860" x2="860" y1="300" y2="300" stroke="#E5484D" stroke-width="6"/>
     <rect id="stb" x="540" y="636" width="352" height="52" rx="12" fill="#E5484D" opacity="0"/><text id="stt" x="716" y="672" text-anchor="middle" class="lbl" font-size="30" fill="#fff" opacity="0">STOP TÉCNICO = −3R</text></g>
    <polyline id="pl" fill="none" stroke="#0B1533" stroke-width="7" stroke-linejoin="round" stroke-linecap="round" points=""/>
    <circle id="pd" r="13" fill="#0B1533" stroke="#fff" stroke-width="5" cx="-50" cy="-50"/>
    <g id="gExit" opacity="0"><circle id="exc" r="20" fill="#E5484D" stroke="#fff" stroke-width="6"/></g>
   </svg>
   <div id="zer">ZERAR</div><div id="sem">sem ele</div>
  </div>
  <div id="rstamp"><b>−2R</b></div>
 </div>
 <div class="scene" id="X">
  <div id="xa"><span>RISCO</span> <span>PEQUENO?</span></div><div id="xs"></div>
  <div id="xd"><small>RESULTADO DO DIA</small><b>−3R</b></div>
 </div>
 <div class="scene" id="Q"><div id="qq"><div class="a" id="qa">Stop pequeno</div><div class="b" id="qb">não é <i>risco pequeno.</i></div></div></div>
 <div class="scene" id="F">
  <div class="logo" id="logo"><img src="file://__LOGO__"><div class="sh" id="shine"></div></div>
  <div class="q" id="eq">O erro começa antes da entrada.</div>
  <div class="u" id="eu">tradeyouup.net</div>
  <div class="d" id="ed">Exemplo ilustrativo · conta demo · resultados em R, sem custos.<br>Conteúdo educativo. Não é recomendação de investimento.</div>
 </div>
</div>
<div id="vig"></div>
<div id="top"><div class="tag"><i></i>CAIXA-PRETA DO TRADER</div><div class="tag" id="ep">#1</div></div>
<div id="day"><small>RESULTADO DO DIA</small><div id="dayv">0R</div></div>
<div id="note">Exemplo ilustrativo · conta demo · resultados em R</div>
<div id="cap"></div>
<canvas id="grain" width="360" height="640"></canvas>
<script>
const W=__WORDS__, G=__GROUPS__, M=__M__, SP=__SP__, END=SP+__TAIL__;
const $=id=>document.getElementById(id);
const cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)), lerp=(a,b,k)=>a+(b-a)*k, seg=(t,a,b)=>cl((t-a)/(b-a));
const eo=x=>1-Math.pow(1-cl(x),3), eio=x=>{x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2};
const eexp=x=>{x=cl(x);return x===1?1:1-Math.pow(2,-10*x)};
const spring=(x,f=1)=>{x=Math.max(0,x);return 1-Math.exp(-7*x)*Math.cos(10*f*x)};
function vis(el,o){el.style.opacity=o;el.style.visibility=o<=0.001?'hidden':'visible'}
const pop=(t,a,d=.5)=>t<a?0:Math.min(1.08,spring((t-a)/d));
const MIN=['09:38','09:40','09:43','09:46'];
const gc=$('grain').getContext('2d'), gimg=gc.createImageData(360,640);
function grain(f){let s=f*7919+1;const d=gimg.data;for(let i=0;i<d.length;i+=4){s=(s*16807)%2147483647;const v=s%255;d[i]=d[i+1]=d[i+2]=v;d[i+3]=255}gc.putImageData(gimg,0,0)}
const HITS=[[M.er,14],[M.open,10],[M.ev[1],12],[M.crack,8],[M.ev[3],8],[M.stopT,10],[M.stamp,20],[M.alvo,8],[M.dia,18]];
function shake(t){let x=0,y=0;HITS.forEach(([h,a],j)=>{const d=t-h;if(d>=0&&d<.5){const k=a*Math.exp(-9*d);x+=k*Math.sin(d*90+j);y+=k*Math.cos(d*77+j*2)}});return [x,y]}
const AX=m=>60+(m-34)*35.5;
{let h='';for(let m=34;m<=58;m+=2){h+=`<div class="tk" style="left:${AX(m)}px;${m%4==2?'':'height:30px;top:418px'}"></div>`;if(m%4==2)h+=`<div class="tl" style="left:${AX(m)}px">9h${String(m).padStart(2,'0')}</div>`}$('ticks').innerHTML=h;}
const EY=i=>200+i*150;
['e0','e1','e2','e3'].forEach((id,i)=>{$(id).style.top=EY(i)+'px'});
const DOTC=['#F59E0B','#7A8499','#F59E0B','#E5484D'];
// gráfico: x 40..880; fase 1 (entrada -> perto do stop, x 40..430), fase 2 (vira -> alvo, x 430..880)
function py(x){ // y do preço em função de x
 const n=Math.sin(x*.09)*10+Math.sin(x*.031)*14;
 if(x<=430){const k=x/430; return 300+ (585-300)*Math.pow(k,1.25) + n*(1-k*.6);}
 if(x<=520){const k=(x-430)/90; return 585-40*eio(k)+n*.4;}
 const k=(x-520)/360; return 545-(545-92)*eio(k)+n*(1-k);
}
const capEl=$('cap');let capG=-1,capSpans=[];
const COL={r:'#E5484D',g:'#16A34A',b:'#2563EB',y:'#D97706'}, COLBG={y:'#FFD43B'};
function buildCap(gi){capEl.innerHTML='';capSpans=[];const [a,b]=G[gi];for(let i=a;i<=b;i++){const s=document.createElement('span');s.textContent=W[i][0];capEl.appendChild(s);capSpans.push([i,s])}}
function inScene(id,a,b,t){const S=$(id),on=t>a&&t<b;vis(S,on?1:0);return on}

window.render=function(t,f){
 grain(Math.floor(f/2));
 const [sx,sy]=shake(t); $('world').style.transform=`translate(${sx}px,${sy}px)`;
 $('bg').style.transform=`translate(${Math.sin(t*.25)*30}px,${Math.cos(t*.2)*24}px) scale(${1.05+.03*Math.sin(t*.15)})`;
 $('floor').style.transform=`perspective(900px) rotateX(74deg) translateY(${(t*40)%120}px)`;
 const topO=seg(t,.15,.55)*(1-seg(t,SP-.2,SP+.1)); vis($('top'),topO);
 // contador do dia (C, R)
 {const on=t>M.cIn&&t<M.xIn+.1; const o=(on?seg(t,M.cIn,M.cIn+.3)*(1-seg(t,M.xIn-.2,M.xIn+.05)):0); vis($('day'),o);
  let v='0R',c='#fff'; if(t>=M.ev[1]){v='−1R';c='#FF9AA0'} if(t>=M.stamp){v='−3R';c='#FF6B70'}
  $('dayv').textContent=v; $('dayv').style.color=c;
  const pk=Math.max(t>=M.ev[1]?Math.exp(-6*(t-M.ev[1])):0,t>=M.stamp?Math.exp(-6*(t-M.stamp)):0);
  $('day').style.transform=`scale(${1+.25*pk})`; $('day').style.background=pk>.3?'#E5484D':'#0B1533';}
 vis($('note'),seg(t,M.cIn+.3,M.cIn+.7)*(1-seg(t,M.xIn-.3,M.xIn)));
 // ---------- A
 if(inScene('A',-1,M.bIn+.2,t)){const S=$('A');
  const out=seg(t,M.bIn-.25,M.bIn+.1); S.style.transform=`translateX(${-1300*eio(out)}px)`; S.style.filter=`blur(${Math.sin(Math.PI*out)*14}px)`;
  const k1=spring((t-0.05)/0.9); $('ax').style.transform=`translateY(${(1-Math.min(1,k1))*-160}px)`; $('ax').style.opacity=cl((t-.05)/.15);
  const ok=eexp(seg(t,M.op,M.op+.6)); $('opb').style.left=AX(46)+'px'; $('opb').style.width=(AX(50)-AX(46))*ok+'px';
  $('opl').style.opacity=eo(seg(t,M.op+.1,M.op+.5)); $('opl').style.left=(AX(50)-340)+'px'; $('opl').style.width='340px';
  const ek=eio(seg(t,M.er,M.er+.9)); const x0=lerp(AX(46),AX(38),ek); $('erb').style.left=x0+'px'; $('erb').style.width=(AX(46)-x0+10)+'px'; $('erb').style.opacity=t>=M.er?1:0;
  const lk=spring((t-M.er-.5)/0.6); $('erl').style.left=(AX(38))+'px'; $('erl').style.opacity=cl((t-M.er-.5)/.12); $('erl').style.transform=`translateY(${(1-Math.min(1,lk))*40}px)`;}
 // ---------- B
 if(inScene('B',M.bIn-.1,M.cIn+.25,t)){const S=$('B');
  const ik=spring((t-M.bIn)/0.8), out=seg(t,M.cIn-.2,M.cIn+.2);
  $('box').style.transform=`translateY(${(1-Math.min(1,ik))*900}px) rotate(${(1-Math.min(1,ik))*-8}deg) scale(${1+1.6*eio(out)})`;
  S.style.opacity=1-eo(out);
  const lid=eio(seg(t,M.open,M.open+.5)); $('lid').style.transform=`rotateX(${lid*-110}deg)`;
  $('beam').style.opacity=eo(seg(t,M.open+.1,M.open+.5))*(1-out);}
 // ---------- C: 9h38 -> 9h46
 if(inScene('C',M.cIn-.1,M.rIn+.2,t)){const S=$('C');
  const ik=eexp(seg(t,M.cIn-.1,M.cIn+.35)), out=seg(t,M.rIn-.2,M.rIn+.15);
  S.style.transform=`translateY(${(1-ik)*1500-eio(out)*1600}px)`; S.style.filter=`blur(${Math.sin(Math.PI*seg(t,M.cIn-.1,M.cIn+.35))*12+Math.sin(Math.PI*out)*14}px)`;
  let cur=-1; M.ev.forEach((a,i)=>{if(t>=a)cur=i});
  const ck=cur<0?0:spring((t-M.ev[cur])/0.5); $('clock').firstChild.textContent=cur<0?'09:38':MIN[cur];
  $('clock').style.transform=`translateY(${(1-Math.min(1,ck))*-30}px)`; $('clock').style.color=cur>=3?'#E5484D':'#0B1533';
  ['e0','e1','e2','e3'].forEach((id,i)=>{const a=M.ev[i], k=spring((t-a)/0.7), el=$(id);
   el.style.opacity=cl((t-a)/.12); el.style.transform=`translateX(${(1-Math.min(1,k))*120}px)`;
   const dot=el.querySelector('.dot'); dot.style.borderColor=DOTC[i]; dot.style.transform=`scale(${t<a?0:Math.min(1.15,spring((t-a)/0.5))})`;
   el.querySelector('.tm').style.color=DOTC[i]==='#7A8499'?'#0B1533':DOTC[i];
   const bx=el.querySelector('.bx'); bx.style.borderColor=(i===3&&t>M.ev[3])?'#E5484D':'transparent'; bx.style.background=(i===3&&t>M.ev[3])?'#FDECEC':'#F6F8FC';});
  $('railf').style.height=Math.max(0,cur<0?0:(EY(cur)-200+52)*eo(seg(t,M.ev[cur],M.ev[cur]+.5))+(cur>0?(EY(cur-1)-200+52)*(1-eo(seg(t,M.ev[cur],M.ev[cur]+.5))):0))+'px';
  // balão "só 1R"
  const bk=pop(t,M.bub,.6); $('bub').style.top=(EY(0)-78)+'px'; $('bub').style.opacity=cl((t-M.bub)/.12)*(1-seg(t,M.ev[1]+.6,M.ev[1]+1));
  $('bub').style.transform=`scale(${bk}) rotate(-2deg)`; $('bub').style.transformOrigin='10% 100%';
  // selo dentro do plano -> racha
  const sk=pop(t,M.seal,.5); $('seal').style.left='480px'; $('seal').style.top=(EY(1)+12)+'px'; $('seal').style.opacity=cl((t-M.seal)/.12)*(1-eo(seg(t,M.crack,M.crack+.25)));
  $('seal').style.transform=`scale(${sk}) rotate(${t>M.crack?-6*eo(seg(t,M.crack,M.crack+.3)):0}deg)`; $('seal').style.textDecoration=t>M.crack?'line-through':'none';
  const kk=pop(t,M.crack+.15,.5); $('crk').style.left='440px'; $('crk').style.top=(EY(1)+12)+'px'; $('crk').style.opacity=cl((t-M.crack-.15)/.12)*(1-seg(t,M.ev[2]-.2,M.ev[2]+.1)); $('crk').style.transform=`scale(${kk}) rotate(-3deg)`;
  // tags 9h46
  [['g1',M.ev[3]+.75],['g2',M.ev[3]+1.9],['g3',M.ev[3]+2.6]].forEach(([id,a])=>{$(id).style.opacity=cl((t-a)/.12);$(id).style.display='inline-block';$(id).style.transform=`scale(${pop(t,a,.45)})`});
  // pressão: 0 -> 20% (entrada) -> 60% (emocional) -> 75% -> 92%
  let pv=0; if(t>M.ev[0])pv=.2*eo(seg(t,M.ev[0],M.ev[0]+.6)); if(t>M.crack)pv=lerp(.2,.6,eo(seg(t,M.crack,M.crack+.5))); if(t>M.ev[2])pv=lerp(.6,.75,eo(seg(t,M.ev[2],M.ev[2]+.6))); if(t>M.ev[3])pv=lerp(.75,.92,eo(seg(t,M.ev[3],M.ev[3]+.6)));
  $('prf').style.height=(660*pv)+'px';}
 // ---------- R: a operação (gráfico)
 if(inScene('R',M.rIn-.1,M.xIn+.2,t)){const S=$('R');
  const ik=eexp(seg(t,M.rIn-.1,M.rIn+.35)), out=seg(t,M.xIn-.2,M.xIn+.15);
  S.style.transform=`translateY(${(1-ik)*1500-eio(out)*1600}px)`; S.style.filter=`blur(${Math.sin(Math.PI*seg(t,M.rIn-.1,M.rIn+.35))*12+Math.sin(Math.PI*out)*14}px)`;
  const clk=t<M.zerar?'09:46':(t<M.vira?'09:50':'09:54'); $('rclock').firstChild.textContent=clk; $('rclock').style.color=t>=M.zerar?'#E5484D':'#0B1533';
  $('gEnt').setAttribute('opacity',eo(seg(t,M.rIn+.2,M.rIn+.6)));
  $('gAlvo').setAttribute('opacity',eo(seg(t,M.rIn+.5,M.rIn+.9)));
  // risco: régua desce até o stop técnico
  const rk=eio(seg(t,M.stopT-.3,M.stopT+.5)); $('gRisk').setAttribute('opacity',t>M.stopT-.3?1:0);
  $('rul').setAttribute('y2',300+320*rk); $('stl').setAttribute('opacity',rk); $('rzone').setAttribute('height',320*rk);
  $('stb').setAttribute('opacity',eo(seg(t,M.stopT+.4,M.stopT+.7))); $('stt').setAttribute('opacity',eo(seg(t,M.stopT+.4,M.stopT+.7)));
  // preço
  let xe=40; if(t>M.back-.4) xe=lerp(40,430,eio(seg(t,M.back-.4,M.zerar))); if(t>M.vira-.3) xe=lerp(430,880,eio(seg(t,M.vira-.3,M.alvo+.1)));
  let pts=[]; for(let x=40;x<=xe;x+=6)pts.push(x+','+py(x).toFixed(1)); pts.push(xe+','+py(xe).toFixed(1));
  $('pl').setAttribute('points',pts.join(' ')); $('pl').setAttribute('opacity',t>M.rIn+.3?1:0);
  $('pd').setAttribute('cx',xe); $('pd').setAttribute('cy',py(xe)); $('pd').setAttribute('opacity',t>M.rIn+.3?1:0);
  $('pl').setAttribute('stroke',t>M.zerar?'#9AA3B5':'#0B1533'); $('pl').setAttribute('stroke-dasharray',t>M.zerar+.3?'':'');
  // zerar
  const zk=pop(t,M.zerar-.1,.45); $('zer').style.left=(30+430-60)+'px'; $('zer').style.top=(170+py(430)-120)+'px'; $('zer').style.opacity=cl((t-M.zerar+.1)/.1)*(1-seg(t,M.stamp+.6,M.stamp+.9));
  $('zer').style.transform=`scale(${zk*(t>M.zerar&&t<M.zerar+.15?.88:1)})`;
  $('gExit').setAttribute('opacity',t>M.zerar?1:0); $('exc').setAttribute('cx',430); $('exc').setAttribute('cy',py(430));
  // carimbo −2R
  const sk=spring((t-M.stamp)/0.6); vis($('rstamp'),t>=M.stamp&&t<M.stamp+1.2?1-seg(t,M.stamp+.8,M.stamp+1.1):0);
  $('rstamp').style.transform=`rotate(-4deg) scale(${t<M.stamp?2.2:2.2-1.2*Math.min(1.03,sk)})`;
  // alvo: pulso + "sem ele"
  if(t>M.alvo){const p=Math.exp(-4*(t-M.alvo)); $('gAlvo').setAttribute('transform',`translate(${817*-.15*p},${90*-.15*p}) scale(${1+.15*p})`)}
  $('sem').style.left='470px'; $('sem').style.top=(170+120)+'px'; $('sem').style.opacity=cl((t-M.sem)/.12); $('sem').style.transform=`rotate(-4deg) scale(${pop(t,M.sem,.5)})`;}
 // ---------- X: risco pequeno? -> dia −3R
 if(inScene('X',M.xIn-.1,M.qIn+.2,t)){const S=$('X');
  const ik=eexp(seg(t,M.xIn-.1,M.xIn+.35)), out=seg(t,M.qIn-.2,M.qIn+.15);
  S.style.transform=`translateY(${(1-ik)*1500-eio(out)*1600}px)`; S.style.filter=`blur(${Math.sin(Math.PI*out)*14}px)`;
  [...$('xa').children].forEach((s,i)=>{const a=M.xIn+.15+i*.25;s.style.opacity=cl((t-a)/.1);s.style.transform=`translateY(${(1-Math.min(1,spring((t-a)/.6)))*60}px)`});
  $('xs').style.transform=`scaleX(${eio(seg(t,M.dia-.2,M.dia+.2))})`; $('xs').style.top='520px';
  $('xd').style.opacity=cl((t-M.dia)/.1); $('xd').querySelector('b').style.transform=`scale(${t<M.dia?1.8:1.8-.8*Math.min(1.03,spring((t-M.dia)/.6))}) rotate(-2deg)`;}
 // ---------- Q
 if(inScene('Q',M.qIn-.1,SP+.2,t)){const S=$('Q');
  const out=seg(t,SP-.12,SP+.15); S.style.opacity=1-out;
  $('qa').style.opacity=eo(seg(t,M.qIn,M.qIn+.3)); $('qa').style.transform=`translateY(${(1-eo(seg(t,M.qIn,M.qIn+.3)))*40}px)`;
  const bk=spring((t-M.q2)/0.7); $('qb').style.opacity=cl((t-M.q2)/.1); $('qb').style.transform=`scale(${t<M.q2?1.5:1.5-.5*Math.min(1.03,bk)})`;}
 // ---------- F
 {const S=$('F'), k=seg(t,SP-.05,SP+.35); vis(S,t>SP-.06?eo(k):0);
  const lk=spring((t-SP-.05)/0.9); $('logo').style.transform=`scale(${t<SP?0.8:0.8+.2*Math.min(1.02,lk)})`; $('logo').style.opacity=seg(t,SP,SP+.25);
  $('shine').style.left=(-200+1100*eio(seg(t,SP+.6,SP+1.5)))+'px';
  [['eq',SP+.5],['eu',SP+.85],['ed',SP+1.0]].forEach(([id,a])=>{const kk=eo(seg(t,a,a+.45));$(id).style.opacity=kk;$(id).style.transform=`translateY(${(1-kk)*30}px)`});}
 // ---------- legendas (somem na frase final, que já está na tela)
 let gi=-1; for(let i=0;i<G.length;i++){const s=W[G[i][0]][1]-0.12; const e=(i+1<G.length)?W[G[i+1][0]][1]-0.12:M.qIn; if(t>=s&&t<e)gi=i}
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
    words, groups = words_and_groups()
    sp = END_NARR + 0.25
    rep = {"__INTER__": INTER, "__LOGO__": LOGO, "__WORDS__": json.dumps(words, ensure_ascii=False), "__GROUPS__": json.dumps(groups),
           "__M__": json.dumps(M), "__SP__": "%.3f" % sp, "__TAIL__": str(TAIL)}
    h = HTML
    for k, v in rep.items(): h = h.replace(k, v)
    return h, sp + TAIL


async def render(out, fps, stills=None):
    from playwright.async_api import async_playwright
    html, end = build()
    hp = os.path.join(HERE, "cp2.html"); open(hp, "w").write(html)
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
