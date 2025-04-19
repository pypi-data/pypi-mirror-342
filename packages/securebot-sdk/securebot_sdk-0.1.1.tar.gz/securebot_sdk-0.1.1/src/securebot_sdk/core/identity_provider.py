import uuid
from typing import Optional

from securebot_sdk.core.config import Config, get_config
from securebot_sdk.core.identity_manager import (
    IdentityManagerContext,
    get_identity_manager,
)
from securebot_sdk.logger import configure_logging
from securebot_sdk.tracing.tracing import Tracing

logger = configure_logging()


class IdentityProvider:
    """Handles agent authentication and token management."""

    def __init__(
        self,
        project_id: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        tracing: Optional[bool] = False,
    ):
        """Initialize the AgentAuth class with configuration.

        Args:
            project_id: The project ID for the agent
            client_id: The client ID for the agent
            client_secret: The client secret for the agent
        """
        self.session_id = str(uuid.uuid4())
        if any([project_id, client_id, client_secret]):
            Config.initialize(
                project_id=project_id,
                client_id=client_id,
                client_secret=client_secret,
                session_id=self.session_id,
            )
        self.config = get_config()
        self.identity_manager = get_identity_manager()
        logger.info(
            "Initialized AgentAuth with project_id=%s, client_id=%s, session_id=%s",
            self.config.project_id,
            self.config.client_id,
            self.session_id,
        )

        if tracing:
            logger.info("Initializing the access token for tracing")
            token = self.create_agent_context("")
            self.tracer = Tracing(token).get_tracer()

    @property
    def get_session_id(self) -> str:
        """Get the current session ID.

        Returns:
            str: The session ID
        """
        return self.session_id

    def get_agent_token(self, agent_iam_role: str) -> Optional[str]:
        """Get a token for the specified agent role.

        Args:
            agent_iam_role: The IAM role for the agent

        Returns:
            str: The agent token
        """
        return self.identity_manager.get_token(agent_iam_role)

    def create_agent_context(self, agent_iam_role: str) -> IdentityManagerContext:
        """Create a new agent context for the specified agent role.

        Args:
            agent_iam_role: The IAM role for the agent

        Returns:
            AgentIAMContext: The agent context
        """
        return self.identity_manager.create_context(agent_iam_role)

    def get_agent_context(
        self, agent_iam_role: str
    ) -> Optional[IdentityManagerContext]:
        """Get the context for the specified agent role.

        Args:
            agent_iam_role: The IAM role for the agent

        Returns:
            IdentityManagerContext: The agent context
        """
        return self.identity_manager.get_context(agent_iam_role)

    def validate_scope(self, token: str, required_scope: str) -> bool:
        """Validate if a token has the required scope.

        Args:
            token: The token to validate
            required_scope: The required scope

        Returns:
            bool: True if the token has the required scope, False otherwise
        """
        return self.identity_manager.validate_scope(token, required_scope)
