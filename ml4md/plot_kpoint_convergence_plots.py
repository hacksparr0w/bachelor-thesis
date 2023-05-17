import sys

from enum import Enum
from pathlib import Path

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots

import _home


def main():
    args = sys.argv[1:]

    if len(args) != 1:
        raise ValueError

    output_dir = Path(args[0]).resolve()

    energy_data = np.genfromtxt(
        output_dir / "energy_kpoint_convergence.csv",
        delimiter=" ",
        skip_header=1
    )

    force_data = np.genfromtxt(
        output_dir / "force_kpoint_convergence.csv",
        delimiter=" ",
        skip_header=1
    )

    output_file = (
        output_dir / f"kpoint_convergence.jpg"
    )

    plot(energy_data, force_data, output_file)


def plot(energy_data, force_data, output_file):
    x = energy_data[:,0]

    fig = plotly.subplots.make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1
    )

    fig.add_trace(
        go.Scatter(
            x=x,
            y=energy_data[:,1],
            line=dict(width=1.5),
            showlegend=False
        ),
        row=1,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=x,
            y=force_data[:,1],
            line=dict(width=1.5),
            showlegend=False
        ),
        row=2,
        col=1
    )

    fig.update_xaxes(
        showgrid=False,
        linewidth=1,
        linecolor="black",
        mirror="allticks",
        ticks="inside",
        showline=True
    )

    fig.update_xaxes(
        title_text="$\large{\\text{Number of K-Points}}$",
        col=1,
        row=2
    )

    fig.update_yaxes(
        title_text="$\large{\\text{Total Energy} \, [\mathrm{eV}]}$",
        tickformat=".5f",
        showgrid=False,
        linewidth=1,
        linecolor="black",
        mirror="allticks",
        ticks="inside",
        showline=True,
        row=1,
        col=1
    )

    fig.update_yaxes(
        title_text="$\large{\\text{Average force} \, [\mathrm{ev}/\mathrm{Å}]}$",
        showgrid=False,
        linewidth=1,
        linecolor="black",
        mirror="allticks",
        ticks="inside",
        showline=True,
        row=2,
        col=1
    )

    fig.update_layout(
        font_color="#000",
        font_size=18,
        plot_bgcolor="#fff",
        margin=dict(l=1, r=1, b=1, t=1)
    )

    fig.write_image(output_file, scale=8)


if __name__ == "__main__":
    main()
