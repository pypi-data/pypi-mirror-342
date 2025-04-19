import logging
import pandas as pd
from datasets import load_from_disk, load_dataset
import os


class DatasetProcessor:

    def __init__(
        self,
        cache_path: str = "petharbor_cache/",
    ):
        self.cache_path = cache_path
        self.logger = logging.getLogger(__name__)

    def validate_dataset(self, dataset, text_column) -> None:
        if text_column not in dataset.column_names:
            error_message = f"Text column '{text_column}' not found in dataset. Please add 'text_column' column to the class."
            self.logger.error(error_message)
            raise ValueError(error_message)
        # drop missing rows
        clean_dataset = dataset.filter(lambda example: example[text_column] is not None)
        self.logger.info(
            f"Dataset contains {len(dataset)} rows. After removing missing rows, {len(clean_dataset)} rows remain."
        )
        return clean_dataset

    def load_dataset_file(self, file_path: str, split="train") -> dict:
        """
        Attempt to load a dataset using multiple strategies:
        1. As a HuggingFace Arrow dataset from disk.
        2. As a CSV file via HuggingFace `load_dataset`.
        3. As a generic dataset via HuggingFace `load_dataset`.

        Args:
            file_path (str): Path to the dataset file.
            split (str): The split of the HuggingFace dataset to load (e.g., 'train', 'test', 'eval). Default is 'train'.

        Returns:
            A dictionary with keys as split names (e.g., 'train', 'test') and values as datasets.
        """
        # Try loading from disk
        if file_path.endswith("csv"):
            try:
                dataset = load_dataset("csv", data_files=file_path)["train"]
                self.logger.info(f"Loaded dataset from {file_path}")
                # if dataset contains multiple splits, return just train
            except Exception as e:
                self.logger.error(f"Failed to load dataset from {file_path}: {e}.")
                raise
        else:
            try:
                dataset = load_from_disk(file_path)
                self.logger.info(f"Loaded dataset from {file_path}")
            except Exception as e:
                self.logger.error(f"Failed to load dataset from {file_path}: {e}")
                raise
        if not dataset:  # Check if dataset is empty
            self.logger.error(f"Dataset is empty or not found at {file_path}")
            raise ValueError(f"Dataset is empty or not found at {file_path}")
        else:
            if split in dataset:  # Check if the dataset contains multiple splits
                self.logger.info(
                    f"Dataset contains multiple splits, returning '{split}' split. If you want to use a different split, please specify it."
                )
                dataset = dataset[split]
        return dataset

    def load_cache(self, dataset, cache=False) -> tuple:
        """
        Filter out anonymised data from the dataset using a cache.

        Args:
            dataset: The dataset to filter.
            cache (bool | str): If True, removes examples where "annonymised" == 1.
                                If str, treats it as a column name and filters out rows
                                based on cached record IDs from a text file.
            cache_path (str): Path to cache directory (only used if `cache` is a str).

        Returns:
            tuple: (filtered_dataset, original_dataset)
        """
        target_dataset = dataset

        if cache:
            try:
                if isinstance(cache, bool):
                    target_dataset = dataset.filter(
                        lambda example: example.get("annonymised", 0) == 0
                    )

                elif isinstance(cache, str):
                    if cache not in dataset.column_names:
                        self.logger.error(f"Column '{cache}' not found in dataset.")
                        raise ValueError(f"Column '{cache}' not found in dataset.")
                    self.cache_path = os.path.join(
                        self.cache_path, f"{cache}_cache.txt"
                    )
                    if os.path.exists(self.cache_path):
                        with open(self.cache_path, "r") as f:
                            cached_ids = set(f.read().splitlines())
                        # if the cached_ids (in a dict format), appear in the cache column of the dataset, filter them out
                        target_dataset = dataset.filter(
                            lambda example: str(example[cache]) not in cached_ids
                        )
                    else:
                        os.makedirs(self.cache_path, exist_ok=True)
                        with open(self.cache_path, "w") as f:
                            f.write("")
                        self.logger.warning(
                            f"Cache file not found at {self.cache_path}. Proceeding without filtering."
                        )
                        self.logger.info(f"Cache file created at {self.cache_path}.")

                else:
                    raise ValueError(
                        "`cache` must be either a boolean or a string (column name)."
                    )

                self.logger.info(
                    f"Cache enabled | Skipping {len(dataset) - len(target_dataset)} anonymised rows | Processing {len(target_dataset)} rows"
                )

            except Exception as e:
                self.logger.error(f"Failed to apply cache filtering: {e}")

            if not target_dataset:
                self.logger.info("All data appears to have been anonymised. Exiting...")
                self.logger.warning(
                    "If this was unexpected, please check your cache file or delete a column called 'annonymised' in your dataset."
                )
                import sys

                sys.exit(0)
            else:
                self.logger.info(
                    f"Processing {len(target_dataset)} non-anonymised rows"
                )
                return dataset, target_dataset
        else:
            self.logger.info("Cache disabled | Processing all data")
            return dataset, target_dataset

    def save_dataset_file(
        self,
        original_data,
        target_dataset,
        output_dir: str = None,
        cache=False,
    ):
        """
        Save dataset predictions to a file.
        """
        target_dataset = target_dataset.to_pandas()

        if cache:
            if isinstance(cache, bool):
                target_dataset["annonymised"] = 1
                self.logger.info(
                    "Cache enabled || 'annoymised' column added to dataset. Note: Review our documentation for more details."
                )
            elif isinstance(cache, str):
                cache_ids = target_dataset[cache].tolist()
                # Read in the cache file and append the new ids to the bottom
                with open(self.cache_path, "a") as f:
                    for id in cache_ids:
                        f.write(f"{id}\n")
            original_data = original_data.to_pandas()
            target_dataset = pd.concat(
                [original_data, target_dataset], ignore_index=True
            )

        date = pd.Timestamp.now().strftime("%Y-%m-%d")

        if output_dir == None:
            output_dir = f"{date}_anonymised.csv"
        elif output_dir.endswith(".csv"):
            output_dir = f"{output_dir}"
        else:
            output_dir = f"{output_dir}/{date}_anonymised.csv"
        target_dataset.to_csv(output_dir, index=False)
        self.logger.info(f"Saved anonymised dataset to {output_dir}")
