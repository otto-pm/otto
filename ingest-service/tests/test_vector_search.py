"""
Tests for src/rag/vector_search.py
"""
import sys
import os
from unittest.mock import MagicMock
# Patch sys.modules to mock only cloud/AI dependencies (not numpy)
sys.modules["google.cloud"] = MagicMock()
sys.modules["google.cloud.storage"] = MagicMock()
sys.modules["google.cloud.aiplatform"] = MagicMock()
sys.modules["vertexai"] = MagicMock(language_models=MagicMock(TextEmbeddingModel=MagicMock()))
sys.modules["vertexai.language_models"] = MagicMock(TextEmbeddingModel=MagicMock())
sys.modules["google.auth"] = MagicMock(default=MagicMock())
import pytest
from unittest.mock import MagicMock, patch
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from rag.vector_search import VectorSearch

@pytest.fixture
def vector_search():
    with patch("rag.vector_search.storage.Client"), \
         patch("rag.vector_search.aiplatform"), \
         patch("rag.vector_search.get_default_credentials", return_value=(MagicMock(), "proj")), \
         patch("rag.vector_search.TextEmbeddingModel"):
        return VectorSearch("proj", "bucket")

def test_get_model_loads_model(vector_search):
    with patch("rag.vector_search.TextEmbeddingModel.from_pretrained", return_value=MagicMock(get_embeddings=lambda x: [MagicMock(values=[0.1]*768)])) as mock_model:
        vector_search.model = None
        model = vector_search._get_model()
        assert model is not None
        mock_model.assert_called_with("text-embedding-004")

def test_embed_query_returns_embedding(vector_search):
    mock_model = MagicMock(get_embeddings=lambda x: [MagicMock(values=[0.1]*768)])
    vector_search.model = mock_model
    out = vector_search._embed_query("query")
    assert isinstance(out, list)
    assert len(out) == 768

def test_search_no_blob(vector_search):
    mock_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_blob.exists.return_value = False
    mock_bucket.blob.return_value = mock_blob
    vector_search.bucket = mock_bucket
    out = vector_search.search("query", "repo")
    assert out == []

def test_search_with_chunks_and_embeddings(vector_search):
    mock_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_blob.exists.return_value = True
    # 2 chunks, one with embedding, one without
    chunk1 = {"embedding": [0.1]*768, "file_path": "f.py", "chunk_type": "code_block", "start_line": 1, "end_line": 10}
    chunk2 = {"file_path": "f2.py"}
    mock_blob.download_as_text.return_value = "\n".join([str(chunk1).replace("'", '"'), str(chunk2).replace("'", '"')])
    mock_bucket.blob.return_value = mock_blob
    vector_search.bucket = mock_bucket
    with patch.object(vector_search, "_embed_query", return_value=[0.1]*768):
        with patch.object(vector_search, "_cosine_similarity", return_value=0.9):
            out = vector_search.search("query", "repo", top_k=1)
            assert isinstance(out, list)
            assert out[0]["file_path"] == "f.py"
            assert "similarity_score" in out[0]

def test_cosine_similarity_basic(vector_search):
    v1 = [1, 0, 0]
    v2 = [1, 0, 0]
    out = vector_search._cosine_similarity(v1, v2)
    assert out == 1.0
    v3 = [0, 1, 0]
    out2 = vector_search._cosine_similarity(v1, v3)
    assert out2 == 0.0

def test_batch_search_handles_exceptions(vector_search):
    with patch.object(vector_search, "search", side_effect=[Exception("fail"), [{"file_path": "f.py"}]]):
        out = vector_search.batch_search(["q1", "q2"], "repo")
        assert "q1" in out and out["q1"] == []
        assert "q2" in out and out["q2"][0]["file_path"] == "f.py"

