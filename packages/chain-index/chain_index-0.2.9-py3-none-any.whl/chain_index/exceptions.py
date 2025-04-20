class ChainNotFoundError(Exception):
    """Raised when a requested chain is not found in the index."""
    pass

class TokenNotFoundError(Exception):
    """Raised when a requested token is not found on the specified chain."""
    pass
