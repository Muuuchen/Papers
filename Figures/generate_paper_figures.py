#!/usr/bin/env python3
"""Generate publication-style figures for the Megakernel proposal.

The script is intentionally deterministic and reads only checked-in CSV files.
It emits PDF for LaTeX, SVG for editing, and PNG for quick inspection.
"""

from __future__ import annotations

import csv
import os
from collections import defaultdict
from pathlib import Path

os.environ.setdefault("SOURCE_DATE_EPOCH", "0")

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Patch, Rectangle


ROOT = Path(__file__).resolve().parents[1]
DATA = Path(__file__).resolve().parent / "data"
OUT = ROOT / "Img" / "paper_figures"

BLUE = "#3B6FB6"
BLUE_LIGHT = "#E9F0FA"
TEAL = "#228C79"
TEAL_LIGHT = "#E5F4EF"
ORANGE = "#D98E1A"
ORANGE_TEXT = "#995800"
ORANGE_LIGHT = "#FFF0D8"
RED = "#C75D4D"
RED_LIGHT = "#F9E8E4"
INK = "#20262E"
MID = "#66707A"
GRID = "#D8DEE5"
PAPER = "#FFFFFF"


plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 8.0,
        "axes.titlesize": 8.5,
        "axes.labelsize": 8.0,
        "xtick.labelsize": 7.2,
        "ytick.labelsize": 7.2,
        "legend.fontsize": 7.0,
        "axes.linewidth": 0.7,
        "lines.linewidth": 1.25,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "svg.hashsalt": "mega-fusion-paper-figures-v1",
        "savefig.facecolor": PAPER,
        "figure.facecolor": PAPER,
    }
)


def read_rows(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def save_figure(fig: plt.Figure, stem: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        OUT / f"{stem}.pdf",
        bbox_inches="tight",
        pad_inches=0.025,
        metadata={"Creator": "generate_paper_figures.py", "CreationDate": None},
    )
    fig.savefig(
        OUT / f"{stem}.svg",
        bbox_inches="tight",
        pad_inches=0.025,
        metadata={"Creator": "generate_paper_figures.py"},
    )
    fig.savefig(
        OUT / f"{stem}.png",
        dpi=360,
        bbox_inches="tight",
        pad_inches=0.025,
        metadata={"Software": "generate_paper_figures.py"},
    )
    plt.close(fig)


def rounded_box(
    ax: plt.Axes,
    x: float,
    y: float,
    width: float,
    height: float,
    text: str,
    *,
    facecolor: str,
    edgecolor: str,
    linewidth: float = 0.9,
    linestyle: str = "-",
    fontsize: float = 7.4,
    text_color: str = INK,
    hatch: str | None = None,
    zorder: int = 2,
) -> FancyBboxPatch:
    patch = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.025,rounding_size=0.07",
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=linewidth,
        linestyle=linestyle,
        hatch=hatch,
        zorder=zorder,
    )
    ax.add_patch(patch)
    if text:
        ax.text(
            x + width / 2,
            y + height / 2,
            text,
            ha="center",
            va="center",
            color=text_color,
            fontsize=fontsize,
            zorder=zorder + 1,
        )
    return patch


def arrow(
    ax: plt.Axes,
    start: tuple[float, float],
    end: tuple[float, float],
    *,
    color: str = INK,
    linewidth: float = 0.9,
    style: str = "-|>",
    connectionstyle: str = "arc3",
    linestyle: str = "-",
    zorder: int = 4,
) -> None:
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle=style,
            mutation_scale=8.0,
            linewidth=linewidth,
            color=color,
            connectionstyle=connectionstyle,
            linestyle=linestyle,
            zorder=zorder,
        )
    )


def clean_axis(ax: plt.Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(MID)
    ax.spines["bottom"].set_color(MID)
    ax.tick_params(colors=MID, width=0.7, length=3)
    ax.xaxis.label.set_color(INK)
    ax.yaxis.label.set_color(INK)


def generate_execution_plans() -> None:
    fig, ax = plt.subplots(figsize=(7.15, 3.55))
    ax.set_xlim(0.0, 10.6)
    ax.set_ylim(-0.35, 4.25)
    ax.axis("off")

    rows = [3.45, 2.45, 1.45, 0.45]
    labels = [
        (r"$\Pi_E$", "Early-Inside"),
        (r"$\Pi_G$", "Admission-Gated Inside"),
        (r"$\Pi_S$", "Serial-Split"),
        (r"$\Pi_P$", "Split+PDL"),
    ]
    for y, (symbol, name) in zip(rows, labels):
        ax.text(0.06, y + 0.18, symbol, fontsize=9.0, fontweight="bold", va="center")
        ax.text(0.55, y + 0.18, name, fontsize=7.3, va="center", color=INK)

    ready_x = 6.55
    for y in rows:
        ax.plot([ready_x, ready_x], [y - 0.05, y + 0.58], color=ORANGE_TEXT, lw=0.8, ls=(0, (3, 2)), zorder=5)
    ax.text(ready_x, 4.08, "minimum dependency ready", ha="center", va="bottom", fontsize=7.0, color=ORANGE_TEXT)

    # Early-Inside.
    rounded_box(ax, 2.15, rows[0], 6.95, 0.56, "", facecolor="#F8FAFC", edgecolor=BLUE, linewidth=1.0)
    rounded_box(ax, 2.28, rows[0] + 0.31, 4.27, 0.18, "producer A", facecolor=BLUE_LIGHT, edgecolor=BLUE, fontsize=6.7)
    rounded_box(
        ax,
        3.42,
        rows[0] + 0.06,
        ready_x - 3.42,
        0.18,
        "pre-ready residence",
        facecolor=ORANGE_LIGHT,
        edgecolor=ORANGE,
        hatch="////",
        fontsize=6.6,
    )
    rounded_box(ax, ready_x, rows[0] + 0.06, 2.05, 0.18, "consumer B", facecolor=TEAL_LIGHT, edgecolor=TEAL, fontsize=6.7)
    ax.text(9.25, rows[0] + 0.28, "one grid", color=BLUE, fontsize=6.7, va="center")

    # Admission-gated single grid.
    rounded_box(ax, 2.15, rows[1], 6.95, 0.56, "", facecolor="#F8FAFC", edgecolor=BLUE, linewidth=1.0)
    rounded_box(ax, 2.28, rows[1] + 0.31, 4.27, 0.18, "producer A", facecolor=BLUE_LIGHT, edgecolor=BLUE, fontsize=6.7)
    rounded_box(ax, ready_x, rows[1] + 0.06, 2.05, 0.18, "consumer B", facecolor=TEAL_LIGHT, edgecolor=TEAL, fontsize=6.7)
    arrow(ax, (6.10, rows[1] + 0.15), (6.48, rows[1] + 0.15), color=ORANGE_TEXT)
    ax.text(4.76, rows[1] + 0.15, "B not admitted", color=MID, fontsize=6.5, ha="center", va="center")
    ax.text(9.25, rows[1] + 0.28, "one grid", color=BLUE, fontsize=6.7, va="center")

    # Serial split.
    rounded_box(ax, 2.15, rows[2], 4.35, 0.38, "producer grid A", facecolor=BLUE_LIGHT, edgecolor=BLUE, fontsize=7.0)
    rounded_box(ax, 6.92, rows[2], 2.30, 0.38, "consumer grid B", facecolor=TEAL_LIGHT, edgecolor=TEAL, fontsize=7.0)
    ax.add_patch(Rectangle((6.56, rows[2]), 0.34, 0.38, facecolor=ORANGE_LIGHT, edgecolor=ORANGE, hatch="////", lw=0.8))
    ax.text(6.73, rows[2] + 0.50, "grid gap", color=ORANGE_TEXT, fontsize=6.5, ha="center")

    # PDL split.
    rounded_box(ax, 2.15, rows[3], 4.35, 0.38, "producer grid A", facecolor=BLUE_LIGHT, edgecolor=BLUE, fontsize=7.0)
    rounded_box(ax, 5.15, rows[3] - 0.02, 4.05, 0.42, "", facecolor="#FAFCFB", edgecolor=TEAL, linewidth=1.0)
    rounded_box(ax, 5.25, rows[3] + 0.06, 0.78, 0.26, "prefix", facecolor=TEAL_LIGHT, edgecolor=TEAL, fontsize=6.6)
    rounded_box(
        ax,
        6.03,
        rows[3] + 0.06,
        ready_x - 6.03,
        0.26,
        "wait",
        facecolor=ORANGE_LIGHT,
        edgecolor=ORANGE,
        hatch="////",
        fontsize=6.6,
    )
    rounded_box(ax, ready_x, rows[3] + 0.06, 2.20, 0.26, "dependent body", facecolor=TEAL_LIGHT, edgecolor=TEAL, fontsize=6.8)
    arrow(ax, (4.92, rows[3] + 0.57), (5.34, rows[3] + 0.36), color=TEAL, connectionstyle="arc3,rad=-0.2")
    ax.text(4.57, rows[3] + 0.63, "dependent launch", color=TEAL, fontsize=6.6, ha="center")

    legend = [
        Patch(facecolor=BLUE_LIGHT, edgecolor=BLUE, label="producer"),
        Patch(facecolor=ORANGE_LIGHT, edgecolor=ORANGE, hatch="////", label="wait / boundary cost"),
        Patch(facecolor=TEAL_LIGHT, edgecolor=TEAL, label="consumer"),
    ]
    ax.legend(handles=legend, loc="lower center", bbox_to_anchor=(0.58, -0.02), ncol=3, frameon=False, handlelength=1.6)
    save_figure(fig, "fig_execution_plans")


def generate_hazy_mechanism() -> None:
    fig, axes = plt.subplots(2, 1, figsize=(7.15, 3.20), sharex=True, gridspec_kw={"hspace": 0.48})
    ready_x = 6.35

    for ax in axes:
        ax.set_xlim(0.0, 10.0)
        ax.set_ylim(0.0, 2.05)
        ax.axis("off")
        ax.plot([ready_x, ready_x], [0.16, 1.74], color=ORANGE, lw=1.0, ls=(0, (3, 2)), zorder=6)

    ax = axes[0]
    ax.text(0.02, 1.94, "(a) Early-Inside: one persistent grid", fontsize=8.4, fontweight="bold", va="top")
    rounded_box(ax, 1.30, 0.18, 7.82, 1.42, "", facecolor="#FAFBFC", edgecolor=BLUE, linewidth=1.0)
    ax.text(0.12, 1.15, "queues 0–7", color=MID, fontsize=7.0, va="center")
    ax.text(0.12, 0.55, "queues 8–131", color=MID, fontsize=7.0, va="center")
    rounded_box(ax, 1.52, 0.92, ready_x - 1.52, 0.45, "8 PartialAttention tasks: long K/V scan", facecolor=BLUE_LIGHT, edgecolor=BLUE, fontsize=7.2)
    rounded_box(
        ax,
        2.32,
        0.32,
        ready_x - 2.32,
        0.45,
        "124 queues: pre-ready residence\n(wait and preparation)",
        facecolor=ORANGE_LIGHT,
        edgecolor=ORANGE,
        hatch="////",
        fontsize=6.8,
    )
    rounded_box(ax, ready_x, 0.32, 2.25, 0.45, "128 O-projection tasks", facecolor=TEAL_LIGHT, edgecolor=TEAL, fontsize=7.1)
    ax.text(2.32, 0.18, "consumer task admitted", color=ORANGE_TEXT, fontsize=6.6, ha="center", va="top")
    arrow(ax, (2.32, 0.23), (2.32, 0.34), color=ORANGE_TEXT)
    ax.text(ready_x, 1.72, "32/32 heads ready", color=ORANGE_TEXT, fontsize=7.0, ha="center")
    ax.text(8.83, 1.04, "read full\nattn_out[2048]", fontsize=6.6, color=TEAL, ha="center", va="center")

    ax = axes[1]
    ax.text(0.02, 1.94, "(b) Serial-Split: readiness-matched grid completion", fontsize=8.4, fontweight="bold", va="top")
    ax.text(0.12, 1.15, "producer SMs", color=MID, fontsize=7.0, va="center")
    ax.text(0.12, 0.55, "consumer SMs", color=MID, fontsize=7.0, va="center")
    rounded_box(ax, 1.30, 0.80, ready_x - 1.30, 0.80, "", facecolor="#FAFBFC", edgecolor=BLUE, linewidth=1.0)
    rounded_box(ax, 1.52, 0.98, ready_x - 1.52, 0.45, "8 PartialAttention tasks: long K/V scan", facecolor=BLUE_LIGHT, edgecolor=BLUE, fontsize=7.2)
    ax.add_patch(Rectangle((ready_x, 0.26), 0.34, 1.20, facecolor=ORANGE_LIGHT, edgecolor=ORANGE, hatch="////", lw=0.8, zorder=2))
    ax.text(ready_x + 0.17, 0.86, "grid gap", color=ORANGE_TEXT, fontsize=6.3, ha="center", va="center", rotation=90)
    rounded_box(ax, ready_x + 0.34, 0.20, 2.61, 0.80, "", facecolor="#FAFCFB", edgecolor=TEAL, linewidth=1.0)
    rounded_box(ax, ready_x + 0.53, 0.38, 2.20, 0.45, "128 O-projection tasks", facecolor=TEAL_LIGHT, edgecolor=TEAL, fontsize=7.1)
    ax.text(ready_x - 0.08, 1.53, "32/32 heads ready", color=ORANGE_TEXT, fontsize=7.0, ha="right")
    ax.text(4.00, 0.51, "consumer grid is absent before global readiness", color=MID, fontsize=6.8, ha="center")

    save_figure(fig, "fig_hazy_boundary_mechanism")


def generate_h800_boundary_results() -> None:
    fig, (ax0, ax1) = plt.subplots(
        1,
        2,
        figsize=(7.15, 3.15),
        gridspec_kw={"width_ratios": [1.08, 1.0], "wspace": 0.42},
    )

    # Panel (a): context scaling, with all independent process medians visible.
    context_rows = read_rows("context_gain_process.csv")
    grouped_context: dict[str, list[tuple[float, float, float]]] = defaultdict(list)
    token_order: dict[str, int] = {}
    for row in context_rows:
        grouped_context[row["context_label"]].append(
            (
                float(row["split_saving_us"]),
                float(row["ci_low_us"]),
                float(row["ci_high_us"]),
            )
        )
        token_order[row["context_label"]] = int(row["context_tokens"])
    labels = sorted(grouped_context, key=lambda item: token_order[item])
    x_values = list(range(len(labels)))
    medians: list[float] = []
    offsets = [-0.075, 0.0, 0.075]
    for x, label in zip(x_values, labels):
        observations = sorted(grouped_context[label], key=lambda item: item[0])
        values = [item[0] for item in observations]
        median = values[len(values) // 2]
        medians.append(median)
        for offset, (value, ci_low, ci_high) in zip(offsets, observations):
            ax0.errorbar(
                x + offset,
                value,
                yerr=[[value - ci_low], [ci_high - value]],
                fmt="o",
                color=BLUE,
                markeredgecolor="white",
                markeredgewidth=0.45,
                markersize=3.7,
                elinewidth=0.65,
                capsize=1.8,
                alpha=0.92,
                zorder=4,
            )
        ax0.errorbar(
            x,
            median,
            yerr=[[median - min(values)], [max(values) - median]],
            color=BLUE,
            marker="D",
            markersize=4.0,
            capsize=3.0,
            linewidth=1.1,
            zorder=5,
        )
        ax0.text(x, max(values) + 2.0, f"{min(values):.1f}–{max(values):.1f}", ha="center", va="bottom", fontsize=6.7, color=INK)
    ax0.plot(x_values, medians, color=BLUE, lw=1.1, alpha=0.72, zorder=2)
    ax0.scatter(2, 1.056, marker="^", s=30, color=ORANGE, edgecolor="white", linewidth=0.4, zorder=6)
    ax0.annotate(
        "120K visible grid gap: 1.056 μs",
        xy=(2, 1.056),
        xytext=(1.35, 8.5),
        fontsize=6.5,
        color=ORANGE_TEXT,
        arrowprops={"arrowstyle": "->", "color": ORANGE_TEXT, "lw": 0.7},
    )
    ax0.set_xticks(x_values, labels)
    ax0.set_ylim(0, 52)
    ax0.set_ylabel(r"Physical-split saving, $T_E-T_S$ ($\mu$s)")
    ax0.set_xlabel("Context length")
    ax0.set_title("(a) Same boundary across context", loc="left", fontweight="bold")
    ax0.grid(axis="y", color=GRID, lw=0.6, alpha=0.8)
    clean_axis(ax0)

    # Panel (b): all four adjacent edges at the same 32K workload.
    boundary_rows = read_rows("boundary_32k_process.csv")
    edge_order = ["partial_o", "qkv_partial", "oproj_upgate", "upgate_down"]
    edge_values: dict[str, list[float]] = defaultdict(list)
    for row in boundary_rows:
        edge_values[row["edge"]].append(float(row["split_minus_inside_us"]))
    short_edge_labels = {
        "partial_o": "Attn → O  (3 proc.)",
        "qkv_partial": "QKV → Attn  (2 proc.)",
        "oproj_upgate": "O → UpGate  (2 proc.)",
        "upgate_down": "UpGate → Down  (1 proc.)",
    }
    y_positions = list(reversed(range(len(edge_order))))
    ax1.axvspan(-60, 0, color=TEAL_LIGHT, alpha=0.62, zorder=0)
    ax1.axvspan(0, 60, color=ORANGE_LIGHT, alpha=0.52, zorder=0)
    ax1.axvline(0, color=INK, lw=0.9, zorder=2)
    for edge, y in zip(edge_order, y_positions):
        values = sorted(edge_values[edge])
        color = TEAL if sum(values) / len(values) < 0 else RED
        if len(values) > 1:
            ax1.plot([min(values), max(values)], [y, y], color=color, lw=2.0, solid_capstyle="round", zorder=3)
        local_offsets = [0.0] if len(values) == 1 else [(-0.08 + 0.16 * idx / (len(values) - 1)) for idx in range(len(values))]
        for value, offset in zip(values, local_offsets):
            ax1.scatter(value, y + offset, s=24, color=color if len(values) > 1 else PAPER, edgecolor=color, linewidth=1.0, zorder=4)
        mean = sum(values) / len(values)
        ha = "right" if mean < 0 else "left"
        shift = -1.8 if mean < 0 else 1.8
        ax1.text(mean + shift, y + 0.19, f"{min(values):+.1f}" if len(values) == 1 else f"{min(values):+.1f}…{max(values):+.1f}", ha=ha, va="bottom", fontsize=6.5, color=color)
    ax1.set_yticks(y_positions)
    ax1.set_yticklabels([])
    for edge, y in zip(edge_order, y_positions):
        ax1.text(-58.0, y, short_edge_labels[edge], ha="left", va="center", fontsize=6.7, color=MID)
    ax1.set_xlim(-60, 60)
    ax1.set_xlabel(r"$T_{split}-T_{inside}$ ($\mu$s)")
    ax1.set_title("(b) Adjacent boundaries at 32K", loc="left", fontweight="bold")
    ax1.text(-57, -0.72, "split faster", color=TEAL, fontsize=6.8, ha="left")
    ax1.text(57, -0.72, "inside faster", color=RED, fontsize=6.8, ha="right")
    ax1.grid(axis="x", color=GRID, lw=0.6, alpha=0.8)
    clean_axis(ax1)
    ax1.spines["left"].set_visible(False)
    ax1.tick_params(axis="y", length=0)

    save_figure(fig, "fig_h800_boundary_results")


def generate_pdl_timeline() -> None:
    rows = {row["variant"]: row for row in read_rows("pdl_nsys_medians.csv")}
    serial = rows["Ordinary-Split"]
    pdl = rows["Split+PDL"]

    serial_producer = float(serial["producer_us"])
    serial_start = float(serial["consumer_start_rel_producer_us"])
    serial_tail = float(serial["post_producer_tail_us"])
    pdl_producer = float(pdl["producer_us"])
    pdl_start = float(pdl["consumer_start_rel_producer_us"])
    pdl_tail = float(pdl["post_producer_tail_us"])

    fig, (ax0, ax1) = plt.subplots(
        1,
        2,
        figsize=(7.15, 3.10),
        gridspec_kw={"width_ratios": [1.45, 1.0], "wspace": 0.32},
    )

    y_serial, y_pdl = 1.0, 0.0
    height = 0.38
    # Align each producer completion at t=0; consumer intervals are overlaid.
    ax0.barh(y_serial, serial_producer, left=-serial_producer, height=height, color=BLUE_LIGHT, edgecolor=BLUE, linewidth=0.8)
    ax0.barh(y_pdl, pdl_producer, left=-pdl_producer, height=height, color=BLUE_LIGHT, edgecolor=BLUE, linewidth=0.8)
    ax0.barh(y_serial, serial_tail - serial_start, left=serial_start, height=height * 0.60, color=TEAL_LIGHT, edgecolor=TEAL, linewidth=0.8, zorder=4)
    ax0.barh(y_pdl, -pdl_start, left=pdl_start, height=height * 0.60, color=ORANGE_LIGHT, edgecolor=ORANGE, hatch="////", linewidth=0.8, zorder=4)
    ax0.barh(y_pdl, pdl_tail, left=0, height=height * 0.60, color=TEAL_LIGHT, edgecolor=TEAL, linewidth=0.8, zorder=5)
    ax0.axvline(0, color=INK, lw=1.0, ls=(0, (3, 2)))
    ax0.set_xlim(-815, 22)
    ax0.set_yticks([y_serial, y_pdl], ["Ordinary-Split", "Split+PDL"])
    ax0.set_xlabel(r"Time relative to producer completion ($\mu$s)")
    ax0.set_title("(a) Full consumer-grid residency", loc="left", fontweight="bold")
    ax0.text(-350, y_pdl + 0.03, "dependency wait + legal\nindependent work", fontsize=6.6, ha="center", va="center", color="#8A5B12", zorder=7)
    ax0.text(-805, -0.72, f"Producer median: {serial_producer:.3f} → {pdl_producer:.3f} μs", fontsize=6.6, color=MID, ha="left")
    ax0.grid(axis="x", color=GRID, lw=0.6, alpha=0.8)
    clean_axis(ax0)
    ax0.spines["left"].set_visible(False)
    ax0.tick_params(axis="y", length=0)

    ax1.barh(y_serial, serial_start, left=0, height=height, color=ORANGE_LIGHT, edgecolor=ORANGE, hatch="////", linewidth=0.8, label="visible gap")
    ax1.barh(y_serial, serial_tail - serial_start, left=serial_start, height=height, color=TEAL_LIGHT, edgecolor=TEAL, linewidth=0.8, label="post-ready suffix")
    ax1.barh(y_pdl, pdl_tail, left=0, height=height, color=TEAL_LIGHT, edgecolor=TEAL, linewidth=0.8)
    ax1.axvline(0, color=INK, lw=0.9)
    ax1.set_xlim(-0.2, 11.5)
    ax1.set_yticks([y_serial, y_pdl], ["Ordinary-Split", "Split+PDL"])
    ax1.set_xlabel(r"Post-producer tail ($\mu$s)")
    ax1.set_title("(b) Boundary-tail zoom", loc="left", fontweight="bold")
    ax1.text(serial_tail + 0.18, y_serial, f"{serial_tail:.3f}", va="center", fontsize=7.0, color=INK)
    ax1.text(pdl_tail + 0.18, y_pdl, f"{pdl_tail:.3f}", va="center", fontsize=7.0, color=INK)
    ax1.text(0.15, -0.72, "paired envelope: PDL − serial = −2.687 μs", fontsize=6.7, color=TEAL, ha="left")
    ax1.legend(
        loc="center right",
        bbox_to_anchor=(1.0, 0.52),
        frameon=True,
        framealpha=0.92,
        facecolor=PAPER,
        edgecolor="none",
        handlelength=1.5,
    )
    ax1.grid(axis="x", color=GRID, lw=0.6, alpha=0.8)
    clean_axis(ax1)
    ax1.spines["left"].set_visible(False)
    ax1.tick_params(axis="y", length=0)

    save_figure(fig, "fig_pdl_nsys_timeline")


def main() -> None:
    generate_execution_plans()
    generate_hazy_mechanism()
    generate_h800_boundary_results()
    generate_pdl_timeline()
    print(f"Generated paper figures under {OUT}")


if __name__ == "__main__":
    main()
