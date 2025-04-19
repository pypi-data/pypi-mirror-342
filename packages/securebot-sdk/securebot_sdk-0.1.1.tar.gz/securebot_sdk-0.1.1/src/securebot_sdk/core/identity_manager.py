"""IdentityManager module for handling IAM roles, tokens, and authentication.

This module provides functionality for managing agent IAM contexts, tokens, and authentication.
It implements a singleton pattern to ensure consistent token management across the application.
"""

import threading
import time
from dataclasses import dataclass, field, fields
from datetime import datetime
from threading import RLock
from typing import Dict, List, Optional

import httpx

from securebot_sdk.core.config import get_config
from securebot_sdk.core.http_client import HttpClientConfig, get_client
from securebot_sdk.logger import configure_logging

logger = configure_logging()


@dataclass
class IdentityManagerContext:
    """Data class representing an agent's IAM state and token information.

    Attributes:
        iam_role: The IAM role identifier for the agent
        created_at: Timestamp when the context was created
        last_used: Timestamp of the last token usage
        roles: List of IAM roles associated with this agent
        is_active: Whether the agent context is currently active
        access_token: Current access token for the agent
        token_expires_at: Timestamp when the current token expires
    """

    iam_role: str
    created_at: datetime = field(default_factory=datetime.now)
    last_used: datetime = field(default_factory=datetime.now)
    roles: List[str] = field(default_factory=list)
    is_active: bool = True
    access_token: Optional[str] = None
    token_expires_at: Optional[float] = None

    def update_token(self, token: str, expires_in: int):
        """Update the agent's access token and expiration time.

        Args:
            token: The new access token
            expires_in: Token expiration time in seconds
        """
        self.access_token = token
        self.token_expires_at = time.time() + expires_in

    def is_token_valid(self) -> bool:
        """Check if the current token is still valid.

        Returns:
            bool: True if the token exists and hasn't expired, False otherwise
        """
        if not self.access_token or not self.token_expires_at:
            return False
        return time.time() < self.token_expires_at


@dataclass
class AuthzResponse:
    """Data class representing the response from the authorization endpoint.

    Attributes:
        access_token: The access token string
        expires_in: Token expiration time in seconds
        refresh_expires_in: Refresh token expiration time in seconds
        token_type: Type of the token (e.g., 'Bearer')
        not_before_policy: Time before which the token cannot be used
        scope: The scope of the token
        id_token: Optional ID token from the response
    """

    access_token: str
    expires_in: int
    refresh_expires_in: int
    token_type: str
    not_before_policy: int = field(metadata={"json_field": "not-before-policy"})
    scope: str
    id_token: Optional[str] = None

    @classmethod
    def from_json(cls, data: dict) -> "AuthzResponse":
        """Create an AuthzResponse instance from JSON data.

        Args:
            data: Dictionary containing the authorization response data

        Returns:
            AuthzResponse: A new instance with the parsed data
        """
        mapped_data = data.copy()
        if "not-before-policy" in mapped_data:
            mapped_data["not_before_policy"] = mapped_data.pop("not-before-policy")
        # Remove any fields that aren't in the class definition
        valid_fields = {f.name for f in fields(cls)}
        mapped_data = {k: v for k, v in mapped_data.items() if k in valid_fields}
        return cls(**mapped_data)


class IdentityManager:
    """Manages agent IAM contexts and token lifecycle.

    This class implements a singleton pattern to ensure consistent token management
    across the application. It handles token creation, refresh, and validation.
    """

    _instance = None  # Singleton instance

    def __init__(self):
        """Initialize the IdentityManager with configuration and setup."""
        self._identity_contexts: Dict[str, IdentityManagerContext] = {}
        self._identity_contexts_lock = RLock()
        self._refresh_thread = None
        self._running = True
        self._start_refresh_thread()
        self._client = get_client(
            HttpClientConfig(
                timeout_seconds=30.0,
                connect_timeout_seconds=10.0,
                read_timeout_seconds=30.0,
                write_timeout_seconds=30.0,
                max_retries=3,
            )
        )

    @classmethod
    def get_instance(cls) -> "IdentityManager":
        """Get the singleton instance of the IdentityManager.

        Returns:
            IdentityManager: The singleton instance
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __del__(self):
        """Clean up resources when the instance is destroyed."""
        self._running = False
        if hasattr(self, "_refresh_thread") and self._refresh_thread:
            self._refresh_thread.join(timeout=1.0)
        if hasattr(self, "_client"):
            self._client.close()

    def _start_refresh_thread(self):
        """Start a background thread to refresh tokens.

        The thread runs every minute to check and refresh tokens that are about to expire.
        """

        def refresh():
            while self._running:
                try:
                    self._refresh_tokens()
                except (httpx.HTTPError, ValueError) as e:
                    logger.error("Error in token refresh: %s", str(e), exc_info=True)
                time.sleep(60)  # Run refresh every minute

        self._refresh_thread = threading.Thread(target=refresh, daemon=True)
        self._refresh_thread.start()

    def _refresh_tokens(self):
        """Refresh tokens that are about to expire.

        This method checks all active agent contexts and refreshes tokens that are
        within the expiration buffer time.
        """
        with self._identity_contexts_lock:
            current_time = time.time()
            for context in self._identity_contexts.values():
                if not context.is_active:
                    continue

                if context.token_expires_at and (
                    context.token_expires_at - current_time
                    < get_config().token_expiration_buffer
                ):
                    try:
                        logger.debug(
                            "Auto-refreshing token for agent: %s", context.iam_role
                        )
                        scope = (
                            "openid"
                            if not context.iam_role
                            else f"{get_config().project_id}:{context.iam_role}"
                        )
                        token_data = self._fetch_new_token(scope)
                        context.update_token(
                            token_data.access_token, token_data.expires_in
                        )
                        logger.debug(
                            "Token auto-refreshed for agent: %s", context.iam_role
                        )
                    except (httpx.HTTPError, ValueError) as e:
                        logger.error(
                            "Failed to auto-refresh token for agent %s: %s",
                            context.iam_role,
                            str(e),
                        )

    def create_context(self, agent_iam_role: str) -> IdentityManagerContext:
        """Create a new agent context with initialized token.

        Args:
            agent_iam_role: The IAM role identifier for the agent. If empty, will use "openid" scope.

        Returns:
            AgentIAMContext: The created or existing context

        Raises:
            RuntimeError: If token initialization fails
        """
        with self._identity_contexts_lock:
            if agent_iam_role not in self._identity_contexts:
                try:
                    scope = (
                        "openid"
                        if not agent_iam_role
                        else f"{get_config().project_id}:{agent_iam_role}"
                    )
                    token_data = self._fetch_new_token(scope)
                    context = IdentityManagerContext(
                        iam_role=agent_iam_role,
                        roles=[scope],
                    )
                    context.update_token(token_data.access_token, token_data.expires_in)
                    self._identity_contexts[agent_iam_role] = context
                except (httpx.HTTPError, ValueError) as e:
                    logger.error(
                        "Failed to initialize token for agent %s: %s",
                        agent_iam_role,
                        str(e),
                    )
                    raise RuntimeError(f"Failed to create agent context: {e}") from e
            return self._identity_contexts[agent_iam_role]

    def get_context(self, agent_iam_role: str) -> Optional[IdentityManagerContext]:
        """Get the context for a specific agent.

        Args:
            agent_iam_role: The IAM role identifier for the agent

        Returns:
            Optional[IdentityManagerContext]: The agent context if it exists, None otherwise
        """
        with self._identity_contexts_lock:
            return self._identity_contexts.get(agent_iam_role)

    def get_token(self, agent_iam_role: str) -> Optional[str]:
        """Get a valid token for the agent.

        Args:
            agent_iam_role: The IAM role identifier for the agent

        Returns:
            Optional[str]: The access token if available, None otherwise
        """
        context = self.get_context(agent_iam_role)
        return context.access_token if context else None

    def _fetch_new_token(self, scope: str) -> AuthzResponse:
        """Fetch a new token for the given agent role and scopes.

        Args:
            scope: The scope to use for the token

        Returns:
            AuthzResponse: The authorization response containing the new token

        Raises:
            RuntimeError: If token fetch fails
        """
        try:
            url = f"{get_config().auth_endpoint}/realms/ui-eastus-dev-identity/protocol/openid-connect/token"

            payload = {
                "client_id": get_config().client_id,
                "client_secret": get_config().client_secret,
                "grant_type": "client_credentials",
                "scope": scope,
            }

            headers = {"Content-Type": "application/x-www-form-urlencoded"}

            logger.debug("Fetching token for agent %s", payload)

            response = self._client.post(url, data=payload, headers=headers)
            token_data = AuthzResponse.from_json(response.json())

            logger.debug("Token fetched for agent %s", token_data)
            return token_data

        except httpx.HTTPError as e:
            logger.error("Failed to get agent token: %s", e)
            raise RuntimeError(f"Failed to get agent token: {e}") from e

    def validate_scope(self, token: str, required_scope: str) -> bool:
        """Validate if agent is allowed to access the resource.

        Args:
            token: The access token to validate
            required_scope: The required scope to check

        Returns:
            bool: True if the token has the required scope, False otherwise
        """
        try:
            urn = f"urn:{get_config().project_id}:{required_scope}"
            response = self._client.get(
                f"{get_config().authz_endpoint}",
                headers={
                    "Authorization": f"Bearer {token}",
                    "X-RESOURCE-URN": urn,
                },
            )
            is_authorized = response.status_code == 200

            # Update agent context with scope validation result
            agent_iam_role = required_scope.split(":")[-1]  # Extract role from scope
            context = self.get_context(agent_iam_role)
            if context:
                context.update_scope_grant(required_scope, is_authorized)

            return is_authorized
        except httpx.HTTPError as e:
            logger.error("Scope validation failed: %s", e)
            return False

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit, ensuring cleanup of resources."""
        self._running = False
        if self._refresh_thread:
            self._refresh_thread.join(timeout=1.0)
        if self._client:
            self._client.close()


def get_identity_manager() -> IdentityManager:
    """Get the singleton agent manager instance.

    Returns:
        IdentityManager: The singleton instance
    """
    return IdentityManager.get_instance()
