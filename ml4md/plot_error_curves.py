import sys

from pathlib import Path

import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from plotly.subplots import make_subplots

import _home

from generate_models import (
    DATASET_DIRS,
    DEFAULT_DESCRIPTOR_NEURONS,
    DEFAULT_FITTING_NEURONS,
    DEFAULT_SEED,
    DESCRIPTOR_NEURONS,
    FITTING_NEURONS,
    generate_model_slug
)


def main():
    args = sys.argv[1:]

    if len(args) != 1:
        raise ValueError

    output_dir = Path(args[0]).resolve()

    descriptor_data = {}

    for descriptor_neurons in DESCRIPTOR_NEURONS:
        fitting_neurons = DEFAULT_FITTING_NEURONS

        for dataset_dir in DATASET_DIRS:
            slug = generate_model_slug(
                descriptor_neurons,
                fitting_neurons,
                DEFAULT_SEED,
                dataset_dir
            )

            if descriptor_data.get(dataset_dir.stem) is None:
                descriptor_data[dataset_dir.stem] = []

            data = np.genfromtxt(
                _home.find_model(slug).evaluation_file
            ).tolist()

            x = ",".join([str(d) for d in descriptor_neurons])
            descriptor_data[dataset_dir.stem].append([x, *data])

    descriptor_energy_figure = go.Figure()
    descriptor_force_figure = go.Figure()
    colors = iter(px.colors.qualitative.Plotly)

    for name, v in descriptor_data.items():
        color = next(colors)
        data = np.array(v)

        x = data[:,0]
        training_energy_rmse = data[:,1].astype(float) * 1e3
        training_force_rmse = data[:,2].astype(float)
        validation_energy_rmse = data[:,3].astype(float) * 1e3
        validation_force_rmse = data[:,4].astype(float)

        descriptor_energy_figure.add_trace(
            go.Scatter(
                x=x,
                y=validation_energy_rmse,
                line=dict(width=1.5, color=color),
                name=f"{name}, validation"
            )
        )

        descriptor_energy_figure.add_trace(
            go.Scatter(
                x=x,
                y=training_energy_rmse,
                line=dict(width=1.5, dash="dash", color=color),
                name=f"{name}, training",
            )
        )

        descriptor_force_figure.add_trace(
            go.Scatter(
                x=x,
                y=validation_force_rmse,
                line=dict(width=1.5, color=color),
                name=f"{name}, validation"
            )
        )

        descriptor_force_figure.add_trace(
            go.Scatter(
                x=x,
                y=training_force_rmse,
                line=dict(width=1.5, dash="dash", color=color),
                name=f"{name}, training"
            )
        )

        descriptor_energy_figure.update_layout(
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
                title="$\large{E_\\text{RMSE} \, [\mathrm{meV}/\mathrm{atom}]}$",
                showgrid=False,
                linewidth=1,
                linecolor="black",
                mirror="allticks",
                ticks="inside",
                showline=True
            ),
            xaxis_title="$\large{\\text{Parameters}}$",
            legend=dict(
                x=.05,
                y=.2,
                traceorder="normal",
                bordercolor="#000",
                borderwidth=1
            ),
            margin=dict(l=1, r=1, b=1, t=1)
        )

        descriptor_force_figure.update_layout(
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
                title="$\large{F_\\text{RMSE} \, [\mathrm{eV}/\mathrm{Å}]}$",
                showgrid=False,
                linewidth=1,
                linecolor="black",
                mirror="allticks",
                ticks="inside",
                showline=True
            ),
            xaxis_title="$\large{\\text{Parameters}}$",
            legend=dict(
                x=.6,
                y=.5,
                traceorder="normal",
                bordercolor="#000",
                borderwidth=1
            ),
            margin=dict(l=1, r=1, b=1, t=1)
        )

        descriptor_energy_figure.write_image(
            output_dir / "descriptor_energy_error_evaluation.jpg",
            scale=8
        )

        descriptor_force_figure.write_image(
            output_dir / "descriptor_force_error_evaluation.jpg",
            scale=8   
        )

    fitting_data = {}

    for fitting_neurons in FITTING_NEURONS:
        descriptor_neurons = DEFAULT_DESCRIPTOR_NEURONS

        for dataset_dir in DATASET_DIRS:
            slug = generate_model_slug(
                descriptor_neurons,
                fitting_neurons,
                DEFAULT_SEED,
                dataset_dir
            )

            if fitting_data.get(dataset_dir.stem) is None:
                fitting_data[dataset_dir.stem] = []

            data = np.genfromtxt(
                _home.find_model(slug).evaluation_file
            ).tolist()

            x = ",".join([str(d) for d in fitting_neurons])
            fitting_data[dataset_dir.stem].append([x, *data])

    fitting_energy_figure = go.Figure()
    fitting_force_figure = go.Figure()
    colors = iter(px.colors.qualitative.Plotly)

    for name, v in fitting_data.items():
        color = next(colors)
        data = np.array(v)

        x = data[:,0]
        training_energy_rmse = data[:,1].astype(float) * 1e3
        training_force_rmse = data[:,2].astype(float)
        validation_energy_rmse = data[:,3].astype(float) * 1e3
        validation_force_rmse = data[:,4].astype(float)

        fitting_energy_figure.add_trace(
            go.Scatter(
                x=x,
                y=validation_energy_rmse,
                line=dict(width=1.5, color=color),
                name=f"{name}, validation"
            )
        )

        fitting_energy_figure.add_trace(
            go.Scatter(
                x=x,
                y=training_energy_rmse,
                line=dict(width=1.5, dash="dash", color=color),
                name=f"{name}, training",
            )
        )

        fitting_force_figure.add_trace(
            go.Scatter(
                x=x,
                y=validation_force_rmse,
                line=dict(width=1.5, color=color),
                name=f"{name}, validation"
            )
        )

        fitting_force_figure.add_trace(
            go.Scatter(
                x=x,
                y=training_force_rmse,
                line=dict(width=1.5, dash="dash", color=color),
                name=f"{name}, training"
            )
        )

        fitting_energy_figure.update_layout(
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
                title="$\large{E_\\text{RMSE} \, [\mathrm{meV}/\mathrm{atom}]}$",
                showgrid=False,
                linewidth=1,
                linecolor="black",
                mirror="allticks",
                ticks="inside",
                showline=True
            ),
            xaxis_title="$\large{\\text{Parameters}}$",
            legend=dict(
                x=.02,
                y=.98,
                traceorder="normal",
                bordercolor="#000",
                borderwidth=1
            ),
            margin=dict(l=1, r=1, b=1, t=1)
        )

        fitting_force_figure.update_layout(
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
                title="$\large{F_\\text{RMSE} \, [\mathrm{eV}/\mathrm{Å}]}$",
                showgrid=False,
                linewidth=1,
                linecolor="black",
                mirror="allticks",
                ticks="inside",
                showline=True
            ),
            xaxis_title="$\large{\\text{Parameters}}$",
            legend=dict(
                x=.65,
                y=.5,
                traceorder="normal",
                bordercolor="#000",
                borderwidth=1
            ),
            margin=dict(l=1, r=1, b=1, t=1)
        )

        fitting_energy_figure.write_image(
            output_dir / "fitting_energy_error_evaluation.jpg",
            scale=8
        )

        fitting_force_figure.write_image(
            output_dir / "fitting_force_error_evaluation.jpg",
            scale=8
        )


if __name__ == "__main__":
    main()
