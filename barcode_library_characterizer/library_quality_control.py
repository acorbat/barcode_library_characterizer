import csv
from collections import defaultdict, Counter
from itertools import combinations
from math import comb
from multiprocessing import Pool, Array
import pathlib

from tqdm import tqdm
from tinyalign import hamming_distance


def build_histogram(csv_path: pathlib.Path) -> dict:
    """Reads line by line a csv with the extracted barcodes to build a read
    frequency histogram."""
    histogram = defaultdict(int)
    with open(csv_path) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)

        for row in reader:
            histogram[int(row[0])] += 1
    return histogram


def save_histogram(
    histogram: dict, save_path: pathlib.Path, columns=(["reads", "frequency"])
) -> None:
    """Saves histogram to save_path"""
    with open(save_path, "w") as csv_file:
        csv_file.write(f"{columns[0]},{columns[1]}\n")
        for data in histogram.items():
            csv_file.write(f"{data[0]},{data[1]}\n")


def skip_lines(csv_reader: csv.reader, n) -> None:
    """Skips n lines in the reader"""
    for i in range(n):
        next(csv_reader)


def get_csv_length(csv_path: pathlib.Path) -> None:
    """Get the number of rows in a CSV file"""
    with open(csv_path) as csv_file:
        length = len(csv_file.read().split("\n"))
    return length


def build_hamming_distance_histogram(csv_path: pathlib.Path) -> dict:
    """Reads line by line a csv with the extracted barcodes to build a Hamming
    distance histogram."""
    hamming_histogram = defaultdict(int)
    csv_length = get_csv_length(csv_path)
    with open(csv_path) as csv_file:
        reader_slow = csv.reader(csv_file)
        skip_lines(reader_slow, 1)

        already_compared = 1
        for row_slow in tqdm(reader_slow, total=csv_length):
            with open(csv_path) as csv_file_2:
                reader_fast = csv.reader(csv_file_2)
                skip_lines(reader_fast, 1 + already_compared)

                for row_fast in reader_fast:
                    sequence_fast = row_fast[1]
                    sequence_slow = row_slow[1]
                    distance = hamming_distance(sequence_fast, sequence_slow)

                    hamming_histogram[distance] += 1

            already_compared += 1

    return hamming_histogram


def build_hamming_distance_histogram_loading(csv_path: pathlib.Path) -> dict:
    """Reads all extracted barcodes from a csv to build a Hamming distance
    histogram."""
    hamming_histogram = defaultdict(int)
    csv_length = get_csv_length(csv_path)
    barcodes = []
    with open(csv_path) as csv_file:
        reader = csv.reader(csv_file)
        skip_lines(reader, 1)

        for row in reader:
            barcodes.append(row[1])

    for n, sequence_slow in enumerate(tqdm(barcodes)):
        for sequence_fast in barcodes[n + 1 :]:
            distance = hamming_distance(sequence_fast, sequence_slow)

            hamming_histogram[distance] += 1

    return hamming_histogram


def my_hamming_distance(sequences):
    return hamming_distance(*sequences)


def build_hamming_distance_histogram_parallel(
    csv_path: pathlib.Path, processes=4
) -> dict:
    """Reads all extracted barcodes from a csv to build a Hamming distance
    histogram using parallelization."""
    hamming_histogram = defaultdict(int)
    barcodes = []
    with open(csv_path) as csv_file:
        reader = csv.reader(csv_file)
        skip_lines(reader, 1)

        for row in reader:
            barcodes.append(row[1])
    possible_combinations = comb(len(barcodes), 2)

    with Pool(processes) as pool:
        for distance in pool.imap_unordered(
            my_hamming_distance,
            tqdm(combinations(barcodes, 2), total=possible_combinations),
            2048,
        ):
            hamming_histogram[distance] += 1

    return hamming_histogram


def build_hamming_distance_simple(
        csv_path: pathlib.Path) -> dict:
    hamming_histogram = defaultdict(int)
    
    with open(csv_path) as csv_file:
        reader = csv.reader(csv_file)
        skip_lines(reader, 1)
        barcodes = [
            row[1]
            for row in reader ]

    return build_histogram_simple(barcodes)
        
        
def build_histogram_simple(barcodes):
    arr = [0]*(len(barcodes[0])+1)
    c = Counter( hamming_distance(barcodes[fast], barcodes[slow])
                    for slow,fast in pairs(len(barcodes)) )
    for i,count in c.items():
        arr[i] = count
    return arr

def build_histogram_arr(barcodes):
    arr = [0]*(len(barcodes[0])+1)

    for slow,fast in pairs(len(barcodes)):
        d = hamming_distance(barcodes[fast], barcodes[slow])
        arr[d] += 1
    return arr

# Trick to share state between processes, add it to a module field 
from . import shared

# can't define as a local function because it can't be pickled to send between processes
def update(i, j):
    d = hamming_distance(shared.barcodes[i], shared.barcodes[j])
    shared.A[d] += 1
    #return d

# https://stackoverflow.com/a/1721911
def initProcess(A, barcodes):
    shared.A = A
    shared.barcodes = barcodes


def build_histogram_multiprocess(barcodes):
    arr = [0]*(len(barcodes[0])+1)
    A = Array('i', arr)

    with Pool(initializer=initProcess,initargs=(A,barcodes)) as p:
        p.starmap(update, pairs(len(barcodes)))
    
    return list(A)

def pairs(n=10):
    for slow in range(n):
        for fast in range(slow+1,n):
            yield (slow, fast)

def map_f(idx):
    i,j = idx
    arr = [0]*(len(shared.barcodes[0])+1)
    d = hamming_distance(shared.barcodes[i], shared.barcodes[j])
    arr[d] = 1
    return arr
    
def reduce_f(st, new):
    # array componentwise sum
    return [ x+y for x,y in zip(st,new) ]

def build_histogram_mapReduce(barcodes):
    from functools import reduce
    initProcess(None,barcodes)
    return reduce(reduce_f, map(map_f, pairs(len(barcodes))))
