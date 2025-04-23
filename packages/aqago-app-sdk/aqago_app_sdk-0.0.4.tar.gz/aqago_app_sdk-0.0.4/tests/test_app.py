"""Tests for the App class in aqago_app_sdk.app module."""

import json
import subprocess

import pytest
from pytest_mock import MockerFixture

from aqago_app_sdk.app import (
    AgentNotRunningError,
    App,
    GetArtifactError,
    GetArtifactResponseError,
)
from aqago_app_sdk.artifact import Artifact


def test_get_artifact(mocker: MockerFixture) -> None:
    """Test the get_artifact method of the App class."""
    artifact_res = {
        "name": "test-artifact",
        "version": "1.0.0",
        "metadata": {"key": "value"},
        "url": "s3://bucket/key",
        "digest": "sha256:123456",
        "tags": ["tag1", "tag2"],
        "variant": "test-variant",
        "get": "https://signed-url",
    }
    mock_check_output = mocker.patch("subprocess.check_output")
    mock_check_output.return_value = bytes(json.dumps(artifact_res), "utf-8")
    app = App(reference="test-app", deployment="main", resources=[])
    artifact = app.get_artifact("test-artifact")
    assert isinstance(artifact, Artifact)
    assert artifact.name == "test-artifact"
    assert artifact.version == "1.0.0"
    assert artifact.metadata == {"key": "value"}
    assert artifact.url == "s3://bucket/key"
    assert artifact.digest == "sha256:123456"
    assert artifact.tags == ["tag1", "tag2"]
    assert artifact.variant == "test-variant"
    assert artifact.get == "https://signed-url"


def test_get_artifact_command_error(mocker: MockerFixture) -> None:
    """Test the get_artifact method of the App class with command error."""
    mock_check_output = mocker.patch("subprocess.check_output")
    mock_check_output.side_effect = subprocess.CalledProcessError(
        1,
        "cmd",
        output=b"Error",
    )
    app = App(reference="test-app", deployment="main", resources=[])
    with pytest.raises(GetArtifactError):
        app.get_artifact("test-artifact")


def test_get_artifact_json_error(mocker: MockerFixture) -> None:
    """Test the get_artifact method of the App class with invalid JSON."""
    mock_check_output = mocker.patch("subprocess.check_output")
    mock_check_output.return_value = b"Invalid JSON"
    app = App(reference="test-app", deployment="main", resources=[])
    with pytest.raises(GetArtifactResponseError):
        app.get_artifact("test-artifact")


def test_get_artifact_agent_not_running(mocker: MockerFixture) -> None:
    """Test the get_artifact method when the agent is not running."""
    mock_check_output = mocker.patch("subprocess.check_output")
    mock_check_output.side_effect = FileNotFoundError("Command not found")
    app = App(reference="test-app", deployment="main", resources=[])
    with pytest.raises(AgentNotRunningError):
        app.get_artifact("test-artifact")
