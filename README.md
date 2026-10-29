# GLMstore Social — Conteúdo para Instagram

Conteúdo social gerado por **GLM CORDIS** (Córdis) — Core Operational Resolver for Digital Intelligence & Solutions, braço direito digital da GLMstore.

## Estrutura

```
2026-10-29-meta-navegacao-produto/          # POST 01 — Meta: navegação de produto
├── slide-01.png ... slide-08.png             # Carrossel final (1080×1350)
├── legenda-e-roteiro.md                      # Legenda + roteiro dos slides
└── design-A-post01/                          # DIREÇÃO A (versão A deste post)
    ├── gen3.py                               # Gerador HTML → Chrome headless → PNG
    ├── html/s01.html ... s08.html            # HTMLs individuais dos slides
    ├── icons/                                # Ícones Lucide + WhatsApp (SVG)
    ├── frame-a.png, frame-b.png              # Frames do vídeo do site
    └── logo-glm.png                          # Logo GLM (branco)
```

## NÃO existe template fixo

Cada post nasce com um **design novo**. `design-A-post01/` é a **direção A daquele post específico**, não um template reutilizável. A cada novo post são construídas **2–3 direções distintas** e o Gui escolhe a vencedora.

O Instagram é uma **identidade separada do site**. Do site GLMstore entram apenas **cores e fontes**. Layout, fundo, ícones, elementos e efeitos variam livremente a cada post.

### O que vem do site (identidade fixa)
- Cores: `#0f0f0f` (fundo), `#d2d2d2` (texto), `#f5eded` (branco), `#ca3e47` (acento)
- Fontes: Space Grotesk, Inter, B612 Mono

### O que muda a cada post
Fundo, grid/layout, estrutura dos slides, iconografia, elementos decorativos, efeitos, densidade, tom, foto vs. ilustração.

## Direção A — Post 01 (Swiss escuro com cards)
Fundo escuro com textura do vídeo do site, cards com brilho sutil, ícones Lucide, footer com logo.

## Direções em produção
- **A** — `design-A-post01/` (Post 01, publicado)
- **B** — Swiss claro / brutalista (type gigante, grid racional, zero decoração)
- **C** — Editorial Press / jornal (papel, mono para metadados, número gigante)
- **D** — Foto + texto editorial (fotografia real, corte editorial, anti-AI-slop)

## Workflow

1. Boletim diário (cron 09:00) define o conteúdo do post.
2. CORDIS constrói 2–3 direções de design novas.
3. Gui compara e escolhe a vencedora.
4. PNGs + arquivos da direção vencedora sobem para este repositório.
5. Página no Notion é criada/atualizada com legenda, hashtags, música e URLs.
6. Gui publica manualmente no Instagram.

## Atribuição

Design, direções, template, copy e deploy: **GLM CORDIS**
Agência: GLMstore — marketing digital e desenvolvimento web
Site: glms.glmsites.com.br | contato: (11) 98984-2541
