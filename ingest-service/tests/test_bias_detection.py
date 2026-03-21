"""
Tests for src/validation/bias_detection.py
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
import pytest
from validation.bias_detection import BiasDetector

def test_bias_detector_no_bias():
    detector = BiasDetector()
    chunks = [
        {"content": "code", "embedding": [0]*768, "language": "python", "file_path": "f.py"},
        {"content": "code2", "embedding": [0]*768, "language": "python", "file_path": "f2.py"},
        {"content": "code3", "embedding": [0]*768, "language": "python", "file_path": "f3.py"},
        {"content": "code4", "embedding": [0]*768, "language": "python", "file_path": "f4.py"},
        {"content": "code5", "embedding": [0]*768, "language": "python", "file_path": "f5.py"},
        {"content": "code6", "embedding": [0]*768, "language": "python", "file_path": "f6.py"},
    ]
    result = detector.detect(chunks, repo="test/repo")
    assert result["bias_detected"] is False
    assert "slicing_analyses" in result

def test_bias_detector_with_bias():
    detector = BiasDetector()
    # 10 python chunks, all with embeddings
    python_chunks = [
        {"content": f"code{i}", "embedding": [0]*768, "language": "python", "file_path": f"f{i}.py"}
        for i in range(10)
    ]
    # 12 java chunks, all missing embeddings
    java_chunks = [
        {"content": f"codej{i}", "embedding": None, "language": "java", "file_path": f"f{i}.java"}
        for i in range(12)
    ]
    # 8 go chunks, all with embeddings
    go_chunks = [
        {"content": f"codeg{i}", "embedding": [0]*768, "language": "go", "file_path": f"f{i}.go"}
        for i in range(8)
    ]
    chunks = python_chunks + java_chunks + go_chunks
    result = detector.detect(chunks, repo="test/repo")
    assert result["bias_detected"] is True
    assert "slicing_analyses" in result
    # Optionally, check that at least one slice is flagged as biased
    assert any(a.get("bias_detected") for a in result["slicing_analyses"].values())

