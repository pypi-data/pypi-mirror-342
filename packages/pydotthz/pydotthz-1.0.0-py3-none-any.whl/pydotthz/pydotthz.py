"""
DotTHz File Interface

This module defines classes and methods to read, write, and manipulate `.thz` files,
a format for storing terahertz time-domain spectroscopy (THz-TDS) measurements. It
supports automatic saving, metadata handling, and dataset management using HDF5.

Classes:
--------
- DotthzMetaData: Stores user and measurement metadata.
- DotthzMeasurement: Encapsulates datasets and metadata for a single measurement.
- MeasurementDict: Dictionary wrapper to automatically persist DotthzMeasurement instances.
- DotthzFile: Handles reading/writing `.thz` files and provides access to stored measurements.

Dependencies:
-------------
- numpy
- h5py
"""

from dataclasses import dataclass, field
from typing import Dict, Any
from collections.abc import Iterable
from warnings import warn
import numpy as np
import h5py
import warnings

warnings.simplefilter("always", DeprecationWarning)


@dataclass
class DotthzMetaData:
    """Data class holding metadata for measurements in the .thz file format.

    Attributes
    ----------
    user : str
        The user who performed the measurement.
    email : str
        The email of the user.
    orcid : str
        The ORC ID of the user.
    institution : str
        The institution the user belongs to.
    description : str
        A description of the measurement.
    md : dict
        A dictionary of custom metadata (e.g. thickness, temperature, etc.).
    version : str, optional
        The version of the .thz file standard used.
        Defaults to "1.00".
    mode : str
        The measurement modality (e.g. transmission).
    instrument : str
        The instrument used to perform the measurement.
    time : str
        Timestamp of when the measurement was conducted.
    date : str
        The date on which the measurement was conducted.
    """
    user: str = ""
    email: str = ""
    orcid: str = ""
    institution: str = ""
    description: str = ""
    md: Dict[str, Any] = field(default_factory=dict)
    version: str = "1.00"
    mode: str = ""
    instrument: str = ""
    time: str = ""
    date: str = ""

    def add_field(self, key, value):
        """
        Add a custom metadata field.

        Parameters
        ----------
        key : str
            Name of the metadata field.
        value : Any
            Value of the metadata field.
        """
        self.md[key] = value


class MeasurementDict(dict):
    """
       A custom dictionary-like class that wraps around the standard Python dictionary.

       This class is designed to store `DotthzMeasurement` objects and ensure that
       whenever a new measurement is added or modified, the corresponding measurement
       is written to the file using the `write_measurement()` method.

       Inherits from `dict` to retain normal dictionary behavior (e.g., iteration,
       item retrieval), while adding the functionality of writing measurements to
       an HDF5 file automatically.

       Attributes
       ----------
       _file : DotthzFile
           A reference to the `DotthzFile` instance to which measurements will be written.

       Methods
       -------
       __setitem__(self, key, value):
           Adds a new measurement to the dictionary and automatically writes it to the file.

       __init__(self, base_file, *args, **kwargs):
           Initializes the `MeasurementDict` and stores a reference to the parent `DotthzFile`.
       """

    def __init__(self, base_file, *args, **kwargs):
        """
        Initializes the `MeasurementDict` object.

        Parameters
        ----------
        base_file : DotthzFile
            A reference to the `DotthzFile` instance that will be used to write measurements.
        *args : tuple
            Positional arguments passed to the parent `dict` constructor.
        **kwargs : dict
            Keyword arguments passed to the parent `dict` constructor.
        """
        super().__init__(*args, **kwargs)
        self._file = base_file

    def __setitem__(self, key, value):
        """
        Adds a new `DotthzMeasurement` to the dictionary and writes it to the file.

        When a new measurement is assigned to the dictionary using the key-value syntax
        (i.e., `measurement_dict[key] = value`), this method is called. It ensures that
        the `value` is a valid `DotthzMeasurement` object and then automatically calls
        the `write_measurement()` method of `DotthzFile` to store the measurement.

        Parameters
        ----------
        key : str
           The key under which the measurement will be stored (usually the measurement name).
        value : DotthzMeasurement
           The `DotthzMeasurement` object that is being added to the dictionary.

        Raises
        ------
        TypeError
           If `value` is not an instance of `DotthzMeasurement`.
        """

        if isinstance(value, DotthzMeasurement):
            value._file = self._file
            value._measurement_name = key
            super().__setitem__(key, value)
            self._file.write_measurement(key, value)

        elif isinstance(value, np.ndarray):
            measurement = self[key]
            measurement.datasets[key] = value  # This now triggers the dataset setter
            self._file.write_measurement(key, measurement)

        else:
            raise TypeError("Value must be a DotthzMeasurement or a numpy array.")

    def __getitem__(self, key):
        return super().__getitem__(key)


@dataclass
class DotthzMeasurement:
    """
    A data class representing a single terahertz measurement.

    This class holds both the metadata and the datasets associated with a measurement.
    It includes automatic persistence support: when either `datasets` or `meta_data` is modified,
    and the measurement is part of a `DotthzFile`, the corresponding file is updated.

    Attributes
    ----------
    _file : DotthzFile, optional
        Reference to the parent `DotthzFile` object. Used to trigger automatic saving.
    _measurement_name : str, optional
        The name of the measurement within the file. Used for file I/O.
    _datasets : dict of str -> np.ndarray
        Dictionary of datasets related to the measurement.
    _meta_data : DotthzMetaData
        Metadata associated with the measurement.
    """

    _file: "DotthzFile" = field(default=None, repr=False, compare=False)
    _measurement_name: str = field(default=None, repr=False, compare=False)

    _datasets: Dict[str, np.ndarray] = field(default_factory=dict, repr=False)
    _meta_data: DotthzMetaData = field(default_factory=DotthzMetaData, repr=False)

    def __str__(self):
        """
        Return a string representation of the measurement, showing its metadata and dataset keys.
        """
        return f"{self._meta_data} {self._datasets}"

    @property
    def datasets(self) -> Dict[str, np.ndarray]:
        """
        Access the datasets of the measurement.

        Returns
        -------
        dict
            Dictionary mapping dataset names to NumPy arrays.
        """
        return self._datasets

    @datasets.setter
    def datasets(self, value: Dict[str, np.ndarray]):
        """
        Set the datasets for the measurement.

        Automatically triggers a write to the associated file if available.

        Parameters
        ----------
        value : dict
            Dictionary of datasets to assign.
        """
        self._datasets = value
        if self._file and self._measurement_name:
            self._file.write_measurement(self._measurement_name, self)

    @property
    def meta_data(self) -> DotthzMetaData:
        """
        Access the metadata of the measurement.

        Returns
        -------
        DotthzMetaData
            The metadata object.
        """
        return self._meta_data

    @meta_data.setter
    def meta_data(self, value: DotthzMetaData):
        """
        Set the metadata for the measurement.

        Automatically triggers a write to the associated file if available.

        Parameters
        ----------
        value : DotthzMetaData
            Metadata object to assign.
        """
        self._meta_data = value
        if self._file and self._measurement_name:
            self._file.write_measurement(self._measurement_name, self)

    def __getitem__(self, key: str) -> np.ndarray:
        """
        Access an individual dataset by name using indexing syntax.

        Parameters
        ----------
        key : str
            The name of the dataset to retrieve.

        Returns
        -------
        np.ndarray
            The requested dataset.
        """
        return self._datasets[key]

    def __setitem__(self, key: str, value: np.ndarray):
        """
        Set or replace an individual dataset by name using indexing syntax.

        Automatically triggers a write to the associated file if available.

        Parameters
        ----------
        key : str
            The name of the dataset.
        value : np.ndarray
            The dataset to assign.
        """
        self._datasets[key] = value
        if self._file and self._measurement_name:
            self._file.write_measurement(self._measurement_name, self)


class DotthzFile:
    """
    Interface for reading, writing, and managing measurements in the `.thz` file format.

    This class provides persistent storage of THz time-domain spectroscopy data via HDF5.
    Measurements are represented using the `DotthzMeasurement` class and organized via a
    dictionary-like interface.

    Supports context manager (`with` statement) for automatic file handling.

    Parameters
    ----------
    name : str
        Path to the `.thz` file.
    mode : str, optional
        File mode: 'r' (read), 'w' (write), or 'a' (append). Default is 'r'.
    **kwds : dict
        Additional keyword arguments passed to `h5py.File`.

    Attributes
    ----------
    file : h5py.File
        Underlying HDF5 file object.
    measurements : MeasurementDict
        Dictionary-like object of `DotthzMeasurement` instances.

    Methods
    -------
    get_measurements()
        Deprecated. Returns all measurements.
    get_measurement(name)
        Deprecated. Returns a measurement by name.
    get_measurement_names()
        Returns list of available measurement names.
    write_measurement(name, measurement)
        Persist a measurement to the file.
    """

    def __init__(self, name, mode="r", driver=None, libver=None,
                 userblock_size=None, swmr=False, rdcc_nslots=None,
                 rdcc_nbytes=None, rdcc_w0=None, track_order=None,
                 fs_strategy=None, fs_persist=False, fs_threshold=1,
                 fs_page_size=None, page_buf_size=None, min_meta_keep=0,
                 min_raw_keep=0, locking=None, alignment_threshold=1,
                 alignment_interval=1, meta_block_size=None, **kwds):
        self._measurements = MeasurementDict(self)
        self.file = h5py.File(name, mode, driver=driver, libver=libver,
                              userblock_size=userblock_size, swmr=swmr,
                              rdcc_nslots=rdcc_nslots, rdcc_nbytes=rdcc_nbytes,
                              rdcc_w0=rdcc_w0, track_order=track_order,
                              fs_strategy=fs_strategy, fs_persist=fs_persist,
                              fs_threshold=fs_threshold,
                              fs_page_size=fs_page_size,
                              page_buf_size=page_buf_size,
                              min_meta_keep=min_meta_keep,
                              min_raw_keep=min_raw_keep, locking=locking,
                              alignment_threshold=alignment_threshold,
                              alignment_interval=alignment_interval,
                              meta_block_size=meta_block_size, **kwds)

        if "r" in mode or "a" in mode:
            self._load(self.file)

    def __enter__(self):
        # Enable the use of the `with` statement.

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Close any resources if applicable.

        if self.file is not None:
            self.file.close()
            self.file = None

    def __getitem__(self, key):
        return self._measurements[key]

    def __setitem__(self, key, value: DotthzMeasurement):
        self._measurements[key] = value
        # self.write_measurement(key, value)

    @property
    def measurements(self):
        return self._measurements

    @measurements.setter
    def measurements(self, value):
        for name, measurement in value.items():
            self._measurements[name] = measurement

    def _get_descriptions(self, desc_in):
        # Handles inconsistent formatting for metadata descriptions.

        desc_in = self._sanatize(desc_in)

        if isinstance(desc_in, str):
            desc_list = [desc.strip() for desc in desc_in.split(",")]
        else:
            if not isinstance(desc_in, Iterable):
                desc_in = [desc_in]

            try:
                desc_list = list(map(str, desc_in))
            except (TypeError, ValueError):
                desc_list = []
                warn("Could not import descriptions.")

        return desc_list

    def _sanatize(self, md_in):
        # Reduces redundant iterables to base data.

        if isinstance(md_in, np.ndarray) and len(md_in) == 1:
            return self._sanatize(md_in[0])
        else:
            return md_in

    def _load(self, file):
        """
        Internal method to load measurements from an existing .thz HDF5 file.

        Parameters
        ----------
        file : h5py.File
            Opened HDF5 file object from which to load data.
        """
        groups = {}
        for group_name, group in file.items():
            measurement = DotthzMeasurement()

            # Load datasets.
            if "dsDescription" in group.attrs:
                ds_description_attr = group.attrs["dsDescription"]
                ds_descriptions = self._get_descriptions(ds_description_attr)

                for i, desc in enumerate(ds_descriptions):
                    dataset_name = f"ds{i + 1}"
                    if dataset_name in group:
                        measurement.datasets[desc] = group[dataset_name]

            # Load metadata attributes.
            for attr in ["description", "date", "instrument",
                         "mode", "time", "thzVer"]:
                if attr in group.attrs:
                    setattr(measurement.meta_data,
                            attr,
                            self._sanatize(group.attrs[attr]))

            # Special handling for user metadata.
            if "user" in group.attrs:
                user_info = self._sanatize(group.attrs["user"])
                if isinstance(user_info, str):
                    user_info = user_info.split("/")
                    fields = ["orcid", "user", "email", "institution"]
                    for i, part in enumerate(user_info):
                        if i < len(fields):
                            setattr(measurement.meta_data, fields[i], part)

            # Lead measurement metadata.
            if "mdDescription" in group.attrs:
                md_description_attr = group.attrs["mdDescription"]
                md_descriptions = self._get_descriptions(md_description_attr)

                for i, desc in enumerate(md_descriptions):
                    md_name = f"md{i + 1}"
                    if md_name in group.attrs:
                        md_val = self._sanatize(group.attrs[md_name])
                        try:
                            measurement.meta_data.md[desc] = float(md_val)
                        except (ValueError, TypeError):
                            measurement.meta_data.md[desc] = md_val

            groups[group_name] = measurement

        self._measurements.update(groups)

    def get_measurements(self):
        """
        Return a dict of all measurements in the file object.

        .. deprecated:: 1.0.0
            Use `file.measurements` instead.
        """
        warnings.warn(
            "get_measurements is deprecated and will be removed in a future version. "
            "Use file.measurements instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.measurements

    def get_measurement_names(self):
        """Return a list of all measurement names in the file object."""
        return list(self._measurements.keys())

    def get_measurement(self, name):
        """Return the specified measurement from the file object.

        .. deprecated:: 1.0.0
            Use `file.measurements[name]` or `file[name]` instead.

        Parameters
        ----------
        name : str
            The name of the measurement.

        Returns
        -------
        DotthzMeasurement
            The requested measurement
        """
        warnings.warn(
            "get_measurement is deprecated and will be removed in a future version. "
            "Use file.measurements[name] or file[name] instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self._measurements.get(name)

    def write_measurement(self, name: str,
                          measurement: DotthzMeasurement):
        """
        Persist a `DotthzMeasurement` instance to the HDF5 file under the given name.

        Handles writing datasets, user metadata, and additional metadata fields.
        Overwrites existing datasets and metadata when applicable.

        Parameters
        ----------
        name : str
            The name under which to store the measurement in the file.
        measurement : DotthzMeasurement
            The measurement object containing datasets and metadata.
        """

        group = self.file[name] if name in self.file else self.file.create_group(name)

        # Write dataset descriptions
        ds_descriptions = ", ".join(measurement.datasets.keys())
        group.attrs["dsDescription"] = ds_descriptions

        # Write datasets
        for i, (name, dataset) in enumerate(measurement.datasets.items()):
            ds_name = f"ds{i + 1}"
            if ds_name in group:
                existing_ds = group[ds_name]
                if existing_ds.shape == dataset.shape and existing_ds.dtype == dataset.dtype:
                    existing_ds[...] = dataset
                else:
                    del group[ds_name]
                    group.create_dataset(ds_name, data=dataset)
            else:
                group.create_dataset(ds_name, data=dataset)

            measurement.datasets[name] = group[ds_name]

        # Write metadata
        for attr_name, attr_value in measurement.meta_data.__dict__.items():
            if attr_name == "md":
                # Write md descriptions as an attribute
                md_descriptions = ", ".join(measurement.meta_data.md.keys())
                group.attrs["mdDescription"] = md_descriptions
                for i, md_val in enumerate(measurement.meta_data.md.values()):
                    md_name = f"md{i + 1}"
                    try:
                        # Attempt to save as float if possible
                        group.attrs[md_name] = float(md_val)
                    except (ValueError, TypeError):
                        group.attrs[md_name] = md_val
            elif attr_name == "version":
                group.attrs["thzVer"] = measurement.meta_data.version

            elif attr_name in ["orcid", "user", "email", "institution"]:
                continue
            else:
                if attr_value:  # Only write non-empty attributes
                    group.attrs[attr_name] = attr_value

        # Write user metadata in the format "ORCID/user/email/institution"
        user_info = "/".join([
            measurement.meta_data.orcid,
            measurement.meta_data.user,
            measurement.meta_data.email,
            measurement.meta_data.institution
        ])
        group.attrs["user"] = user_info
