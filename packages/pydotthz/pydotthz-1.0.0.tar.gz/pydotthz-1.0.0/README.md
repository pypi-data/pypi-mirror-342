# Interface with dotTHz files using Python

[![PEP8](https://github.com/dotTHzTAG/pydotthz/actions/workflows/format.yml/badge.svg)](https://github.com/dotTHzTAG/pydotthz/actions/workflows/format.yml)
[![PyPI](https://img.shields.io/pypi/v/pydotthz?label=pypi%20package)](https://pypi.org/project/pydotthz/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pydotthz)](https://pypi.org/project/pydotthz/)

This crate provides an easy way to interface with [dotTHz](https://github.com/dotTHzTAG) files in Python.

Install it

```shell
pip install pydotthz
```

or

```shell
pip3 install pydotthz
```

and then use like specified in the following example:

```python
from pathlib import Path
import numpy as np
from pydotthz import DotthzFile, DotthzMeasurement, DotthzMetaData

if __name__ == "__main__":
    # Sample data
    time = np.linspace(0, 1, 100)  # your time array
    data = np.random.rand(100)  # example 3D data array

    # save the file
    path1 = Path("test1.thz")
    with DotthzFile(path1, "w") as file:
        file["Measurement 1"] = DotthzMeasurement()

        # create meta-data
        meta_data = DotthzMetaData()
        meta_data.user = "John Doe"
        meta_data.version = "1.00"
        meta_data.instrument = "Toptica TeraFlash Pro"
        meta_data.mode = "THz-TDS/Transmission"

        file["Measurement 1"].meta_data = meta_data

        # for thzVer 1.00, we need to transpose the array!
        # important: do not manipulate keys on the `dataset` field, otherwise it won't be written to the file.
        file["Measurement 1"]["Sample"] = np.array([time, data]).T

    del file  # optional, not required as the file is already closed

    # create and save a second file
    path2 = Path("test2.thz")
    with DotthzFile(path2, "w") as file:
        file["Measurement 2"] = DotthzMeasurement()
    del file  # optional, not required as the file is already closed

    # open the first file again in append mode and the second in read mode
    with DotthzFile(path1, "a") as file1, DotthzFile(path2) as file2:
        measurements = file2.measurements
        for name, measurement in measurements.items():
            file1[name] = measurement
    del file1  # optional, not required as the file is already closed

    with DotthzFile(path1, "r") as file1:
        # read the first measurement
        key = list(file1.measurements.keys())[0]
        print(file1.measurements.get(key).meta_data)
        print(file1.measurements.get(key).datasets)

    # read out an image file:
    path3 = Path("tests/test_files/test_image.thz")
    with DotthzFile(path3, "r") as image_file:
        # read the first group/measurement
        key = list(image_file.measurements.keys())[0]
        print(image_file.measurements.get(key).meta_data)
        datasets = image_file.measurements.get(key).datasets
        print(datasets.keys())

        # from the first dataset, extract the image:
        time_trace = datasets["time"]
        image = datasets["dataset"]

        # print image dimensions
        print(image.shape)

    # save an image file:
    path4 = Path("tests/test_files/test_image_2.thz")
    with DotthzFile(path4, "w") as file:

        file.measurements["Image"] = DotthzMeasurement()

        # set meta_data
        meta_data = DotthzMetaData()
        meta_data.user = "John Doe"
        meta_data.email = "john.doe@unibe.ch"
        meta_data.institution = "University of Bern"
        meta_data.orcid = "ORCID"
        meta_data.description = "some comment"
        meta_data.date = "date"
        meta_data.time = "time"
        meta_data.version = "1.10"
        meta_data.instrument = "Toptica TeraFlash Pro"
        meta_data.mode = "THz-TDS/Transmission"

        # add more keys from your "info" dictionary ...
        # for (key, value) in info.items():
        #    meta_data.add_field(key, value)

        file.measurements["Image"].meta_data = meta_data

        # important: do not manipulate keys on the `dataset` field, otherwise it won't be written to the file.
        file.measurements["Image"]["time"] = time_trace
        file.measurements["Image"]["dataset"] = image

```

Requires hdf5 to be installed.
