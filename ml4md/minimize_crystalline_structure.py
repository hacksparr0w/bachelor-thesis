import json
import os
import re
import subprocess
import sys

from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

from dacite import from_dict

import _home


LMP_EXECUTABLE = "lmp"
LMP_SCRIPT_FILE = Path(__file__).parent / "minimize.lmp"
COHESIVE_ENERGY_PATTERN = re.compile(
    r"Cohesive energy \(eV\) = ([+-]?([0-9]*[.])?[0-9]+)"
)

FINAL_VOLUME_PATTERN = re.compile(
    r"Final volume \(angstrom\^3\) = ([+-]?([0-9]*[.])?[0-9]+)"
)


@dataclass
class InputData:
    model: str
    a_initial: float


@dataclass
class OutputData:
    values: list[tuple[float, float]]


def run(command, env=None):
    return subprocess.run(command, capture_output=True, env=env)


def main():
    data = from_dict(data_class=InputData, data=json.load(sys.stdin))

    a_initial = data.a_initial
    model_file = _home.find_model(data.model).model_file
    values = []

    print("asdf")

    for volume_scale in np.linspace(0.94, 1.06, 20):
        a_final = round(a_initial * volume_scale ** (1 / 3), 3)

        env = {
            **os.environ,
            "MD_A_INITIAL": str(a_initial),
            "MD_A_FINAL": str(a_final),
            "MD_DEEPMD_MODEL": str(model_file)
        }

        process = run([LMP_EXECUTABLE, "-in", LMP_SCRIPT_FILE], env=env)
        output = process.stdout.decode()
        final_volume_match = FINAL_VOLUME_PATTERN.search(output)
        cohesive_energy_match = COHESIVE_ENERGY_PATTERN.search(output)

        if not final_volume_match or not cohesive_energy_match:
            print(output)
            raise RuntimeError

        final_volume = float(final_volume_match.group(1))
        cohesive_energy = float(cohesive_energy_match.group(1))

        values.append((final_volume, cohesive_energy))

    output = OutputData(values)
    json.dump(asdict(output), sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
