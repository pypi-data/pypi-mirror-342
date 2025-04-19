import unittest
from pydotthz import DotthzFile, DotthzMeasurement, DotthzMetaData
import numpy as np
from tempfile import NamedTemporaryFile
from pathlib import Path
import os


class TestDotthzFile(unittest.TestCase):

    def test_copy_and_compare_dotthz_files(self):
        root = Path(__file__).parent
        paths = [root.joinpath("test_files", "PVDF_520um.thz"),
                 root.joinpath("test_files", "2_VariableTemperature.thz")]
        for path in paths:
            # Create a temporary file to save the copy
            with NamedTemporaryFile(delete=False) as temp_file:
                copy_file_path = temp_file.name

            # Load data from the original file
            with DotthzFile(path) as original_dotthz_file, DotthzFile(copy_file_path, "w") as copied_dotthz_file:
                # test writing all measurements at once
                original_measurements = original_dotthz_file.measurements
                copied_dotthz_file.measurements = original_measurements

            # Load data from the new copy file
            with DotthzFile(path) as original_dotthz_file, DotthzFile(copy_file_path) as copied_dotthz_file:
                original_measurements = original_dotthz_file.measurements
                # Compare the original and copied Dotthz structures
                self.assertEqual(len(original_measurements), len(copied_dotthz_file.measurements))

                for group_name, original_measurement in original_measurements.items():
                    copied_measurement = copied_dotthz_file.measurements[group_name]
                    self.assertIsNotNone(copied_measurement)

                    # Compare metadata fields
                    self.assertEqual(original_measurement.meta_data.user, copied_measurement.meta_data.user)
                    self.assertEqual(original_measurement.meta_data.email, copied_measurement.meta_data.email)
                    self.assertEqual(original_measurement.meta_data.orcid, copied_measurement.meta_data.orcid)
                    self.assertEqual(original_measurement.meta_data.institution,
                                     copied_measurement.meta_data.institution)
                    self.assertEqual(original_measurement.meta_data.description,
                                     copied_measurement.meta_data.description)
                    self.assertEqual(original_measurement.meta_data.version, copied_measurement.meta_data.version)
                    self.assertEqual(original_measurement.meta_data.mode, copied_measurement.meta_data.mode)
                    self.assertEqual(original_measurement.meta_data.instrument, copied_measurement.meta_data.instrument)
                    self.assertEqual(original_measurement.meta_data.time, copied_measurement.meta_data.time)
                    self.assertEqual(original_measurement.meta_data.date, copied_measurement.meta_data.date)

                    # Compare metadata key-value pairs
                    self.assertEqual(original_measurement.meta_data.md, copied_measurement.meta_data.md)

                    # Compare datasets
                    self.assertEqual(len(original_measurement.datasets), len(copied_measurement.datasets))
                    for dataset_name, original_dataset in original_measurement.datasets.items():
                        copied_dataset = copied_measurement.datasets.get(dataset_name)
                        self.assertIsNotNone(copied_dataset)
                        np.testing.assert_array_equal(original_dataset, copied_dataset)

            # Clean up temporary file
            os.remove(copy_file_path)

    def test_dotthz_save_and_load(self):
        with NamedTemporaryFile(delete=False) as temp_file:
            path = temp_file.name

        # Initialize test data for Dotthz
        datasets = {
            "ds1": np.array([[1.0, 2.0], [3.0, 4.0]], dtype=np.float32)
        }

        # create deep copy
        original_datasets = {key: val for key, val in datasets.items()}

        meta_data = DotthzMetaData(
            user="Test User",
            email="test@example.com",
            orcid="0000-0001-2345-6789",
            institution="Test Institute",
            description="Test description",
            md={"md1": "Thickness (mm)"},
            version="1.00",
            mode="Test mode",
            instrument="Test instrument",
            time="12:34:56",
            date="2024-11-08"
        )

        with DotthzFile(path, "w") as file_to_write:
            # test writing measurement by measurement
            file_to_write.measurements["Measurement 1"] = DotthzMeasurement()
            file_to_write.measurements["Measurement 1"].meta_data = meta_data
            file_to_write.measurements["Measurement 1"].datasets = datasets

        # Load from the temporary file
        with DotthzFile(path) as loaded_file:
            # Compare original and loaded data
            self.assertEqual(1, len(loaded_file.measurements))

            loaded_measurement = loaded_file.measurements["Measurement 1"]
            self.assertIsNotNone(loaded_measurement)

            # Compare metadata fields
            self.assertEqual(meta_data.user, loaded_measurement.meta_data.user)
            self.assertEqual(meta_data.email, loaded_measurement.meta_data.email)
            self.assertEqual(meta_data.orcid, loaded_measurement.meta_data.orcid)
            self.assertEqual(meta_data.institution, loaded_measurement.meta_data.institution)
            self.assertEqual(meta_data.description, loaded_measurement.meta_data.description)
            self.assertEqual(meta_data.version, loaded_measurement.meta_data.version)
            self.assertEqual(meta_data.mode, loaded_measurement.meta_data.mode)
            self.assertEqual(meta_data.instrument, loaded_measurement.meta_data.instrument)
            self.assertEqual(meta_data.time, loaded_measurement.meta_data.time)
            self.assertEqual(meta_data.date, loaded_measurement.meta_data.date)

            # Compare metadata's key-value pairs
            self.assertEqual(meta_data.md, loaded_measurement.meta_data.md)

            # Compare datasets
            self.assertEqual(len(original_datasets), len(loaded_measurement.datasets))
            for dataset_name, dataset in original_datasets.items():
                loaded_dataset = loaded_measurement.datasets.get(dataset_name)
                self.assertIsNotNone(loaded_dataset)
                np.testing.assert_array_equal(dataset, loaded_dataset)

        # Clean up temporary file
        os.remove(path)

    def test_dotthz_key(self):
        with NamedTemporaryFile(delete=False) as temp_file:
            path = temp_file.name

        # Initialize test data for Dotthz
        datasets = {
            "ds1": np.array([[1.0, 2.0], [3.0, 4.0]], dtype=np.float32)
        }

        # create deep copy
        original_datasets = {key: val for key, val in datasets.items()}

        meta_data = DotthzMetaData(
            user="Test User",
            email="test@example.com",
            orcid="0000-0001-2345-6789",
            institution="Test Institute",
            description="Test description",
            md={"md1": "Thickness (mm)"},
            version="1.00",
            mode="Test mode",
            instrument="Test instrument",
            time="12:34:56",
            date="2024-11-08"
        )

        with DotthzFile(path, "w") as file_to_write:
            file_to_write.measurements["Measurement 1"] = DotthzMeasurement()
            file_to_write.measurements["Measurement 1"].meta_data = meta_data
            file_to_write.measurements["Measurement 1"].datasets = datasets

        # Load from the temporary file
        with DotthzFile(path) as loaded_file:
            # Compare original and loaded data
            self.assertEqual(1, len(loaded_file.measurements))

            loaded_measurement = loaded_file["Measurement 1"]
            self.assertIsNotNone(loaded_measurement)

            # Compare metadata fields
            self.assertEqual(meta_data.user, loaded_measurement.meta_data.user)
            self.assertEqual(meta_data.email, loaded_measurement.meta_data.email)
            self.assertEqual(meta_data.orcid, loaded_measurement.meta_data.orcid)
            self.assertEqual(meta_data.institution, loaded_measurement.meta_data.institution)
            self.assertEqual(meta_data.description, loaded_measurement.meta_data.description)
            self.assertEqual(meta_data.version, loaded_measurement.meta_data.version)
            self.assertEqual(meta_data.mode, loaded_measurement.meta_data.mode)
            self.assertEqual(meta_data.instrument, loaded_measurement.meta_data.instrument)
            self.assertEqual(meta_data.time, loaded_measurement.meta_data.time)
            self.assertEqual(meta_data.date, loaded_measurement.meta_data.date)

            # Compare metadata's key-value pairs
            self.assertEqual(meta_data.md, loaded_measurement.meta_data.md)

            # Compare datasets
            self.assertEqual(len(original_datasets), len(loaded_measurement.datasets))
            for dataset_name, dataset in original_datasets.items():
                loaded_dataset = loaded_measurement.datasets[dataset_name]
                self.assertIsNotNone(loaded_dataset)
                np.testing.assert_array_equal(dataset, loaded_dataset)

        # Clean up temporary file
        os.remove(path)

    def test_dotthz_extend_existing_dataset(self):
        with NamedTemporaryFile(delete=False) as temp_file:
            path = temp_file.name

        # Initialize test data for Dotthz
        datasets = {
            "ds1": np.array([[1.0, 2.0], [3.0, 4.0]], dtype=np.float32)
        }
        meta_data = DotthzMetaData(
            user="Test User",
            email="test@example.com",
            orcid="0000-0001-2345-6789",
            institution="Test Institute",
            description="Test description",
            md={"md1": "Thickness (mm)"},
            version="1.00",
            mode="Test mode",
            instrument="Test instrument",
            time="12:34:56",
            date="2024-11-08"
        )

        with DotthzFile(path, "w") as file_to_write:
            file_to_write.measurements["Measurement 1"] = DotthzMeasurement()
            file_to_write.measurements["Measurement 1"].meta_data = meta_data
            file_to_write.measurements["Measurement 1"].datasets = datasets
            file_to_write.measurements["Measurement 1"]["ds1"][0, 0] = 0.0

        # Load from the temporary file
        with DotthzFile(path) as loaded_file:
            # Compare original and loaded data
            self.assertEqual(1, len(loaded_file.measurements))

            for group_name, measurement in file_to_write.measurements.items():
                loaded_measurement = loaded_file[group_name]

                self.assertIsNotNone(loaded_measurement)
                self.assertIsNotNone(measurement)

                # Compare metadata fields
                self.assertEqual(measurement.meta_data.user, loaded_measurement.meta_data.user)
                self.assertEqual(measurement.meta_data.email, loaded_measurement.meta_data.email)
                self.assertEqual(measurement.meta_data.orcid, loaded_measurement.meta_data.orcid)
                self.assertEqual(measurement.meta_data.institution, loaded_measurement.meta_data.institution)
                self.assertEqual(measurement.meta_data.description, loaded_measurement.meta_data.description)
                self.assertEqual(measurement.meta_data.version, loaded_measurement.meta_data.version)
                self.assertEqual(measurement.meta_data.mode, loaded_measurement.meta_data.mode)
                self.assertEqual(measurement.meta_data.instrument, loaded_measurement.meta_data.instrument)
                self.assertEqual(measurement.meta_data.time, loaded_measurement.meta_data.time)
                self.assertEqual(measurement.meta_data.date, loaded_measurement.meta_data.date)

                # Compare metadata's key-value pairs
                self.assertEqual(measurement.meta_data.md, loaded_measurement.meta_data.md)

                # Compare datasets
                self.assertEqual(len(measurement.datasets), len(loaded_measurement.datasets))

                for dataset_name, dataset in measurement.datasets.items():
                    loaded_dataset = loaded_measurement.datasets[dataset_name]
                    self.assertIsNotNone(loaded_dataset)
                    np.testing.assert_array_equal(loaded_dataset, np.array([[0.0, 2.0], [3.0, 4.0]], dtype=np.float32))

        # Clean up temporary file
        os.remove(path)

    def test_dotthz_extend_existing_measurement(self):
        with NamedTemporaryFile(delete=False) as temp_file:
            path = temp_file.name

        # Initialize test data for Dotthz

        meta_data = DotthzMetaData(
            user="Test User",
            email="test@example.com",
            orcid="0000-0001-2345-6789",
            institution="Test Institute",
            description="Test description",
            md={"md1": "Thickness (mm)"},
            version="1.00",
            mode="Test mode",
            instrument="Test instrument",
            time="12:34:56",
            date="2024-11-08"
        )

        measurements = {
            "Measurement 1": DotthzMeasurement()
        }

        with DotthzFile(path, "w") as file_to_write:
            for name, measurement in measurements.items():
                file_to_write.measurements[name] = measurement
                file_to_write.measurements[name].meta_data = meta_data
                file_to_write.measurements[name]["ds1"] = np.array([[1.0, 2.0], [3.0, 4.0]], dtype=np.float32)
                file_to_write.measurements[name]["ds2"] = np.array([[1.0, 2.0], [3.0, 4.0]], dtype=np.float32)

        with DotthzFile(path, "r+") as file_to_extend:
            file_to_extend.measurements["Measurement 2"] = DotthzMeasurement()

        # Load from the temporary file
        with DotthzFile(path) as loaded_file:
            # Compare original and loaded data
            self.assertEqual(2, len(loaded_file.measurements))

            loaded_measurement = loaded_file["Measurement 1"]
            self.assertIsNotNone(loaded_measurement)

            # Compare metadata fields
            self.assertEqual(measurement.meta_data.user, loaded_measurement.meta_data.user)
            self.assertEqual(measurement.meta_data.email, loaded_measurement.meta_data.email)
            self.assertEqual(measurement.meta_data.orcid, loaded_measurement.meta_data.orcid)
            self.assertEqual(measurement.meta_data.institution, loaded_measurement.meta_data.institution)
            self.assertEqual(measurement.meta_data.description, loaded_measurement.meta_data.description)
            self.assertEqual(measurement.meta_data.version, loaded_measurement.meta_data.version)
            self.assertEqual(measurement.meta_data.mode, loaded_measurement.meta_data.mode)
            self.assertEqual(measurement.meta_data.instrument, loaded_measurement.meta_data.instrument)
            self.assertEqual(measurement.meta_data.time, loaded_measurement.meta_data.time)
            self.assertEqual(measurement.meta_data.date, loaded_measurement.meta_data.date)

            # Compare metadata's key-value pairs
            self.assertEqual(measurement.meta_data.md, loaded_measurement.meta_data.md)

            # Compare datasets
            self.assertEqual(2, len(loaded_measurement.datasets))

            for dataset_name, dataset in measurement.datasets.items():
                loaded_dataset = loaded_measurement.datasets[dataset_name]
                self.assertIsNotNone(loaded_dataset)
                np.testing.assert_array_equal(np.array([[1.0, 2.0], [3.0, 4.0]], dtype=np.float32), loaded_dataset)

        # Clean up temporary file
        os.remove(path)


if __name__ == "__main__":
    unittest.main()
