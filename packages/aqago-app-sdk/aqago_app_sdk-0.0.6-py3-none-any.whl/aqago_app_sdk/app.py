"""Application class."""

import json
import subprocess

from .artifact import Artifact
from .errors import (
    AgentNotRunningError,
    GetArtifactError,
    GetArtifactResponseError,
)


class App:
    """Class representing an application."""

    def __init__(
        self,
        reference: str,
        deployment: str,
        resources: dict[str, dict] | None = None,
    ) -> None:
        """Initialize the App object."""
        self.reference: str = reference
        self.deployment: str = deployment
        self.resources: dict[str, dict] | None = resources

    def get_artifact(self, reference: str) -> Artifact:
        """Get the artifact by its reference."""
        try:
            data: dict[str, any] = json.loads(
                subprocess.check_output(
                    [
                        "aqago-agent",
                        "get-artifact",
                        reference,
                    ],
                ).decode(),
            )
            return Artifact(
                name=data["name"],
                version=data.get("version"),
                metadata=data.get(
                    "metadata",
                    {},
                ),
                url=data["url"],
                digest=data["digest"],
                tags=data.get("tags", []),
                variant=data.get("variant"),
                get=data["get"],
                reference=reference,
            )
        except FileNotFoundError as e:
            raise AgentNotRunningError from e
        except subprocess.CalledProcessError as e:
            raise GetArtifactError(e.cmd, e.returncode) from e
        except json.JSONDecodeError as e:
            raise GetArtifactResponseError(e.msg) from e
        except Exception as e:
            raise RuntimeError from e

    @property
    def artifacts(self) -> "ArtifactCollection":
        """Get all artifacts associated with the application."""
        return ArtifactCollection(self)


class ArtifactCollection:
    """Helper class for dictionary-like access to artifacts."""

    def __init__(self, _app: App) -> None:
        """Initialize the ArtifactCollection object."""
        self.app: App = _app

    def __getitem__(self, reference: str) -> Artifact:
        """Get an artifact by its reference."""
        return self.app.get_artifact(reference)
