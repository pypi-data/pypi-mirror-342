"""Error classes."""


class AqagoAppSdkError(Exception):
    """Base class for all exceptions in the aqago_app_sdk module."""

    def __init__(self, msg: str | None = None) -> None:
        """Initialize the AqagoAppSdkError."""
        super().__init__(msg)


class GetArtifactError(AqagoAppSdkError):
    """Error retrieving an artifact."""

    def __init__(self, command: str, returncode: int) -> None:
        """Initialize GetArtifactError."""
        msg = f"command: {command}, return code: {returncode}"
        super().__init__(msg)


class GetArtifactResponseError(AqagoAppSdkError):
    """Error parsing artifact response."""


class FetchArtifactError(AqagoAppSdkError):
    """Error fetching an artifact."""

    def __init__(self, command: str, returncode: int) -> None:
        """Initialize FetchArtifactError."""
        msg = f"command: {command}, return code: {returncode}"
        super().__init__(msg)


class AgentNotRunningError(Exception):
    """Agent not running error."""
