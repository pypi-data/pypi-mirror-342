"""
This module contains unit tests for the Parquet path rewriter.
"""

import ast
from pathlib import Path
import pytest

from src.parquet_path_rewriter.rewriter import rewrite_parquet_paths_in_code

BASE_TEST_PATH = Path("/test/data/base").resolve()


def normalize_code(code: str) -> str:
    """Normalize code string by removing extra whitespace and newlines."""
    try:
        return ast.unparse(ast.parse(code))
    except AttributeError:
        return "\n".join(
            line.strip() for line in code.strip().splitlines() if line.strip()
        )
    except SyntaxError:
        return code.strip()


def test_simple_read_rewrite():
    code = "df = spark.read.parquet('input/my_data')"
    expected_path = str(BASE_TEST_PATH / "my_data.parquet")
    expected_code = f"df = spark.read.parquet('{expected_path}')"

    modified_code, rewritten, inputs = rewrite_parquet_paths_in_code(
        code, BASE_TEST_PATH
    )

    assert normalize_code(modified_code) == normalize_code(expected_code)
    assert rewritten == {"input/my_data": expected_path}
    assert inputs == ["input/my_data"]


def test_s3_rewrite():
    code = "df = spark.read.parquet('s3://bucket/F8_QUWRY_AHSGSG')"
    prefix = "s3://bucket/tmp/data"
    expected_path = f"{prefix}/F8_QUWRY_AHSGSG.parquet"
    expected_code = f"df = spark.read.parquet('{expected_path}')"

    modified_code, rewritten, inputs = rewrite_parquet_paths_in_code(
        code, base_path=BASE_TEST_PATH, s3_rewrite_prefix=prefix
    )

    assert normalize_code(modified_code) == normalize_code(expected_code)
    assert rewritten == {"s3://bucket/F8_QUWRY_AHSGSG": expected_path}
    assert inputs == ["s3://bucket/F8_QUWRY_AHSGSG"]


def test_keyword_argument_rewrite_with_parquet_suffix():
    code = "df = spark.read.parquet(path='stage/zone/data.parquet')"
    expected_path = str(BASE_TEST_PATH / "data.parquet")
    expected_code = f"df = spark.read.parquet(path='{expected_path}')"

    modified_code, rewritten, inputs = rewrite_parquet_paths_in_code(
        code, BASE_TEST_PATH
    )

    assert normalize_code(modified_code) == normalize_code(expected_code)
    assert rewritten == {"stage/zone/data.parquet": expected_path}
    assert inputs == ["stage/zone/data.parquet"]


def test_absolute_path_no_rewrite():
    absolute_path = "/var/data/input.parquet"
    code = f"df = spark.read.parquet('{absolute_path}')"

    modified_code, rewritten, inputs = rewrite_parquet_paths_in_code(
        code, BASE_TEST_PATH
    )

    assert normalize_code(modified_code) == normalize_code(code)
    assert not rewritten
    assert not inputs


def test_invalid_base_path_type():
    code = "df = spark.read.parquet('input')"
    with pytest.raises(TypeError):
        rewrite_parquet_paths_in_code(code, base_path=123)


def test_invalid_python_code():
    code = "spark.read.parquet('data'"
    with pytest.raises(SyntaxError):
        rewrite_parquet_paths_in_code(code, BASE_TEST_PATH)


def test_ast_unparse_failure_raises_runtimeerror(monkeypatch):
    """Test that a failure during ast.unparse raises a RuntimeError."""
    code = "df = spark.read.parquet('some/path')"

    def broken_unparse(_):
        raise ValueError("forced error for test")

    monkeypatch.setattr(ast, "unparse", broken_unparse)

    with pytest.raises(
        RuntimeError, match="Failed to generate code from modified AST:"
    ):
        rewrite_parquet_paths_in_code(code, base_path="/tmp/data")


def test_ast_unparse_not_available(monkeypatch):
    """Test RuntimeError is raised when ast.unparse is not available (Python <3.9 fallback)."""
    code = "df = spark.read.parquet('some/path')"

    # Remove ast.unparse to simulate older Python environments
    monkeypatch.delattr(ast, "unparse", raising=True)

    with pytest.raises(
        RuntimeError, match="ast.unparse is not available.*requires Python 3.9+"
    ):
        rewrite_parquet_paths_in_code(code, base_path="/tmp/test")
