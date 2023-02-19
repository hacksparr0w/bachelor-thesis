import copy
import json

from pathlib import Path

from _home import DATASET_DIR, MODEL_DIR
from _utility import flatten, unique


MODEL_INPUT_TEMPLATE = {
    "model": {
        "type_map": ["Si"],
        "descriptor": {
            "type": "se_e2_a",
            "sel": [70],
            "rcut_smth": 1.8,
            "rcut": 6.0,
            "neuron": None,
            "resnet_dt": False,
            "seed": None
        },
        "fitting_net": {
            "neuron": None,
            "resnet_dt": True,
            "seed": None
        }
    },
    "learning_rate": {
        "type": "exp",
        "decay_steps": 20000,
        "start_lr": 0.001,
        "stop_lr": 1e-8
    },
    "loss": {
        "type": "ener",
        "start_pref_e": 1,
        "limit_pref_e": 500,
        "start_pref_f": 1000,
        "limit_pref_f": 10,
        "start_pref_v": 0,
        "limit_pref_v": 0
    },
    "training": {
        "training_data": {
            "systems": None,
            "batch_size": "auto"
        },
        "validation_data": {
            "systems": None,
            "batch_size": "auto",
            "numb_btch": 1
        },
        "numb_steps": int(2e6),
        "seed": 10,
        "disp_file": "l_curve.csv",
        "disp_freq": 1000,
        "save_freq": 1000
    }
}

DATASET_DIRS = (
    DATASET_DIR / "crystalline",
    DATASET_DIR / "amorphous",
    DATASET_DIR / "combined"
)

DESCRIPTOR_NEURONS = (
    (5, 10, 20),
    (10, 20, 40),
    (25, 50, 100)
)

FITTING_NEURONS = (
    (10, 10, 10),
    (20, 20, 20),
    (50, 50, 50),
    (75, 75, 75)
)

DEFAULT_DESCRIPTOR_NEURONS = DESCRIPTOR_NEURONS[1]
DEFAULT_FITTING_NEURONS = FITTING_NEURONS[1]
DEFAULT_SEED = 260222622

INPUT_MATRIX = unique(
        flatten([
            [
                (
                    descriptor_neurons,
                    DEFAULT_FITTING_NEURONS,
                    DEFAULT_SEED,
                    dataset_dir
                )
                for dataset_dir in DATASET_DIRS
                for descriptor_neurons in DESCRIPTOR_NEURONS
            ],
            [
                (
                    DEFAULT_DESCRIPTOR_NEURONS,
                    fitting_neurons,
                    DEFAULT_SEED,
                    dataset_dir
                )
                for dataset_dir in DATASET_DIRS
                for fitting_neurons in FITTING_NEURONS
            ]
    ])
)


def generate_model_input(
        descriptor_neurons,
        fitting_neurons,
        seed,
        training_dataset_dirs,
        validation_dataset_dirs
):
    input = copy.deepcopy(MODEL_INPUT_TEMPLATE)

    input["model"]["descriptor"]["neuron"] = descriptor_neurons
    input["model"]["descriptor"]["seed"] = seed

    input["model"]["fitting_net"]["neuron"] = fitting_neurons
    input["model"]["fitting_net"]["seed"] = seed

    input["training"]["training_data"]["systems"] = list(
        map(str, training_dataset_dirs)
    )

    input["training"]["validation_data"]["systems"] = list(
        map(str, validation_dataset_dirs)
    )

    return input


def generate_model_slug(
        descriptor_neurons,
        fitting_neurons,
        seed,
        dataset_dir
):
    p = dataset_dir.stem
    d = ",".join(map(str, descriptor_neurons))
    f = ",".join(map(str, fitting_neurons))
    s = str(seed)

    return f"{p}_{d}d_{f}f_{s}s"


def generate_model(
        descriptor_neurons,
        fitting_neurons,
        seed,
        dataset_dir
):
    slug = generate_model_slug(
        descriptor_neurons,
        fitting_neurons,
        seed,
        dataset_dir
    )

    root_dir = MODEL_DIR / slug
    root_dir.mkdir(exist_ok=False)

    input_file = root_dir / "input.json"
    training_dataset_dirs = map(
        lambda d: Path("../..") / d.relative_to(root_dir.parent.parent),
        (dataset_dir / "training").iterdir()
    )

    validation_dataset_dirs = map(
        lambda d: Path("../..") / d.relative_to(root_dir.parent.parent),
        (dataset_dir / "validation").iterdir()
    )

    input = generate_model_input(
        descriptor_neurons,
        fitting_neurons,
        seed,
        training_dataset_dirs,
        validation_dataset_dirs
    )

    with input_file.open("w", encoding="utf-8") as stream:
        json.dump(input, stream, indent=2)


def main():
    MODEL_DIR.mkdir(exist_ok=False)

    for entry in INPUT_MATRIX:
        generate_model(*entry)


if __name__ == "__main__":
    main()
