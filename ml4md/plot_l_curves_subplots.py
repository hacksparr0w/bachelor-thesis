import sys

from enum import Enum
from pathlib import Path

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots

from scipy.signal import savgol_filter

import _home


def main():
    args = sys.argv[1:]

    if len(args) != 1:
        raise ValueError

    output_dir = Path(args[0]).resolve()

    for model in _home.list_models():
        if not model.l_curve_file.exists():
            continue

        data = np.genfromtxt(model.l_curve_file)

        output_file = (
            output_dir / f"{model.slug}_energy_force_l_curve.jpg"
        )

        plot_l_cuves(data, output_file)


def plot_l_cuves(data, output_file, savgol_window=40):
    x = data[:,0]

    subplots = {
        "energy": {
            
            "y_1": savgol_filter(data[:,3] * 1e3, savgol_window, 5),
            "y_2": savgol_filter(data[:,4] * 1e3, savgol_window, 5),
            "training_color": px.colors.qualitative.Plotly[0],
            "validation_color": px.colors.qualitative.Plotly[1],
            "y_title_text": "Energy RMSE [meV/atom]"
        },
        "force": {
            "x": data[:,0],
            "y_1": savgol_filter(data[:,5], savgol_window, 5),
            "y_2": savgol_filter(data[:,6], savgol_window, 5),
            "training_color": px.colors.qualitative.Plotly[2],
            "validation_color": px.colors.qualitative.Plotly[3],
            "y_title_text": "Force RMSE [eV/Å]"
        }
    }

    fig = plotly.subplots.make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1
    )

    fig.add_trace(
        go.Scatter(
            x=x,
            y=subplots["energy"]["y_2"],
            line=dict(width=1.5, color=subplots["energy"]["training_color"]),
            name="Energy Training"
        ),
        row=1,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=x,
            y=subplots["energy"]["y_1"],
            line=dict(width=1.5, color=subplots["energy"]["validation_color"]),
            name="Energy Validation"
        ),
        row=1,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=x,
            y=subplots["force"]["y_2"],
            line=dict(width=1.5, color=subplots["force"]["training_color"]),
            name="Force Training"
        ),
        row=2,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=x,
            y=subplots["force"]["y_1"],
            line=dict(width=1.5, color=subplots["force"]["validation_color"]),
            name="Force Validation"
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
        showline=True,
        exponentformat="e"
    )

    fig.update_xaxes(
        title_text="Step",
        col=1,
        row=2
    )

    fig.update_yaxes(
        type="log",
        title_text=subplots["energy"]["y_title_text"],
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
        type="log",
        title_text=subplots["force"]["y_title_text"],
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
        legend=dict(
            x=.015,
            y=.165,
            traceorder="normal",
            bordercolor="#000",
            borderwidth=1,
        ),
        margin=dict(l=1, r=1, b=1, t=1)
    )

    fig.write_image(output_file, scale=8)


if __name__ == "__main__":
    main()
