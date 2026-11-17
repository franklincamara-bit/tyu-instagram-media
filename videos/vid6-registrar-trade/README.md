# VID-6 — Como registrar um trade manualmente (tutorial narrado com quadros, 1:12)
Produzido em 17/11/2026 (rotina de produção). Motor `render.py` (tutorial-narrado-v2, cópia do VID-7). 8 cenas + tela final.
- Prints 800×600 da conta de teste (franklin.camara.s@outlook.com), Novo Trade preenchido com dados fictícios e **nada salvo** (MNQ, Macro PO3, compra, 2 contratos, −150, NY AM, Normal, Seguiu Totalmente, a favor do bias). Rodapé com nome/e-mail borrado. Prints ficam fora do repo (`src/`, no OneDrive).
- Ajustes ao roteiro aprovado, conferidos na tela em 17/11: não há campo de horário (só Data); a sessão fica em "Detalhes do trade"; "Tipo de saída" está na Análise de Proteção (beta, só convidados) e ficou fora; falhas de disciplina aparecem ao escolher "Não Seguiu"; o link "Falha na disciplina vs Erro" abre um modal explicativo; não aparece selo de bias no formulário; parciais fora (bug do R$ em conta USD nos cards de parcial).
- Narração Rafael Valente (ElevenLabs eleven_v4) em `narr-elevenlabs.mp3`, cortada por pausas em s1..s8 (`vid6.py`).
- Render: `python3 vid6.py all` → `out/vid6-final.mp4` (−16 LUFS). Capas: `python3 capa6.py` (3 opções 1280×720).
