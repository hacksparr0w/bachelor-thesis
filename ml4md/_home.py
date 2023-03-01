import json

from dataclasses import dataclass
from pathlib import Path


HOME_DIR = Path(__file__).parent
MODEL_DIR = HOME_DIR / "model"
DATASET_DIR = HOME_DIR / "dataset"


@dataclass
class Model:
    root_dir: Path
    model_file: Path
    evaluation_file: Path

    config: dict


def list_models() -> list[Model]:
    root_dirs = [p for p in MODEL_DIR.iterdir() if p.is_dir()]
    models = []

    for root_dir in root_dirs:
        model_file = root_dir / "frozen_model.pb"
        config_file = root_dir / "input.json"
        evaluation_file = root_dir / "evaluation.csv"

        with config_file.open(encoding="utf-8") as stream:
            config = json.load(stream)
            model = Model(root_dir, model_file, config)

            models.append(model)

    return models
