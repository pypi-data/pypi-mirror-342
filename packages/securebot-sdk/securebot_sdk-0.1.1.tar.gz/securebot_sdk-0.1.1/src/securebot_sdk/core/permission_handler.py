import asyncio
import functools
import inspect
import threading
from abc import ABC, abstractmethod
from typing import Any, Callable, Optional, Type, TypeVar, cast

from opentelemetry import trace
from opentelemetry.trace import SpanKind, Status, StatusCode

from securebot_sdk.logger import configure_logging

logger = configure_logging()

F = TypeVar("F", bound=Callable[..., Any])

# Parameter name for passing agent role
AGENT_ROLE_PARAM = "agent_iam_role"


class BasePermissionHandler(ABC):
    """Base class for handling permissions across different frameworks."""

    def __init__(self):
        self.tracer = trace.get_tracer(__name__)

    @abstractmethod
    def check_permission(self, scope: str, agent_role: str) -> bool:
        """Check if the agent has the required permission."""

    @abstractmethod
    def handle_no_permission(
        self, scope: str, agent_role: str, context_type: Type, *args, **kwargs
    ) -> Any:
        """Handle the case when permission is denied.

        Args:
            scope: The required scope
            agent_role: The agent's role
            context_type: The type of the decorated function's first argument (if any).
                        For CrewAI, this would be the Task or Tool class being decorated.
                        For other frameworks, this could be their equivalent task/tool types.
        """
        pass

    def create_decorator(self, scope: str, pass_token: bool = False) -> Callable:
        """Create a permission decorator for the specific framework."""

        def decorator(func: F) -> F:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # Create a new span for each call
                span = self.tracer.start_span(
                    f"permission_check.{func.__name__}", kind=SpanKind.INTERNAL
                )
                try:
                    # Set input attributes
                    span.set_attribute("permission.scope", scope)

                    # We need the agent_iam_role parameter
                    if AGENT_ROLE_PARAM not in kwargs:
                        raise RuntimeError(
                            f"Missing required parameter: {AGENT_ROLE_PARAM}"
                        )

                    # Get the agent role
                    agent_role = kwargs[AGENT_ROLE_PARAM]
                    span.set_attribute("agent.role", agent_role)

                    # Set function context
                    span.set_attribute("function.name", func.__name__)
                    span.set_attribute("function.module", func.__module__)

                    # Clone kwargs without agent_role to avoid passing it to the function
                    filtered_kwargs = {
                        k: v for k, v in kwargs.items() if k != AGENT_ROLE_PARAM
                    }

                    # Get token
                    token = self.get_token(agent_role)
                    if token:
                        span.set_attribute("auth.token_present", True)

                    # Validate scope
                    logger.info(
                        "Performing scope validation for agent %s and resource urn: %s",
                        agent_role,
                        scope,
                    )

                    is_authorized = self.check_permission(scope, agent_role)
                    span.set_attribute("permission.authorized", is_authorized)

                    if not is_authorized:
                        # Get the context from the first argument if it exists
                        context = args[0] if args else None
                        logger.info(
                            "Access denied to the agent %s for the resource %s",
                            agent_role,
                            scope,
                        )
                        span.set_status(Status(StatusCode.ERROR))
                        return self.handle_no_permission(
                            scope,
                            agent_role,
                            type(context) if context else None,
                            *args,
                            **filtered_kwargs,
                        )

                    # Log successful access
                    logger.info(
                        "[%s] Access granted to the agent %s for the resource %s",
                        threading.current_thread().name,
                        agent_role,
                        scope,
                    )
                    span.set_status(Status(StatusCode.OK))

                    # Pass token if requested
                    if pass_token:
                        filtered_kwargs["token"] = token

                    # Call the function
                    result = func(*args, **filtered_kwargs)

                    # Set output attributes
                    if result is not None:
                        span.set_attribute(
                            "function.result_type", type(result).__name__
                        )

                    return result
                finally:
                    span.end()

            if inspect.iscoroutinefunction(func):

                @functools.wraps(func)
                async def async_wrapper(*args, **kwargs):
                    # Create a new span for each call
                    span = self.tracer.start_span(
                        f"permission_check.async.{func.__name__}",
                        kind=SpanKind.INTERNAL,
                    )
                    try:
                        # Set input attributes
                        span.set_attribute("permission.scope", scope)

                        # We need the agent_iam_role parameter
                        if AGENT_ROLE_PARAM not in kwargs:
                            raise RuntimeError(
                                f"Missing required parameter: {AGENT_ROLE_PARAM}"
                            )

                        # Get the agent role
                        agent_role = kwargs[AGENT_ROLE_PARAM]
                        span.set_attribute("agent.role", agent_role)

                        # Set function context
                        span.set_attribute("function.name", func.__name__)
                        span.set_attribute("function.module", func.__module__)

                        # Clone kwargs without agent_role to avoid passing it to the function
                        filtered_kwargs = {
                            k: v for k, v in kwargs.items() if k != AGENT_ROLE_PARAM
                        }

                        # Get token asynchronously if possible
                        loop = asyncio.get_event_loop()
                        token = await loop.run_in_executor(
                            None, lambda: self.get_token(agent_role)
                        )
                        if token:
                            span.set_attribute("auth.token_present", True)

                        # Validate scope
                        is_authorized = await loop.run_in_executor(
                            None, lambda: self.check_permission(scope, agent_role)
                        )
                        span.set_attribute("permission.authorized", is_authorized)

                        if not is_authorized:
                            # Get the context from the first argument if it exists
                            context = args[0] if args else None
                            logger.info(
                                "Access denied to the agent %s for the resource %s",
                                agent_role,
                                scope,
                            )
                            span.set_status(Status(StatusCode.ERROR))
                            return self.handle_no_permission(
                                scope,
                                agent_role,
                                type(context) if context else None,
                                *args,
                                **filtered_kwargs,
                            )

                        # Log successful access
                        logger.info(
                            "[%s] Access granted to the agent %s for the resource %s",
                            threading.current_thread().name,
                            agent_role,
                            scope,
                        )
                        span.set_status(Status(StatusCode.OK))

                        # Pass token if requested
                        if pass_token:
                            filtered_kwargs["token"] = token

                        # Call the function
                        result = await func(*args, **filtered_kwargs)

                        # Set output attributes
                        if result is not None:
                            span.set_attribute(
                                "function.result_type", type(result).__name__
                            )

                        return result
                    finally:
                        span.end()

                return cast(F, async_wrapper)

            return cast(F, wrapper)

        return decorator

    @abstractmethod
    def get_token(self, agent_role: str) -> Optional[str]:
        """Get the token for the agent."""
        pass
