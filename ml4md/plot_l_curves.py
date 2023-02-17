import numpy as np
import plotly.express as px
import plotly.graph_objects as go


FILE_NAMES = ["l_curve_00.csv", "l_curve_01.csv", "l_curve_02.csv"]


def main():
    fig = go.Figure()

    for file_name in FILE_NAMES:
        data = np.genfromtxt(file_name)
        x, y = data[:,0], data[:,3]
        
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                name=file_name,
                line=dict(width=1.5)
            )
        )

    fig.update_layout(
        font_color="#000",
        plot_bgcolor="#fff",
        xaxis=dict(
            showgrid=False,
            linewidth=1,
            linecolor="black",
            mirror=True,
            ticks="outside",
            showline=True
        ),
        yaxis=dict(
            showgrid=False,
            linewidth=1,
            linecolor="black",
            mirror=True,
            ticks="outside",
            showline=True
        ),
        xaxis_title="Step",
        yaxis_title="ΔE [eV/atom]",
        legend=dict(
            x=.05,
            y=.05,
            traceorder="normal",
            bordercolor="#000",
            borderwidth=1
        )
    )

    fig.update_yaxes(type="log")

    fig.write_image("l_curves.jpeg", scale=8)


if __name__ == "__main__":
    main()
