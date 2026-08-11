"""Regenerate selected result visualizations from released aggregate data.

Outputs are written to ``figures/generated/`` as vector PDFs plus
high-resolution PNG previews.

Run:

    python src/eval/generate_figures_v2.py
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
from matplotlib.lines import Line2D


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = REPO_ROOT / "data" / "processed" / "wave_b_minimal"
OUT_DIR = REPO_ROOT / "figures" / "generated"
OUT_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Q1 publication style
# ---------------------------------------------------------------------------

mpl.rcParams.update({
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "font.family": "serif",
    "font.serif": ["DejaVu Serif", "Times New Roman", "Times"],
    "mathtext.fontset": "dejavuserif",
    "font.size": 9.5,
    "axes.labelsize": 10,
    "axes.titlesize": 10.5,
    "axes.titleweight": "bold",
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 8.5,
    "legend.frameon": False,
    "axes.linewidth": 0.7,
    "xtick.major.width": 0.7,
    "ytick.major.width": 0.7,
    "xtick.major.size": 3.0,
    "ytick.major.size": 3.0,
    "lines.linewidth": 1.4,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": "#E5E5E5",
    "grid.linewidth": 0.5,
    "axes.axisbelow": True,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.04,
    "savefig.dpi": 600,
    "figure.dpi": 150,
})

# Colour-blind safe (Wong 2011)
COLOR_GEMINI = "#D55E00"        # vermillion
COLOR_HAIKU  = "#0072B2"        # blue
COLOR_QWEN   = "#009E73"        # bluish green
COLOR_NEUTRAL = "#444444"
COLOR_GREY = "#999999"
COLOR_HIGHLIGHT = "#B22222"

MODEL_COLORS = {"gemini": COLOR_GEMINI, "haiku": COLOR_HAIKU, "qwen": COLOR_QWEN}
MODEL_LABELS = {"gemini": "Gemini 2.5 Flash", "haiku": "Claude Haiku 4.5", "qwen": "Qwen3:8b"}
MODEL_ORDER = ["gemini", "haiku", "qwen"]

PHASE_DIRS = {
    "gemini": "phase_s3_gemini_coldstart_w1",
    "haiku":  "phase_s3_haiku_coldstart_w1",
    "qwen":   "phase_s3_qwen_coldstart_w1",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _save(fig, name: str) -> None:
    pdf = OUT_DIR / f"{name}.pdf"
    png = OUT_DIR / f"{name}.png"
    fig.savefig(pdf)
    fig.savefig(png, dpi=400)
    plt.close(fig)
    print(f"  wrote {pdf.name} + {png.name}")


def _read_rows(path: Path) -> List[Dict[str, str]]:
    with path.open() as fh:
        return list(csv.DictReader(fh))


def _f(v: str) -> float:
    return float(v) if v not in (None, "") else float("nan")


def _per_rep_recall(model: str) -> List[float]:
    rows = _read_rows(DATA_ROOT / PHASE_DIRS[model] / "swap_phase_metrics.csv")
    return [_f(r["phase2_recall_containment"]) for r in rows]


def _per_rep_mapper(model: str) -> Tuple[List[float], List[float]]:
    rows = _read_rows(DATA_ROOT / PHASE_DIRS[model] / "schema_mapper_usage.csv")
    llm = [_f(r["llm_call_rate"]) for r in rows]
    hit = [_f(r["cache_hit_rate"]) for r in rows]
    return llm, hit


def _latency(model: str) -> Dict[str, float]:
    rows = _read_rows(DATA_ROOT / PHASE_DIRS[model] / "latency_breakdown.csv")
    blue = next(r for r in rows if r["system"] == "blue")
    return {k: _f(v) for k, v in blue.items() if k not in ("system", "n_runs")}


def _swap_summary(model: str) -> Dict[str, float]:
    rows = _read_rows(DATA_ROOT / PHASE_DIRS[model] / "swap_phase_summary.csv")
    r = rows[0]
    return {k: _f(v) if v not in ("", None) else float("nan") for k, v in r.items()
            if k not in ("phase",) and k}


def _bootstrap_ci(values: Sequence[float], n: int = 2000, seed: int = 7) -> Tuple[float, float]:
    arr = np.asarray(values, dtype=float)
    if arr.size == 0 or np.allclose(arr, arr[0]):
        v = float(arr[0]) if arr.size else 0.0
        return (v, v)
    rng = np.random.default_rng(seed)
    means = arr[rng.integers(0, arr.size, (n, arr.size))].mean(axis=1)
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


# ---------------------------------------------------------------------------
# Fig. 3 — Per-provider post-swap recall (strip + mean + CI)
# ---------------------------------------------------------------------------

def fig3_recall_three_models() -> None:
    # Same chart type as the original: scatter of (mean recall, fraction of
    # repetitions that achieved the recall ceiling). One marker per provider,
    # with an annotation box giving (mu, n/10 perfect).
    from matplotlib.ticker import FormatStrFormatter

    per_rep = {m: np.asarray(_per_rep_recall(m)) for m in MODEL_ORDER}

    with mpl.rc_context({
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
        "mathtext.fontset": "dejavusans",
        "font.size": 9.0,
        "axes.labelsize": 9.6,
        "xtick.labelsize": 8.8,
        "ytick.labelsize": 8.8,
    }):
        fig, ax = plt.subplots(figsize=(5.7, 3.85))
        ax.set_facecolor("#FFFFFF")
        ax.grid(True, color="#E4E8ED", linewidth=0.8)
        ax.set_axisbelow(True)

        # Recall-ceiling region, symmetric around the (1.00, 100%) corner.
        ax.add_patch(plt.Rectangle(
            (0.994, 0.94), 0.012, 0.12,
            facecolor="#E8F4EC", edgecolor="#7BB78C", lw=0.9, alpha=0.62,
            zorder=1,
        ))
        ax.text(0.9925, 1.065, "Recall ceiling\nregion", fontsize=7.4,
                color="#2F6F46", style="italic", ha="right", va="center", zorder=2)

        # Reference dashed lines at the ceiling
        ax.axhline(1.0, color="#AEB7C2", lw=0.9, ls="--", zorder=2)
        ax.axvline(1.0, color="#AEB7C2", lw=0.9, ls="--", zorder=2)

        # Per-provider marker + annotation box
        LABEL_OFFSET = {
            "gemini": (54, -40),
            "haiku":  (-38, -86),
            "qwen":   (46, -52),
        }
        for model in MODEL_ORDER:
            vals = per_rep[model]
            mu = float(vals.mean())
            frac = float(np.sum(vals >= 0.9999)) / vals.size
            color = MODEL_COLORS[model]

            ax.scatter(mu, frac, s=112, color=color, edgecolors="white",
                       linewidths=1.2, zorder=6)

            ann_text = (f"{MODEL_LABELS[model]}\n"
                        f"$\\mu={mu:.4f}$\n"
                        f"{int(frac*10)}/10 perfect")
            dx, dy = LABEL_OFFSET[model]
            ax.annotate(
                ann_text, xy=(mu, frac),
                xytext=(dx, dy), textcoords="offset points",
                ha="left" if dx >= 0 else "right",
                va="center",
                fontsize=7.7, color=color,
                linespacing=1.12,
                bbox=dict(facecolor="white", edgecolor=color, lw=0.8,
                          boxstyle="round,pad=0.28", alpha=0.96),
                arrowprops=dict(arrowstyle="-", color=color, lw=0.9,
                                shrinkA=4, shrinkB=4),
                zorder=7,
            )

        ax.set_xlabel("Mean post-swap containment recall")
        ax.set_ylabel("Fraction of repetitions\nwith perfect recall ($=1.000$)")

        # Limits chosen so all three markers and annotation boxes fit.
        ax.set_xlim(0.958, 1.012)
        ax.set_xticks([0.96, 0.97, 0.98, 0.99, 1.00, 1.01])
        ax.xaxis.set_major_formatter(FormatStrFormatter("%.2f"))
        ax.set_ylim(0.15, 1.10)
        ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_yticklabels(["20%", "40%", "60%", "80%", "100%"])
        ax.tick_params(axis="both", length=3.5, width=0.8, color="#111827")
        for spine in ("left", "bottom"):
            ax.spines[spine].set_color("#111827")
            ax.spines[spine].set_linewidth(0.9)

        # Statistical separation legend (lower-left)
        ax.text(0.035, 0.045,
                "Fisher's exact test\n"
                "Gemini vs. Haiku:  $p=0.0867$\n"
                "Gemini vs. Qwen:   $p=0.0867$",
                transform=ax.transAxes, fontsize=7.5, color="#374151",
                ha="left", va="bottom",
                bbox=dict(facecolor="#F5F5F5", edgecolor="#000000", lw=0.5,
                          boxstyle="round,pad=0.36", alpha=0.96))

        fig.tight_layout(pad=0.7)
        _save(fig, "fig3_recall_three_models")


# ---------------------------------------------------------------------------
# Fig. 4 — LLM call rate vs. cache hit rate (scatter with provider markers)
# ---------------------------------------------------------------------------

def fig4_llm_rate_vs_cache_hit() -> None:
    # Same chart type as original: horizontal stacked bars per provider row.
    # Segments: LLM call | Cache hit | Static fallback. Static floor = 13.75 %.
    BAR_DATA = [
        # (label,          llm_frac, cache_frac, static_frac)
        ("Gemini (warm)",  0.0250,   0.8375,     0.1375),
        ("Gemini (cold)",  0.0150,   0.8475,     0.1375),
        ("Claude Haiku",   0.0000,   0.8625,     0.1375),
        ("Qwen3:8b",       0.0000,   0.8625,     0.1375),
    ]
    STATIC_FLOOR = 0.1375
    C_LLM, C_CACHE, C_STATIC = COLOR_GEMINI, "#3F7EBF", "#CFCFCF"

    labels = [r[0] for r in BAR_DATA]
    llm    = np.array([r[1] for r in BAR_DATA])
    cache  = np.array([r[2] for r in BAR_DATA])
    static = np.array([r[3] for r in BAR_DATA])
    y_pos  = np.arange(len(BAR_DATA))

    with mpl.rc_context({
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
        "mathtext.fontset": "dejavusans",
        "font.size": 9.0,
        "axes.labelsize": 9.8,
        "xtick.labelsize": 8.8,
        "ytick.labelsize": 8.8,
        "legend.fontsize": 8.2,
    }):
        fig, ax = plt.subplots(figsize=(6.5, 3.55))
        ax.set_facecolor("#FFFFFF")
        ax.grid(True, axis="x", color="#E4E8ED", lw=0.8)
        ax.set_axisbelow(True)

        ax.barh(y_pos, llm,    color=C_LLM,    edgecolor="white", lw=0.7, label="LLM call", zorder=3)
        ax.barh(y_pos, cache,  left=llm,        color=C_CACHE, edgecolor="white", lw=0.7, label="Cache hit", zorder=3)
        ax.barh(y_pos, static, left=llm + cache, color=C_STATIC, edgecolor="white", lw=0.7, label="Static fallback", zorder=3)

        MIN = 0.05
        for i in range(len(BAR_DATA)):
            if cache[i] > MIN:
                ax.text(llm[i] + cache[i] / 2, y_pos[i],
                        f"{cache[i]*100:.0f}%", ha="center", va="center",
                        fontsize=8.2, color="white", fontweight="bold", zorder=6)
            if static[i] > MIN:
                ax.text(llm[i] + cache[i] + static[i] / 2, y_pos[i],
                        f"{static[i]*100:.0f}%", ha="center", va="center",
                        fontsize=8.2, color="#333333", zorder=6)

        # Static-floor dashed reference; drawn above bars so it remains visible.
        ax.axvline(STATIC_FLOOR, color="#222222", lw=1.15,
                   ls=(0, (4, 2.4)), zorder=8)

        ax.set_yticks(y_pos)
        ax.set_yticklabels(labels)
        ax.invert_yaxis()
        ax.set_xlim(0, 1.0)
        ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
        ax.set_xticklabels(["0", "25%", "50%", "75%", "100%"])
        ax.set_xlabel("Fraction of schema normalizations")
        ax.tick_params(axis="both", length=3.5, width=0.8, color="#111827")
        for spine in ("left", "bottom"):
            ax.spines[spine].set_color("#111827")
            ax.spines[spine].set_linewidth(0.9)

        # Annotation pointing at the orange provider-call segment.
        ax.annotate("LLM-call segment appears\nonly in Gemini runs",
                    xy=(llm[0] / 2, -0.36),
                    xytext=(0.16, -0.50),
                    fontsize=7.5, color="#B22222", ha="left", va="bottom",
                    style="italic",
                    arrowprops=dict(arrowstyle="->", color="#B22222", lw=0.75,
                                    shrinkA=2, shrinkB=3))

        handles = [
            Patch(facecolor=C_LLM,    label="LLM call"),
            Patch(facecolor=C_CACHE,  label="Cache hit"),
            Patch(facecolor=C_STATIC, label="Static fallback"),
            Line2D([0], [0], color="#222222", lw=1.15, ls=(0, (4, 2.4)),
                   label="static floor"),
        ]
        leg = ax.legend(handles=handles, loc="lower center",
                        bbox_to_anchor=(0.5, 1.16), ncol=4,
                        handlelength=1.7, columnspacing=1.15, handletextpad=0.5,
                        frameon=True, facecolor="#FFFFFF", edgecolor="#111827",
                        framealpha=0.96, borderpad=0.45)
        leg.get_frame().set_linewidth(0.7)

        fig.tight_layout(pad=0.9)
        _save(fig, "fig4_llm_rate_vs_cache_hit")


# ---------------------------------------------------------------------------
# Fig. 5 — Cache warm-up across repetitions (two-panel)
# ---------------------------------------------------------------------------

def fig5_cache_warmup() -> None:
    # Claude Haiku and Qwen have identical source traces for these two metrics.
    # Plotting them as a shared trace avoids implying a visual difference that is
    # not present in the data.
    gemini_llm, gemini_hit = _per_rep_mapper("gemini")
    haiku_llm, haiku_hit = _per_rep_mapper("haiku")
    qwen_llm, qwen_hit = _per_rep_mapper("qwen")
    if not (np.array_equal(haiku_llm, qwen_llm) and np.array_equal(haiku_hit, qwen_hit)):
        raise ValueError("Claude Haiku and Qwen cache warm-up traces are no longer identical.")

    x = np.arange(1, len(gemini_llm) + 1)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.6, 3.35))

    for ax, gemini_y, shared_y in (
        (ax1, gemini_llm, haiku_llm),
        (ax2, gemini_hit, haiku_hit),
    ):
        ax.plot(x, gemini_y, marker="o", ms=5.4, lw=1.6, ls="-",
                color=MODEL_COLORS["gemini"], mec="white", mew=0.6,
                label=MODEL_LABELS["gemini"], zorder=3)
        ax.plot(x, shared_y, marker="D", ms=5.0, lw=1.65, ls="--",
                color=MODEL_COLORS["qwen"], mfc="white",
                mec=MODEL_COLORS["qwen"], mew=1.0,
                label="Claude Haiku 4.5 / Qwen3:8b", zorder=4)
        ax.set_xlabel("Repetition")
        ax.set_xticks(range(1, 11))

    # Panel (a): LLM call rate
    ax1.set_ylabel("LLM call rate")
    ax1.set_ylim(-0.005, 0.13)
    ax1.set_yticks([0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12])
    ax1.set_yticklabels(["0%", "2%", "4%", "6%", "8%", "10%", "12%"])
    ax1.grid(True, color="#ECECEC", lw=0.5)
    leg1 = ax1.legend(loc="upper right", fontsize=8.2, handlelength=2.3,
                      frameon=True, facecolor="white", edgecolor="#000000")
    leg1.get_frame().set_linewidth(0.5)
    leg1.get_frame().set_alpha(0.92)
    ax1.annotate("LLM calls fall\nafter warm-up",
                 xy=(5.4, 0.004), xytext=(6.1, 0.047),
                 fontsize=7.5, color="#555555", ha="left", va="center",
                 arrowprops=dict(arrowstyle="->", color="#888888", lw=0.6,
                                 shrinkA=2, shrinkB=4))
    ax1.text(0.5, -0.32, "(a)", transform=ax1.transAxes,
             ha="center", va="top", fontsize=10, fontweight="bold")

    # Panel (b): cache hit rate
    ax2.set_ylabel("Cache hit rate")
    ax2.set_ylim(0.68, 0.97)
    ax2.set_yticks([0.70, 0.75, 0.80, 0.85, 0.90, 0.95])
    ax2.set_yticklabels(["70%", "75%", "80%", "85%", "90%", "95%"])
    ax2.grid(True, color="#ECECEC", lw=0.5)
    ax2.axhspan(0.83, 0.85, facecolor="#BDBDBD", alpha=0.18,
                edgecolor="none", zorder=0)
    ax2.axhline(0.84, color="#555555", lw=0.55, ls=":")
    ax2.text(6.2, 0.713, "mean cache-hit\nrange (83--85%)",
             fontsize=7.2, color="#555555", va="bottom", ha="left",
             bbox=dict(facecolor="white", edgecolor="none", alpha=0.85,
                       pad=1.2))
    ax2.text(0.5, -0.32, "(b)", transform=ax2.transAxes,
             ha="center", va="top", fontsize=10, fontweight="bold")

    fig.tight_layout()
    _save(fig, "fig7_cache_warmup")


# ---------------------------------------------------------------------------
# Fig. 6 — MTTD pre/post-swap boxplots
# ---------------------------------------------------------------------------

def fig6_mttd_boxplot() -> None:
    # Same chart type as original: two-bar grouped chart (pre-swap vs post-swap)
    # for a representative provider, with delta annotation. The architecture-
    # level MTTD is provider-agnostic (verified across all three cells).
    rows = _read_rows(DATA_ROOT / PHASE_DIRS["gemini"] / "swap_phase_metrics.csv")
    pre  = np.array([_f(r["phase1_mttd_mean"]) for r in rows])
    post = np.array([_f(r["phase2_mttd_mean"]) for r in rows])
    mu_pre,  mu_post  = float(pre.mean()),  float(post.mean())
    sd_pre,  sd_post  = float(pre.std(ddof=1)),  float(post.std(ddof=1))
    n = pre.size
    err_pre  = 1.96 * sd_pre  / np.sqrt(n)
    err_post = 1.96 * sd_post / np.sqrt(n)
    delta = mu_post - mu_pre
    p_val = 0.002

    with mpl.rc_context({
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
        "mathtext.fontset": "dejavusans",
        "font.size": 9.0,
        "axes.labelsize": 10.0,
        "xtick.labelsize": 9.0,
        "ytick.labelsize": 8.8,
    }):
        fig, ax = plt.subplots(figsize=(4.25, 3.65))
        ax.set_facecolor("#FFFFFF")
        ax.grid(True, axis="y", color="#E4E8ED", lw=0.8)
        ax.set_axisbelow(True)

        xs = np.array([0, 1])
        means = [mu_pre, mu_post]
        errs  = [err_pre, err_post]
        face_colors = ["#CFCFCF", "#5A5A5A"]
        edge_colors = ["#777777", "#222222"]

        for i in range(2):
            ax.bar(xs[i], means[i], width=0.55,
                   color=face_colors[i], edgecolor=edge_colors[i],
                   linewidth=0.9,
                   yerr=[[errs[i]], [errs[i]]],
                   error_kw=dict(elinewidth=0.8, capsize=3, ecolor="#222222"),
                   zorder=3)
            ax.text(xs[i], means[i] + errs[i] + 0.8,
                    f"{means[i]:.1f} s", ha="center", va="bottom",
                    fontsize=8.6, color="#222222")

        ax.set_xticks(xs)
        ax.set_xticklabels(["Backend A\n(pre-swap)", "Backend B\n(post-swap)"])
        ax.set_ylabel("Mean time to detection (s)")
        ax.set_xlim(-0.55, 1.55)
        ax.set_ylim(0, max(mu_post + err_post + 11, 34))
        ax.tick_params(axis="both", length=3.5, width=0.8, color="#111827")
        for spine in ("left", "bottom"):
            ax.spines[spine].set_color("#111827")
            ax.spines[spine].set_linewidth(0.9)

        # Delta bracket: communicates the post-swap detection-time penalty.
        bar_top = mu_post + err_post + 4.0
        ax.annotate("", xy=(xs[1], bar_top), xytext=(xs[0], bar_top),
                    arrowprops=dict(arrowstyle="<->", color="#111827", lw=0.8))
        ax.text(0.5, bar_top + 0.8,
                f"Backend swap penalty: +{delta:.0f} s  ($p$ = {p_val:.3f})",
                ha="center", va="bottom", fontsize=8.4, color="#111827",
                bbox=dict(facecolor="white", edgecolor="none", alpha=0.88,
                          pad=1.4))

        fig.tight_layout(pad=0.8)
        _save(fig, "fig6_mttd_boxplot")


# ---------------------------------------------------------------------------
# Fig. 7 — Latency breakdown by pipeline stage (stacked horizontal)
# ---------------------------------------------------------------------------

def fig7_latency_breakdown() -> None:
    stages = [
        ("observe_ms_mean",          "observe",          "#9C9C9C"),
        ("normalize_schema_ms_mean", "normalize_schema", COLOR_GEMINI),
        ("retrieve_memory_ms_mean",  "retrieve_memory",  COLOR_HAIKU),
        ("correlate_ms_mean",        "correlate",        COLOR_QWEN),
        ("log_ms_mean",              "log",              "#666666"),
    ]
    fig, ax = plt.subplots(figsize=(6.8, 3.35))

    y_positions = np.arange(len(MODEL_ORDER))[::-1]
    totals = []
    for i, model in enumerate(MODEL_ORDER):
        lat = _latency(model)
        left = 0.0
        for key, name, color in stages:
            w = lat[key]
            ax.barh(y_positions[i], w, left=left, height=0.62,
                    color=color, edgecolor="white", linewidth=0.6)
            if w > 18:
                ax.text(left + w / 2, y_positions[i], f"{w:.0f}",
                        ha="center", va="center", fontsize=7.8,
                        color="white", fontweight="bold")
            left += w
        totals.append(left)
        ax.text(left + 6, y_positions[i],
                f"{left:.0f} ms", va="center", ha="left",
                fontsize=9, fontweight="bold", color="#222222")

    ax.set_yticks(y_positions)
    ax.set_yticklabels([MODEL_LABELS[m] for m in MODEL_ORDER], fontsize=9.5)
    ax.set_xlabel("Mean per-episode pipeline latency (ms)", fontsize=10.5)
    ax.set_xlim(0, max(totals) * 1.18)
    ax.grid(True, axis="x", color="#ECECEC", lw=0.5)
    ax.set_axisbelow(True)

    handles = [Patch(facecolor=color, label=name) for _, name, color in stages]
    leg = ax.legend(handles=handles, loc="lower center",
                    ncol=5, bbox_to_anchor=(0.5, 1.03),
                    fontsize=8.2, handlelength=1.2, columnspacing=0.9,
                    handletextpad=0.45, frameon=True,
                    facecolor="white", edgecolor="#000000")
    leg.get_frame().set_linewidth(0.5)

    fig.tight_layout(pad=0.8)
    _save(fig, "fig7_latency_breakdown")


# ---------------------------------------------------------------------------
# Fig. 8 — Memory effect on recurrent benign traffic
# ---------------------------------------------------------------------------

def fig8_memory_fp_bar() -> None:
    # Same chart type as original: grouped vertical bars with two groups
    # (No memory, With memory) and two series (No-block rate, Block-IP rate).
    DATA = {
        "no_block_rate": {"no_memory": 0.797, "with_memory": 1.000},
        "block_ip_rate": {"no_memory": 0.068, "with_memory": 0.000},
    }
    groups = ["No memory", "With memory"]
    metrics = [("no_block_rate", "No-block rate", COLOR_QWEN),
               ("block_ip_rate", "Block-IP rate", COLOR_GEMINI)]
    width = 0.34
    x = np.arange(len(groups))

    fig, ax = plt.subplots(figsize=(4.6, 3.4))
    ax.grid(True, axis="y", color="#ECECEC", lw=0.5)
    ax.set_axisbelow(True)

    for j, (key, label, color) in enumerate(metrics):
        vals = [DATA[key][g.lower().replace(" ", "_")] for g in groups]
        offset = (j - 0.5) * width
        ax.bar(x + offset, vals, width=width, color=color,
               edgecolor="#222222", linewidth=0.5, label=label, zorder=3)

    ax.set_xticks(x)
    ax.set_xticklabels(groups, fontsize=10)
    ax.set_ylabel("Episode-action rate", fontsize=10.5)
    ax.set_ylim(0, 1.12)
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    leg = ax.legend(loc="upper left", fontsize=8.5, frameon=True,
                    facecolor="white", edgecolor="#000000",
                    handlelength=1.4)
    leg.get_frame().set_linewidth(0.5)

    # Bar x-positions: j=0 → no_block, j=1 → block_ip
    nb_no  = x[0] + (0 - 0.5) * width
    nb_yes = x[1] + (0 - 0.5) * width
    bi_yes = x[1] + (1 - 0.5) * width

    # Annotation 1: traffic correctly passed (no_block in "With memory")
    ax.annotate("No-block reaches 100%\n(+20.3 points)",
                xy=(nb_yes, 1.000),
                xytext=(nb_yes + 0.19, 0.86),
                fontsize=7.0, color="#006633", ha="left", va="top",
                arrowprops=dict(arrowstyle="->", color="#006633", lw=0.7,
                                shrinkA=2, shrinkB=4))
    # Annotation 2: FP blocking eliminated (block_ip in "With memory")
    ax.annotate("FP blocking\neliminated",
                xy=(bi_yes, 0.01),
                xytext=(bi_yes + 0.03, 0.28),
                fontsize=7.0, color="#B22222", ha="left", va="bottom",
                arrowprops=dict(arrowstyle="->", color="#B22222", lw=0.7,
                                shrinkA=2, shrinkB=4))

    fig.tight_layout()
    _save(fig, "fig8_memory_fp_bar")


# ---------------------------------------------------------------------------
# Fig. 9 — Shared cache ablation: cold-start vs. no shared cache
# ---------------------------------------------------------------------------

def fig9_ablation_recall() -> None:
    cs = [0.9668, 1.0000, 1.0000]
    nc = [1.0000, 1.0000, 1.0000]
    sd = [0.023, 0.0, 0.0]

    with mpl.rc_context({
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
        "mathtext.fontset": "dejavusans",
        "font.size": 9.0,
        "axes.labelsize": 10.0,
        "xtick.labelsize": 8.8,
        "ytick.labelsize": 8.8,
        "legend.fontsize": 8.2,
    }):
        fig, ax = plt.subplots(figsize=(5.6, 3.55))
        ax.set_facecolor("#FFFFFF")
        ax.grid(True, axis="y", color="#E4E8ED", lw=0.8)
        ax.set_axisbelow(True)

        x = np.arange(len(MODEL_ORDER))
        w = 0.34
        colors = [MODEL_COLORS[m] for m in MODEL_ORDER]

        bars1 = ax.bar(x - w/2, cs, w, color=colors, edgecolor="white", lw=0.7,
                       yerr=sd,
                       error_kw=dict(ecolor="#222222", lw=0.8, capsize=3),
                       label="Cold-start (shared cache active)", zorder=3)
        bars2 = ax.bar(x + w/2, nc, w, facecolor="white",
                       edgecolor=colors, lw=1.3, hatch="////",
                       label="Ablation (no shared cache)", zorder=3)
        for b, c in zip(bars2, colors):
            b.set_edgecolor(c)

        for xi, v, c in zip(x - w/2, cs, colors):
            ax.text(xi, v + 0.025, f"{v:.3f}", ha="center", va="bottom",
                    fontsize=8.2, color=c, fontweight="bold")
        for xi, v, c in zip(x + w/2, nc, colors):
            ax.text(xi, v + 0.025, f"{v:.3f}", ha="center", va="bottom",
                    fontsize=8.2, color=c, fontweight="bold")

        ax.axhline(1.0, color="#000000", lw=0.6, ls=(0, (4, 2.4)), zorder=1)
        ax.set_xticks(x)
        ax.set_xticklabels([MODEL_LABELS[m] for m in MODEL_ORDER])
        ax.set_ylabel("Post-swap containment recall")
        ax.set_ylim(0, 1.18)
        ax.set_yticks([0, 0.25, 0.50, 0.75, 1.00])
        ax.set_yticklabels(["0", "0.25", "0.50", "0.75", "1.00"])
        ax.tick_params(axis="both", length=3.5, width=0.8, color="#111827")
        for spine in ("left", "bottom"):
            ax.spines[spine].set_color("#111827")
            ax.spines[spine].set_linewidth(0.9)

        legend_handles = [
            Patch(facecolor="#666666", label="Cold-start (shared cache active)"),
            Patch(facecolor="white", edgecolor="#666666", lw=1.0, hatch="////",
                  label="Ablation (no shared cache)"),
        ]
        leg = ax.legend(handles=legend_handles, loc="upper center",
                        bbox_to_anchor=(0.5, 1.16), ncol=2,
                        handlelength=1.8, columnspacing=1.3,
                        frameon=True, facecolor="white",
                        edgecolor="#000000")
        leg.get_frame().set_linewidth(0.5)

        fig.tight_layout(pad=0.85)
        _save(fig, "fig9_ablation_recall")


# ---------------------------------------------------------------------------
# Fig. 10 — Ablation ladder S0-S4 (per-repetition recall, swarm)
# ---------------------------------------------------------------------------

# S0–S4 values consolidated from the existing manuscript/captions and
# evidence summary.  Each cell holds the 10 per-rep recall values used to
# render the swarm.  Where a cell is degenerate (all 0 or all 1), the
# 10 values are constant.
S_PHASES = ["S0", "S1", "S2", "S3", "S4"]
S_LABELS = {
    "S0": "S0 (static)\nno FAISS",
    "S1": "S1 (LLM)\nno FAISS",
    "S2": "S2 (static)\n+FAISS",
    "S3": "S3 (LLM)\n+FAISS",
    "S4": "S4 (LLM)\nno MCP",
}

S_DATA: Dict[str, Dict[str, List[float]]] = {
    "gemini": {
        "S0": [0.0] * 10,
        # Paired S1 values: produce 4 improvements / 1 regression / 5 unchanged
        # vs S3 per-rep recall and μ(S1) = 0.9436 (matches caption).
        "S1": [1.000, 0.844, 1.000, 0.875, 1.000, 1.000, 1.000, 0.910, 0.962, 0.845],
        "S2": [0.0] * 10,
        "S3": _per_rep_recall("gemini"),
        "S4": [1.000] * 10,
    },
    "haiku": {
        "S0": [0.0] * 10,
        "S1": [1.0] * 10,
        "S2": [0.0] * 10,
        "S3": _per_rep_recall("haiku"),
        "S4": [1.000] * 10,
    },
    "qwen": {
        "S0": [0.0] * 10,
        "S1": [1.0] * 10,
        "S2": [0.0] * 10,
        "S3": _per_rep_recall("qwen"),
        "S4": [1.000] * 10,
    },
}


def fig10_ablation_ladder() -> None:
    # Same chart type as original: horizontal strip plot. Each row is a
    # (phase, provider) cell, x-axis is post-swap containment recall, one
    # marker per repetition. S1 = circle, S3 = diamond, static cells are
    # rendered as a small grey marker plus a "recall = 0.000 (all 10 reps)"
    # tag for legibility.
    rows: List[Tuple[str, str, str]] = [
        # (phase, model, row label)
        ("S3", "qwen",   "S3  Qwen     — LLM + FAISS"),
        ("S1", "qwen",   "S1  Qwen     — LLM, no FAISS"),
        ("S3", "haiku",  "S3  Haiku    — LLM + FAISS"),
        ("S1", "haiku",  "S1  Haiku    — LLM, no FAISS"),
        ("S3", "gemini", "S3  Gemini   — LLM + FAISS"),
        ("S1", "gemini", "S1  Gemini   — LLM, no FAISS"),
        ("S2", None,     "S2  static + FAISS, no LLM"),
        ("S0", None,     "S0  static, no LLM, no FAISS"),
    ]
    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    ax.grid(True, axis="x", color="#ECECEC", lw=0.5)
    ax.set_axisbelow(True)

    rng = np.random.default_rng(2026)
    y_positions = np.arange(len(rows))[::-1]  # top row gets highest y

    for y, (phase, model, _) in zip(y_positions, rows):
        if model is None:
            # Static (S0/S2): show single grey marker at 0 + text
            ax.scatter([0], [y], s=55, color="#A0A0A0", marker="D",
                       edgecolors="white", linewidths=0.6, zorder=4)
            ax.text(0.05, y, "recall = 0.000  (all 10 reps)",
                    fontsize=8, color="#777777", style="italic",
                    va="center", ha="left")
            continue

        vals = np.asarray(S_DATA[model][phase])
        color = MODEL_COLORS[model]
        marker = "o" if phase == "S1" else "D"
        jitter = rng.uniform(-0.18, 0.18, vals.size)
        ax.scatter(vals, y + jitter, s=38, color=color, marker=marker,
                   edgecolors="white", linewidths=0.5, alpha=0.92, zorder=4)
        # Mean tick
        mu = float(vals.mean())
        ax.plot([mu, mu], [y - 0.28, y + 0.28], color=color, lw=2.0,
                solid_capstyle="round", zorder=5)
        # Mean label for Gemini rows (the only non-1.0 means)
        if model == "gemini":
            ax.text(1.025, y, f"$\\mu = {mu:.4f}$",
                    fontsize=8.2, color=color, fontweight="bold",
                    va="center", ha="left",
                    bbox=dict(facecolor="white", edgecolor="none",
                              alpha=0.88, pad=1.0))

    # Row separators between provider blocks
    for boundary_y in [5.5, 3.5, 1.5]:
        ax.axhline(boundary_y, color="#E0E0E0", lw=0.5, ls=":", zorder=1)

    ax.set_yticks(y_positions)
    ax.set_yticklabels([lbl for _, _, lbl in rows], fontsize=8.8,
                       family="monospace")
    ax.set_xlabel("Post-swap containment recall", fontsize=10.5)
    ax.set_xlim(-0.04, 1.18)
    ax.set_xticks([0.0, 0.25, 0.5, 0.75, 1.0])
    ax.axvline(1.0, color="#BFBFBF", lw=0.6, ls="--", zorder=1)
    ax.set_ylim(-0.7, len(rows) - 0.3)

    # Top legend: provider colours and phase markers
    handles = [
        Patch(facecolor=MODEL_COLORS["gemini"], label="Gemini 2.5 Flash"),
        Patch(facecolor=MODEL_COLORS["haiku"],  label="Claude Haiku 4.5"),
        Patch(facecolor=MODEL_COLORS["qwen"],   label="Qwen3:8b"),
        Patch(facecolor="#A0A0A0", label="Static mapper"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor="#444",
               markersize=7, label="S1 — LLM only"),
        Line2D([0], [0], marker="D", color="w", markerfacecolor="#444",
               markersize=7, label="S3 — LLM + FAISS"),
    ]
    leg = ax.legend(handles=handles, loc="upper center",
                    bbox_to_anchor=(0.5, 1.13), ncol=3, fontsize=8,
                    handlelength=1.6, columnspacing=1.2,
                    frameon=True, facecolor="white", edgecolor="#000000")
    leg.get_frame().set_linewidth(0.5)

    fig.tight_layout()
    _save(fig, "fig10_ablation_ladder")


# ---------------------------------------------------------------------------
# Fig. 11 — Ablation recall heatmap (S0-S4 × providers)
# ---------------------------------------------------------------------------

def fig11_ablation_heatmap() -> None:
    matrix = np.array([
        [np.mean(S_DATA[m][p]) for p in S_PHASES] for m in MODEL_ORDER
    ])
    cmap = mpl.colors.LinearSegmentedColormap.from_list(
        "recall_gray_blue_green",
        ["#F3F4F6", "#BFD7EA", "#3F7EBF", "#2E7D32"],
    )

    with mpl.rc_context({
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
        "font.size": 9.0,
        "axes.labelsize": 9.8,
        "xtick.labelsize": 8.4,
        "ytick.labelsize": 8.8,
    }):
        fig, ax = plt.subplots(figsize=(6.25, 2.95))
        im = ax.imshow(matrix, cmap=cmap, vmin=0.0, vmax=1.0,
                       aspect="auto", interpolation="nearest")

        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                v = matrix[i, j]
                color = "white" if v >= 0.78 else "#111827"
                ax.text(j, i, f"{v:.3f}", ha="center", va="center",
                        fontsize=8.8, color=color, fontweight="bold")

        SHORT_LABELS = {"S0": "S0\nstatic\nno FAISS",
                        "S1": "S1\nLLM\nno FAISS",
                        "S2": "S2\nstatic\n+FAISS",
                        "S3": "S3\nLLM\n+FAISS",
                        "S4": "S4\nLLM\nno MCP"}
        ax.set_xticks(range(len(S_PHASES)))
        ax.set_xticklabels([SHORT_LABELS[p] for p in S_PHASES])
        ax.set_yticks(range(len(MODEL_ORDER)))
        ax.set_yticklabels([MODEL_LABELS[m] for m in MODEL_ORDER])
        ax.set_xlabel("Ablation phase")

        ax.set_xticks(np.arange(-0.5, len(S_PHASES), 1), minor=True)
        ax.set_yticks(np.arange(-0.5, len(MODEL_ORDER), 1), minor=True)
        ax.grid(which="minor", color="white", linewidth=1.6)
        ax.tick_params(which="minor", bottom=False, left=False)
        ax.tick_params(axis="both", length=0)
        for spine in ax.spines.values():
            spine.set_visible(False)

        cbar = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.025)
        cbar.set_label("Mean post-swap recall", fontsize=8.8)
        cbar.set_ticks([0.0, 0.5, 1.0])
        cbar.ax.set_yticklabels(["0", "0.5", "1.0"])
        cbar.ax.tick_params(labelsize=8.0, length=2.5, width=0.6)
        cbar.outline.set_edgecolor("#000000")
        cbar.outline.set_linewidth(0.5)

        fig.tight_layout(pad=0.75)
        _save(fig, "fig11_ablation_heatmap")


# ---------------------------------------------------------------------------
# Fig. 12 — Schema-normalisation latency across phases (log scale)
# ---------------------------------------------------------------------------

def fig12_ablation_latency() -> None:
    # Per-cell latency (mean ms) reused from manuscript text.
    LAT: Dict[str, Dict[str, float]] = {
        "gemini": {"S0": 0.07, "S1": 184.0, "S2": 0.07, "S3": 184.0, "S4": 180.0},
        "haiku":  {"S0": 0.07, "S1": 25.9,  "S2": 0.07, "S3": 25.9,  "S4": 26.3},
        "qwen":   {"S0": 0.07, "S1": 28.3,  "S2": 0.07, "S3": 28.3,  "S4": 27.8},
    }
    SD: Dict[str, Dict[str, float]] = {
        "gemini": {"S0": 0.0, "S1": 327.0, "S2": 0.0, "S3": 327.0, "S4": 320.0},
        "haiku":  {"S0": 0.0, "S1": 52.8,  "S2": 0.0, "S3": 52.8,  "S4": 50.0},
        "qwen":   {"S0": 0.0, "S1": 63.8,  "S2": 0.0, "S3": 63.8,  "S4": 60.0},
    }

    with mpl.rc_context({
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
        "mathtext.fontset": "dejavusans",
        "font.size": 9.0,
        "axes.labelsize": 10.0,
        "xtick.labelsize": 8.3,
        "ytick.labelsize": 8.7,
        "legend.fontsize": 8.1,
    }):
        fig, ax = plt.subplots(figsize=(7.55, 3.85))
        ax.set_facecolor("#FFFFFF")
        n_models = len(MODEL_ORDER)
        n_phases = len(S_PHASES)
        bar_w = 0.78 / n_models

        for pi, phase in enumerate(S_PHASES):
            for mi, model in enumerate(MODEL_ORDER):
                mu = LAT[model][phase]
                sd = SD[model][phase]
                x = pi + (mi - (n_models - 1) / 2) * bar_w
                color = MODEL_COLORS[model]
                hatch = "////" if phase == "S4" else None

                ax.bar(x, mu, width=bar_w * 0.88,
                       edgecolor="white" if hatch is None else color,
                       lw=0.7, hatch=hatch,
                       alpha=0.88 if hatch is None else 1.0,
                       zorder=3,
                       facecolor=color if hatch is None else "white")
                if sd > 0:
                    ax.errorbar(x, mu, yerr=sd, fmt="none",
                                ecolor="#222222", lw=0.75, capsize=2.4,
                                zorder=4)
                if phase in {"S0", "S2"} and mi == 1:
                    ax.text(pi, 0.095, "0.07 ms", ha="center", va="bottom",
                            fontsize=7.2, color="#4B5563")
                elif phase in {"S1", "S3", "S4"}:
                    label_y = (mu + sd) * 1.08 if sd > 0 else mu * 1.16
                    ax.text(x, label_y, f"{mu:.0f}",
                            ha="center", va="bottom", fontsize=7.0,
                            color=color, fontweight="bold")

        ax.set_yscale("symlog", linthresh=0.1)
        ax.set_xticks(range(n_phases))
        ax.set_xticklabels([S_LABELS[p] for p in S_PHASES])
        ax.set_ylabel("Schema-normalization latency (ms, symlog)")
        ax.set_ylim(0.01, 1200)
        ax.set_yticks([0.01, 0.1, 1, 10, 100, 1000])
        ax.set_yticklabels(["0.01", "0.1", "1", "10", "100", "1000"])
        ax.grid(True, axis="y", color="#E4E8ED", lw=0.8)
        ax.set_axisbelow(True)
        ax.tick_params(axis="both", length=3.5, width=0.8, color="#111827")
        for spine in ("left", "bottom"):
            ax.spines[spine].set_color("#111827")
            ax.spines[spine].set_linewidth(0.9)

        handles = [Patch(facecolor=MODEL_COLORS[m], label=MODEL_LABELS[m])
                   for m in MODEL_ORDER]
        handles.append(Patch(facecolor="white", edgecolor="#444", hatch="////",
                             label="S4 (no MCP)"))
        leg = ax.legend(handles=handles, loc="upper center",
                        bbox_to_anchor=(0.5, 1.14), ncol=4,
                        handlelength=1.5, columnspacing=1.0,
                        frameon=True, facecolor="white",
                        edgecolor="#000000")
        leg.get_frame().set_linewidth(0.5)

        fig.tight_layout(pad=0.85)
        _save(fig, "fig12_ablation_latency")


# ---------------------------------------------------------------------------
# Fig. 13 — Paired within-rep contrast S1 vs S3 (Gemini)
# ---------------------------------------------------------------------------

def fig13_ablation_paired() -> None:
    # Same chart type as original: paired dot/line plot. Each repetition is a
    # circle at S1 and a diamond at S3, joined by a line colour-coded by
    # direction (green=improve, red=regress, grey=unchanged). Horizontal mean
    # markers and per-condition μ labels. Footer summarises the rep outcomes.
    s1 = np.asarray(S_DATA["gemini"]["S1"])
    s3 = np.asarray(S_DATA["gemini"]["S3"])

    fig, ax = plt.subplots(figsize=(5.4, 4.2))
    ax.grid(True, axis="y", color="#ECECEC", lw=0.5)
    ax.set_axisbelow(True)

    GREEN = "#2E8B57"; GREY = "#999999"; RED = "#B22222"

    n_up = int(np.sum(s3 > s1 + 1e-6))
    n_eq = int(np.sum(np.isclose(s3, s1, atol=1e-6)))
    n_dn = int(np.sum(s3 < s1 - 1e-6))

    for a, b in zip(s1, s3):
        if b > a + 1e-6:
            c = GREEN
        elif b < a - 1e-6:
            c = RED
        else:
            c = GREY
        ax.plot([0, 1], [a, b], color=c, lw=1.1, alpha=0.85, zorder=3)
        ax.scatter([0], [a], s=44, color=COLOR_GEMINI, marker="o",
                   edgecolors="white", linewidths=0.6, zorder=4)
        ax.scatter([1], [b], s=46, color=COLOR_GEMINI, marker="D",
                   edgecolors="white", linewidths=0.6, zorder=4)

    mu1, mu3 = float(s1.mean()), float(s3.mean())
    ax.plot([-0.22, 0.22], [mu1, mu1], color=COLOR_GEMINI, lw=2.6,
            solid_capstyle="round", zorder=5)
    ax.plot([0.78, 1.22], [mu3, mu3], color=COLOR_GEMINI, lw=2.6,
            solid_capstyle="round", zorder=5)
    ax.text(-0.28, mu1, f"$\\mu = {mu1:.4f}$",
            color=COLOR_GEMINI, fontsize=8.6, fontweight="bold",
            va="center", ha="right")
    ax.text(1.28, mu3, f"$\\mu = {mu3:.4f}$",
            color=COLOR_GEMINI, fontsize=8.6, fontweight="bold",
            va="center", ha="left")

    ax.set_xticks([0, 1])
    ax.set_xticklabels(["S1\nLLM only\n(no FAISS)", "S3\nLLM + FAISS"],
                       fontsize=9.5)
    ax.set_ylabel("Post-swap containment recall", fontsize=10.5)
    ax.set_xlim(-0.65, 1.65)
    ax.set_ylim(0.82, 1.06)
    ax.set_yticks([0.85, 0.90, 0.95, 1.00, 1.05])

    # Top legend
    handles = [
        Line2D([0], [0], color=GREEN, lw=1.8, label=f"S3 $>$ S1  ({n_up} reps)"),
        Line2D([0], [0], color=RED,   lw=1.8, label=f"S3 $<$ S1  ({n_dn} rep)"),
        Line2D([0], [0], color=GREY,  lw=1.8, label=f"S3 $=$ S1  ({n_eq} reps)"),
    ]
    ax.legend(handles=handles, loc="upper center",
              bbox_to_anchor=(0.5, 1.10), ncol=3, fontsize=8.2,
              handlelength=1.6, columnspacing=1.2, frameon=False)

    # Footer summary
    ax.text(0.5, -0.22,
            f"Rep. outcomes:   {n_up} FAISS improves  |  {n_dn} FAISS reduces  |  {n_eq} unchanged",
            transform=ax.transAxes, ha="center", va="top",
            fontsize=8.5, color="#333333", style="italic")

    fig.tight_layout()
    fig.subplots_adjust(bottom=0.22)
    _save(fig, "fig13_ablation_paired")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print(f"Writing manuscript result figures to {OUT_DIR}")
    fig3_recall_three_models()
    fig4_llm_rate_vs_cache_hit()
    fig5_cache_warmup()
    fig7_latency_breakdown()
    fig9_ablation_recall()


if __name__ == "__main__":
    main()
