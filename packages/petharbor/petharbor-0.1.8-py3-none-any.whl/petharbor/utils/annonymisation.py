from petharbor.utils.logging_setup import get_logger

logger = get_logger()
from tqdm import tqdm


def replace_token(dataset, predictions, text_col: str):
    """
    Anonymizes entities in text by replacing them with their respective tags.

    Args:
        dataset: List of dictionaries containing the text data
        predictions: List of dictionaries containing entity predictions
        text_column: Name of the column containing the text to anonymize

    Returns:
        List of dictionaries with anonymized text

    Example:
        predictions format:
        [{'entities': [{'text': 'John', 'labels': [{'value': 'PERSON'}],
                       'start': 0, 'end': 4}]}]
    """
    logger.info("Anonymizing entities...")

    # Create a deep copy to avoid modifying the original dataset
    processed_dataset = [{**item} for item in dataset]

    for idx in tqdm(range(len(dataset)), desc="Anonymizing..."):
        if not predictions[idx]:
            continue

        text = dataset[idx][text_col]
        if not text:
            logger.warning(f"Empty text found at index {idx}")
            continue

        # Sort entities by start position in reverse order
        # This ensures we process longer entities before shorter ones
        entities = sorted(predictions[idx], key=lambda x: x.get("start_pos"), reverse=True)

        # Create a list of all positions that have been replaced
        replaced_positions = set()

        for entity in entities:
            try:
                start = entity.get("start_pos")
                end = entity.get("end_pos")
                target_text = entity.get("text")
                label = entity.get("labels", [{}])[0].get("value")

                if not all([start is not None, end is not None, target_text, label]):
                    logger.warning(f"Invalid entity at index {idx}: {entity}")
                    continue

                # Check if this position has already been replaced
                if any(pos in replaced_positions for pos in range(start, end)):
                    continue

                # Create the replacement tag
                replacement = f"<<{label}>>"

                # Replace the specific occurrence at the correct position
                text = text[:start] + replacement + text[end:]

                # Mark these positions as replaced
                replaced_positions.update(range(start, end))

            except Exception as e:
                logger.error(f"Error processing entity at index {idx}: {str(e)}")
                continue

        processed_dataset[idx][text_col] = text

    return processed_dataset
