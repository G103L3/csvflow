"""CSVFlow: A lightweight library for CSV data processing and transformation."""

# Package version
__version__ = "0.1.0"

# Import core modules for convenient access
from .core import CSVFlow
from .transformers import (
    FilterTransformer,
    MapTransformer,
    GroupByTransformer,
    AggregateTransformer,
)

# Public API
__all__ = [
    "CSVFlow",
    "FilterTransformer",
    "MapTransformer",
    "GroupByTransformer",
    "AggregateTransformer",
]