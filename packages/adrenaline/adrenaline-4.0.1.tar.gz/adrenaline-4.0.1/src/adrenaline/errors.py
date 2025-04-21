__all__ = ("NotSupportedError",)


class NotSupportedError(RuntimeError):
    """Error thrown when the power management API is not supported or implemented
    in the OS that the system is running on.
    """

    pass
