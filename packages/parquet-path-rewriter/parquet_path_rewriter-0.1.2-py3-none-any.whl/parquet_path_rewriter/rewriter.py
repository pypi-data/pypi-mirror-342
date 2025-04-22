"""
Core implementation for rewriting Parquet paths in Python code using AST.

This module defines the `ParquetPathRewriter` class, an `ast.NodeTransformer`
that traverses Python code's Abstract Syntax Tree (AST) to find and modify
string literals used as paths in '.parquet()' method calls. It also provides
a helper function `rewrite_parquet_paths_in_code` for easier usage.
"""

import ast
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Union

# Define a specific type for AST string constants for clarity
AstStringConstant = (
    ast.Constant  # In Python 3.8+, ast.Constant replaces ast.Str, ast.Num etc.
)


class ParquetPathRewriter(ast.NodeTransformer):
    """
    Traverses a Python Abstract Syntax Tree (AST) and rewrites string literal
    arguments in calls to '.parquet()' methods.

    It modifies paths to be rooted within a specified base directory or S3 prefix,
    preserving the original filename component and adding `.parquet` extension.

    Attributes:
        base_path: Local directory path used for rewriting.
        s3_rewrite_prefix: Optional prefix like 's3://bucket/tmp/data' for S3 rewrites.
        rewritten_paths: A dictionary mapping original path strings to new path strings.
        identified_inputs: A list of path strings used in read operations.
    """

    def __init__(
        self,
        base_path: Path,
        s3_rewrite_prefix: Optional[str] = None,
    ):
        if not isinstance(base_path, Path):
            raise TypeError("base_path must be a pathlib.Path object")
        self.base_path = base_path.resolve()
        self.s3_rewrite_prefix = (
            s3_rewrite_prefix.rstrip("/") if s3_rewrite_prefix else None
        )
        self.rewritten_paths: Dict[str, str] = {}
        self.identified_inputs: List[str] = []

    def _is_parquet_call(self, node: ast.Call) -> bool:
        return isinstance(node.func, ast.Attribute) and node.func.attr == "parquet"

    def _analyze_call_chain(self, node: ast.Call) -> Tuple[bool, bool]:
        is_read = False
        is_write = False
        current_expr = node.func
        call_chain_parts: List[str] = []

        while isinstance(current_expr, ast.Attribute):
            call_chain_parts.insert(0, current_expr.attr)
            current_expr = current_expr.value

        if isinstance(current_expr, ast.Name):
            call_chain_parts.insert(0, current_expr.id)

        if "read" in call_chain_parts:
            is_read = True
        if "write" in call_chain_parts:
            is_write = True

        return is_read, is_write

    def _find_path_argument(
        self, node: ast.Call
    ) -> Tuple[Optional[AstStringConstant], Optional[int], bool]:
        path_arg_node: Optional[AstStringConstant] = None
        arg_index: Optional[int] = None
        is_keyword = False

        if (
            node.args
            and isinstance(node.args[0], AstStringConstant)
            and isinstance(node.args[0].value, str)
        ):
            path_arg_node = node.args[0]
            arg_index = 0
            is_keyword = False
        else:
            for i, kw in enumerate(node.keywords):
                if (
                    kw.arg == "path"
                    and isinstance(kw.value, AstStringConstant)
                    and isinstance(kw.value.value, str)
                ):
                    path_arg_node = kw.value
                    arg_index = i
                    is_keyword = True
                    break

        return path_arg_node, arg_index, is_keyword

    def visit_Call(self, node: ast.Call) -> ast.AST:
        if not self._is_parquet_call(node):
            return self.generic_visit(node)

        is_read, _is_write = self._analyze_call_chain(node)
        path_arg_node, arg_index, is_keyword = self._find_path_argument(node)

        if path_arg_node is not None and arg_index is not None:
            original_path_str: str = path_arg_node.value
            original_path = Path(original_path_str)
            should_rewrite = (
                original_path_str
                and not original_path.is_absolute()
                and not original_path_str.startswith(str(self.base_path))
            )

            if should_rewrite:
                try:
                    filename = original_path.name
                    final_filename = (
                        f"{filename}.parquet"
                        if not filename.endswith(".parquet")
                        else filename
                    )

                    if self.s3_rewrite_prefix:
                        new_path_str = f"{self.s3_rewrite_prefix}/{final_filename}"
                    else:
                        new_path = self.base_path / final_filename
                        new_path_str = str(new_path)

                    self.rewritten_paths[original_path_str] = new_path_str
                    if is_read:
                        self.identified_inputs.append(original_path_str)

                    new_const_node = ast.Constant(value=new_path_str)
                    ast.copy_location(new_const_node, path_arg_node)

                    if is_keyword:
                        node.keywords[arg_index].value = new_const_node
                    else:
                        if not isinstance(node.args, list):
                            node.args = list(node.args)
                        node.args[arg_index] = new_const_node

                except (TypeError, ValueError) as e:
                    print(
                        f"Warning: Could not process path '{original_path_str}'. Error: {e}"
                    )

        return self.generic_visit(node)


def rewrite_parquet_paths_in_code(
    code_string: str,
    base_path: Union[str, Path],
    *,
    s3_rewrite_prefix: Optional[str] = None,
    filename: str = "<string>",
) -> Tuple[str, Dict[str, str], List[str]]:
    """
    Parses Python code, rewrites relative parquet paths, and returns the modified code.

    Args:
        code_string: The Python code as a string.
        base_path: The base directory (as a string or Path object) to prepend
                   to relative parquet paths.
        s3_rewrite_prefix: If provided, rewrites to this S3 prefix instead of local path.
        filename: The filename to report in case of parsing errors.

    Returns:
        A tuple containing:
        - The modified Python code string.
        - A dictionary mapping original paths to rewritten paths.
        - A list of original paths identified as inputs.
    """
    if isinstance(base_path, str):
        base_path_obj = Path(base_path)
    elif isinstance(base_path, Path):
        base_path_obj = base_path
    else:
        raise TypeError("base_path must be a string or pathlib.Path object")

    try:
        tree = ast.parse(code_string, filename=filename)
    except SyntaxError as e:
        print(f"Error parsing Python code: {e}")
        raise

    rewriter = ParquetPathRewriter(
        base_path=base_path_obj,
        s3_rewrite_prefix=s3_rewrite_prefix,
    )

    modified_tree = rewriter.visit(tree)
    ast.fix_missing_locations(modified_tree)

    try:
        modified_code = ast.unparse(modified_tree)
    except AttributeError as exc:
        raise RuntimeError(
            "ast.unparse is not available (requires Python 3.9+). "
            "Install 'astunparse' for older versions."
        ) from exc
    except Exception as e:
        raise RuntimeError(f"Failed to generate code from modified AST: {e}") from e

    return modified_code, rewriter.rewritten_paths, rewriter.identified_inputs
