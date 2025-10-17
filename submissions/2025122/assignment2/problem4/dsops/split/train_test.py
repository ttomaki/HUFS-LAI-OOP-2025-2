import random
from typing import Optional


def train_test_split(seq: list, test_ratio: float, seed: Optional[int] = None) -> tuple[list, list]:
    """
    Split a sequence into train and test sets.

    Args:
        seq: Input sequence to split
        test_ratio: Ratio of test set (0.0 to 1.0)
        seed: Random seed for reproducibility

    Returns:
        Tuple of (train_set, test_set)

    Raises:
        ValueError: If test_ratio is not between 0.0 and 1.0
    """
    if not (0.0 <= test_ratio <= 1.0):
        raise ValueError("test_ratio must be between 0.0 and 1.0")

    if not seq:
        return [], []

    # Copy to preserve original
    seq_copy = seq.copy()

    # Set seed and shuffle if seed provided
    if seed is not None:
        random.seed(seed)
    random.shuffle(seq_copy)

    # Calculate split index
    cut_index = int(round(len(seq) * (1 - test_ratio)))

    train_set = seq_copy[:cut_index]
    test_set = seq_copy[cut_index:]

    return train_set, test_set