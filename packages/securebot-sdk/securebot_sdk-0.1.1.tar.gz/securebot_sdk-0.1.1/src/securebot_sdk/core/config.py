import json
import logging
import os
from dataclasses import dataclass, field
from typing import Optional, TypedDict, Union


class ConfigDict(TypedDict):
    """Dictionary representation of the Config class"""

    api_endpoint: Optional[str]
    authz_endpoint: Optional[str]
    token_expiration_buffer: Optional[int]

    log_level: Optional[Union[str, int]]
    client_id: Optional[str]
    client_secret: Optional[str]
    project_id: Optional[str]


@dataclass
class Config:
    """Configuration for the SecureBot SDK"""

    _instance = None

    auth_endpoint: str = field(
        default_factory=lambda: os.getenv(
            "SECUREBOT_AUTH_ENDPOINT", "https://auth.eastus.dev.securebot.io/"
        ),
        metadata={"description": "Base URL for the SecureBot Auth API"},
    )

    authz_endpoint: str = field(
        default_factory=lambda: os.getenv(
            "SECUREBOT_AUTHZ_ENDPOINT", "https://authz.eastus.dev.securebot.io/"
        ),
        metadata={"description": "Base URL for the SecureBot Authz API"},
    )

    trace_endpoint: str = field(
        default_factory=lambda: os.getenv(
            "SECUREBOT_TRACE_ENDPOINT",
            "https://traces.eastus.dev.securebot.io/v1/traces",
        ),
        metadata={"description": "Base URL for the SecureBot Trace API"},
    )

    log_level: Union[str, int] = field(
        default_factory=lambda: os.getenv("SECUREBOT_LOG_LEVEL", "INFO"),
        metadata={"description": "Logging level for SecureBot logs"},
    )
    client_id: str = field(
        default_factory=lambda: os.getenv("SECUREBOT_CLIENT_ID", ""),
        metadata={"description": "Client ID for the Agent Project"},
    )
    client_secret: str = field(
        default_factory=lambda: os.getenv("SECUREBOT_CLIENT_SECRET", ""),
        metadata={"description": "Client secret for the Agent Project"},
    )
    project_id: str = field(
        default_factory=lambda: os.getenv("SECUREBOT_PROJECT_ID", ""),
        metadata={"description": "Project ID for the Agent Project"},
    )
    token_expiration_buffer: int = field(
        default_factory=lambda: int(
            os.getenv("SECUREBOT_TOKEN_EXPIRATION_BUFFER", "300")
        ),
        metadata={"description": "Buffer time for token expiration in seconds"},
    )
    session_id: str = field(
        default_factory=lambda: os.getenv("SECUREBOT_SESSION_ID", ""),
        metadata={"description": "Session ID for the Agent Project"},
    )

    @classmethod
    def initialize(cls, **kwargs) -> "Config":
        """Initialize the singleton instance with provided configuration.

        This should be called before any other Config operations if you want to
        set initial configuration values.
        """
        instance = cls()
        # Configure first, then validate
        instance.configure(**kwargs)
        instance._validate()
        cls._instance = instance
        return instance

    @classmethod
    def get_instance(cls) -> "Config":
        """Get the singleton instance of the Config class."""
        if cls._instance is None:
            cls._instance = cls()
            cls._instance._validate()
        return cls._instance

    def _validate(self):
        """Validate and normalize config"""
        # Normalize auth endpoint
        if self.auth_endpoint:
            self.auth_endpoint = self.auth_endpoint.rstrip("/")
            if not self.auth_endpoint.startswith(("http://", "https://")):
                self.auth_endpoint = f"https://{self.auth_endpoint}"

        # Normalize authz endpoint
        if self.authz_endpoint:
            self.authz_endpoint = self.authz_endpoint.rstrip("/")
            if not self.authz_endpoint.startswith(("http://", "https://")):
                self.authz_endpoint = f"https://{self.authz_endpoint}"

        # Normalize trace endpoint
        if self.trace_endpoint:
            self.trace_endpoint = self.trace_endpoint.rstrip("/")
            if not self.trace_endpoint.startswith(("http://", "https://")):
                self.trace_endpoint = f"https://{self.trace_endpoint}"

        # Normalize log level
        if isinstance(self.log_level, str):
            log_level_str = self.log_level.upper()
            if hasattr(logging, log_level_str):
                self.log_level = getattr(logging, log_level_str)
            else:
                self.log_level = logging.INFO

        # Validate required fields
        if not self.client_id or not self.client_secret or not self.project_id:
            raise ValueError(
                "Missing required configuration. Please provide client_id, client_secret, "
                "and project_id either through environment variables or configuration."
            )

    def configure(
        self,
        auth_endpoint: Optional[str] = None,
        authz_endpoint: Optional[str] = None,
        trace_endpoint: Optional[str] = None,
        log_level: Optional[Union[str, int]] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        project_id: Optional[str] = None,
        token_expiration_buffer: Optional[int] = None,
        session_id: Optional[str] = None,
    ) -> "Config":
        """Configure settings from kwargs, validating where necessary"""
        if auth_endpoint is not None:
            self.auth_endpoint = auth_endpoint
        if authz_endpoint is not None:
            self.authz_endpoint = authz_endpoint
        if trace_endpoint is not None:
            self.trace_endpoint = trace_endpoint
        if log_level is not None:
            self.log_level = log_level
        if client_id is not None:
            self.client_id = client_id
        if client_secret is not None:
            self.client_secret = client_secret
        if project_id is not None:
            self.project_id = project_id
        if token_expiration_buffer is not None:
            self.token_expiration_buffer = token_expiration_buffer
        if session_id is not None:
            self.session_id = session_id
        return self

    def dict(self) -> ConfigDict:
        """Return a dictionary representation of the config"""
        return {
            "log_level": self.log_level,
            "client_id": self.client_id,
            "trace_endpoint": self.trace_endpoint,
            "client_secret": self.client_secret,
            "project_id": self.project_id,
            "auth_endpoint": self.auth_endpoint,
            "authz_endpoint": self.authz_endpoint,
            "token_expiration_buffer": self.token_expiration_buffer,
            "session_id": self.session_id,
        }

    def json(self) -> str:
        """Return a JSON representation of the config"""
        return json.dumps(self.dict())


def get_config() -> Config:
    """Get the singleton config instance"""
    return Config.get_instance()
