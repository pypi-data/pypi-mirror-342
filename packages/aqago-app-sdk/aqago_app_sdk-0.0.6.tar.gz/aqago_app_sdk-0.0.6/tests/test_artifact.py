"""Tests for the App class in aqago_app_sdk.app module."""

import subprocess

from pytest_mock import MockerFixture

from aqago_app_sdk.artifact import Artifact


def test_artifact_initialization() -> None:
    """Test the initialization of the Artifact class."""
    artifact = Artifact(
        name="test-artifact",
        version="1.0.0",
        metadata={"key": "value"},
        url="s3://bucket/key",
        digest="sha256:123456",
        tags=["tag1", "tag2"],
        variant="test-variant",
        get="https://signed-url",
    )
    assert artifact.name == "test-artifact"
    assert artifact.version == "1.0.0"
    assert artifact.metadata == {"key": "value"}
    assert artifact.url == "s3://bucket/key"
    assert artifact.digest == "sha256:123456"
    assert artifact.tags == ["tag1", "tag2"]
    assert artifact.variant == "test-variant"
    assert artifact.get == "https://signed-url"


def test_artifact_fetch(mocker: MockerFixture) -> None:
    """Test the fetch method of the Artifact class."""
    mock_check_output = mocker.patch("subprocess.check_output")
    mock_check_output.return_value = "Fetch successful"
    artifact = Artifact(
        name="test-artifact",
        version="1.0.0",
        metadata={"key": "value"},
        url="s3://bucket/key",
        digest="sha256:123456",
        tags=["tag1", "tag2"],
        variant="test-variant",
        get="https://signed-url",
        reference="test-artifact-ref",
    )
    result = artifact.fetch()
    mock_check_output.assert_called_once_with(
        ["aqago-agent", "fetch-artifact", "test-artifact-ref"],
        stderr=subprocess.STDOUT,
        text=True,
    )
    assert result == "Fetch successful"
