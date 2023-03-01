import re
import subprocess

from pathlib import Path

import numpy as np

from _home import Model, list_models


ENERGY_RMSE_PATTERN = re.compile(r"Energy RMSE/Natoms : (.+?) eV")
FORCE_RMSE_PATTERN = re.compile(r"Force  RMSE        : (.+?) eV/A")


def dp_test(m: Path, s: Path, n: int = 100):
    result = subprocess.run(
        ["dp", "test", "-m", str(m), "-s", str(s), "-n", str(n)],
        capture_output=True
    )

    output = result.stderr.decode("utf-8")

    match = ENERGY_RMSE_PATTERN.search(output)

    if not match:
        raise RuntimeError
    
    energy_rmse = float(match.group(1))

    match = FORCE_RMSE_PATTERN.search(output)

    if not match:
        raise RuntimeError

    force_rmse = float(match.group(1))

    return (energy_rmse, force_rmse)


def evaluate_model(model: Model):
    training_config = model.config["training"]

    training_system_dir = (
        model.root_dir / training_config["training_data"]["systems"][0]
    )

    validation_system_dir = (
        model.root_dir / training_config["validation_data"]["systems"][0]
    )

    training_evaluation = dp_test(model.model_file, training_system_dir)
    validation_evaluation = dp_test(model.model_file, validation_system_dir)

    data = np.array([*training_evaluation, *validation_evaluation])

    return data


def main():
    for model in list_models():
        data = evaluate_model(model)
        np.savetxt(str(model.evaluation_file), data)


if __name__ == "__main__":
    main()
