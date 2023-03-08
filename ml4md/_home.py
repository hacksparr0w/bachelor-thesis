import json

from dataclasses import dataclass
from pathlib import Path


HOME_DIR = Path(__file__).parent
MODEL_DIR = HOME_DIR / "model"
DATASET_DIR = HOME_DIR / "dataset"


@dataclass
class Model:
    slug: str
    root_dir: Path
    model_file: Path
    evaluation_file: Path
    l_curve_file: Path

    config: dict


def list_models() -> list[Model]:
    root_dirs = [p for p in MODEL_DIR.iterdir() if p.is_dir()]
    models = []

    for root_dir in root_dirs:
        slug = root_dir.stem
        model_file = root_dir / "frozen_model.pb"
        config_file = root_dir / "input.json"
        evaluation_file = root_dir / "evaluation.csv"
        l_curve_file = root_dir / "l_curve.csv"

        with config_file.open(encoding="utf-8") as stream:
            config = json.load(stream)
            model = Model(
                slug,
                root_dir,
                model_file,
                evaluation_file,
                l_curve_file,
                config
            )

            models.append(model)

    return models


def find_model(slug: str) -> Model:
    for model in list_models():
        if model.slug == slug:
            return model

    raise ValueError
