from random import choices
from barcode_library_characterizer import library_quality_control as lb

ALPHABET="ABCDE"

def samples(k=10):
    while True:
        yield "".join(choices(ALPHABET, k=k))
        
def test_simple_vs_arr():
    s = samples(k=5)
    barcodes = [ next(s) for _ in range(10) ]
    arr = lb.build_histogram_arr(barcodes)
    simple = lb.build_histogram_simple(barcodes)
    assert arr == simple
    
def test_mp_vs_arr():
    s = samples(k=5)
    barcodes = [ next(s) for _ in range(10) ]
    arr = lb.build_histogram_arr(barcodes)
    mp = lb.build_histogram_multiprocess(barcodes)
    assert arr == mp
