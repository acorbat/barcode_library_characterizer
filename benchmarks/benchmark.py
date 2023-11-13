from itertools import islice
from timeit import timeit
from random import choices
from barcode_library_characterizer import library_quality_control as lb

ALPHABET = "ABCDE"
NUM = 10


def samples(k=10):
    while True:
        yield "".join(choices(ALPHABET, k=k))


barcodes = list(islice(samples(), 10000))

sizes = [10, 100, 1000, 10000]

# Not very reliable, prefer ipython %timeit
for size in sizes:
    b = barcodes[:size]
    # arr = timeit("lb.build_histogram_arr(b)", globals=globals(), number=NUM)
    # counter = timeit("lb.build_histogram_simple(b)",globals=globals(), number=NUM)
    # multi = timeit("lb.build_histogram_multiprocess(b)",globals=globals(), number=NUM)
    # print(f"Barcodes Number: {size} - counter:{counter} array:{arr} multiprocess:{multi}")

# in ipython
# %run benchmarks/benchmark.py
# %timeit lb.build_histogram(b)
