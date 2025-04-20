import csv
import os
import typing
from collections import defaultdict
from pathlib import Path
from urllib.request import urlopen, urlretrieve
from platformdirs import user_cache_dir

import numpy as np

FilePath = typing.Union[str, os.PathLike]
Url = str
ArrayDict = typing.Dict[str, np.ndarray]
GroupedArrays = typing.Dict[str, typing.List[np.ndarray]]
Header = typing.List[str]

class CSVDataConverter:
    
    @staticmethod
    def _convert_to_object(column_data: typing.List[typing.Optional[str]], missing_values: typing.Set[str]) -> np.ndarray:
        object_values = [None if (v is None or v in missing_values) else v for v in column_data]
        return np.array(object_values, dtype=object)

    @staticmethod
    def _is_float(value: any) -> bool:
        from contextlib import suppress
        with suppress(ValueError):
            float(value)
            return True
        return False

    def __init__(self, missing_values: typing.Set[str] = None) -> None:
        self.DEFAULT_MISSING_VALUES = {"", "NA", "N/A", "NaN", "nan"}
        self.missing_values = missing_values if missing_values else self.DEFAULT_MISSING_VALUES
    
    def _is_numeric_column(self, column_data: typing.List[typing.Optional[str]]) -> bool:
        for value in column_data:
            if value is None or value in self.missing_values:
                continue
            if not self._is_float(value):
                return False
        return True
    
    def _convert_to_numeric(self, column_data: typing.List[typing.Optional[str]]) -> np.ndarray:
        numeric_values = []
        for value in column_data:
            if value is None or value in self.missing_values:
                numeric_values.append(np.nan)
            else:
                numeric_values.append(float(value))
        return np.array(numeric_values, dtype=np.float64)
    
    def convert_column(self, column_data: typing.List[typing.Optional[str]]) -> np.ndarray:
        if self._is_numeric_column(column_data):
            return self._convert_to_numeric(column_data)
        return self._convert_to_object(column_data, self.missing_values)

class CSVReader:
    def __init__(self, delimiter: str = ',', skip_header: int = 0, missing_values: typing.Set[str] = None):
        self.delimiter = delimiter
        self.skip_header = skip_header
        self.converter = CSVDataConverter(missing_values)
    
    def read(self, source: typing.Union[FilePath, typing.TextIO]) -> typing.Tuple[Header, ArrayDict]:
        header = []
        columns_data = defaultdict(list)
        
        if isinstance(source, (str, os.PathLike)):
            with open(source, 'r', encoding='utf-8', newline='') as f:
                self._process_file(f, header, columns_data)
        elif hasattr(source, 'read'):
            self._process_file(source, header, columns_data)
        
        numpy_arrays = {
            col_name: self.converter.convert_column(column_data)
            for col_name, column_data in columns_data.items()
        }
        
        return header, numpy_arrays
    
    def _process_file(self, file_obj, header: Header, columns_data: defaultdict):
        reader = csv.reader(file_obj, delimiter=self.delimiter)
        header.extend(next(reader))
        
        for _ in range(self.skip_header):
            next(reader)
            
        for row in reader:
            if len(row) != len(header):
                continue
            for col_name, value in zip(header, row):
                columns_data[col_name].append(value.strip() if value else "")

class DatasetManager:
    def __init__(self, data_cache_path: typing.Optional[FilePath] = 'funJplot-cache'):
        self.DATASET_SOURCE = "https://raw.githubusercontent.com/s0SimoneP0s/dataset/refs/heads/main"
        self.DATASET_NAMES_URL = f"{self.DATASET_SOURCE}/dataset_names.txt"
        self.data_cache_path = self._get_data_cache_path(data_cache_path)
    
    def _get_data_cache_path(self, data_cache_path: typing.Optional[FilePath]) -> Path:
        if data_cache_path is None:
            data_cache_path_str = os.environ.get("EXAMPLE_DATASET", user_cache_dir("fanJplot-dataset", "fanJplot"))
        else:
            data_cache_path_str = str(data_cache_path)
        
        resolved_path = Path(data_cache_path_str).expanduser()
        resolved_path.mkdir(parents=True, exist_ok=True)
        return resolved_path
    
    def get_dataset_names(self) -> typing.List[str]:
        with urlopen(self.DATASET_NAMES_URL, timeout=5) as resp:
            txt = resp.read().decode('utf-8')
        dataset_names = [name.strip() for name in txt.splitlines()]
        return list(filter(None, dataset_names))
    
    def _group_arrays_by_type(self, arrays_dict: ArrayDict) -> GroupedArrays:
        grouped = defaultdict(list)
        for array in arrays_dict.values():
            if np.issubdtype(array.dtype, np.number):
                grouped['numeric'].append(array)
            else:
                grouped['object'].append(array)
        return dict(grouped)

class DatasetLoader:
    def __init__(self, data_cache_path: typing.Optional[FilePath] = 'funJplot-cache'):
        self.manager = DatasetManager(data_cache_path)
    
    def load_dataset( self, name: str, cache: bool = True, **kws: typing.Any  ) -> GroupedArrays:
        csv_kws = {
            'delimiter': kws.get('delimiter', ','),
            'skip_header': kws.get('skip_header', 0),
            'missing_values': kws.get('missing_values', None)
        }
        
        url = f"{self.manager.DATASET_SOURCE}/{name}.csv"
        cache_path = self.manager.data_cache_path / f"{name}.csv"
        
        if cache or not cache_path.exists():
            available_datasets = self.manager.get_dataset_names()
            if name not in available_datasets and not cache_path.exists():
                raise ValueError(f"'{name}' is not a known dataset")
            
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            urlretrieve(url, cache_path)
        
        reader = CSVReader(**csv_kws)
        _, arrays_dict = reader.read(cache_path)
        
        return self.manager._group_arrays_by_type(arrays_dict)

if __name__ == '__main__':
    loader = DatasetLoader()
    data = loader.load_dataset("dowjones")
    print(data)