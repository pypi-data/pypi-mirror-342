import unittest
import tempfile
import os
from pathlib import Path
from io import StringIO
import numpy as np
from unittest.mock import patch, MagicMock

# Import the classes to test (would normally be from your module)


DATASET_LIST=[
              "anagrams", "anscombe", "attention", "brain_networks", 
              "car_crashes", "diamonds", "dots", "dowjones", "exercise", 
              "flights", "fmri", "geyser", "glue", "healthexp", "iris", "mpg", 
              "penguins", "planets", "seaice", "taxis", "tips", "titanic",
]


from data_retriving_tools import CSVDataConverter, CSVReader, DatasetManager, DatasetLoader

class TestCSVDataConverter(unittest.TestCase):
    def setUp(self):
        self.converter = CSVDataConverter()
    
    def test_is_float(self):
        self.assertTrue(self.converter._is_float("3.14"))
        self.assertTrue(self.converter._is_float("-1.5"))
        self.assertTrue(self.converter._is_float("0"))
        self.assertFalse(self.converter._is_float("abc"))
        self.assertFalse(self.converter._is_float(""))
        self.assertFalse(self.converter._is_float(None))
    
    def test_is_numeric_column(self):
        self.assertTrue(self.converter._is_numeric_column(["1", "2.5", "3"]))
        self.assertTrue(self.converter._is_numeric_column(["1", "NA", "3"]))
        self.assertFalse(self.converter._is_numeric_column(["1", "abc", "3"]))
        self.assertTrue(self.converter._is_numeric_column([]))
    
    def test_convert_to_numeric(self):
        result = self.converter._convert_to_numeric(["1", "2.5", "NA", "3"])
        self.assertTrue(np.isnan(result[2]))
        self.assertEqual(result[0], 1.0)
        self.assertEqual(result[1], 2.5)
        self.assertEqual(result[3], 3.0)
    
    def test_convert_to_object(self):
        result = self.converter._convert_to_object(["a", "NA", "b", None], {"NA"})
        self.assertEqual(result[0], "a")
        self.assertIsNone(result[1])
        self.assertEqual(result[2], "b")
        self.assertIsNone(result[3])
    
    def test_convert_column_numeric(self):
        result = self.converter.convert_column(["1", "2.5", "3"])
        self.assertEqual(result.dtype, np.float64)
    
    def test_convert_column_object(self):
        result = self.converter.convert_column(["a", "b", "c"])
        self.assertEqual(result.dtype, object)
    
    def test_custom_missing_values(self):
        converter = CSVDataConverter(missing_values={"NULL"})
        result = converter.convert_column(["1", "NULL", "3"])
        self.assertTrue(np.isnan(result[1]))

class TestCSVReader(unittest.TestCase):
    def setUp(self):
        self.csv_data = "col1,col2\n1,a\n2.5,b\n3,c"
        self.file_obj = StringIO(self.csv_data)
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w')
        self.temp_file.write(self.csv_data)
        self.temp_file.close()
    
    def tearDown(self):
        os.unlink(self.temp_file.name)
    
    def test_read_from_file_object(self):
        reader = CSVReader()
        header, arrays = reader.read(self.file_obj)
        self.assertEqual(header, ["col1", "col2"])
        self.assertEqual(arrays["col1"].dtype, np.float64)
        self.assertEqual(arrays["col2"].dtype, object)
    
    def test_read_from_file_path(self):
        reader = CSVReader()
        header, arrays = reader.read(self.temp_file.name)
        self.assertEqual(header, ["col1", "col2"])
        self.assertEqual(arrays["col1"].dtype, np.float64)
        self.assertEqual(arrays["col2"].dtype, object)
    
    def test_read_with_skip_header(self):
        reader = CSVReader(skip_header=1)
        header, arrays = reader.read(self.file_obj)
        self.assertEqual(len(arrays["col1"]), 2)  # Skipped one row
    
    def test_read_with_custom_delimiter(self):
        csv_data = "col1;col2\n1;a\n2;b"
        file_obj = StringIO(csv_data)
        reader = CSVReader(delimiter=';')
        header, arrays = reader.read(file_obj)
        self.assertEqual(header, ["col1", "col2"])
    
    def test_read_with_missing_values(self):
        csv_data = "col1,col2\n1,a\nNA,b\n3,c"
        file_obj = StringIO(csv_data)
        reader = CSVReader(missing_values={"NA"})
        _, arrays = reader.read(file_obj)
        self.assertTrue(np.isnan(arrays["col1"][1]))

class TestDatasetManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.manager = DatasetManager(data_cache_path=self.temp_dir)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    @patch('urllib.request.urlopen')
    def test_get_dataset_names(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = b"dataset1\ndataset2\n"
        mock_urlopen.return_value = mock_response
        
        names = self.manager.get_dataset_names()
        self.assertEqual(names, DATASET_LIST)
    
    def test_get_data_cache_path(self):
        # Test with custom path
        manager = DatasetManager(data_cache_path=r"${HOME}/.cache/")
        self.assertTrue(str(manager.data_cache_path).endswith(r"${HOME}/.cache/"))
        
        # Test with None (should use default)
        manager = DatasetManager(data_cache_path=None)
        self.assertTrue(manager.data_cache_path.is_dir())
    
    def test_group_arrays_by_type(self):
        arrays = {
            "num1": np.array([1, 2, 3], dtype=np.float64),
            "num2": np.array([4, 5, 6], dtype=np.int32),
            "str1": np.array(["a", "b", "c"], dtype=object),
            "str2": np.array(["x", "y", "z"], dtype=object),
        }
        grouped = self.manager._group_arrays_by_type(arrays)
        self.assertEqual(len(grouped["numeric"]), 2)
        self.assertEqual(len(grouped["object"]), 2)
        self.assertTrue(all(np.issubdtype(arr.dtype, np.number) for arr in grouped["numeric"]))
        self.assertTrue(all(arr.dtype == object for arr in grouped["object"]))

class TestDatasetLoader(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.loader = DatasetLoader(data_cache_path=self.temp_dir)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    @patch('urllib.request.urlretrieve')
    @patch.object(DatasetManager, 'get_dataset_names')
    def test_load_dataset(self, mock_get_names, mock_urlretrieve):
        # Setup mock
        mock_get_names.return_value = ["test_dataset"]
        
        # Create a temporary CSV file that would be "downloaded"
        csv_path = Path(self.temp_dir) / "test_dataset.csv"
        with open(csv_path, 'w') as f:
            f.write("col1,col2\n1,a\n2,b\n3,c")
        
        # Test loading
        result = self.loader.load_dataset("test_dataset")
        
        # Verify results
        self.assertIn("numeric", result)
        self.assertIn("object", result)
        self.assertEqual(len(result["numeric"]), 1)
        self.assertEqual(len(result["object"]), 1)
        self.assertEqual(result["numeric"][0].dtype, np.float64)
        self.assertEqual(result["object"][0].dtype, object)
        
        # Verify urlretrieve was called
        mock_urlretrieve.assert_called_once()
    
    @patch('urllib.request.urlretrieve')
    @patch.object(DatasetManager, 'get_dataset_names')
    def test_load_unknown_dataset(self, mock_get_names, mock_urlretrieve):
        mock_get_names.return_value = ["known_dataset"]
        
        with self.assertRaises(ValueError):
            self.loader.load_dataset("unknown_dataset")
        
        mock_urlretrieve.assert_not_called()
    
    def test_load_with_custom_parameters(self):
        # Create a test CSV with custom delimiter
        csv_path = Path(self.temp_dir) / "custom.csv"
        with open(csv_path, 'w') as f:
            f.write("col1;col2\n1;a\n2;b")
        
        # Mock that this dataset is "known"
        with patch.object(DatasetManager, 'get_dataset_names', return_value=["custom"]):
            result = self.loader.load_dataset("custom", delimiter=';')
        
        self.assertEqual(len(result["numeric"]), 1)
        self.assertEqual(len(result["object"]), 1)

if __name__ == '__main__':
    unittest.main()