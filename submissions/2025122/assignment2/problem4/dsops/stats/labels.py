def label_distribution(labels: list[str]) -> dict[str, int]:
    """
    Calculate the frequency distribution of labels.

    Args:
        labels: List of string labels

    Returns:
        Dictionary mapping label to frequency count
    """
    distribution = {}
    for label in labels:
        distribution[label] = distribution.get(label, 0) + 1
    return distribution