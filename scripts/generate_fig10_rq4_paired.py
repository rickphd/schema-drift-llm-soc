#!/usr/bin/env python3
"""Generate a repetition-level paired plot for the RQ4 false-positive result."""

from __future__ import annotations

import argparse
import csv
import math
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np


NO_MEMORY_COLOR = "#D55E00"  # Okabe-Ito vermillion
WITH_MEMORY_COLOR = "#0072B2"  # Okabe-Ito blue
CONNECTOR_COLOR = "#7F8790"


@dataclass(frozen=True)
class RepetitionResult:
    repetition: int
    episodes: int
    block_ip_rate: float


def read_results(path: Path) -> list[RepetitionResult]:
    with path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))

    results = [
        RepetitionResult(
            repetition=int(row["repetition"]),
            episodes=int(row["episodes_total"]),
            block_ip_rate=float(row["block_ip_rate"]),
        )
        for row in rows
    ]
    if len(results) != 5:
        raise ValueError(f"Expected five repetitions in {path}; found {len(results)}")
    if len({result.repetition for result in results}) != len(results):
        raise ValueError(f"Duplicate repetition identifiers in {path}")
    if any(result.episodes != 20 for result in results):
        raise ValueError(f"Expected 20 episodes per repetition in {path}")
    if any(not 0.0 <= result.block_ip_rate <= 1.0 for result in results):
        raise ValueError(f"Invalid block_ip rate in {path}")
    return sorted(results, key=lambda result: result.repetition)


def exact_two_sided_sign_test(differences: np.ndarray) -> float:
    nonzero = differences[~np.isclose(differences, 0.0)]
    positives = int(np.sum(nonzero > 0.0))
    negatives = int(np.sum(nonzero < 0.0))
    n = positives + negatives
    if n == 0:
        return 1.0
    tail = min(positives, negatives)
    probability = 2.0 * sum(math.comb(n, k) for k in range(tail + 1)) / (2**n)
    return min(1.0, probability)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-memory", required=True, type=Path)
    parser.add_argument("--with-memory", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    no_memory = read_results(args.no_memory)
    with_memory = read_results(args.with_memory)
    if [result.repetition for result in no_memory] != [result.repetition for result in with_memory]:
        raise ValueError("Paired conditions have different repetition identifiers")

    repetitions = np.array([result.repetition for result in no_memory], dtype=float)
    no_memory_rates = np.array([result.block_ip_rate for result in no_memory], dtype=float)
    with_memory_rates = np.array([result.block_ip_rate for result in with_memory], dtype=float)
    p_value = exact_two_sided_sign_test(no_memory_rates - with_memory_rates)

    fig, ax = plt.subplots(figsize=(4.25, 2.95))
    ax.set_axisbelow(True)
    ax.grid(axis="y", color="#D9E0E7", linewidth=0.65)

    for repetition, no_memory_rate, with_memory_rate in zip(
        repetitions, no_memory_rates, with_memory_rates
    ):
        ax.plot(
            [repetition, repetition],
            [with_memory_rate, no_memory_rate],
            color=CONNECTOR_COLOR,
            linewidth=1.0,
            zorder=2,
        )

    ax.scatter(
        repetitions,
        no_memory_rates,
        marker="s",
        s=48,
        facecolor=NO_MEMORY_COLOR,
        edgecolor="#7A3500",
        linewidth=0.8,
        zorder=4,
    )
    ax.scatter(
        repetitions,
        with_memory_rates,
        marker="D",
        s=48,
        facecolor=WITH_MEMORY_COLOR,
        edgecolor="#004B75",
        linewidth=0.9,
        zorder=4,
    )

    ax.set_xlim(0.55, 5.45)
    ax.set_ylim(-0.10, 1.10)
    ax.set_xticks(repetitions)
    ax.set_xticklabels([str(int(value)) for value in repetitions], fontsize=10)
    ax.set_yticks([0.0, 0.5, 1.0])
    ax.set_yticklabels(["0.0", "0.5", "1.0"], fontsize=10)
    ax.set_xlabel("Repetition pair", fontsize=9)
    ax.set_ylabel("False-positive $\\mathtt{block\\_ip}$ rate", fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    legend_handles = [
        Line2D(
            [0],
            [0],
            marker="s",
            linestyle="None",
            markerfacecolor=NO_MEMORY_COLOR,
            markeredgecolor="#7A3500",
            markersize=6.5,
            label="No memory (20/20)",
        ),
        Line2D(
            [0],
            [0],
            marker="D",
            linestyle="None",
            markerfacecolor=WITH_MEMORY_COLOR,
            markeredgecolor="#004B75",
            markersize=6.5,
            label="With memory (0/20)",
        ),
    ]
    ax.legend(
        handles=legend_handles,
        loc="lower center",
        bbox_to_anchor=(0.5, 1.12),
        ncol=2,
        frameon=False,
        fontsize=9.5,
        handletextpad=0.45,
        columnspacing=1.5,
    )
    ax.text(
        1.0,
        1.035,
        f"$n=5$ pairs; exact sign test: $p={p_value:.4f}$",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=8.8,
        color="#333333",
    )

    fig.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
