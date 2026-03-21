"""
Tests for src/validation/schema_validation.py
"""
import sys
import os
import pytest
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from validation.schema_validation import SchemaValidator

@pytest.fixture
def validator():
    return SchemaValidator()

def make_chunk(**kwargs):
    base = {
        "content": "code", "language": "python", "file_path": "f.py",
        "chunk_index": 0, "start_line": 1, "end_line": 2, "embedding": [0]*768
    }
    base.update(kwargs)
    return base

def test_validate_all_pass(validator):
    chunks = [make_chunk() for _ in range(5)]
    result = validator.validate(chunks)
    assert result["overall_pass"] is True
    assert result["failed"] == 0
    assert result["expectations"]["required_fields_present"]["passed"]
    assert result["expectations"]["embedding_dim_768"]["passed"]

def test_missing_required_fields(validator):
    chunks = [make_chunk(), {"content": "", "language": "python"}]
    result = validator.validate(chunks)
    assert not result["expectations"]["required_fields_present"]["passed"]
    assert result["expectations"]["required_fields_present"]["failed_count"] == 1

def test_empty_content(validator):
    chunks = [make_chunk(content=" "), make_chunk()]
    result = validator.validate(chunks)
    assert not result["expectations"]["content_non_empty"]["passed"]
    assert result["expectations"]["content_non_empty"]["failed_count"] == 1

def test_invalid_language(validator):
    chunks = [make_chunk(language="notalanguage"), make_chunk()]
    result = validator.validate(chunks)
    assert not result["expectations"]["language_valid"]["passed"]
    assert result["expectations"]["language_valid"]["failed_count"] == 1

def test_negative_chunk_index(validator):
    chunks = [make_chunk(chunk_index=-1), make_chunk()]
    result = validator.validate(chunks)
    assert not result["expectations"]["chunk_index_non_negative"]["passed"]
    assert result["expectations"]["chunk_index_non_negative"]["failed_count"] == 1

def test_start_gt_end_line(validator):
    chunks = [make_chunk(start_line=5, end_line=2), make_chunk()]
    result = validator.validate(chunks)
    assert not result["expectations"]["start_lte_end_line"]["passed"]
    assert result["expectations"]["start_lte_end_line"]["failed_count"] == 1

def test_embedding_wrong_dim(validator):
    chunks = [make_chunk(embedding=[0]*100), make_chunk()]
    result = validator.validate(chunks)
    assert not result["expectations"]["embedding_dim_768"]["passed"]
    assert result["expectations"]["embedding_dim_768"]["failed_count"] == 1

def test_generate_statistics(validator):
    chunks = [make_chunk(language="python", content="abc", file_path="f1.py"),
              make_chunk(language="java", content="defg", file_path="f2.java")]
    stats = validator._generate_statistics(chunks)
    assert stats["total_chunks"] == 2
    assert stats["total_files"] == 2
    assert stats["languages"]["python"] == 1
    assert stats["languages"]["java"] == 1
    assert stats["chunk_size"]["avg"] > 0

