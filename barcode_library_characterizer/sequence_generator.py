from collections import Counter
from typing import List

import numpy as np
import pandas as pd


def generate_barcode(length_of_sequence: int, number_of_sequences: int) -> np.array:
    """Generates a list of random barcodes of the selected size"""
    mat = np.random.choice(['A', 'C', 'G', 'T'], size=(length_of_sequence, number_of_sequences))
    return np.apply_along_axis(''.join, 0, mat)


def build_histogram(barcode_list: List[str]) -> pd.DataFrame:
    """Counts how many occurrences of each barcode"""
    counts = Counter(barcode_list)
    counts_df = pd.DataFrame.from_dict(counts, orient="index", columns=["frequency"])
    counts_df.sort_index(inplace=True)

    return counts_df