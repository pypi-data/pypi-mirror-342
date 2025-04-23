"""Artifact class."""

import subprocess

from .errors import AgentNotRunningError, FetchArtifactError


class Artifact:
    """Artifact class for aqago agent."""

    def __init__(  # noqa: PLR0913
        self,
        name: str,
        version: str,
        metadata: dict,
        url: str,
        digest: str,
        tags: list[str] | None,
        variant: str | None,
        get: str,
        reference: str | None = None,
    ) -> None:
        """Initialize Artifact."""
        self.name = name
        self.version = version
        self.metadata = metadata
        self.url = url
        self.digest = digest
        self.tags = tags
        self.variant = variant
        self.get = get
        self.reference = reference

    def fetch(self) -> str:
        """Fetch the artifact."""
        if not self.reference:
            msg = "Artifact reference is required to fetch the artifact."
            raise ValueError(msg)
        try:
            return subprocess.check_output(
                ["aqago-agent", "fetch-artifact", self.reference],
                stderr=subprocess.STDOUT,
                text=True,
            )
        except FileNotFoundError as e:
            raise AgentNotRunningError from e
        except subprocess.CalledProcessError as e:
            raise FetchArtifactError(e.cmd, e.returncode) from e
        except Exception as e:
            raise RuntimeError from e
