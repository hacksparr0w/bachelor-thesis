import sys

from enum import Enum
from pathlib import Path

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots

from scipy.signal import savgol_filter

import _home


class LCurveVariant(Enum):
    ENERGY = "ENERGY"
    FORCE = "FORCE"


def main():
    args = sys.argv[1:]

    if len(args) != 1:
        raise ValueError

    output_dir = Path(args[0]).resolve()

    for model in _home.list_models():
        data = np.genfromtxt(model.l_curve_file)

        energy_l_curve_output_file = (
            output_dir / f"{model.slug}_energy_l_curve.jpg"
        )

        force_l_curve_output_file = (
            output_dir / f"{model.slug}_force_l_curve.jpg"
        )

        plot_l_cuve(data, LCurveVariant.ENERGY, energy_l_curve_output_file)
        plot_l_cuve(data, LCurveVariant.FORCE, force_l_curve_output_file)


def plot_l_cuve(data, variant, output_file, savgol_window=40, subplots=False):
    if variant == LCurveVariant.ENERGY:
        x, y_1, y_2 = data[:,0], data[:,3] * 1e3, data[:,4] * 1e3
        training_color = px.colors.qualitative.Plotly[0]
        validation_color = px.colors.qualitative.Plotly[1]
        y_title_text = "Energy RMSE [meV/atom]"
    elif variant == LCurveVariant.FORCE:
        x, y_1, y_2 = data[:,0], data[:,5], data[:,6]
        training_color = px.colors.qualitative.Plotly[2]
        validation_color = px.colors.qualitative.Plotly[3]
        y_title_text = "Force RMSE [eV/Å]"

    y_1 = savgol_filter(y_1, savgol_window, 5)
    y_2 = savgol_filter(y_2, savgol_window, 5)

    if subplots:
        fig = plotly.subplots.make_subplots(
            rows=2,
            cols=1,
            shared_xaxes=True,
            subplot_titles=("Training", "Validation")
        )
    else:
        fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y_2,
            line=dict(width=1.5, color=training_color),
            name="Training",
            showlegend=not subplots
        ),
        row=1 if subplots else None,
        col=1 if subplots else None
    )

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y_1,
            line=dict(width=1.5, color=validation_color),
            name="Validation",
            showlegend=not subplots
        ),
        row=2 if subplots else None,
        col=1 if subplots else None
    )

    fig.update_xaxes(
        showgrid=False,
        linewidth=1,
        linecolor="black",
        mirror=True,
        ticks="outside",
        showline=True,
        exponentformat="e"
    )

    fig.update_xaxes(
        title_text="Step",
        col=1 if subplots else None,
        row=2 if subplots else None
    )

    fig.update_yaxes(
        type="log",
        title_text=y_title_text,
        showgrid=False,
        linewidth=1,
        linecolor="black",
        mirror=True,
        ticks="outside",
        showline=True,
        row=1 if subplots else None,
        col=1 if subplots else None
    )

    if subplots:
        fig.update_yaxes(
            type="log",
            title_text=y_title_text,
            showgrid=False,
            linewidth=1,
            linecolor="black",
            mirror=True,
            ticks="outside",
            showline=True,
            row=2,
            col=1
        )

    fig.update_layout(
        font_color="#000",
        plot_bgcolor="#fff",
        legend=dict(
            x=.79,
            y=.98,
            traceorder="normal",
            bordercolor="#000",
            borderwidth=1
        )
    )

    fig.write_image(output_file, scale=8)


if __name__ == "__main__":
    main()
