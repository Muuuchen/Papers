# Reproducible paper figures

The figures in `Img/paper_figures/` are generated from the audited, process-level
measurements in `Figures/data/`.

```bash
python3 -m pip install -r Figures/requirements.txt
python3 Figures/generate_paper_figures.py
```

Each figure is emitted as vector PDF, editable SVG, and 360 dpi PNG.  The PDF is
the LaTeX source of record.  The data tables retain the authoritative artifact
path for every value.

Figure conventions:

- blue: producer or single-grid execution;
- orange/hatching: readiness wait, grid gap, or a phase under investigation;
- green: consumer dependent computation or measured improvement;
- process-level points are shown directly; range bars summarize independent
  process medians rather than treating kernel repetitions as independent runs.
