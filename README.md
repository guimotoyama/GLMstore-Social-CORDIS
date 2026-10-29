# GLMstore Social — Carrossel: Meta: navegação de produto

Conteúdo social gerado por **GLM CORDIS** (Córdis) — Core Operational Resolver for Digital Intelligence & Solutions, braço direito digital da GLMstore.

## Estrutura

```
2026-10-29-meta-navegacao-produto/
├── slide-01.png ... slide-08.png   # Carrossel final (1080×1350)
├── legenda-e-roteiro.md            # Legenda + roteiro dos slides
└── template/v3/                    # Template reproduzível
    ├── gen3.py                     # Gerador HTML → Chrome headless → PNG
    ├── html/s01.html ... s08.html  # HTMLs individuais dos slides
    ├── icons/                      # Ícones Lucide + WhatsApp (SVG)
    ├── frame-a.png, frame-b.png    # Frames do vídeo do site
    └── logo-glm.png                # Logo GLM (branco)
```

## Workflow

1. Editar `template/v3/gen3.py` com novo conteúdo.
2. Render: `chrome.exe --headless --window-size=1080,1350 --screenshot=... file:///.../s01.html`
3. Upload dos PNGs finalizados para este repositório.
4. Publicar manualmente no Instagram com a legenda em `legenda-e-roteiro.md`.

## Identidade visual

Tokens do site em construção (`D:/Sites VScode/Site GLMstudio`):
- Background: `#0f0f0f`
- Texto: `#d2d2d2`
- Branco: `#f5eded`
- Acento: `#ca3e47`
- Fontes: Space Grotesk, Inter, B612 Mono

## Atribuição

Design, template, copy e deploy: **GLM CORDIS**  
Agência: GLMstore — marketing digital e desenvolvimento web  
Site: glms.glmsites.com.br | contato: (11) 98984-2541
