"""
Tests for src/rag/rag_services.py
"""
import sys
import os
import pytest
from unittest.mock import MagicMock, patch

# Patch sys.modules to mock google.generativeai
sys.modules["google.generativeai"] = MagicMock()
# Patch sys.modules to mock dotenv
sys.modules["dotenv"] = MagicMock(load_dotenv=MagicMock())
# Patch sys.modules to mock numpy
sys.modules["numpy"] = MagicMock()
# Patch sys.modules to mock google.cloud.aiplatform
sys.modules["google.cloud.aiplatform"] = MagicMock()
# Patch sys.modules to mock vertexai and vertexai.language_models
mock_vertexai_language_models = MagicMock(TextEmbeddingModel=MagicMock())
mock_vertexai = MagicMock(language_models=mock_vertexai_language_models)
sys.modules["vertexai"] = mock_vertexai
sys.modules["vertexai.language_models"] = mock_vertexai_language_models

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from rag.rag_services import RAGServices

@pytest.fixture
def rag():
    with patch("rag.rag_services.GeminiClient"), \
         patch("rag.rag_services.VectorSearch") as mock_search, \
         patch("rag.rag_services.DocumentationManager"):
        r = RAGServices("proj", "bucket")
        r.search = mock_search.return_value
        return r

def test_detect_target_file_high_similarity(rag):
    rag.search.search.return_value = [{
        "file_path": "foo.py", "similarity_score": 0.85, "chunk_type": "code_block", "start_line": 1, "end_line": 10
    }]
    result = rag._detect_target_file("def foo(): pass", "repo", language="python")
    assert result["file_path"] == "foo.py"
    assert result["confidence"] == "high"

def test_detect_target_file_low_similarity(rag):
    rag.search.search.return_value = [{
        "file_path": "foo.py", "similarity_score": 0.5, "chunk_type": "code_block", "start_line": 1, "end_line": 10
    }]
    result = rag._detect_target_file("def foo(): pass", "repo", language="python")
    assert result is None

def test_detect_target_file_no_results(rag):
    rag.search.search.return_value = []
    result = rag._detect_target_file("def foo(): pass", "repo", language="python")
    assert result is None

def test_get_existing_file_content_with_github(rag):
    rag.github_client = MagicMock()
    rag.github_client.get_file_content.return_value = "file content"
    out = rag._get_existing_file_content("repos/owner/repo", "foo.py")
    assert out == "file content"
    rag.github_client.get_file_content.assert_called()

def test_get_existing_file_content_no_github(rag):
    rag.github_client = None
    out = rag._get_existing_file_content("repo", "foo.py")
    assert out is None

def test_insert_completion_into_file_found(rag):
    existing = "def foo():\n    pass"
    context = "def foo():"
    completion = "# new code"
    out = rag._insert_completion_into_file(existing, context, completion)
    assert "# new code" in out
    assert out.index("# new code") > out.index(context)

def test_insert_completion_into_file_not_found(rag):
    existing = "def bar():\n    pass"
    context = "def foo():"
    completion = "# new code"
    out = rag._insert_completion_into_file(existing, context, completion)
    assert out.endswith("# new code")

def test_answer_question_no_chunks(rag):
    rag.search.search.return_value = []
    out = rag.answer_question("What is this?", "repo")
    assert "couldn't find" in out["answer"].lower()
    assert out["chunks_used"] == 0

