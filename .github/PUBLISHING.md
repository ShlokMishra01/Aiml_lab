# Publishing AI Engineering Lab

Maintainer notes for the public repository at
[github.com/zorost/AI-Engineering-Lab](https://github.com/zorost/AI-Engineering-Lab).

## Repository settings

- **Default branch**: `main`
- **Description**: `A free, open, self paced 24 week AI engineering training program, from your first notebook to a governed lakehouse. Developed by Zorost Intelligence AI Lab.`
- **Website**: https://zorost.com/ai-engineering-lab
- **Topics**: `ai-engineering`, `machine-learning`, `llm`, `rag`, `agents`, `databricks`,
  `azure-ai-foundry`, `vertex-ai`, `amazon-bedrock`, `jupyter-notebooks`, `training-program`,
  `mcp`, `prompt-engineering`
- **Social preview**: upload `assets/diagrams/social-preview.png` under
  Settings, General, Social preview. It is rendered at GitHub's 1280x640.
- **Discussions**: enable for questions. The `question` issue template points learners there.
- **Actions**: not required. Notebook smoke-test CI is on the [roadmap](../ROADMAP.md).

## GitHub Pages

The program site in `docs/` is published at
[zorost.github.io/AI-Engineering-Lab](https://zorost.github.io/AI-Engineering-Lab/).

Enable it once: Settings, Pages, Source `Deploy from a branch`, Branch `main`, folder `/docs`.
The first build takes a minute or two, and every later push to `main` republishes automatically.

`docs/index.html` is generated. Never hand-edit it. Edit `curriculum/manifest.json` or
`scripts/build_site.py`, then run:

```bash
python scripts/build_site.py
```

The script reads the manifest so the week list on the site cannot drift from the curriculum, and it
converts `assets/diagrams/lab-*.png` into WebP for the page. `docs/assets/style.css` and
`docs/assets/hero-texture.jpg` are authored by hand.

## Before you push

```bash
python scripts/build_tracker.py     # regenerate the Excel tracker from the manifest
python scripts/check_notebooks.py   # notebooks parse and follow conventions
python scripts/check_links.py       # every internal markdown link resolves
python scripts/check_mermaid.py     # every mermaid block is themed and parses
python scripts/build_site.py --check  # docs/index.html matches the manifest
```

## Verify the public experience

As an anonymous visitor you should be able to:

- Read the README front page with every diagram rendering inline, in both GitHub light and dark
- Follow [`START-HERE.md`](../START-HERE.md) from zero to Week 1 with no signup
- Open any week folder and work Monday through Friday with no signup
- Download `curriculum/tracking/ai-engineering-lab-24-week-tracker.xlsx` and open it in Excel,
  Google Sheets, or LibreOffice
- Open any notebook in GitHub's viewer, [nbviewer](https://nbviewer.org), or Colab
- Browse all 24 weeks on the Pages site and land back in the right folder

## What is deliberately not published

- `internal/`: session logs, scratch exports, drafts. Gitignored, never pushed.
- `.env` files: credentials flow through environment variables per `.env.example`.
- Generated caches: `__pycache__`, `.ipynb_checkpoints`, model weights, and the datasets that
  `zoro.data.save_all()` rebuilds locally.

## Notes

- The repository contains no secrets. Everything flows through `.env` per `.env.example`.
- The Excel workbook is generated. Edit `curriculum/manifest.json` and regenerate, never hand-edit
  the xlsx.
- The diagrams in `assets/diagrams/` are produced by the Lab in the house visual register. To
  request a change, open an issue rather than editing the PNGs.
- Contact for the program is info@zorost.com.
- `reference/knowledge-base/research/` holds working notes used to write the knowledge base. They
  are original Zorost writing, MIT licensed, and contain no private contact details.

---
© 2026 Zorost Intelligence LLC · https://zorost.com
