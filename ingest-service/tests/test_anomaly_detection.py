"""
Tests for src/validation/anomaly_detection.py
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
import pytest
from unittest.mock import patch
from validation.anomaly_detection import AnomalyDetector, send_slack_alert


def test_detect_empty_chunks():
    detector = AnomalyDetector()
    result = detector.detect([], repo="test/repo")
    assert not result["passed"]
    assert "CRITICAL: No chunks found in dataset" in result["anomalies"][0]


def test_detect_missing_fields():
    detector = AnomalyDetector()
    chunks = [
        {"content": "", "embedding": [], "language": "", "file_path": ""},
        {"content": "code", "embedding": None, "language": None, "file_path": None},
    ]
    result = detector.detect(chunks, repo="test/repo")
    assert any("MISSING CONTENT" in a for a in result["anomalies"])
    assert any("MISSING EMBEDDING" in a for a in result["anomalies"])
    assert any("MISSING LANGUAGE" in a for a in result["anomalies"])
    assert any("MISSING FILE PATH" in a for a in result["anomalies"])


def test_detect_wrong_embedding_dim():
    detector = AnomalyDetector()
    chunks = [
        {"content": "code", "embedding": [0]*100, "language": "python", "file_path": "f.py"},
        {"content": "code2", "embedding": [0]*768, "language": "python", "file_path": "f2.py"},
    ]
    result = detector.detect(chunks, repo="test/repo")
    assert any("WRONG EMBEDDING DIM" in a for a in result["anomalies"])


def test_detect_duplicates_and_outliers():
    detector = AnomalyDetector()
    chunks = [
        {"content": "abc", "embedding": [0]*768, "language": "python", "file_path": "f.py"},
        {"content": "abc", "embedding": [0]*768, "language": "python", "file_path": "f2.py"},
        {"content": "a"*20000, "embedding": [0]*768, "language": "python", "file_path": "f3.py"},
        {"content": "b", "embedding": [0]*768, "language": "unknown", "file_path": "f4.py"},
    ]
    result = detector.detect(chunks, repo="test/repo")
    assert any("DUPLICATES" in w for w in result["warnings"])
    assert any("HUGE CHUNKS" in w for w in result["warnings"])
    assert any("HIGH UNKNOWN LANGUAGE" in w for w in result["warnings"])


def test_send_slack_alert_skips_if_no_webhook(monkeypatch):
    with patch("validation.anomaly_detection.SLACK_WEBHOOK", None):
        # Should not raise or send
        send_slack_alert("test message")


def test_send_slack_alert_handles_exception(monkeypatch):
    with patch("validation.anomaly_detection.SLACK_WEBHOOK", "http://bad-url"), \
         patch("urllib.request.urlopen", side_effect=Exception("fail")) as mock_urlopen:
        send_slack_alert("test message")
        mock_urlopen.assert_called()

