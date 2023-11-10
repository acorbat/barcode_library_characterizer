import pathlib
import sys

from library_quality_control import (
    build_histogram,
    build_hamming_distance_histogram_parallel,
    save_histogram,
)

filepath = pathlib.Path(sys.argv[1])
processes = int(sys.argv[2])


print(filepath, processes)
if __name__ == "__main__":
    print(f"Processing file {filepath.name}")

    histogram = build_histogram(filepath)
    save_path = "frequency_histogram_" + filepath.name
    save_histogram(histogram, save_path)

    hamming_histogram = build_hamming_distance_histogram_parallel(filepath, processes)
    save_path = "hamming_histogram_" + filepath.name
    save_histogram(hamming_histogram, save_path, columns=["distance", "frequency"])
