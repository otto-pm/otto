"""
Tests for src/chunking/chunker.py
"""
import sys
import os
import pytest
from unittest.mock import patch, MagicMock

# Patch sys.modules to mock google.cloud and google.cloud.storage before importing CodeChunker
mock_storage = MagicMock()
mock_google_cloud = MagicMock(storage=mock_storage)
sys.modules["google"] = MagicMock(cloud=mock_google_cloud)
sys.modules["google.cloud"] = mock_google_cloud
sys.modules["google.cloud.storage"] = mock_storage

# Patch sys.modules to mock vertexai and vertexai.language_models
mock_vertexai_language_models = MagicMock(TextEmbeddingModel=MagicMock())
mock_vertexai = MagicMock(language_models=mock_vertexai_language_models)
sys.modules["vertexai"] = mock_vertexai
sys.modules["vertexai.language_models"] = mock_vertexai_language_models

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from chunking.chunker import CodeChunker

# --- Fixtures and Mocks ---
@pytest.fixture
def mock_storage_client():
    with patch("chunking.chunker.storage.Client") as mock_client:
        yield mock_client

@pytest.fixture
def chunker(mock_storage_client):
    return CodeChunker("test-proj", "bucket-raw", "bucket-processed")

# --- Tests ---
def test_chunker_init_sets_fields(chunker):
    assert chunker.project_id == "test-proj"
    assert chunker.bucket_raw == "bucket-raw"
    assert chunker.bucket_processed == "bucket-processed"
    assert hasattr(chunker, "storage_client")
    assert isinstance(chunker.parsers, dict)

def test_load_parsers_tree_sitter_available():
    # Patch tree_sitter_languages.get_parser in sys.modules
    mock_get_parser = MagicMock(side_effect=lambda lang: f"parser-{lang}")
    mock_tree_sitter = MagicMock(get_parser=mock_get_parser)
    with patch.dict(sys.modules, {"tree_sitter_languages": mock_tree_sitter}):
        c = CodeChunker("test-proj", "bucket-raw", "bucket-processed")
        assert all(lang in c.parsers for lang in ["python", "javascript", "typescript", "java", "go", "rust"])

def test_load_parsers_tree_sitter_missing():
    with patch.dict("sys.modules", {"tree_sitter_languages": None}):
        c = CodeChunker("test-proj", "bucket-raw", "bucket-processed")
        assert c.parsers == {}

def test_extract_file_context_python(chunker):
    code = """
import os\nfrom sys import path\nclass Foo:\n    pass\ndef bar():\n    pass\nCONSTANT = 1
"""
    ctx = chunker._extract_file_context(code, "python")
    assert "os" in ctx["imports"] and "sys" in ctx["imports"]
    assert "Foo" in ctx["classes"]
    assert "bar" in ctx["functions"]
    assert "CONSTANT" in ctx["constants"]

def test_extract_file_context_js(chunker):
    code = """
import x from 'y';\nclass Bar {}\nfunction baz() {}\nconst Q = 1;
"""
    ctx = chunker._extract_file_context(code, "javascript")
    assert "y" in ctx["imports"]
    assert "Bar" in ctx["classes"]
    assert "baz" in ctx["functions"]

def test_extract_file_context_java(chunker):
    code = """
import java.util.List;\nclass Baz {}\n"""
    ctx = chunker._extract_file_context(code, "java")
    assert "java.util.List" in ctx["imports"]
    assert "Baz" in ctx["classes"]

def test_smart_line_chunk_basic(chunker):
    code = "".join([f"line {i}\n" for i in range(200)])
    chunks = chunker._smart_line_chunk(code)
    assert len(chunks) > 1
    assert all("content" in c for c in chunks)
    assert all(c["type"] == "code_block" for c in chunks)

def test_chunk_file_line_based(chunker):
    code = "def foo():\n    pass\n" * 80
    file_ctx = {"imports": [], "classes": [], "functions": ["foo"], "constants": [], "docstring": None}
    meta = {"repo": "repo", "total_files": 1}
    repo_ctx = {"repo_name": "repo", "description": "", "primary_language": "python", "total_files": 1, "languages": {"python": 1}, "directories": []}
    out = chunker._chunk_file("f.py", code, "python", meta, file_ctx, repo_ctx)
    assert len(out) > 0
    assert all("enriched_content" in c for c in out)

def test_build_enriched_content_fields(chunker):
    chunk = {"content": "print('hi')", "type": "code_block", "name": "lines_0_1", "start_line": 0, "end_line": 1}
    file_ctx = {"imports": ["os"], "classes": ["Foo"], "functions": ["bar"], "constants": [], "docstring": None}
    repo_ctx = {"repo_name": "repo", "description": "desc", "primary_language": "python", "total_files": 1, "languages": {"python": 1}, "directories": []}
    out = chunker._build_enriched_content(chunk, "f.py", file_ctx, repo_ctx, "python")
    assert "# Repository: repo" in out
    assert "# File: f.py" in out
    assert "# Classes: Foo" in out
    assert "# Functions: bar" in out
    assert "print('hi')" in out

def test_process_repository_handles_file_error(chunker):
    # Patch _read_file to raise for one file
    meta = {"repo": "repo", "total_files": 2, "files": [
        {"path": "f1.py", "blob_path": "blob1", "language": "python"},
        {"path": "f2.py", "blob_path": "blob2", "language": "python"}
    ], "repo_info": {"description": "", "language": "python"}}
    with patch.object(chunker, "_load_metadata", return_value=meta), \
         patch.object(chunker, "_read_file", side_effect=["code", Exception("fail")]), \
         patch.object(chunker, "_extract_file_context", return_value={"imports": [], "classes": [], "functions": [], "constants": [], "docstring": None}), \
         patch.object(chunker, "_chunk_file", return_value=[{"content": "c", "type": "code_block", "name": "n", "start_line": 0, "end_line": 1}]), \
         patch.object(chunker, "_save_chunks") as save_chunks:
        out = chunker.process_repository("repo")
        assert isinstance(out, list)
        assert save_chunks.called

