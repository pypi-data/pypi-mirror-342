"""Tests for the client module."""

from securebot_sdk import AgentAuth


def test_client_initialization():
    """Test that client initializes properly."""
    client = AgentAuth(api_key="test-key")
    assert client.api_key == "test-key"
