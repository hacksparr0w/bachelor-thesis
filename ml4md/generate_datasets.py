import dpdata
import numpy as np

from _home import DATASET_DIR


class DisjunctDatasetType:
    TRAINING = "TRAINING"
    VALIDATION = "VALIDATION"


class DatasetType(DisjunctDatasetType):
    UNIVERSAL = "UNIVERSAL"


AMORPHOUS_DATASETS = (
    ("a-2.15.md", DatasetType.TRAINING, 10),
    ("a-2.20.md", DatasetType.TRAINING, 10),
    ("a-2.25.md", DatasetType.VALIDATION, 10),
    ("a-2.29.md", DatasetType.TRAINING, 10),
    ("a-2.30.md", DatasetType.TRAINING, 10),
    ("a-2.31.md", DatasetType.VALIDATION, 10),
    ("a-2.35.md", DatasetType.TRAINING, 10),
    ("a-2.40.md", DatasetType.TRAINING, 10)
)

CRYSTALLINE_DATASETS = (
    ("c-0.99.md", DatasetType.TRAINING, 5),
    ("c-1.01.md", DatasetType.VALIDATION, 5),
    ("c-1.03.md", DatasetType.TRAINING, 5)
)

DATASET_MATRIX = (
    ("amorphous", AMORPHOUS_DATASETS),
    ("crystalline", CRYSTALLINE_DATASETS),
    ("combined", [*AMORPHOUS_DATASETS, *CRYSTALLINE_DATASETS])
)


def export_dataset(data, data_file, dataset_type, root_dir):
    output_dir = None

    if dataset_type == DisjunctDatasetType.TRAINING:
        output_dir = root_dir / "training" / data_file.stem
    else:
        output_dir = root_dir / "validation" / data_file.stem

    data.to_deepmd_npy(str(output_dir))

    if dataset_type == DisjunctDatasetType.TRAINING:
        print(f"Created training dataset with {len(data)} frames.")
    else:
        print(f"Created validation dataset with {len(data)} frames.")


def generate_dataset(data_file, dataset_type, factor, root_dir):
    data = dpdata.LabeledSystem(str(data_file), fmt="vasp/outcar")
    data = data.sub_system(range(0, len(data), factor))

    if dataset_type == DatasetType.UNIVERSAL:
        validation_data_length = len(data) // 4
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

        export_dataset(
            validation_data,
            data_file,
            DisjunctDatasetType.VALIDATION,
            root_dir
        )

        export_dataset(
            training_data,
            data_file,
            DisjunctDatasetType.TRAINING,
            root_dir
        )
    else:
        export_dataset(data, data_file, dataset_type, root_dir)


def main():
    for (dataset_name, entries) in DATASET_MATRIX:
        root_dir = DATASET_DIR / dataset_name
        root_dir.mkdir(exist_ok=False)

        for data_file_name, dataset_type, factor in entries:
            generate_dataset(
                DATASET_DIR / data_file_name,
                dataset_type,
                factor,
                root_dir
            )


if __name__ == "__main__":
    main()
