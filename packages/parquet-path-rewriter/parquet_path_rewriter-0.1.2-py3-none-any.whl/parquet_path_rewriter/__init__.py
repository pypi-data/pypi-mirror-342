"""
Parquet Path Rewriter Library
-----------------------------

A tool to modify Python code by rewriting relative paths in '.parquet()' calls
to be based on a specified root directory using Abstract Syntax Trees (AST).
"""

__version__ = "0.1.1"

from .rewriter import ParquetPathRewriter, rewrite_parquet_paths_in_code

# Define what gets imported with 'from parquet_path_rewriter import *'
# (Though explicit imports are generally preferred)
__all__ = [
    "ParquetPathRewriter",
    "rewrite_parquet_paths_in_code",
    "__version__",
]