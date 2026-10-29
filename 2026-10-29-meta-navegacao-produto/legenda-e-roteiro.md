# Carrossel GLM Studios — Meta: navegação de produto (28/10/2026)

- **Formato:** carrossel, 8 slides, 1080×1350 (4:5)
- **Identidade:** site novo (`D:/Sites VScode/Site GLMstudio`) — fundo `#0f0f0f` · texto `#d2d2d2` · branco `#f5eded` · acento `#ca3e47`
- **Fontes:** Space Grotesk (títulos) · Inter (texto) · B612 Mono (labels/mono)
- **Status:** design v3 aprovado pelo Gui (29/10) — aguardando publicação
- **Fonte da notícia:** notificação da Meta aos anunciantes (PPC Land, 15/10) · thekeyword.co
- **Arquivos finais:** `slide-01.png` … `slide-08.png` (raiz da pasta)
- **Template reproduzível:** `template/v3/` (gen3.py + ícones + frames + HTMLs)
- **Rascunhos antigos:** `slides/arquivo-v2/` e `template/arquivo-v2/` (identidade do site antigo — descartados)

---

## Assets usados

| Asset | Origem | Licença |
|---|---|---|
| Textura de fundo | frames de `assets/hero loop.mp4` (site novo), ffmpeg @2s e @7s | próprio |
| Ícones | Lucide via `api.iconify.design/lucide/<nome>.svg` | MIT |
| Logo | `assets/logo branco.png` (site novo) | próprio |
| Ícone WhatsApp | `assets/whatsapp.svg` (site novo), inline com `currentColor` | próprio |

---

## Texto dos slides

1. **A Meta mudou o caminho do seu clique** — Se você anuncia no Instagram, parte dos seus leads pode nunca chegar até você. [Anúncio → Vitrine → Seu site]
2. **O clique mudou de caminho** — Antes: clique no anúncio ia direto para o site. Agora: passa antes por uma vitrine de produtos dentro do app.
3. **Essa vitrine do meio não é sua** — não roda o código que mede as visitas no site, não mostra o formulário de contato, o produto exibido é escolhido pelo algoritmo da Meta.
4. **Você paga pelo clique. O lead não chega.** — Parte dos cliques morre naquela tela. O relatório continua bonito; o prejuízo aparece no telefone que não toca.
5. **Como desligar a vitrine** — 01 Gerenciador de Anúncios → abra a campanha · 02 Advantage+ → Creative e Destination · 03 Desligue "navegação de produto".
6. **Faça antes da Black Friday** — é a maior janela de vendas do ano; o tráfego pago encarece justo nessa semana.
7. **O Meta Pixel também muda** — a partir de 12/11 o Meta conta conversões no aparelho do cliente: relatório infla, venda não. [toggle "Ligado por padrão"]
8. **CTA** — Quer revisar suas campanhas antes da Black Friday? + botão "Fale com a gente" + WhatsApp (11) 98984-2541.

---

## Legenda

Ontem a Meta virou o padrão de todos os anúncios que já estavam no ar. A mudança é pequena no nome e grande no resultado: parte dos cliques dos seus clientes pode parar de chegar no site.

Vou explicar do jeito simples.

O clique que hoje vai direto para o site pode passar antes por uma vitrine de produtos dentro do Instagram. Nessa tela não roda o código que mede as visitas, não aparece o formulário e o produto exibido é escolhido pelo algoritmo da Meta.

O efeito é direto: o lead evapora entre o clique e o contato. Você paga pelo clique e não recebe a ligação.

O ajuste é rápido e leva dez minutos:

Gerenciador de Anúncios → abra a campanha → Advantage+ → Creative e Destination → desligue "navegação de produto".

Vale fazer antes da Black Friday, que é a maior janela de vendas do ano e também quando o tráfego pago encarece.

Se você anuncia no Instagram e não quer depender de sorte com a Meta, me chama.
Chame no WhatsApp: (11) 98984-2541

GLM Studios — cuidamos da sua presença digital com autoridade.

#MarketingDigital #MetaAds #BlackFriday #GLMStudios

---

## Regras de publicação

- Publicar só com o "ok" do Gui.
- Antes de publicar, confirmar: perfil profissional (Empresa ou Criador) e @ da conta para autorizar a API.
- Carrossel conta como 1 post no limite da API (~25/dia).
- As imagens precisam de URL pública (bucket Supabase ou raw GitHub) para a Graph API aceitar.

## Comandos de re-render

```bash
cd template/v3 && python gen3.py
# depois, para cada slide:
chrome.exe --headless=new --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=1 --window-size=1080,1350 \
  --virtual-time-budget=9000 --run-all-compositor-stages-before-draw \
  --screenshot="<saida>.png" "file:///<html>"
```
