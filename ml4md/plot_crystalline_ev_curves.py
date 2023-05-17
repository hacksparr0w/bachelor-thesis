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


def shift_ev_curve(ev_curve):
    values = np.array(ev_curve.values)
    values[:,1] -= np.min(values[:,1])
    values[:,1] *= 1e3
    params = {
        **ev_curve.eos_fit.params,
        "E0": 0
    }

    if "B0" in ev_curve.eos_fit.params:
        params["B0"] = ev_curve.eos_fit.params["B0"] * 1e3

    if "B" in ev_curve.eos_fit.params:
        params["B"] = ev_curve.eos_fit.params["B"] * 1e3

    eos_fit = replace(ev_curve.eos_fit, params=params)
    shifted = replace(ev_curve, values=values.tolist(), eos_fit=eos_fit)

    return shifted


def main():
    data = from_dict(
        data_class=InputData,
        data=json.load(sys.stdin),
        config=Config(type_hooks={Eos: Eos.from_id}, cast=[tuple])
    )

    ev_curves = data.ev_curves

    if len(ev_curves) > 1:
        ev_curves = list(map(shift_ev_curve, ev_curves))

    colors = iter(px.colors.qualitative.Plotly)
    figure = go.Figure()

    for ev_curve in ev_curves:
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
                name=f"{eos_fit.eos.title()} fit"
            )
        )

    figure.update_layout(
        title=data.title,
        font_color="#000",
        font_size=18,
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
            x=.60,
            y=.96,
            traceorder="normal",
            bordercolor="#000",
            borderwidth=1
        ),
        xaxis_title=r"$\large{V \, [\mathrm{Å}^3]}$",
        yaxis_title=r"$\large{E \, [\mathrm{meV}/\mathrm{atom}]}$",
        margin=dict(l=1, r=1, b=1, t=1)
    )

    figure.write_image(sys.stdout.buffer, format="jpg")


if __name__ == "__main__":
    main()
