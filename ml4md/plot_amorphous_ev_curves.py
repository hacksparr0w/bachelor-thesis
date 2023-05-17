import json
import sys

from dataclasses import dataclass, replace
from typing import Optional

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

from dacite import Config, from_dict

from eos import Eos
from ev_curve import EvCurve


pio.templates.default = "plotly_white"


@dataclass
class InputData:
    title: Optional[str]
    ev_curves: list[EvCurve]


def main():
    data = from_dict(
        data_class=InputData,
        data=json.load(sys.stdin),
        config=Config(type_hooks={Eos: Eos.from_id}, cast=[tuple])
    )

    ev_curves = data.ev_curves

    colors = iter(px.colors.qualitative.Plotly)
    figure = go.Figure()

    for ev_curve in ev_curves:
        if ev_curve.hidden:
            continue

        color = next(colors)
        values = np.array(ev_curve.values)
        eos_fit = ev_curve.eos_fit
        v, e = values[:,0], values[:,1]
        v_p = np.linspace(np.min(v), np.max(v), 100)
        e_p = eos_fit.f(v_p)

        figure.add_trace(
            go.Scatter(
                x=v,
                y=e,
                mode="markers",
                marker_color=color,
                name=ev_curve.label
            )
        )

        figure.add_trace(
            go.Scatter(
                x=v_p,
                y=e_p,
                line=dict(width=1.5, color=color),
                showlegend=False
            )
        )

    figure.update_layout(
        title=data.title,
        font_size=19,
        font_color="#000",
        plot_bgcolor="#fff",
        xaxis=dict(
            showgrid=False,
            linewidth=1,
            linecolor="black",
            mirror="allticks",
            ticks="inside",
            showline=True
        ),
        yaxis=dict(
            showgrid=False,
            linewidth=1,
            linecolor="black",
            mirror="allticks",
            ticks="inside",
            showline=True,
            zeroline=False
        ),
        legend=dict(
            x=.70,
            y=.98,
            traceorder="normal",
            bordercolor="#000",
            borderwidth=1
        ),
        xaxis_title=r"$\large{V \, [\mathrm{Å}^3/\mathrm{atom}]}$",
        yaxis_title=r"$\large{E \, [\mathrm{eV}/\mathrm{atom}]}$",
        margin=dict(l=1, r=1, b=1, t=1)
    )

    figure.write_image(sys.stdout.buffer, format="jpg")


if __name__ == "__main__":
    main()
