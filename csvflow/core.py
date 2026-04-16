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
            conditions: Dictionary mapping column names to target values for filtering
            
        Returns:
            Filtered list of dictionaries matching all conditions
            
        Note:
            String comparisons are case-insensitive. For case-sensitive matching,
            use the more advanced filter_rows_advanced method.
        """
        if not data:
            return []
        
        filtered = []
        for row in data:
            match = True
            for column, target_value in conditions.items():
                if column not in row:
                    match = False
                    break
                
                cell_value = row[column]
                
                # Handle string comparisons case-insensitively
                if isinstance(target_value, str) and isinstance(cell_value, str):
                    if cell_value.lower() != target_value.lower():
                        match = False
                        break
                else:
                    # For non-string types, use exact equality
                    if cell_value != target_value:
                        match = False
                        break
            
            if match:
                filtered.append(row)
        
        return filtered
```