# Define custom exceptions

class ValidationError(ValueError):
    """Custom exception for input validation errors."""
    pass

class InvalidPathError(ValueError):
    """Custom exception for invalid path errors."""
    pass

class ImageLoadError(IOError):
    """Custom exception for image loading errors."""
    pass
