"""fp-client — Python client for Fingerprint Generator API (fp.mahiru.my.id)"""

from .client import FPClient
from .models import Identity, Fingerprint, FingerprintResult, FingerprintBatch

__version__ = "1.0.0"
__all__ = ["FPClient", "Identity", "Fingerprint", "FingerprintResult", "FingerprintBatch"]
