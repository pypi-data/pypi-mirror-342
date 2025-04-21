class DigestFusionError(Exception):
    """
    Base exception for all Digest Fusion Hashing related errors.
    """
    pass


class InvalidSplitRatioError(DigestFusionError):
    """
    Raised when the split ratio is outside the allowed range (0.30 - 0.70).
    """
    pass


class InvalidHashError(DigestFusionError):
    """
    Raised when a hash verification fails because the hashes do not match.
    """
    pass
