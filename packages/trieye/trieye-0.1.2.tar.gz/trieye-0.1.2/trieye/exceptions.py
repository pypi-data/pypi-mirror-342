class TrieyeError(Exception):
    """Base exception for the Trieye library."""

    pass


class ConfigurationError(TrieyeError):
    """Exception raised for errors in configuration."""

    pass


class SerializationError(TrieyeError):
    """Exception raised for errors during serialization or deserialization."""

    pass


class ProcessingError(TrieyeError):
    """Exception raised for errors during statistics processing."""

    pass
