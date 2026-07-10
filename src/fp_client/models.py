"""Pydantic models for Fingerprint Generator API responses."""

from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field


class Screen(BaseModel):
    """Screen properties."""
    width: int
    height: int
    availWidth: int
    availHeight: int
    colorDepth: int
    devicePixelRatio: int


class Identity(BaseModel):
    """Target-agnostic browser identity."""
    chromeVersion: str = Field(alias="chromeVersion")
    userAgent: str
    secUA: str = Field(alias="secUA")
    secChUaPlatform: str = Field(alias="secChUaPlatform")
    gpuVendor: str
    gpuModel: str
    webglExtensions: list[str]
    canvasHash: int
    histogram: list[int] = Field(min_length=256, max_length=256)
    mathTan: str
    mathSin: str
    mathCos: str
    audioFingerprint: str
    plugins: list[dict[str, str]]
    screen: Screen
    deviceMemory: int
    hardwareConcurrency: int
    platform: str
    timeZone: int
    languages: list[str]
    locale: str
    fonts: list[str]
    webpackHash: Optional[str] = None  # Amazon target extra

    class Config:
        populate_by_name = True


class Fingerprint(BaseModel):
    """Generated fingerprint payload."""
    raw: dict
    encrypted: Optional[str] = None


class FingerprintResult(BaseModel):
    """Single fingerprint result: identity + fingerprint."""
    identity: Identity
    fingerprint: Fingerprint


class FingerprintBatch(BaseModel):
    """Batch fingerprint result."""
    count: int
    fingerprints: list[FingerprintResult]


class Stats(BaseModel):
    """Cache statistics."""
    cache_size: Optional[int] = None
    hits: Optional[int] = None
    misses: Optional[int] = None

    class Config:
        extra = "allow"
