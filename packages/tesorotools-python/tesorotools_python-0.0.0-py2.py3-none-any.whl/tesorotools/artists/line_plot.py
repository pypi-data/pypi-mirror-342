import locale
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter

locale.setlocale(locale.LC_ALL, "")

from tesorotools.utils.globals import DEBUG
from tesorotools.utils.matplotlib import (
    PLOT_CONFIG,
    format_annotation,
    load_fonts,
)

load_fonts()

LINE_PLOT_CONFIG: dict[str, Any] = PLOT_CONFIG["line"]
AX_CONFIG: dict[str, Any] = PLOT_CONFIG["ax"]
FIG_CONFIG: dict[str, Any] = PLOT_CONFIG["figure"]


def _style_spines(
    ax: plt.Axes,
    decimals: int,
    units: str,
    *,
    color: str,
    linewidth: str,
):
    ax.grid(visible=True, axis="y")
    for spine in ax.spines.values():
        spine.set_color(color)
        spine.set_linewidth(linewidth)
    ax.yaxis.tick_right()
    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda y, _: format_annotation(y, decimals, units))
    )
    ax.set_xlabel("")

    ax.tick_params(which="minor", size=0, width=0)
    ax.tick_params(axis="both", which="major")
    for tick in ax.get_xticklines():
        tick.set_markeredgecolor(color)
    for tick in ax.get_yticklines():
        tick.set_markeredgecolor(color)


def _style_baseline(ax: plt.Axes, reference: float = 0, **baseline_config):
    color: str = baseline_config["color"]
    bottom_lim, top_lim = ax.get_ylim()
    ax.set_ylim(bottom=min(reference, bottom_lim), top=max(reference, top_lim))
    bottom_lim, top_lim = ax.get_ylim()
    if bottom_lim == reference:
        ax.spines["bottom"].set_edgecolor(color)
    elif top_lim == reference:
        ax.spines["top"].set_edgecolor(color)
    else:
        ax.axhline(y=reference, **baseline_config)


def plot_line_chart(
    out_name: Path,
    data: pd.DataFrame,
    *,
    base_100: bool,
    annotate: bool,
    format: dict[str, Any],
    **kwargs,
):
    if base_100:
        data = data / data.iloc[0, :] * 100
    if format["units"] == "p.b.":
        data = data * 100
    fig = plt.figure(**FIG_CONFIG)
    ax = fig.add_subplot()
    data.plot(ax=ax)
    if annotate:
        pass

    reference = 100 if base_100 else 0
    _style_spines(ax, **format, **AX_CONFIG["spines"])
    _style_baseline(ax, reference, **AX_CONFIG["baseline"])
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, LINE_PLOT_CONFIG["legend_sep"]),
        ncol=(
            kwargs["legend"]["ncol"]
            if kwargs is not None and kwargs.get("legend", None) is not None
            else LINE_PLOT_CONFIG["ncol"]
        ),
    )

    fig.savefig(out_name)


def plot_line_charts(data: pd.DataFrame, config_dicts: dict[str, Any]):
    for name, config in config_dicts.items():
        start_date: pd.Timestamp = pd.to_datetime(config["start_date"])
        end_date_str: str | None = config["end_date"]
        end_date: pd.Timestamp = (
            data.index.max()
            if end_date_str is None
            else pd.to_datetime(end_date_str)
        )
        series: dict[str, str] = config["series"]
        trimmed_data: pd.DataFrame = data.loc[
            slice(start_date, end_date), series.keys()
        ]
        trimmed_data = trimmed_data.rename(columns=series)
        out_name: Path = DEBUG / "line" / f"{name}.png"
        plot_line_chart(out_name, trimmed_data, **config)
