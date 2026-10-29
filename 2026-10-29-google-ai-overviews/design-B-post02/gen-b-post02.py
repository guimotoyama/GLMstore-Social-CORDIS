# -*- coding: utf-8 -*-
"""Direção B (vencedora) — Swiss claro / Brutalista. 8 slides completos.
Post: Google AI Overviews — 80% das buscas terminam sem clique.
Off-white, type gigante, grid racional, zero decoração. SEM numero gigante ao fundo."""
import os, re, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "B-post02")
ICON_DIR = os.path.join(BASE, "icons")
os.makedirs(OUT, exist_ok=True)

def _prep_svg(svg, size, cls):
    m = re.search(r"<svg([^>]*)>", svg)
    attrs = m.group(1)
    vb = re.search(r'viewBox="[^"]*"', attrs)
    attrs = re.sub(r'\s(width|height)="[^"]*"', "", attrs)
    attrs = re.sub(r'\sclass="[^"]*"', "", attrs)
    new = f'<svg width="{size}" height="{size}" class="{cls}"'
    if vb:
        new += " " + vb.group(0)
    return svg[:m.start()] + new + attrs + ">" + svg[m.end():]

def icon(name, size=30, cls="ic"):
    p = os.path.join(ICON_DIR, name + ".svg")
    svg = open(p, encoding="utf-8").read()
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    return _prep_svg(svg, size, cls)

def wa_icon(size=34):
    svg = open(os.path.join(ICON_DIR, "whatsapp-solid.svg"), encoding="utf-8").read()
    return _prep_svg(svg, size, "ic wa-ic")

CSS = """@import url('https://fonts.googleapis.com/css2?family=B612+Mono:wght@700&family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
* { margin:0; padding:0; box-sizing:border-box; }
html,body { width:1080px; height:1350px; overflow:hidden; }
body { background:#f5eded; color:#0f0f0f; font-family:'Space Grotesk',sans-serif; -webkit-font-smoothing:antialiased; }
.slide { position:relative; width:1080px; height:1350px; padding:80px 100px 0; display:flex; flex-direction:column; overflow:hidden; }
.layer { position:relative; z-index:2; display:flex; flex-direction:column; flex:1; min-height:0; padding-bottom:180px; }
.meta { font-family:'B612 Mono',monospace; font-size:22px; letter-spacing:.18em; text-transform:uppercase; color:#979797; margin-bottom:48px; display:flex; justify-content:space-between; }
h1 { font-family:'Space Grotesk',sans-serif; font-size:132px; line-height:.95; font-weight:700; letter-spacing:-.04em; color:#0f0f0f; }
h2 { font-family:'Space Grotesk',sans-serif; font-size:92px; line-height:.98; font-weight:700; letter-spacing:-.035em; color:#0f0f0f; }
.red { color:#ca3e47; }
.rule { width:80px; height:6px; background:#ca3e47; margin:34px 0; border-radius:3px; }
.lead { font-family:'Inter',sans-serif; font-size:33px; line-height:1.45; color:#0f0f0f; max-width:760px; font-weight:500; }
.spacer { flex:1; }
.row { display:flex; align-items:baseline; gap:26px; padding:28px 0; border-top:2px solid #0f0f0f; }
.row:last-of-type { border-bottom:2px solid #0f0f0f; }
.row .n { font-family:'B612 Mono',monospace; font-size:27px; color:#ca3e47; min-width:56px; flex:0 0 auto; }
.row p { font-size:37px; line-height:1.28; color:#0f0f0f; font-weight:600; }
.chip { display:inline-block; font-family:'B612 Mono',monospace; font-size:20px; letter-spacing:.16em; text-transform:uppercase; color:#ca3e47; border:2px solid #ca3e47; border-radius:999px; padding:12px 24px; margin-top:28px; }
.footer { position:absolute; left:100px; right:100px; bottom:74px; z-index:3; display:flex; align-items:center; justify-content:space-between; font-family:'B612 Mono',monospace; font-size:20px; letter-spacing:.16em; text-transform:uppercase; color:#979797; }
.foot-logo { height:50px; width:auto; opacity:.9; }
.cta { display:inline-flex; align-items:center; gap:18px; font-family:'Space Grotesk',sans-serif; font-size:38px; font-weight:600; color:#f5eded; padding:26px 38px; background:#0f0f0f; border-radius:999px; }
.cta .ic { color:#ca3e47; }
.wa-row { display:inline-flex; align-items:center; gap:20px; margin-top:26px; padding:20px 34px; border:2px solid #0f0f0f; border-radius:999px; }
.wa-row .wa-ic { width:38px; height:38px; color:#ca3e47; flex:0 0 auto; }
.wa-row .num { font-family:'Space Grotesk',sans-serif; font-size:38px; font-weight:600; color:#0f0f0f; }
.swipe { position:absolute; right:100px; bottom:132px; z-index:3; font-family:'B612 Mono',monospace; font-size:22px; letter-spacing:.16em; text-transform:uppercase; color:#ca3e47; }
"""

def page(body, foot_n=None):
    foot = f'<div class="footer">{footer(foot_n or 0)}</div>' if foot_n is not None else ""
    return f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="slide">
<div class="layer">{body}</div>{foot}
<div class="swipe">arraste &rarr;</div>
</div></body></html>"""

def footer(n, total=8):
    return f'<img class="foot-logo" src="logo-glm.png"><span>{n:02d} / {total:02d}</span>'

def meta(section):
    return f'<div class="meta"><span>{section}</span><span>03 NOV 2026</span></div>'

S = []

# 1 capa — SEM numero gigante ao fundo
S.append(page(f"""
{meta('Google Ads &middot; SEO')}
<h1>80% das buscas<br>agora <span class="red">terminam<br>sem clique</span></h1>
<div class="rule"></div>
<p class="lead">O Google passou a mostrar respostas diretas no topo da busca. Para donos de negócio local, isso significa que o cliente pode nem saber que você existe.</p>
<div class="spacer"></div>
""", foot_n=1))

# 2 antes x agora
S.append(page(f"""
{meta('O que mudou')}
<h2>O jogo mudou</h2>
<div class="rule"></div>
<div class="row"><span class="n">01</span><p>Antes: clicar no anúncio levava direto para o seu site.</p></div>
<div class="row"><span class="n">02</span><p>Agora: o clique morre numa tela de respostas diretas do Google.</p></div>
<div class="row"><span class="n">03</span><p>Resultado: você paga pelo clique, mas o visitante nunca chega até você.</p></div>
<div class="spacer"></div>
<div class="chip">Google AI Overviews</div>
""", foot_n=2))

# 3 o que e AI Overviews
S.append(page(f"""
{meta('O que e')}
<h2>A resposta vem pronta</h2>
<div class="rule"></div>
<p class="lead">O Google lê várias páginas, monta um resumo e mostra no topo da busca. Você não precisa clicar em nada.</p>
<div class="row" style="margin-top:26px"><span class="n">01</span><p>Você pergunta &ldquo;barbearia em Pinheiros&rdquo;</p></div>
<div class="row"><span class="n">02</span><p>O Google mostra nome, endereço e horários</p></div>
<div class="row"><span class="n">03</span><p>Sem abrir nenhum site</p></div>
<div class="spacer"></div>
""", foot_n=3))

# 4 por que importa
S.append(page(f"""
{meta('Por que importa')}
<h2>Quem n&atilde;o aparece<br>n&atilde;o existe</h2>
<div class="rule"></div>
<div class="row"><span class="n">01</span><p>Seu site n&atilde;o apareceu — o do concorrente apareceu.</p></div>
<div class="row"><span class="n">02</span><p>O cliente viu a resposta e foi embora.</p></div>
<div class="row"><span class="n">03</span><p>Do seu lado, o telefone continua sem tocar.</p></div>
<div class="spacer"></div>
""", foot_n=4))

# 5 o efeito na conta
S.append(page(f"""
{meta('O efeito na conta')}
<h2>O painel continua<br>belo</h2>
<div class="rule"></div>
<p class="lead">O clique entra, a visita n&atilde;o vem. O relat&oacute;rio mostra convers&otilde;es que nunca aconteceram — e o or&ccedil;amento continua sendo gasto.</p>
<div class="spacer"></div>
<div class="row"><span class="n">!</span><p>N&uacute;mero subindo n&atilde;o &eacute; campanha melhorando.</p></div>
""", foot_n=5))

# 6 o que fazer
S.append(page(f"""
{meta('O que fazer')}
<h2>Quatro coisas<br>para come&ccedil;ar</h2>
<div class="rule"></div>
<div class="row"><span class="n">01</span><p>Google Business Profile em dia: hor&aacute;rios, fotos, avalia&ccedil;&otilde;es</p></div>
<div class="row"><span class="n">02</span><p>Conte&uacute;do que responde perguntas do seu cliente</p></div>
<div class="row"><span class="n">03</span><p>SEO local: uma p&aacute;gina por cidade e por servi&ccedil;o</p></div>
<div class="row"><span class="n">04</span><p>Perguntas e respostas no seu perfil</p></div>
<div class="spacer"></div>
""", foot_n=6))

# 7 dica pratica
S.append(page(f"""
{meta('Dica pratica')}
<h2>Escreva o que<br>o cliente pergunta</h2>
<div class="rule"></div>
<p class="lead">O Google copia das respostas diretas. Ent&atilde;o escreva as respostas que voc&ecirc; daria no balc&atilde;o:</p>
<div class="row" style="margin-top:22px"><span class="n">&bull;</span><p>&ldquo;Quanto custa o corte?&rdquo;</p></div>
<div class="row"><span class="n">&bull;</span><p>&ldquo;Fazem atendimento remoto?&rdquo;</p></div>
<div class="row"><span class="n">&bull;</span><p>&ldquo;Qual o melhor hor&aacute;rio?&rdquo;</p></div>
<div class="spacer"></div>
<div class="chip">Pergunta + resposta clara</div>
""", foot_n=7))

# 8 cta
S.append(page(f"""
{meta('Proximo passo')}
<h2>Quer aparecer<br>nas respostas<br><span class="red">diretas</span>?</h2>
<div class="spacer"></div>
<div><span class="cta">Fale com a gente {icon('phone-call',26)}</span></div>
<div class="wa-row">{wa_icon(34)}<span class="num">(11) 98984-2541</span></div>
<p style="margin-top:28px;font-family:'Inter',sans-serif;font-size:24px;color:#979797">Cuidamos da sua presen&ccedil;a digital com autoridade.</p>
""", foot_n=8))

for i, s in enumerate(S, 1):
    open(os.path.join(OUT, f"s{i:02d}.html"), "w", encoding="utf-8").write(s)

for f in ["frame-a.png", "frame-b.png", "logo-glm.png"]:
    shutil.copy(os.path.join(BASE, f), os.path.join(OUT, f))
print(f"Direcao B post02: {len(S)} slides em {OUT}")
