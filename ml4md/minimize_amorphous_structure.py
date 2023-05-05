import json
import multiprocessing
import os
import psutil
import re
import shutil
import subprocess
import sys

from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

from dacite import from_dict

import _home

PARALELLISM = psutil.cpu_count(logical=False)
PROCESSES = psutil.cpu_count() / PARALELLISM
LMP_EXECUTABLE = "lmp"
MPI_EXECUTABLE = "mpirun"
LMP_SCRIPT_FILE = Path(__file__).parent / "minimize_amorphous_structure.lmp"
COHESIVE_ENERGY_PATTERN = re.compile(
    r"Cohesive energy \(eV\) = ([+-]?([0-9]*[.])?[0-9]+)"
)

FINAL_VOLUME_PATTERN = re.compile(
    r"Final volume \(angstrom\^3\) = ([+-]?([0-9]*[.])?[0-9]+)"
)


@dataclass
class InputData:
    model: str
    target_t: float


@dataclass
class OutputData:
    values: list[tuple[float, float]]


def run(command, env=None):
    return subprocess.run(command, capture_output=True, env=env)


def simulate(volume_scale, target_t, model_file, mpi_support):
    env = {
        **os.environ,
        "MD_TARGET_TEMPERATURE": str(target_t),
        "MD_VOLUME_SCALE": str(volume_scale),
        "MD_DEEPMD_MODEL": str(model_file)
    }
    
    command = []

    if mpi_support:
        command.extend([MPI_EXECUTABLE, "-np", str(PARALELLISM)])

    command.extend([LMP_EXECUTABLE, "-in", LMP_SCRIPT_FILE])

    process = run(command, env=env)
    output = process.stdout.decode()
    final_volume_match = FINAL_VOLUME_PATTERN.search(output)
    cohesive_energy_match = COHESIVE_ENERGY_PATTERN.search(output)

    if not final_volume_match or not cohesive_energy_match:
        print(output, file=sys.stderr)
        raise RuntimeError

    final_volume = float(final_volume_match.group(1))
    cohesive_energy = float(cohesive_energy_match.group(1))

    print(final_volume, cohesive_energy, file=sys.stderr)

    return final_volume, cohesive_energy


def simulate_wrapper(args):
    return simulate(*args)


def main():
    data = from_dict(data_class=InputData, data=json.load(sys.stdin))

    model_file = _home.find_model(data.model).model_file
    values = []
    mpi_support = shutil.which(MPI_EXECUTABLE) is not None
    volume_scales = np.linspace(0.90, 1.10, 20)
    args = map(
        lambda scale: (scale, data.target_t, model_file, mpi_support),
        volume_scales
    )

    values = None

    with multiprocessing.Pool(PROCESSES) as pool:
        values = pool.map(simulate_wrapper, args)

    output = OutputData(values)
    json.dump(asdict(output), sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
