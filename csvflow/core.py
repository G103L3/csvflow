```python
import csv
import io
from typing import List, Dict, Any, Optional, Union, Iterator
from pathlib import Path


class CSVProcessor:
    """Core CSV processing class for reading and basic filtering operations."""
    
    def __init__(self, delimiter: str = ',', quotechar: str = '"', skip_initial_space: bool = True):
        """
        Initialize CSV processor with configuration options.
        
        Args:
            delimiter: Field delimiter character (default: ',')
            quotechar: Quote character (default: '"')
            skip_initial_space: Skip whitespace after delimiter (default: True)
        """
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.skip_initial_space = skip_initial_space
    
    def read_csv(self, source: Union[str, Path, io.TextIOBase]) -> List[Dict[str, str]]:
        """
        Read CSV data from file path or file-like object into list of dictionaries.
        
        Args:
            source: File path (str/Path) or file-like object
            
        Returns:
            List of dictionaries where keys are column headers and values are cell values
            
        Raises:
            FileNotFoundError: If file path doesn't exist
            ValueError: If CSV is malformed or has inconsistent columns
        """
        if isinstance(source, (str, Path)):
            if not isinstance(source, Path):
                source = Path(source)
            if not source.exists():
                raise FileNotFoundError(f"CSV file not found: {source}")
            with open(source, 'r', newline='', encoding='utf-8') as f:
                return self._parse_csv(f)
        else:
            return self._parse_csv(source)
    
    def _parse_csv(self, file_obj: io.TextIOBase) -> List[Dict[str, str]]:
        """Internal method to parse CSV from file object."""
        try:
            reader = csv.DictReader(
                file_obj,
                delimiter=self.delimiter,
                quotechar=self.quotechar,
                skipinitialspace=self.skip_initial_space
            )
            
            # Validate that we have headers
            if reader.fieldnames is None:
                raise ValueError("CSV file has no header row")
            
            rows = []
            for i, row in enumerate(reader):
                # Ensure all expected fields are present
                if len(row) != len(reader.fieldnames):
                    raise ValueError(f"Inconsistent number of columns at row {i+2}")
                rows.append(row)
            
            return rows
        except csv.Error as e:
            raise ValueError(f"Invalid CSV format: {e}")
    
    def filter_rows(
        self,
        data: List[Dict[str, str]],
        conditions: Dict[str, Union[str, int, float, bool, None]]
    ) -> List[Dict[str, str]]:
        """
        Filter rows based on exact field-value matches.
        
        Args:
            data: List of dictionaries representing CSV rows
            conditions: Dictionary mapping column names to target values
            
        Returns:
            Filtered list of rows matching all conditions
        """
        if not data:
            return []
        
        filtered = []
        for row in data:
            match = True
            for field, value in conditions.items():
                if field not in row:
                    match = False
                    break
                # Convert value to string for comparison since CSV values are strings
                if str(row[field]).strip() != str(value).strip():
                    match = False
                    break
            if match:
                filtered.append(row)
        
        return filtered
    
    def filter_rows_by_predicate(
        self,
        data: List[Dict[str, str]],
        predicate: callable
    ) -> List[Dict[str, str]]:
        """
        Filter rows using a custom predicate function.
        
        Args:
            data: List of dictionaries representing CSV rows
            predicate: Function that takes a row dict and returns True/False
            
        Returns:
            Filtered list of rows where predicate returns True
        """
        return [row for row in data if predicate(row)]
    
    def get_column_values(self, data: List[Dict[str, str]], column: str) -> List[str]:
        """
        Extract all values from a specific column.
        
        Args:
            data: List of dictionaries representing CSV rows
            column: Column name to extract
            
        Returns:
            List of string values from the specified column
            
        Raises:
            KeyError: If column doesn't exist in any row
        """
        if not data:
            return []
        
        if column not in data[0]:
            raise KeyError(f"Column '{column}' not found in CSV data")
        
        return [row[column] for row in data]
    
    def get_unique_values(self, data: List[Dict[str, str]], column: str) -> List[str]:
        """
        Get unique values from a specific column.
        
        Args:
            data: List of dictionaries representing CSV rows
            column: Column name to extract unique values from
            
        Returns:
            List of unique string values from the specified column
        """
        values = self.get_column_values(data, column)
        return list(set(values))
    
    def count_by_column(self, data: List[Dict[str, str]], column: str) -> Dict[str, int]:
        """
        Count occurrences of each value in a column.
        
        Args:
            data: List of dictionaries representing CSV rows
            column: Column name to count values from
            
        Returns:
            Dictionary mapping values to their counts
        """
        counts = {}
        for row in data:
            if column in row:
                value = row[column].strip()
                counts[value] = counts.get(value, 0) + 1
        return counts


# Convenience functions for common operations
def read_csv(
    source: Union[str, Path, io.TextIOBase],
    delimiter: str = ',',
    quotechar: str = '"',
    skip_initial_space: bool = True
) -> List[Dict[str, str]]:
    """
    Read CSV file into list of dictionaries.
    
    Args:
        source: File path or file-like object
        delimiter: Field delimiter (default: ',')
        quotechar: Quote character (default: '"')
        skip_initial_space: Skip whitespace after delimiter (default: True)
        
    Returns:
        List of dictionaries representing CSV rows
    """
    processor = CSVProcessor(delimiter, quotechar, skip_initial_space)
    return processor.read_csv(source)


def filter_csv(
    data: List[Dict[str, str]],
    **conditions: Union[str, int, float, bool, None]
) -> List[Dict[str, str]]:
    """
    Filter CSV data by exact field-value matches.
    
    Args:
        data: List of dictionaries representing CSV rows
        **conditions: Keyword arguments mapping column names to values
        
    Returns:
        Filtered list of rows
    """
    processor = CSVProcessor()
    return processor.filter_rows(data, conditions)


def filter_csv_by_predicate(
    data: List[Dict[str, str]],
    predicate: callable
) -> List[Dict[str, str]]:
    """
    Filter CSV data using a custom predicate function.
    
    Args:
        data: List of dictionaries representing CSV rows
        predicate: Function that takes a row dict and returns True/False
        
    Returns:
        Filtered list of rows
    """
    processor = CSVProcessor()
    return processor.filter_rows_by_predicate(data, predicate)
```