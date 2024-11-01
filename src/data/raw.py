import os
import pandas as pd
import kagglehub
from src.data.csv import CSVData


class MangoDataset:
    DATASET_NAME = "adrinbd/unripe-ripe-rotten-mango"
    LABELS = ["Ripe", "Rotten"]
    CSV_DIR = "../data/raw"

    def __init__(self):
        self.path = self._check_and_download_dataset()
        self.train_data = self._create_csv_dataset("train")
        self.validation_data = self._create_csv_dataset("validation")

    def _check_and_download_dataset(self):
        if not os.path.exists(self.CSV_DIR):
            os.makedirs(self.CSV_DIR)
            dataset_path = self._download_dataset()
            CSVData.save_dataset_path(dataset_path)
            return dataset_path

        return CSVData.get_saved_dataset_path()

    @classmethod
    def _download_dataset(cls):
        return kagglehub.dataset_download(cls.DATASET_NAME)

    def _create_csv_dataset(self, split):
        return CSVData(
            os.path.join(self.CSV_DIR, f"{split}.csv"),
            data_generator=lambda: self._load_data(split),
        )

    def _load_data(self, split):
        data = []
        for label in self.LABELS:
            label_folder = os.path.join(self.path, "Dataset", split, label)
            if os.path.exists(label_folder):
                data.extend(
                    {"label": label, "filename": filename}
                    for filename in os.listdir(label_folder)
                )

        return data
