/* ===== Mesmo stop, três traders (TYU-19) — cenas ===== */
/* CENA 1 — 10:15, o stop */
const P1=makePanel(0,0,3.45,'O STOP');
addRough(rc.circle(150,230,190,R()),0.3,0.62,P1);
addRough(rc.linearPath([[150,230],[150,168]],R({strokeWidth:7})),0.62,0.68,P1);
addRough(rc.linearPath([[150,230],[180,250]],R({strokeWidth:6})),0.68,0.74,P1);
addText('10:15',150,400,76,0.74,1.15,P1,{anchor:'middle',color:BLUE});
printed('line',{x1:300,y1:560,x2:910,y2:560,stroke:RED,'stroke-width':5,'stroke-dasharray':'16 12'},1.0,P1);
addText('stop',905,540,44,1.05,1.3,P1,{anchor:'end',color:RED});
addRough(rc.linearPath([[310,250],[380,300],[430,270],[500,360],[560,330],[640,450],[700,420],[770,560]],R({stroke:INK,strokeWidth:6})),1.3,1.92,P1);
addRough(rc.circle(770,560,70,R({stroke:RED,strokeWidth:6})),1.92,2.1,P1);
addRough(rc.rectangle(330,620,540,150,R({stroke:RED,strokeWidth:8,roughness:1.8,fill:'#FFE3E3',fillStyle:'hachure',hachureGap:12,fillWeight:2})),2.1,2.33,P1,'#FFE3E3');
addText('STOP −1R',600,730,104,2.33,2.95,P1,{anchor:'middle',color:RED});
illus(P1);

/* CENA 2 — três traders, o mesmo stop */
const P2=makePanel(1,3.5,6.1,'TRÊS TRADERS');
[0,1,2].forEach(k=>{const x=50+k*300,cx=x+130,a=3.62+k*0.25;
  addRough(rc.rectangle(x,130,260,500,R({strokeWidth:4.5})),a,a+0.22,P2);
  addRough(rc.circle(cx,270,120,R({strokeWidth:5})),a+0.22,a+0.4,P2);
  addRough(rc.arc(cx,450,190,170,Math.PI,Math.PI*2,false,R({strokeWidth:5})),a+0.4,a+0.55,P2);
  addText('trader '+(k+1),cx,500,46,a+0.6,a+0.85,P2,{anchor:'middle',color:BLUE});
  addRough(rc.rectangle(x+45,540,170,62,R({stroke:RED,strokeWidth:5,fill:'#FFE3E3',fillStyle:'solid'})),4.85+k*0.18,4.98+k*0.18,P2,'#FFE3E3');
  addText('−1R',cx,588,48,4.98+k*0.18,5.12+k*0.18,P2,{font:'Archivo',weight:900,color:RED,anchor:'middle'});
});
addText('o mesmo stop',480,740,70,5.25,5.95,P2,{anchor:'middle',color:RED});
illus(P2);

/* CENA 3 — trader 1 */
const P3=makePanel(2,6.15,9.95,'TRADER 1');
addText('O que veio depois:',40,150,64,6.23,6.9,P3);
const card3=el('g',{},null);el('rect',{x:70,y:210,width:820,height:380,rx:14,fill:'#FFF3BF'},card3);el('rect',{x:70,y:210,width:820,height:20,fill:'#FFE066'},card3);
addFade(card3,6.5,6.75,P3);
[['anota o motivo',6.85],['fecha a plataforma',7.6],['volta amanhã',8.7]].forEach(([w,a],k)=>{const y=310+k*105;
  addRough(rc.rectangle(115,y-48,54,54,R({strokeWidth:4})),a,a+0.15,P3);
  addText(w,205,y,66,a+0.15,a+0.6,P3);
  addRough(rc.linearPath([[122,y-24],[140,y-4],[180,y-64]],R({stroke:GREEN,strokeWidth:8})),a+0.6,a+0.8,P3)});
addRough(rc.rectangle(250,650,460,110,R({stroke:GREEN,strokeWidth:6,roughness:1.6})),9.3,9.55,P3);
addText('o stop ficou −1R',480,722,56,9.5,9.9,P3,{anchor:'middle',color:GREEN});
illus(P3);

/* CENA 4 — trader 2 */
const P4=makePanel(3,10.0,13.5,'TRADER 2');
addText('entra de novo…',40,160,72,10.25,11.1,P4);
addRough(rc.rectangle(120,240,720,230,R({stroke:RED,strokeWidth:8,roughness:1.8,fill:'#FFE3E3',fillStyle:'hachure',hachureGap:12,fillWeight:2})),11.15,11.45,P4,'#FFE3E3');
addText('MÃO 2×',480,410,150,11.45,11.95,P4,{anchor:'middle',color:RED});
addText('pra recuperar',480,600,82,12.4,13.15,P4,{anchor:'middle',color:INK});
addRough(rc.line(230,625,730,618,R({stroke:RED,strokeWidth:7})),13.15,13.4,P4);
illus(P4);

/* CENA 5 — trader 3 */
const P5=makePanel(4,13.55,17.35,'TRADER 3');
addRough(rc.rectangle(80,110,380,260,R({strokeWidth:5})),13.75,14.05,P5);
addRough(rc.linearPath([[110,300],[180,250],[230,280],[300,190],[360,230],[430,170]],R({stroke:GRAY,strokeWidth:4})),14.05,14.35,P5);
addText('trava.',700,260,110,14.1,14.75,P5,{anchor:'middle',color:BLUE});
addText('…',700,330,70,14.75,14.9,P5,{anchor:'middle',color:GRAY});
addText('próximo trade:',40,500,66,15.25,16.1,P5);
addRough(rc.rectangle(440,560,420,150,R({strokeWidth:6})),16.1,16.3,P5);
addText('STOP',650,670,100,16.3,16.55,P5,{font:'Archivo',weight:900,color:INK,anchor:'middle'});
addRough(rc.line(460,700,840,570,R({stroke:RED,strokeWidth:10})),16.55,16.8,P5);
addText('tirou',300,660,80,16.6,17.05,P5,{anchor:'middle',color:RED});
illus(P5);

/* CENA 6 — o depois */
const P6=makePanel(5,17.4,20.45,'O DEPOIS');
addText('O stop foi igual.',480,140,72,17.56,18.4,P6,{anchor:'middle'});
[['1','volta amanhã',GREEN,true],['2','mão 2×',RED,false],['3','sem stop',RED,false]].forEach(([n,w,c,ok],k)=>{const x=50+k*300,cx=x+130,a=17.7+k*0.3;
  addRough(rc.rectangle(x,210,260,380,R({strokeWidth:4.5,stroke:c})),a,a+0.2,P6);
  addText('trader '+n,cx,280,44,a+0.2,a+0.4,P6,{anchor:'middle',color:GRAY});
  addText('−1R',cx,370,60,a+0.4,a+0.5,P6,{font:'Archivo',weight:900,color:INK,anchor:'middle'});
  addText(w,cx,470,50,a+0.5,a+0.8,P6,{anchor:'middle',color:c});
  if(ok)addRough(rc.linearPath([[cx-40,535],[cx-10,565],[cx+45,500]],R({stroke:GREEN,strokeWidth:9})),a+0.8,a+0.95,P6);
  else{addRough(rc.line(cx-35,505,cx+35,570,R({stroke:RED,strokeWidth:8})),a+0.8,a+0.88,P6);addRough(rc.line(cx+35,505,cx-35,570,R({stroke:RED,strokeWidth:8})),a+0.88,a+0.96,P6)}});
addText('O que veio depois, não.',480,720,70,18.82,19.9,P6,{anchor:'middle',color:BLUE});
addRough(rc.line(150,748,810,742,R({stroke:BLUE,strokeWidth:7})),19.9,20.2,P6);
const N4={};

/* ---------- selo do stop (canto inferior esquerdo) ---------- */
const CK={g:el('g',{},main)};
const ckTitle=el('text',{x:64,y:1470,'font-family':'Archivo','font-weight':800,'font-size':22,'letter-spacing':3,fill:GRAY},CK.g);ckTitle.textContent='O MESMO STOP';
const ckVal=el('text',{x:60,y:1600,'font-family':'Archivo','font-weight':900,'font-size':130,fill:RED},CK.g);
const ckSub=el('text',{x:64,y:1645,'font-family':'Archivo','font-weight':600,'font-size':22,fill:'#64748B'},CK.g);ckSub.textContent='exemplo ilustrativo · conta demo';
const SCORE=[[0,'',GRAY],[2.33,'−1R',RED]];
function updScore(t){let k=0;SCORE.forEach((s,i)=>{if(t>=s[0])k=i});ckVal.textContent=SCORE[k][1];ckVal.setAttribute('fill',SCORE[k][2]);
  const since=t-SCORE[k][0];const sc=k>0?1+0.22*Math.max(0,1-since/0.3):1;ckVal.setAttribute('transform',`translate(60,1600) scale(${sc}) translate(-60,-1600)`);
  ckTitle.style.opacity=k>0?1:0;ckSub.style.opacity=k>0?1:0}

/* ---------- tela final ---------- */
const END={g:el('g',{},main),t0:20.45};
END.g.style.opacity=0;
el('image',{href:'../../assets/logo.png',x:250,y:330,width:580,height:217},END.g);
addText('Conhece um',540,700,104,20.75,21.4,END,{anchor:'middle',color:INK});
addText('trader 2?',540,820,110,21.4,22.0,END,{anchor:'middle',color:RED});
addText('Manda pra ele.',540,930,72,22.1,22.7,END,{anchor:'middle',color:BLUE});
addRough(rc.line(300,955,780,949,R({stroke:BLUE,strokeWidth:7})),22.7,22.95,END);
const url=el('text',{x:540,y:1050,'text-anchor':'middle','font-family':'Archivo','font-weight':800,'font-size':44,fill:INK},END.g);url.textContent='tradeyouup.net';
const disc=el('text',{x:540,y:1100,'text-anchor':'middle','font-family':'Archivo','font-weight':500,'font-size':24,fill:'#64748B'},END.g);disc.textContent='Exemplo ilustrativo · conta demo. Conteúdo educativo.';
