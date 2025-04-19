import functools
from typing import Any, Callable, TypeVar

from securebot_sdk.core.identity_manager import get_identity_manager
from securebot_sdk.logger import configure_logging

# Parameter name for passing agent role
AGENT_ROLE_PARAM = "agent_iam_ctx"
F = TypeVar("F", bound=Callable[..., Any])
logger = configure_logging()


def requires_tool_scope(scope: str, pass_token: bool = False):
    """Class decorator to intercept method calls."""

    def decorator(cls):
        #  __init__
        original_init = cls.__init__
        idm = get_identity_manager()
        agent_iam_role = ""

        # Update __init__ method
        @functools.wraps(original_init)
        def new_init(self, *args, **kwargs):
            logger.info("Initializing %s", cls.__name__)

            if AGENT_ROLE_PARAM not in kwargs:
                raise RuntimeError(f"Missing required parameter: {AGENT_ROLE_PARAM}")
            else:
                agent_iam_role = kwargs[AGENT_ROLE_PARAM]

            if pass_token:
                try:
                    logger.info("Getting token for agent %s", agent_iam_role)
                    ctx = idm.get_context(agent_iam_role)
                    kwargs["token"] = ctx.access_token
                except (ValueError, RuntimeError) as e:
                    raise RuntimeError(f"Failed to get token: {e}") from e

            # Call the original __init__
            original_init(self, *args, **kwargs)
            logger.info("Initialized %s with scope: %s", cls.__name__, scope)

        # Update _run method
        if hasattr(cls, "_run"):
            original_run = cls._run

            @functools.wraps(original_run)
            def new_run(self, *args, **kwargs):
                try:
                    logger.info(
                        "Performing scope validation for agent %s with scope %s",
                        agent_iam_role,
                        scope,
                    )
                    valid = idm.validate_scope(self.token, scope)

                    if valid:
                        logger.info(
                            "Access allowed for agent %s for scope %s",
                            agent_iam_role,
                            scope,
                        )
                        try:
                            result = original_run(self, *args, **kwargs)
                            return result
                        except (ValueError, RuntimeError) as run_error:
                            logger.error(
                                "Error during execution of tool %s: %s",
                                self.name,
                                run_error,
                            )
                            return None
                    else:
                        logger.info(
                            "Access denied for agent %s for scope %s",
                            agent_iam_role,
                            scope,
                        )
                        return None
                except (ValueError, RuntimeError) as e:
                    logger.error(
                        "Error occurred while validating scope for agent %s: %s",
                        agent_iam_role,
                        e,
                    )
                    return None

            # Update _run method
            cls._run = new_run

        # Update __init__ method
        cls.__init__ = new_init

        return cls

    return decorator
