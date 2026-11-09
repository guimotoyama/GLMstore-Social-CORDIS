# -*- coding: utf-8 -*-
"""Gerador HTML -> PNG 1080x1350 via Chrome headless.
Direcao E - "Velocimetro / Telemetria". Instrumento de painel: arco, ticks, leitura.
Layout: cabecalho fixo no topo, corpo centralizado, fonte no rodape.
"""
import math
import os
import re
import subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, 'v6')
ICON_DIR = os.path.join(BASE, 'assets', 'icons')
os.makedirs(OUT, exist_ok=True)

CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
TOTAL = 8

CSS = """
@import url('https://fonts.googleapis.com/css2?family=B612+Mono:wght@400;700&family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px;overflow:hidden}
body{background:#0f0f0f;color:#d2d2d2;font-family:'Inter',sans-serif;font-weight:500;-webkit-font-smoothing:antialiased}
.slide{position:relative;width:1080px;height:1350px;padding:82px 80px 0;display:flex;flex-direction:column;overflow:hidden}
.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.05;mix-blend-mode:lighten;z-index:0}
.grid{position:absolute;inset:0;z-index:0;
 background-image:linear-gradient(rgba(245,237,237,.028) 1px,transparent 1px),linear-gradient(90deg,rgba(245,237,237,.028) 1px,transparent 1px);
 background-size:60px 60px}
.glow{position:absolute;z-index:0;width:900px;height:900px;right:-330px;top:-360px;
 background:radial-gradient(circle,rgba(202,62,71,.16),rgba(202,62,71,0) 64%)}
.layer{position:relative;z-index:2;display:flex;flex-direction:column;flex:1;min-height:0;padding-bottom:168px}
.head{flex:0 0 auto}
.body{flex:1;display:flex;flex-direction:column;justify-content:center;min-height:0}
.eyebrow{font-family:'B612 Mono',monospace;font-size:24px;font-weight:700;letter-spacing:.16em;
 text-transform:uppercase;color:#ca3e47;margin-bottom:28px;display:flex;align-items:center;gap:16px}
.eyebrow:after{content:"";flex:1;height:1px;background:rgba(245,237,237,.14)}
h1{font-family:'Space Grotesk',sans-serif;font-size:100px;font-weight:700;line-height:.98;letter-spacing:-.035em;color:#f5eded}
h2{font-family:'Space Grotesk',sans-serif;font-size:68px;font-weight:700;line-height:1.02;letter-spacing:-.03em;color:#f5eded}
.lead{font-size:33px;line-height:1.38;color:#d2d2d2;margin-top:24px;max-width:880px}
.mono{font-family:'B612 Mono',monospace;font-weight:700}
.src{flex:0 0 auto;font-family:'B612 Mono',monospace;font-size:19px;color:#6d6d6d;letter-spacing:.04em;
 border-top:1px solid rgba(245,237,237,.09);padding-top:18px}
.foot{position:absolute;left:80px;right:80px;bottom:52px;z-index:3;display:flex;align-items:center;
 justify-content:space-between}
.foot img{height:50px;width:auto;opacity:.95}
.foot .n{font-family:'B612 Mono',monospace;font-size:22px;font-weight:700;color:#6d6d6d;letter-spacing:.1em}
.tiles{display:flex;gap:18px;margin-top:34px}
.tile{flex:1;border:1px solid rgba(245,237,237,.13);border-radius:18px;padding:26px 24px 24px;background:rgba(245,237,237,.028)}
.tile .v{font-family:'Space Grotesk',sans-serif;font-size:58px;font-weight:700;color:#f5eded;letter-spacing:-.03em;line-height:1}
.tile .v.red{color:#ca3e47}
.tile .l{font-size:22px;line-height:1.34;color:#979797;margin-top:13px}
.rows{display:flex;flex-direction:column;gap:13px;margin-top:30px}
.row{display:flex;align-items:flex-start;gap:22px;border-left:2px solid rgba(202,62,71,.42);padding:5px 0 5px 24px}
.row .v{font-family:'B612 Mono',monospace;font-size:36px;font-weight:700;color:#ca3e47;flex:0 0 250px}
.row .t{font-size:27px;line-height:1.34;color:#d2d2d2;padding-top:5px}
.cause{display:flex;align-items:center;gap:24px;padding:15px 0;border-bottom:1px solid rgba(245,237,237,.10)}
.cause .ic{width:52px;height:52px;flex:0 0 52px;border:1px solid rgba(202,62,71,.34);border-radius:14px;
 display:flex;align-items:center;justify-content:center;background:rgba(202,62,71,.07)}
.cause .ic svg{width:27px;height:27px;color:#ca3e47}
.cause .n{font-family:'B612 Mono',monospace;font-size:22px;font-weight:700;color:#ca3e47;flex:0 0 40px}
.cause .t{font-size:29px;line-height:1.24;color:#f5eded;font-family:'Space Grotesk',sans-serif;font-weight:500}
.cause .t span{font-family:Inter,sans-serif;font-size:23px;color:#979797}
.steps{display:flex;flex-direction:column;gap:20px;margin-top:32px}
.step{display:flex;gap:26px;align-items:flex-start}
.step .c{width:58px;height:58px;flex:0 0 58px;border-radius:50%;border:2px solid #ca3e47;background:rgba(202,62,71,.09);
 display:flex;align-items:center;justify-content:center;font-family:'Space Grotesk',sans-serif;font-size:28px;font-weight:700;color:#f5eded}
.step .t{font-size:28px;line-height:1.36;color:#d2d2d2;padding-top:9px}
.step .t b{color:#f5eded;font-weight:600}
.checks{display:grid;grid-template-columns:1fr 1fr;gap:15px 24px;margin-top:30px}
.slide.s7 .body{justify-content:stretch}
.slide.s7 .checks{flex:1;grid-template-rows:repeat(3,1fr);align-content:stretch;margin-top:26px}
.slide.s7 .chk{align-items:center}
.chk{display:flex;gap:16px;align-items:flex-start;padding:19px 20px;border:1px solid rgba(245,237,237,.12);
 border-radius:14px;background:rgba(245,237,237,.026)}
.chk svg{width:26px;height:26px;color:#ca3e47;flex:0 0 26px;margin-top:3px}
.chk span{font-size:25px;line-height:1.3;color:#f5eded}
.gauges{display:flex;gap:16px;margin-top:34px}
.gauge{flex:1;border:1px solid rgba(245,237,237,.13);border-radius:18px;padding:24px 20px 22px;text-align:center;background:rgba(245,237,237,.028)}
.gauge .nm{font-family:'Space Grotesk',sans-serif;font-size:36px;font-weight:700;color:#f5eded;letter-spacing:.02em}
.gauge .lim{font-family:'B612 Mono',monospace;font-size:29px;font-weight:700;color:#ca3e47;margin-top:9px}
.gauge .ds{font-size:21px;line-height:1.32;color:#979797;margin-top:11px}
.wa{display:inline-flex;align-items:center;gap:22px;padding:22px 38px;border:1px solid rgba(202,62,71,.38);
 border-radius:999px;background:rgba(202,62,71,.09);margin-top:36px}
.wa svg{width:42px;height:42px;color:#ca3e47}
.wa span{font-family:'Space Grotesk',sans-serif;font-size:40px;font-weight:600;color:#f5eded;letter-spacing:.02em}
.site{font-family:'B612 Mono',monospace;font-size:25px;color:#979797;letter-spacing:.06em;margin-top:26px}
"""


def _prep(svg, size, cls='ic'):
    m = re.search(r'<svg([^>]*)>', svg)
    attrs = m.group(1)
    vb = re.search(r'viewBox="[^"]*"', attrs)
    attrs = re.sub(r'\s(width|height)="[^"]*"', '', attrs)
    attrs = re.sub(r'\sclass="[^"]*"', '', attrs)
    new = f'<svg width="{size}" height="{size}" class="{cls}"'
    if vb:
        new += ' ' + vb.group(0)
    return svg[:m.start()] + new + attrs + '>' + svg[m.end():]


def icon(name, size=27):
    p = os.path.join(ICON_DIR, name + '.svg')
    svg = open(p, encoding='utf-8').read()
    svg = re.sub(r'<!--.*?-->', '', svg, flags=re.S)
    return _prep(svg, size)


def wa_icon(size=42):
    svg = open(os.path.join(ICON_DIR, 'whatsapp-solid.svg'), encoding='utf-8').read()
    svg = re.sub(r'<!--.*?-->', '', svg, flags=re.S)
    return _prep(svg, size, 'ic wa-ic')


def gauge_svg(needle_pct, red_from, w=700, h=392):
    """Velocimetro 0..5s. Sweep 270 graus, agulha curta, leitura no miolo."""
    cx, cy, r = w / 2, h - 26, 268
    a0, span = 135.0, 270.0

    def pt(deg, rr):
        rad = math.radians(deg)
        return (cx + rr * math.cos(rad), cy + rr * math.sin(rad))

    p = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg">']
    # trilho
    x1, y1 = pt(a0, r)
    x2, y2 = pt(a0 + span, r)
    p.append(f'<path d="M {x1:.1f} {y1:.1f} A {r} {r} 0 1 1 {x2:.1f} {y2:.1f}" fill="none" '
             f'stroke="rgba(245,237,237,.13)" stroke-width="20" stroke-linecap="round"/>')
    # zona vermelha a partir do limite
    if red_from is not None:
        zx, zy = pt(a0 + span * red_from / 100.0, r)
        p.append(f'<path d="M {zx:.1f} {zy:.1f} A {r} {r} 0 0 1 {x2:.1f} {y2:.1f}" fill="none" '
                 f'stroke="#ca3e47" stroke-width="20" stroke-linecap="round"/>')
    # ticks
    for i in range(0, 21):
        t = i * 5
        deg = a0 + span * t / 100.0
        major = (i % 5 == 0)
        tx1, ty1 = pt(deg, r - 30)
        tx2, ty2 = pt(deg, r + (7 if major else 1))
        red = red_from is not None and t >= red_from
        col = '#ca3e47' if red else 'rgba(245,237,237,.38)'
        p.append(f'<line x1="{tx1:.1f}" y1="{ty1:.1f}" x2="{tx2:.1f}" y2="{ty2:.1f}" '
                 f'stroke="{col}" stroke-width="{4 if major else 2}"/>')
    # agulha curta
    nd = a0 + span * needle_pct / 100.0
    nx, ny = pt(nd, r - 104)
    p.append(f'<line x1="{cx}" y1="{cy}" x2="{nx:.1f}" y2="{ny:.1f}" stroke="#ca3e47" '
             f'stroke-width="9" stroke-linecap="round"/>')
    p.append(f'<circle cx="{cx}" cy="{cy}" r="18" fill="#ca3e47"/>')
    p.append(f'<circle cx="{cx}" cy="{cy}" r="7" fill="#0f0f0f"/>')
    # leitura dentro do mostrador, deslocada para nao cruzar a agulha
    p.append(f'<text x="{cx - 52}" y="{cy - 74}" text-anchor="middle" fill="#f5eded" '
             f'font-family="Space Grotesk,sans-serif" font-size="54" font-weight="700">3s</text>')
    p.append(f'<text x="{cx - 52}" y="{cy - 38}" text-anchor="middle" fill="#ca3e47" '
             f'font-family="B612 Mono,monospace" font-size="17" font-weight="700" letter-spacing="1.6">LIMITE</text>')
    p.append('</svg>')
    return ''.join(p)


def footer(n):
    return (f'<div class="foot"><img src="logo-glm.png" alt="GLM"><span class="n">'
            f'{n:02d} / {TOTAL:02d}</span></div>')


def page(n, head, body, src='', cls=''):
    srchtml = f'<div class="src">{src}</div>' if src else ''
    return f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">
<style>{CSS}</style></head><body><div class="slide {cls}">
<img class="bg" src="frame-a.png"><div class="grid"></div><div class="glow"></div>
<div class="layer"><div class="head">{head}</div><div class="body">{body}</div>{srchtml}</div>
{footer(n)}</div></body></html>"""


S = {}

# ---------- 1 CAPA ----------
S[1] = page(1,
    '<div class="eyebrow">Performance de site</div>'
    '<h1>O cliente desiste<br>em 3 segundos.</h1>'
    '<p class="lead">53% abandonam o site antes de ver o preço. Os 3 números que o Google mede '
    '&mdash; e o que fazer agora.</p>',
    '<div style="display:flex;justify-content:center">'
    + gauge_svg(60, 60) + '</div>')

# ---------- 2 O CUSTO ----------
S[2] = page(2,
    '<div class="eyebrow">O custo</div>'
    '<h2>53% desistem<br>antes de ver o preço.</h2>'
    '<p class="lead">Cada segundo a mais custa conversão. E a mediana do carregamento no celular '
    'já passou dos 7 segundos.</p>',
    '<div class="tiles">'
    '<div class="tile"><div class="v red">+32%</div><div class="l">de chance de o visitante voltar atrás, '
    'só porque o site foi de 1s para 3s</div></div>'
    '<div class="tile"><div class="v">−7%</div><div class="l">de conversão a cada segundo adicional '
    'de carregamento</div></div>'
    '<div class="tile"><div class="v">7,9s</div><div class="l">é a mediana de carregamento completo '
    'de uma página no celular</div></div></div>',
    'Fontes: Google / Think with Google &middot; SOASTA Research &middot; HTTP Archive')

# ---------- 3 OS 3 NUMEROS ----------
S[3] = page(3,
    '<div class="eyebrow">O que o Google mede</div>'
    '<h2>Três mostradores.<br>Três limites.</h2>'
    '<p class="lead">O Google indexa a versão mobile do seu site. Estes são os números que decidem '
    'se ele aparece.</p>',
    '<div class="gauges">'
    '<div class="gauge"><div class="nm">LCP</div><div class="lim">≤ 2,5s</div>'
    '<div class="ds">conteúdo principal aparece</div></div>'
    '<div class="gauge"><div class="nm">INP</div><div class="lim">≤ 200ms</div>'
    '<div class="ds">o site responde ao toque</div></div>'
    '<div class="gauge"><div class="nm">CLS</div><div class="lim">≤ 0,1</div>'
    '<div class="ds">a página não se mexe sozinha</div></div></div>',
    'Limites oficiais: web.dev / Google &middot; indexação mobile-first: Google Search Central')

# ---------- 4 ONDE ESTA TRAVANDO ----------
S[4] = page(4,
    '<div class="eyebrow">Onde está travando</div>'
    '<h2>O peso que<br>você não vê.</h2>',
    '<div class="rows">'
    '<div class="row"><div class="v">2,6 MB</div><div class="t">é o peso mediano de uma página no celular</div></div>'
    '<div class="row"><div class="v">+75%</div><div class="t">foi o crescimento do JavaScript desde 2020</div></div>'
    '<div class="row"><div class="v">45,9%</div><div class="t">dos sites mobile respondem ao servidor em até 0,8s</div></div>'
    '<div class="row"><div class="v">90%</div><div class="t">dos sites de empresas em São Paulo são lentos no celular</div></div>'
    '</div>',
    'HTTP Archive &middot; auditoria própria de 2.385 sites de empresas em São Paulo')

# ---------- 5 AS 5 CAUSAS ----------
cause = [
    ('image', 'Imagem pesada do celular', '3MB de foto na home é o erro mais comum'),
    ('settings-2', 'Plugins e tema do WordPress', 'cada plugin é um pedido a mais'),
    ('code-2', 'Scripts de terceiros', 'chat, pixel e mapa carregam antes do conteúdo'),
    ('server', 'Hospedagem compartilhada sobrecarregada', 'o servidor não responde em 0,8s'),
    ('type', 'Fontes demais sem versionar', '2 ou 3 fontes, no máximo'),
]
rows5 = ''.join(
    f'<div class="cause"><div class="ic">{icon(ic)}</div><div class="n">{i:02d}</div>'
    f'<div class="t">{t}<br><span>{d}</span></div></div>'
    for i, (ic, t, d) in enumerate(cause, 1))
S[5] = page(5,
    '<div class="eyebrow">Diagnóstico</div>'
    '<h2>As 5 causas.</h2>',
    f'<div>{rows5}</div>')

# ---------- 6 COMO MEDIR ----------
S[6] = page(6,
    '<div class="eyebrow">Passo a passo</div>'
    '<h2>Como medir<br>em 5 minutos.</h2>',
    '<div class="steps">'
    '<div class="step"><div class="c">1</div><div class="t"><b>pagespeed.web.dev</b> &mdash; cole a URL '
    'do seu site e rode no modo celular</div></div>'
    '<div class="step"><div class="c">2</div><div class="t">Leia <b>LCP, INP e CLS</b> e veja o que está '
    'vermelho</div></div>'
    '<div class="step"><div class="c">3</div><div class="t"><b>Search Console &rarr; Core Web Vitals</b> '
    '&mdash; os dados reais dos seus visitantes</div></div></div>',
    'Tudo grátis. Nenhuma ferramenta paga necessária para começar')

# ---------- 7 CHECKLIST ----------
chk = [
    'Imagem em WebP no tamanho real',
    'Carregar sob demanda o que está abaixo da dobra',
    'Remover script que não gera lead',
    'Cache + CDN',
    'Hospedagem que responde em até 0,8s',
    '2 ou 3 fontes, no máximo',
]
checks = ''.join(f'<div class="chk">{icon("circle-check-big")}<span>{c}</span></div>' for c in chk)
S[7] = page(7,
    '<div class="eyebrow">O que fazer</div>'
    '<h2>6 correções que resolvem<br>a maior parte.</h2>',
    f'<div class="checks">{checks}</div>',
    'A ordem que devolve mais resultado primeiro', 's7')

# ---------- 8 CTA ----------
S[8] = page(8,
    '<div class="eyebrow">Diagnóstico gratuito</div>'
    '<h1>Seu site está<br>no grupo dos 90%?</h1>'
    '<p class="lead">Diagnóstico de velocidade gratuito do seu site &mdash; com o que está travando '
    'e por onde começar.</p>',
    f'<div class="wa">{wa_icon()}<span>(11) 98984-2541</span></div>'
    '<div class="site">agencia.glmstore.com.br</div>')


def main():
    for n in range(1, TOTAL + 1):
        hp = os.path.join(OUT, f's{n:02d}.html')
        open(hp, 'w', encoding='utf-8').write(S[n])
    print('html gerados em', OUT)

    for n in range(1, TOTAL + 1):
        hp = os.path.join(OUT, f's{n:02d}.html')
        pp = os.path.join(OUT, f'slide-{n:02d}.png')
        cmd = [CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars',
               '--force-device-scale-factor=1', '--window-size=1080,1350',
               '--virtual-time-budget=9000', '--run-all-compositor-stages-before-draw',
               '--no-sandbox', '--user-data-dir=' + os.path.join(OUT, 'chrome-profile'),
               f'--screenshot={pp}', 'file:///' + hp.replace('\\', '/')]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        sz = os.path.getsize(pp) if os.path.exists(pp) else 0
        print(f'slide {n:02d}: {"OK" if sz > 1000 else "FALHOU"} ({sz}B)')
        if sz <= 1000:
            print(r.stderr[-500:])


if __name__ == '__main__':
    main()
