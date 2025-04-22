# Parquet Path Rewriter

[![PyPI version](https://badge.fury.io/py/parquet-path-rewriter.svg)](https://badge.fury.io/py/parquet-path-rewriter)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python library to automatically rewrite Parquet file paths within Python code strings.  
It uses Abstract Syntax Tree (AST) manipulation to find calls like:

- `spark.read.parquet('relative/path')`
- `df.write.parquet(path='other/path')`

and rewrites the path to match a desired environment—either a **local base directory** or a **custom S3 prefix**—without modifying the original source code manually.

This is especially useful when adapting code for different runtime environments (e.g., local, cloud, production clusters), allowing you to inject absolute paths or cloud paths without altering the original logic.

---

## Features

- ✅ Detects `.parquet()` method calls using heuristic pattern matching (e.g., `.read.parquet()`, `.write.parquet()`).
- 🔍 Rewrites paths passed as:
  - First positional argument: `parquet('path/to/file')`
  - Keyword argument: `parquet(path='path/to/file')`
- 📦 Automatically appends `.parquet` if the original path omits the extension.
- 📁 Prepends a local `base_path` (string or `pathlib.Path`) for file system rewrites.
- ☁️ Optionally rewrites `s3://...` URIs to a new `s3_rewrite_prefix`, resulting in:  
  `s3://bucket/tmp/data/<filename>.parquet`
- 🛡️ Ignores:
  - Absolute paths (`/data/file.parquet`, `s3://bucket/...`) unless explicitly rewritten via S3 prefix
  - Non-literal paths (e.g., variables, f-strings, function calls)
- 🔄 Keeps track of:
  - Rewritten paths as `{ original_path: new_path }`
  - Input paths (read operations) for metadata or lineage tracking
- 🧠 Safely rewrites code using Python’s built-in `ast` module
- 📜 Supports fallback to `astunparse` (for Python < 3.9) if `ast.unparse` is unavailable
- ⚠️ Handles internal edge cases:
  - Ensures `args` are mutable lists before rewriting
  - Prints warnings when path rewriting fails due to invalid characters or OS restrictions

---

## Use Case Examples

- Adapt hardcoded Spark code to run in different environments (e.g., dev, test, prod)
- Convert relative paths in notebooks to absolute S3 URIs before execution
- Preprocess source code strings in LLMs, code linters, or static analyzers

## Installation

```bash
pip install parquet-path-rewriter
```

## Usage

The primary way to use the library is through the rewrite_parquet_paths_in_code function.

```python
from pathlib import Path
# Make sure src is in path if running directly without installation
# sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))

from parquet_path_rewriter import rewrite_parquet_paths_in_code

# --- Example Code ---
# Simulate a Python script that uses Spark or Pandas to read/write Parquet
original_python_code = """
import pyspark.sql

# Assume spark session is created elsewhere
# spark = SparkSession.builder.appName("ETLExample").getOrCreate()

print("Starting ETL process...")

# Read input data
customers_df = spark.read.parquet("raw_data/customers")
orders_df = spark.read.parquet(path="raw_data/orders_2023")

# Some transformations (placeholder)
processed_df = customers_df.join(orders_df, "customer_id")

# Write intermediate results
processed_df.write.mode("overwrite").parquet("staging/customer_orders")

# Read another input for final step
products_df = spark.read.parquet('reference_data/products.parquet')

# Final join and write output
final_df = processed_df.join(products_df, "product_id")
output_path = "final_output/report_data" # Not a literal in call
final_df.write.mode("overwrite").parquet(path="final_output/report_data") # Uses keyword

# Example with an absolute path (should not be changed)
logs_df = spark.read.parquet("/mnt/shared/logs/app_logs.parquet")

# S3 example (should be rewritten)
s3_df = spark.read.parquet("s3://mybucket/data/2023/spark_logs")

# Write to S3 (should be rewritten)
s3_df.write.mode("overwrite").parquet("s3://mybucket/output/processed_logs")

print("ETL process finished.")
"""

# --- Library Usage ---

# Define the base directory where the relative paths should point
# This would typically be determined by your execution environment or configuration
# Use absolute paths for clarity
data_root_directory = Path("/user/project/data").resolve()

s3_rewrite_prefix = "s3://newbucket/data/2023"

print("-" * 30)
print(f"Base Path: {data_root_directory}")
print("-" * 30)
print("Original Code:")
print(original_python_code)
print("-" * 30)

try:
    # Call the library function to rewrite the code
    modified_code, rewritten_map, identified_inputs = rewrite_parquet_paths_in_code(
        code_string=original_python_code, base_path=data_root_directory, s3_rewrite_prefix=s3_rewrite_prefix
    )

    print("Modified Code:")
    print(modified_code)
    print("-" * 30)

    print("Rewritten Paths (Original -> New):")
    if rewritten_map:
        for original, new in rewritten_map.items():
            print(f"  '{original}' -> '{new}'")
    else:
        print("  No paths were rewritten.")
    print("-" * 30)

    print("Identified Input Paths (Original):")
    if identified_inputs:
        for path in identified_inputs:
            print(f"  '{path}'")
    else:
        print("  No input paths were identified.")
    print("-" * 30)

except SyntaxError as e:
    print(f"\nError: Invalid Python syntax in the input code.\n{e}")
except TypeError as e:
    print(f"\nError: Invalid base_path provided.\n{e}")
except Exception as e:
    print(f"\nAn unexpected error occurred: {e}")

```

## How it Works

The library parses the input Python code string into an Abstract Syntax Tree (AST) using Python's built-in `ast` module. It then walks through this tree using a custom `ast.NodeTransformer`. When it encounters a function call node:

1. It checks if the called attribute is named `parquet`.

2. It analyzes the call chain (e.g., `spark.read.parquet`) to heuristically determine whether it's a **read** or **write** operation.

3. It searches for a string literal path in the arguments (either as the first positional argument or as a keyword argument like `path='...'`).

4. If a valid path string is found, the path is transformed based on the configuration:

   - If the path is **relative**, it is rewritten to:  
     `base_path / <filename>.parquet`
   - If the path is an **S3 URI** and `s3_rewrite_prefix` is provided, it is rewritten to:  
     `<s3_rewrite_prefix>/<filename>.parquet`
   - If the path is **absolute** (e.g., `/data/file.parquet` or starts with `s3://`) and does not match the rewrite criteria, it is left untouched.

5. It replaces the original path node in the AST with a new node containing the modified path string.

6. Finally, the modified AST is converted back into a Python code string using `ast.unparse()` (Python 3.9+).

## Limitations

- **Call Pattern Specificity:** Only identifies calls where the method name is directly `.parquet(...)`. It does **not** currently support more dynamic usage like `spark.read.format("parquet").load("...")`. Extending this requires deeper AST pattern matching.

- **String Literals Only:** Only rewrites paths passed as **direct string literals** (e.g., `'path/to/file'`, `"data/file"`). It **ignores** paths built via variables, f-strings, or function returns.

- **Heuristic Read/Write Detection:** Read vs. write detection is **heuristic**, based on checking if `read` or `write` exists in the call chain. While it works for typical Spark/Pandas patterns, it might not apply universally.

- **AST Unparsing:** Relies on `ast.unparse` (Python 3.9+) to reconstruct the modified code. If using Python <3.9, consider using [`astunparse`](https://pypi.org/project/astunparse/). Minor formatting differences in the output code may occur.

## Contributing

Contributions are welcome! If you encounter a bug or have an enhancement idea, feel free to [open an issue](https://github.com/dmux/parquet-path-rewriter/issues) or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
