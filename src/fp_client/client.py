"""Core client for Fingerprint Generator API."""

from __future__ import annotations

import httpx
from typing import Optional, Union

from .models import FingerprintResult, FingerprintBatch, Stats


DEFAULT_BASE_URL = "https://fp.mahiru.my.id"
LOCAL_BASE_URL = "http://127.0.0.1:8800"


class FPClient:
    """Client for the Fingerprint Generator API.

    Args:
        base_url: API base URL (default: public endpoint)
        token: Bearer token for auth (not needed for localhost)
        timeout: Request timeout in seconds
    """

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        token: Optional[str] = None,
        timeout: float = 30.0,
    ):
        self.base_url = base_url.rstrip("/")
        headers = {"Accept": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        self._client = httpx.Client(
            base_url=self.base_url,
            headers=headers,
            timeout=timeout,
        )

    def health(self) -> dict:
        """Check API liveness (no auth required)."""
        resp = self._client.get("/health")
        resp.raise_for_status()
        return resp.json()

    def generate(
        self,
        count: int = 1,
        proxy: Optional[str] = None,
        chrome: Optional[int] = None,
        target: str = "amazon",
        encrypt: bool = True,
        pretty: bool = False,
    ) -> Union[FingerprintResult, FingerprintBatch]:
        """Generate browser fingerprint(s).

        Args:
            count: Number of fingerprints (1-100)
            proxy: Proxy URL to bind identity to (same host reuses for 6h)
            chrome: Pin Chrome major version (e.g. 131)
            target: Antibot target (currently only 'amazon')
            encrypt: Include encrypted payload
            pretty: Pretty-print JSON response

        Returns:
            FingerprintResult if count=1, FingerprintBatch otherwise
        """
        params: dict = {
            "count": count,
            "target": target,
            "encrypt": str(encrypt).lower(),
            "pretty": str(pretty).lower(),
        }
        if proxy:
            params["proxy"] = proxy
        if chrome:
            params["chrome"] = chrome

        resp = self._client.get("/fingerprint", params=params)
        resp.raise_for_status()
        data = resp.json()

        if count == 1:
            return FingerprintResult.model_validate(data)
        return FingerprintBatch.model_validate(data)

    def generate_one(
        self,
        proxy: Optional[str] = None,
        chrome: Optional[int] = None,
        target: str = "amazon",
        encrypt: bool = True,
    ) -> FingerprintResult:
        """Convenience: generate exactly one fingerprint."""
        result = self.generate(
            count=1, proxy=proxy, chrome=chrome,
            target=target, encrypt=encrypt,
        )
        assert isinstance(result, FingerprintResult)
        return result

    def generate_batch(
        self,
        count: int = 10,
        proxy: Optional[str] = None,
        chrome: Optional[int] = None,
        target: str = "amazon",
        encrypt: bool = True,
    ) -> FingerprintBatch:
        """Convenience: generate a batch of fingerprints."""
        result = self.generate(
            count=count, proxy=proxy, chrome=chrome,
            target=target, encrypt=encrypt,
        )
        assert isinstance(result, FingerprintBatch)
        return result

    def stats(self) -> Stats:
        """Get cache statistics."""
        resp = self._client.get("/stats")
        resp.raise_for_status()
        return Stats.model_validate(resp.json())

    def close(self):
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
