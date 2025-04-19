"""
PyDotTHz
=====

Provides classes for interacting with the .thz file format, a format for
storing data from terahertz time-domain spectroscopy measurements. For
more detail see: https://doi.org/10.1007/s10762-023-00947-w

The .thz file fomrat is a domain specific implementation of the widely
used Hierarchical Data Format 5 standard. As such this package acts as
a wrapper around the h5py package, breaking up each HDF5 object into
multiple easier to use objects. A .thz file has the following internal
structure:

    .thz File
    |---->Measurement 1
    |     |---->Metadata
    |     |     |---->User
    |     |     |---->Temperature
    |     |     |...
    |     |---->Dataset 1
    |     |     |---->Electric Field
    |     |     |---->Time
    |     |---->Dataset 2
    |     |...
    |---->Measurement 2
    |...

This package will convert said file into the following objects:
    1. A `DotthzFile` object which holds a dictionary of `DotthzMeasurement`
    objects.
    2. Multiple `DotthzMeaurement` objects each containing a `DotthzMetaData`
    object and a dictionary of datasets. Datasets can take any structure but
    a shape (2, n) array is reccomended.
    3. A `DotthzMetaData` object for each measurement, containg multiple fixed
    attributes as defined in the .thz standard as well as a dictionary of user
    defined attributes.

"""

from .pydotthz import (DotthzFile,
                       DotthzMeasurement,
                       DotthzMetaData)

__all__ = [DotthzFile,
           DotthzMeasurement,
           DotthzMetaData]
