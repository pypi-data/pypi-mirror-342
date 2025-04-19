import hashlib
from tqdm import tqdm


class HashingProcessor:
    def __init__(self):
        None

    def hash_predict(
        self, dataset, hash_table: list, text_column: str, salt: str
    ) -> list:
        """
        Process an Arrow dataset and anonymize sensitive terms in EHR narratives.

        Parameters:
        - dataset: Arrow dataset containing EHR narratives
        - hash_list (list): List of hashed sensitive terms
        - text_column (str): Name of the column containing narrative text
        - salt (str): Shared salt for hashing terms

        Returns:
        - list: List of anonymized narratives
        """

        anonymized_narratives = []

        # Process each row in the dataset
        for row in tqdm(dataset["test"], desc="Anonymizing EHR narratives..."):
            narrative = row[text_column]
            words = narrative.split()
            anonymized_words = []

            # Process each word in the narrative
            for word in words:
                # Clean word (remove punctuation if needed)
                clean_word = word.strip(",.?!:").lower()
                hashed_word = self.hash_term(clean_word, salt)

                # Replace sensitive terms with placeholder
                if hashed_word in hash_table:
                    anonymized_words.append("<<IDENTIFIER>>")
                else:
                    anonymized_words.append(word)

            # Join words back together and add to results
            anonymized_narratives.append(" ".join(anonymized_words))

        return anonymized_narratives

    def spacy_predict(
        self, dataset, spacy_model: str = "en_core_web_sm", text_column: str = "text"
    ) -> list:
        nlp = self.import_spacy(spacy_model)
        anonymized_texts = []
        if isinstance(dataset, dict):
            dataset = dataset["test"][text_column]

        for row in tqdm(dataset, desc="Anonymizing Text"):
            processsed_text = nlp(row)
            anonymized_texts.append(self.anonymize_text(processsed_text))

        return anonymized_texts

    @staticmethod
    def anonymize_text(text: str) -> str:

        entity_map = {
            "PERSON": "<<PER>>",
            "ORG": "<<ORG>>",
            "DATE": "<<DATE>>",
            "TIME": "<<TIME>>",
            "MONEY": "<<COST>>",
            "GPE": "<<LOC>>",
            "LOC": "<<LOC>>",
        }
        try:
            text_string = text.text
        except:
            text_string = text

        if text.ents:
            for entity in text.ents:
                if entity.label_ in entity_map.keys():
                    text_string = text_string.replace(
                        entity.text, entity_map[entity.label_]
                    )
        return text_string

    @staticmethod
    def import_spacy(spacy_model: str = "en_core_web_sm"):
        try:
            import spacy
        except ImportError:
            raise ImportError(
                "spaCy is not installed. Please install it using 'pip install spacy'"
            )
        try:
            nlp = spacy.load(spacy_model)
        except OSError:
            raise ValueError(
                f"spaCy model '{spacy_model}' not found. Please check the model name or ensure it is installed using 'python -m spacy download {spacy_model}'"
            )
        return nlp

    @staticmethod
    def hash_term(term: str, salt: str) -> str:
        """Hash a term with the shared salt."""
        salted_term = term + salt
        hash_object = hashlib.sha256(salted_term.encode("utf-8"))
        return hash_object.hexdigest()
