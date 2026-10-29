# -*- coding: utf-8 -*-
"""Carrossel GLM Studios v3 — identidade nova (#0f0f0f/#ca3e47/Space Grotesk), frame do video do site,
icones Lucide locais, portrait do responsavel. Saida: PNG 1080x1350 via Chrome headless."""
import os, re

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "v3")
os.makedirs(OUT, exist_ok=True)

ICON_DIR = os.path.join(BASE, "icons")

def _prep_svg(svg, size, cls):
    """Ajusta width/height e class do <svg> preservando viewBox, xmlns e fill."""
    m = re.search(r"<svg([^>]*)>", svg)
    attrs = m.group(1)
    vb = re.search(r'viewBox="[^"]*"', attrs)
    attrs = re.sub(r'\s(width|height)="[^"]*"', "", attrs)
    attrs = re.sub(r'\sclass="[^"]*"', "", attrs)
    new = f'<svg width="{size}" height="{size}" class="{cls}"'
    if vb:
        new += " " + vb.group(0)
    return svg[:m.start()] + new + attrs + ">" + svg[m.end():]

def icon(name, size=34, cls="ic"):
    p = os.path.join(ICON_DIR, name + ".svg")
    svg = open(p, encoding="utf-8").read()
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    return _prep_svg(svg, size, cls)

def wa_icon(size=38):
    """Icone WhatsApp do site, inline e com currentColor (renderiza na cor da marca)."""
    svg = open(os.path.join(ICON_DIR, "whatsapp-solid.svg"), encoding="utf-8").read()
    return _prep_svg(svg, size, "ic wa-ic")

CSS = """
@import url('https://fonts.googleapis.com/css2?family=B612+Mono:wght@700&family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
* { margin:0; padding:0; box-sizing:border-box; }
html,body { width:1080px; height:1350px; overflow:hidden; }
body { background:#0f0f0f; color:#d2d2d2; font-family:'Inter',sans-serif; font-weight:500; -webkit-font-smoothing:antialiased; }
.slide { position:relative; width:1080px; height:1350px; padding:96px 80px 0; display:flex; flex-direction:column; overflow:hidden; }
.bgimg { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; opacity:.038; mix-blend-mode:lighten; z-index:0; }
.glow { position:absolute; z-index:0; width:1000px; height:1000px; right:-340px; top:-380px; background:radial-gradient(circle, rgba(202,62,71,.20), rgba(202,62,71,0) 64%); }
.glow.left { right:auto; left:-420px; top:auto; bottom:-420px; }
.layer { position:relative; z-index:2; display:flex; flex-direction:column; flex:1; min-height:0; padding-bottom:200px; }
.eyebrow { font-family:'B612 Mono',monospace; font-size:25px; font-weight:700; letter-spacing:.16em; text-transform:uppercase; color:#ca3e47; margin-bottom:36px; display:flex; align-items:center; gap:16px; }
.eyebrow::after { content:""; flex:1; height:1px; background:rgba(245,237,237,.14); }
h1 { font-family:'Space Grotesk',sans-serif; font-size:104px; line-height:1.02; font-weight:700; letter-spacing:-.035em; color:#f5eded; }
h2 { font-family:'Space Grotesk',sans-serif; font-size:72px; line-height:1.05; font-weight:700; letter-spacing:-.03em; color:#f5eded; }
.grad { background:linear-gradient(125deg, rgba(255,255,255,.7) 0%, #fff 52%, rgba(255,255,255,.5) 100%); -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent; color:transparent; }
.red { color:#ca3e47; -webkit-text-fill-color:#ca3e47; }
.lead { font-size:36px; line-height:1.5; color:#d2d2d2; max-width:840px; }
.spacer { flex:1; }
.rule { width:96px; height:6px; background:#ca3e47; margin:34px 0; border-radius:3px; }
.row { display:flex; align-items:flex-start; gap:30px; padding:34px 0; border-top:1px solid rgba(245,237,237,.11); }
.row:last-of-type { border-bottom:1px solid rgba(245,237,237,.11); }
.row .ic { flex:0 0 auto; margin-top:4px; color:#f5eded; }
.row.hot .ic { color:#ca3e47; }
.row p { font-size:36px; line-height:1.32; color:#d2d2d2; }
.row.hot p { color:#f5eded; }
.mono { font-family:'B612 Mono',monospace; font-size:23px; letter-spacing:.14em; text-transform:uppercase; color:#979797; }
.flow { display:flex; align-items:center; gap:18px; }
.node { display:flex; align-items:center; gap:14px; padding:20px 24px; border:1px solid rgba(245,237,237,.16); border-radius:14px; color:#f5eded; font-size:28px; font-weight:500; }
.node.hot { border-color:#ca3e47; color:#ca3e47; background:rgba(202,62,71,.10); }
.node .ic { color:inherit; }
.arrow { color:#979797; font-size:30px; }
.statement { font-family:'Space Grotesk',sans-serif; font-size:96px; line-height:1.04; font-weight:700; letter-spacing:-.035em; color:#f5eded; max-width:900px; }
.ghost-ic { position:absolute; z-index:1; right:54px; bottom:150px; opacity:.055; color:#f5eded; }
.steps { counter-reset:s; }
.step { display:flex; align-items:baseline; gap:30px; padding:32px 0; border-top:1px solid rgba(245,237,237,.11); }
.step:last-child { border-bottom:1px solid rgba(245,237,237,.11); }
.step .n { font-family:'B612 Mono',monospace; font-size:30px; color:#ca3e47; }
.step .t { font-size:38px; line-height:1.25; color:#f5eded; }
.toggle { display:flex; align-items:center; gap:26px; padding:26px 30px; border:1px solid rgba(245,237,237,.13); border-radius:18px; }
.toggle .sw { width:92px; height:50px; border-radius:30px; background:#ca3e47; position:relative; flex:0 0 auto; }
.toggle .sw::after { content:""; position:absolute; top:5px; right:5px; width:40px; height:40px; border-radius:50%; background:#fff; }
.toggle .lbl { font-family:'B612 Mono',monospace; font-size:24px; letter-spacing:.1em; text-transform:uppercase; color:#f5eded; }
.toggle .st { margin-left:auto; font-family:'B612 Mono',monospace; font-size:22px; letter-spacing:.1em; color:#ca3e47; }
.chip { display:inline-block; font-family:'B612 Mono',monospace; font-size:23px; letter-spacing:.14em; text-transform:uppercase; color:#ca3e47; border:1px solid rgba(202,62,71,.5); border-radius:999px; padding:12px 22px; }
.portrait { width:190px; height:190px; border-radius:24px; object-fit:cover; filter:grayscale(.35) contrast(1.05); border:1px solid rgba(245,237,237,.16); }
.who { display:flex; align-items:center; gap:24px; margin-bottom:34px; }
.who .nm { font-family:'Space Grotesk',sans-serif; font-size:34px; font-weight:600; color:#f5eded; letter-spacing:-.02em; }
.who .rl { font-family:'B612 Mono',monospace; font-size:22px; letter-spacing:.14em; text-transform:uppercase; color:#979797; margin-top:6px; }
.cta { display:inline-flex; align-items:center; gap:18px; font-family:'Space Grotesk',sans-serif; font-size:36px; font-weight:600; color:#f5eded; padding:22px 34px; border:1px solid rgba(245,237,237,.3); border-radius:999px; }
.cta .ic { color:#ca3e47; }
.tagline { font-size:28px; color:#979797; margin-top:26px; }
.footer { position:absolute; left:80px; right:80px; bottom:74px; z-index:3; display:flex; align-items:center; justify-content:space-between; font-family:'B612 Mono',monospace; font-size:22px; letter-spacing:.16em; text-transform:uppercase; color:#6d6d6d; }
.foot-logo { height:50px; width:auto; opacity:.9; }
.swipe { position:absolute; right:80px; bottom:132px; z-index:3; font-family:'B612 Mono',monospace; font-size:24px; letter-spacing:.16em; text-transform:uppercase; color:#ca3e47; }
.wa-row { display:inline-flex; align-items:center; gap:20px; margin-top:28px; padding:18px 30px; border:1px solid rgba(245,237,237,.14); border-radius:999px; }
.wa-row .wa-ic { width:38px; height:38px; color:#ca3e47; flex:0 0 auto; }
.wa-row .num { font-family:'Space Grotesk',sans-serif; font-size:36px; font-weight:600; color:#f5eded; letter-spacing:.01em; }
"""

def page(body, bg="frame-a.png", glow="right", extra="", lstyle="", foot_n=None):
    g = '<div class="glow"></div>' if glow == "right" else ('<div class="glow left"></div>' if glow == "left" else "")
    foot = f'<div class="footer">{footer(foot_n or 0)}</div>' if foot_n is not None else ""
    return f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">
<style>{CSS}</style></head><body><div class="slide">
<img class="bgimg" src="{bg}">{g}
<div class="layer" {lstyle}>{body}</div>{extra}{foot}
<div class="swipe">arraste &rarr;</div>
</div></body></html>"""

def footer(n, total=8):
    return f'<img class="foot-logo" src="logo-glm.png"><span>{n:02d} / {total:02d}</span>'

S = []

# 1 capa
S.append(page(f"""
  <div class="eyebrow">Meta Ads</div>
  <h1 class="grad">A Meta mudou o caminho do seu <span class="red">clique</span></h1>
  <div class="rule"></div>
  <p class="lead">Se voc&ecirc; anuncia no Instagram, parte dos seus leads pode nunca chegar at&eacute; voc&ecirc;.</p>
  <div class="spacer"></div>
  <div class="flow">
    <span class="node">{icon('megaphone',30)} An&uacute;ncio</span><span class="arrow">&rarr;</span>
    <span class="node hot">{icon('shopping-bag',30)} Vitrine</span><span class="arrow">&rarr;</span>
    <span class="node">{icon('store',30)} Seu site</span>
  </div>
""", glow="right", foot_n=1))

# 2 antes / agora
S.append(page(f"""
  <div class="eyebrow">Antes & agora</div>
  <h2>O clique mudou de caminho</h2>
  <div class="row">{icon('megaphone',34)}
    <p><span class="mono" style="display:block;margin-bottom:8px">Antes</span>Clique no an&uacute;ncio e o visitante ia direto para o seu site.</p>
  </div>
  <div class="row hot">{icon('shopping-bag',34)}
    <p><span class="mono" style="display:block;margin-bottom:8px;color:#ca3e47">Agora</span>O clique passa antes por uma vitrine de produtos dentro do app.</p>
  </div>
  <div class="spacer"></div>
  <div class="mono">A vitrine do meio &eacute; nova</div>
""", bg="frame-b.png", glow="left", foot_n=2))

# 3 a vitrine nao e sua
S.append(page(f"""
  <div class="eyebrow">O detalhe que ningu&eacute;m avisa</div>
  <h2>Essa vitrine do meio n&atilde;o &eacute; sua</h2>
  <div class="row">{icon('activity',32)}<p>N&atilde;o roda o c&oacute;digo que mede as visitas no seu site</p></div>
  <div class="row">{icon('message-circle',32)}<p>N&atilde;o mostra o seu formul&aacute;rio de contato</p></div>
  <div class="row hot">{icon('zap',32)}<p>O produto exibido &eacute; escolhido pelo algoritmo da Meta</p></div>
  <div class="spacer"></div>
  <div class="mono">Quem controla essa tela &eacute; a Meta</div>
""", glow="right", foot_n=3))

# 4 declaracao
S.append(page(f"""
  <div class="spacer"></div>
  <div class="eyebrow">O efeito na conta</div>
  <div class="statement">Voc&ecirc; paga pelo clique.<br><span class="red">O lead n&atilde;o chega.</span></div>
  <div class="rule"></div>
  <p class="lead">Parte dos cliques morre naquela tela. O relat&oacute;rio continua bonito; o preju&iacute;zo aparece no telefone que n&atilde;o toca.</p>
  <div class="spacer"></div>
""", bg="frame-b.png", glow="right",
extra=f'<div class="ghost-ic">{icon("eye-off",420)}</div>', foot_n=4))

# 5 como fazer
S.append(page(f"""
  <div class="eyebrow">Dez minutos</div>
  <h2>Como desligar a vitrine</h2>
  <div class="steps">
    <div class="step"><span class="n">01</span><span class="t">Gerenciador de An&uacute;ncios &rarr; abra a campanha</span></div>
    <div class="step"><span class="n">02</span><span class="t">Advantage+ &rarr; Creative e Destination</span></div>
    <div class="step"><span class="n">03</span><span class="t">Desligue &ldquo;navega&ccedil;&atilde;o de produto&rdquo;</span></div>
  </div>
  <div class="spacer"></div>
  <div class="flow">{icon('sliders-horizontal',28)}<span class="mono" style="color:#d2d2d2">D&aacute; para fazer em todas as campanhas</span></div>
""", bg="frame-b.png", glow="left", foot_n=5))

# 6 quando
S.append(page(f"""
  <div class="eyebrow">O prazo</div>
  <h2>Fa&ccedil;a antes da Black Friday</h2>
  <div class="row">{icon('calendar-days',32)}<p>&Eacute; a maior janela de vendas do ano</p></div>
  <div class="row hot">{icon('trending-up',32) if os.path.exists(os.path.join(ICON_DIR,'trending-up.svg')) else icon('target',32)}<p>Tr&aacute;fego pago encarece justo nessa semana</p></div>
  <div class="spacer"></div>
  <span class="chip">Black Friday</span>
""", glow="right", foot_n=6))

# 7 pixel
S.append(page(f"""
  <div class="eyebrow">O que muda no Pixel</div>
  <h2>O Meta Pixel tamb&eacute;m muda</h2>
  <p class="lead">O Meta passa a contar convers&otilde;es no aparelho do cliente. Os relat&oacute;rios v&atilde;o mostrar mais vendas do que houve de verdade.</p>
  <div class="spacer"></div>
  <div class="toggle"><span class="sw"></span><span class="lbl">Medir convers&otilde;es no dispositivo</span><span class="st">Ligado por padr&atilde;o</span></div>
  <div class="mono" style="margin-top:26px">N&uacute;mero subindo n&atilde;o &eacute; campanha melhorando</div>
""", bg="frame-b.png", glow="left", foot_n=7))

# 8 cta — CTA original + WhatsApp (icone e numero na cor da marca)
S.append(page(f"""
  <div class="eyebrow">Vamos resolver</div>
  <h2>Quer revisar suas campanhas antes da Black Friday?</h2>
  <p class="lead" style="margin-top:26px">A gente olha o painel com voc&ecirc; e mostra onde o lead est&aacute; se perdendo.</p>
  <div class="spacer"></div>
  <div><span class="cta">Fale com a gente {icon('phone-call',28)}</span></div>
  <div class="wa-row">{wa_icon(38)}<span class="num">(11) 98984-2541</span></div>
  <p class="tagline" style="margin-top:28px">Cuidamos da sua presen&ccedil;a digital com autoridade.</p>
""", glow="right", foot_n=8))

for i, s in enumerate(S, 1):
    open(os.path.join(OUT, f"s{i:02d}.html"), "w", encoding="utf-8").write(s)

# copia assets para a pasta de render
import shutil
for f in ["frame-a.png", "frame-b.png", "portrait.png", "logo-glm.png"]:
    _p = os.path.join(BASE, f)
    if os.path.exists(_p):
        shutil.copy(_p, os.path.join(OUT, f))
print(f"gerados {len(S)} slides em {OUT}")
