#!/usr/bin/env bash
# Build Thesis.pdf with XeLaTeX (+ optional BibTeX).
#
# Usage:
#   ./build.sh           # full rebuild: xelatex -> bibtex -> xelatex x2
#   ./build.sh quick     # single xelatex pass (text-only edits)
#   ./build.sh bib       # same as full (explicit bibliography refresh)
#   ./build.sh clean     # remove LaTeX auxiliaries (keeps Thesis.pdf / Thesis.bbl)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

FILE="Thesis"
MODE="${1:-full}"

need_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "error: '$1' not found in PATH" >&2
    echo "Install TeX Live (or add it to PATH), then retry." >&2
    exit 1
  fi
}

run_xelatex() {
  # -interaction=nonstopmode keeps CI/agent friendly; -halt-on-error fails fast
  xelatex -interaction=nonstopmode -halt-on-error "${FILE}.tex"
}

run_bibtex() {
  # Thesis.tex uses \input{Thesis.bbl} (no \bibliography), so the .aux may lack
  # \bibdata. Inject it before BibTeX, otherwise BibTeX emits an empty .bbl and
  # all \cite{} render as (?,?).
  if ! grep -q '\\bibdata{' "${FILE}.aux"; then
    printf '\\bibdata{Biblio/ref}\n' >> "${FILE}.aux"
  fi
  if ! grep -q '\\bibstyle{' "${FILE}.aux"; then
    printf '\\bibstyle{Biblio/gbt7714-author-year}\n' >> "${FILE}.aux"
  fi
  bibtex "${FILE}"
  local n_items
  n_items="$(grep -c '\\bibitem' "${FILE}.bbl" || true)"
  if [[ "${n_items}" -lt 1 ]]; then
    echo "error: ${FILE}.bbl has no \\bibitem entries after bibtex" >&2
    exit 1
  fi
  echo "==> bibliography: ${n_items} entries in ${FILE}.bbl"
}

case "$MODE" in
  quick)
    need_cmd xelatex
    echo "==> quick build: xelatex ${FILE}.tex"
    run_xelatex
    ;;
  full|bib)
    need_cmd xelatex
    need_cmd bibtex
    echo "==> full build: xelatex -> bibtex -> xelatex x2"
    run_xelatex
    run_bibtex
    run_xelatex
    run_xelatex
    ;;
  clean)
    echo "==> cleaning auxiliaries"
    rm -f \
      "${FILE}.aux" "${FILE}.log" "${FILE}.out" "${FILE}.toc" \
      "${FILE}.lof" "${FILE}.lot" "${FILE}.fls" "${FILE}.fdb_latexmk" \
      "${FILE}.synctex.gz" "${FILE}.xdv" "${FILE}.blg" \
      "${FILE}.nav" "${FILE}.snm" "${FILE}.vrb"
    # Keep Thesis.bbl / Thesis.pdf; remove Tmp/ from artratex.sh if present
    rm -rf Tmp
    echo "kept: ${FILE}.pdf ${FILE}.bbl (if present)"
    ;;
  -h|--help|help)
    sed -n '2,12p' "$0"
    exit 0
    ;;
  *)
    echo "unknown mode: $MODE" >&2
    echo "usage: $0 [quick|full|bib|clean]" >&2
    exit 1
    ;;
esac

if [[ "$MODE" != "clean" ]]; then
  echo "==> done: ${ROOT}/${FILE}.pdf"
fi
