class ApplicationError(ValueError):
    """User-facing failure that must not leave a partial published result."""
