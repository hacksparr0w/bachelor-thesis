import dpdata
import numpy as np

from _home import DATASET_DIR
from _utility import flatten


AMORPHOUS_DATA_FILES = (
    "a-2.15.md",
    "a-2.20.md",
    "a-2.25.md",
    "a-2.29.md",
    "a-2.30.md",
    "a-2.31.md",
    "a-2.35.md",
    "a-2.40.md"
)

CRYSTALLINE_DATA_FILES = (
    "c-0.99.md",
    "c-1.01.md",
    "c-1.03.md"
)

DATASET_MATRIX = (
    (
        "amorphous",
        [(DATASET_DIR / name, 10) for name in AMORPHOUS_DATA_FILES]
    ),
    (
        "crystalline",
        [(DATASET_DIR / name, 5) for name in CRYSTALLINE_DATA_FILES]
    ),
    (
        "combined",
        flatten([
            [(DATASET_DIR / name, 10) for name in AMORPHOUS_DATA_FILES],
            [(DATASET_DIR / name, 5) for name in CRYSTALLINE_DATA_FILES]
        ])
    )
)


def generate_dataset(data_file, root_dir, n=1, r=4):
    data = dpdata.LabeledSystem(str(data_file), fmt="vasp/outcar")
    data = data.sub_system(range(0, len(data), n))

    validation_data_length = len(data) // r
    validation_data_indices = np.random.choice(
        len(data),
        size=validation_data_length,
        replace=False
    )

    training_data_indices = list(
        set(range(len(data))) - set(validation_data_indices)
    )

    validation_data = data.sub_system(validation_data_indices)
    training_data = data.sub_system(training_data_indices)

    validation_data.to_deepmd_npy(str(root_dir / "validation_data"))
    training_data.to_deepmd_npy(str(root_dir / "training_data"))

    print(f"Created training dataset with {len(training_data)} frames.")
    print(f"Created validation dataset with {len(validation_data)} frames.")


def main():
    for (name, specs) in DATASET_MATRIX:
        dataset_dir = DATASET_DIR / name

        for data_file, n in specs:
            root_dir = dataset_dir / data_file.stem
            root_dir.mkdir(parents=True, exist_ok=False)

            generate_dataset(data_file, root_dir, n)


if __name__ == "__main__":
    main()
