from petharbor.utils.dataset import DatasetProcessor
from petharbor.utils.hashing import HashingProcessor
from petharbor.utils.logging_setup import get_logger

logger = get_logger(method="Lite")


class Anonymiser:
    """
    A class used to anonymize text data using hashing and optional spaCy processing.

    Attributes
    ----------
    dataset_path : str
        The path to the dataset file.
    hash_table : str
        The path to the hash table file.
    salt : str, optional
        An optional salt value for hashing (default is None).
    cache : bool, optional
        Whether to use caching for the dataset processing (default is True).
    use_spacy : bool, optional
        Whether to use spaCy for additional text processing (default is False).
    spacy_model : str, optional
        The spaCy model to use for text processing (default is "en_core_web_sm").
    text_column : str, optional
        The name of the text column in the dataset (default is "item_text").
    output_dir : str, optional
        The directory where the output files will be saved (default is "testing/out/").

    Methods
    -------
    annonymise():
        Anonymizes the dataset by hashing the text data and optionally using spaCy for additional processing.
    read_hash_table(hash_table: str):
        Reads the hash table from a file and returns it as a list of strings.
    """
    def __init__(
        self,
        dataset_path: str,
        hash_table: str,
        salt: str = None,
        cache: bool = True,
        use_spacy: bool = False,
        spacy_model: str = "en_core_web_sm",
        text_column: str = "item_text",
        logs: str = None,
        output_dir: str = "testing/out/",
    ):
        if logs:
            self.logger = get_logger(log_dir=logs, method="lite")
        else:
            self.logger = get_logger(method="lite")
        self.dataset_processor = DatasetProcessor()
        self.hashing_processor = HashingProcessor()
        self.dataset_path = dataset_path
        self.text_column = text_column
        self.salt = salt
        self.cache = cache
        self.use_spacy = use_spacy
        self.spacy_model = spacy_model
        self.hash_table = self.read_hash_table(hash_table)
        self.output_dir = output_dir

    def annonymise(self):
        original_data = self.dataset_processor.load_dataset_file(self.dataset_path)
        original_data["test"] = original_data["test"].select(range(100))
        target_dataset, original_data = self.dataset_processor.load_cache(
            dataset=original_data, use_cache=self.cache
        )
        predictions = self.hashing_processor.hash_predict(
            dataset=target_dataset,
            hash_table=self.hash_table,
            text_column=self.text_column,
            salt=self.salt,
        )
        if self.use_spacy:
            predictions = self.hashing_processor.spacy_predict(
                dataset=predictions,
                spacy_model=self.spacy_model,
                text_column=self.text_column,
            )

        self.dataset_processor.save_dataset_file(
            original_data=original_data,
            target_dataset=target_dataset,
            predictions=predictions,
            text_column=self.text_column,
            output_dir=self.output_dir,
        )

    def read_hash_table(self, hash_table: str):
        list = []
        with open(hash_table, "r") as f:
            for line in f:
                list.append(line.strip())
        return list
