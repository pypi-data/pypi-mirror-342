class NotFoundException(Exception):
    """Raised when a 404 Not Found is returned from the API."""
    def __init__(self, url=None, message="Resource not found."):
        if url:
            message = f"Requested resource at {url} not found. Message: {message}."
        super().__init__(message)