"""Tests for fp-client (uses mocked HTTP responses)."""

import pytest
from unittest.mock import MagicMock, patch
from fp_client import FPClient, FingerprintResult, FingerprintBatch


MOCK_IDENTITY = {
    "chromeVersion": "131.0.0.0",
    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "secUA": '"Chromium";v="131", "Not_A Brand";v="24"',
    "secChUaPlatform": "Windows",
    "gpuVendor": "Google Inc. (NVIDIA)",
    "gpuModel": "ANGLE (NVIDIA GeForce GTX 1660 SUPER)",
    "webglExtensions": ["ANGLE_instanced_arrays", "EXT_blend_minmax"],
    "canvasHash": 1234567890,
    "histogram": [0] * 256,
    "mathTan": "0.5574077246549023",
    "mathSin": "-0.9999999999999999",
    "mathCos": "1.0000000000000002",
    "audioFingerprint": "124.04347527516074",
    "plugins": [{"name": "Chrome PDF Plugin", "description": "Portable Document Format"}],
    "screen": {
        "width": 1920, "height": 1080,
        "availWidth": 1920, "availHeight": 1040,
        "colorDepth": 24, "devicePixelRatio": 1,
    },
    "deviceMemory": 8,
    "hardwareConcurrency": 8,
    "platform": "Win32",
    "timeZone": -5,
    "languages": ["en-US", "en"],
    "locale": "en-US",
    "fonts": ["Arial", "Courier New", "Times New Roman"],
}

MOCK_FINGERPRINT = {
    "raw": {"metrics": {}, "lsUbid": "test"},
    "encrypted": "ECdITeCs:dGVzdA==",
}

MOCK_SINGLE = {
    "identity": MOCK_IDENTITY,
    "fingerprint": MOCK_FINGERPRINT,
}

MOCK_BATCH = {
    "count": 2,
    "fingerprints": [MOCK_SINGLE, MOCK_SINGLE],
}


def _mock_response(data, status=200):
    resp = MagicMock()
    resp.status_code = status
    resp.json.return_value = data
    resp.raise_for_status = MagicMock()
    return resp


class TestFPClient:
    def test_health(self):
        with patch("httpx.Client.get", return_value=_mock_response({"status": "ok"})):
            client = FPClient(base_url="http://localhost:8800")
            result = client.health()
            assert result["status"] == "ok"

    def test_generate_single(self):
        with patch("httpx.Client.get", return_value=_mock_response(MOCK_SINGLE)):
            client = FPClient(base_url="http://localhost:8800")
            result = client.generate(count=1)
            assert isinstance(result, FingerprintResult)
            assert result.identity.chromeVersion == "131.0.0.0"
            assert result.fingerprint.encrypted == "ECdITeCs:dGVzdA=="

    def test_generate_batch(self):
        with patch("httpx.Client.get", return_value=_mock_response(MOCK_BATCH)):
            client = FPClient(base_url="http://localhost:8800")
            result = client.generate(count=2)
            assert isinstance(result, FingerprintBatch)
            assert result.count == 2
            assert len(result.fingerprints) == 2

    def test_generate_one_convenience(self):
        with patch("httpx.Client.get", return_value=_mock_response(MOCK_SINGLE)):
            client = FPClient(base_url="http://localhost:8800")
            result = client.generate_one()
            assert isinstance(result, FingerprintResult)

    def test_generate_batch_convenience(self):
        with patch("httpx.Client.get", return_value=_mock_response(MOCK_BATCH)):
            client = FPClient(base_url="http://localhost:8800")
            result = client.generate_batch(count=2)
            assert isinstance(result, FingerprintBatch)

    def test_context_manager(self):
        client = FPClient(base_url="http://localhost:8800")
        with client:
            pass
        # Should not raise

    def test_token_auth(self):
        with patch("httpx.Client.get", return_value=_mock_response({"status": "ok"})):
            client = FPClient(base_url="https://fp.mahiru.my.id", token="test-token")
            result = client.health()
            assert result["status"] == "ok"
