# Barcode Library Characterizer

A small package for characterizing big (huge) libraries of barcodes.


#

```
python -m venv .env
.env\activate # .env\Scripts\Activate.ps1
python -m pip install -r requirements.txt

python barcode_library_characterizer/main.py sample.csv 1
```

# Known issues

`tinyalign` only works in unix systems. If try to install on Windows needs to be recompiled and requires setup
of *Microsoft C++ build tools*