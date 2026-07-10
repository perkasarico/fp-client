# fp-client

Python client for the [Fingerprint Generator API](https://fp.mahiru.my.id/docs) — generates realistic Chrome browser fingerprints (GPU, WebGL, canvas, screen, fonts, math, audio, timing) for antibot bypass.

## Install

```bash
pip install -e .
```

Or just use it directly:

```bash
pip install httpx pydantic
```

## Usage

### Python

```python
from fp_client import FPClient

# Public endpoint (needs token)
client = FPClient(token="your-token")

# Or localhost (no auth)
client = FPClient(base_url="http://127.0.0.1:8800")

# Generate single fingerprint
fp = client.generate_one()
print(fp.identity.chromeVersion)    # "131.0.0.0"
print(fp.identity.gpuModel)         # "ANGLE (NVIDIA GeForce GTX 1660)"
print(fp.fingerprint.encrypted)     # "ECdITeCs:<base64>"

# Generate batch (up to 100)
batch = client.generate_batch(count=10)
for fp in batch.fingerprints:
    print(fp.identity.canvasHash)

# Bind to proxy (same host reuses identity for 6h)
fp = client.generate_one(proxy="http://user:pass@proxy:port")

# Pin Chrome version
fp = client.generate_one(chrome=131)

# Skip encryption
fp = client.generate_one(encrypt=False)

# Cache stats
stats = client.stats()
```

### CLI

```bash
# Set env vars
export FP_URL="https://fp.mahiru.my.id"
export FP_TOKEN="your-token"

# Health check
fp-client health

# Generate 5 fingerprints
fp-client generate -n 5 --pretty

# Generate with proxy binding
fp-client generate -p "http://user:pass@proxy:port"

# Export to file
fp-client export -o fingerprints.json -n 10

# Cache stats
fp-client stats
```

## API Reference

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/health` | GET | ❌ | Health check |
| `/fingerprint` | GET | ✅ | Generate fingerprint(s) |
| `/stats` | GET | ✅ | Cache statistics |

### Parameters

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `count` | int | 1 | Number of fingerprints (1-100) |
| `proxy` | str | - | Proxy URL to bind identity to (reuses for 6h) |
| `chrome` | int | - | Pin Chrome major version |
| `target` | str | `amazon` | Antibot target |
| `encrypt` | bool | `true` | Include encrypted payload |
| `pretty` | bool | `false` | Pretty-print JSON |

## Response Structure

```json
{
  "identity": {
    "chromeVersion": "131.0.0.0",
    "userAgent": "Mozilla/5.0 ...",
    "gpuVendor": "Google Inc. (NVIDIA)",
    "gpuModel": "ANGLE (NVIDIA GeForce GTX 1660)",
    "canvasHash": 1234567890,
    "histogram": [0, 0, ...],
    "mathTan": "0.5574077246549023",
    "audioFingerprint": "124.04347527516074",
    "screen": { "width": 1920, "height": 1080 },
    "hardwareConcurrency": 8,
    "deviceMemory": 8,
    "fonts": ["Arial", "Courier New", ...]
  },
  "fingerprint": {
    "raw": { ... },
    "encrypted": "ECdITeCs:<base64>"
  }
}
```

## Tests

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT
