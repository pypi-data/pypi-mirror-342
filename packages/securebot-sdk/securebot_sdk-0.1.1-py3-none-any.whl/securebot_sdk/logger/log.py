import logging
import os

from colorama import Fore, Style, init

# Initialize colorama for cross-platform color support
init()


class SecureBotLogFormatter(logging.Formatter):
    """Formatter for console logging with colors and prefix."""

    prefix = "SecureBot: "

    FORMATS = {
        logging.DEBUG: f"{Fore.CYAN}(DEBUG) {prefix}%(message)s{Style.RESET_ALL}",
        logging.INFO: f"{Fore.GREEN}(INFO) {prefix}%(message)s{Style.RESET_ALL}",
        logging.WARNING: f"{Fore.YELLOW}(WARNING) {prefix}%(message)s{Style.RESET_ALL}",
        logging.ERROR: f"{Fore.RED}(ERROR) {prefix}%(message)s{Style.RESET_ALL}",
        logging.CRITICAL: f"{Fore.RED}(CRITICAL){Style.BRIGHT}{prefix}%(message)s{Style.RESET_ALL}",
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self.FORMATS[logging.INFO])
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# Create the logger at module level
logger = logging.getLogger("securebot")
logger.propagate = False
logger.setLevel(logging.INFO)


def configure_logging(config=None):
    """Configure the SecureBot logger with console and optional file handlers."""
    # Use env var as override if present, otherwise use config
    log_level_env = os.environ.get("SECUREBOT_LOG_LEVEL", "").upper()
    if log_level_env and hasattr(logging, log_level_env):
        log_level = getattr(logging, log_level_env)
    else:
        if config and hasattr(config, "log_level"):
            if isinstance(config.log_level, str):
                log_level_str = config.log_level.upper()
                if hasattr(logging, log_level_str):
                    log_level = getattr(logging, log_level_str)
                else:
                    log_level = logging.INFO
            else:
                log_level = (
                    config.log_level
                    if isinstance(config.log_level, int)
                    else logging.INFO
                )
        else:
            log_level = logging.INFO

    logger.setLevel(log_level)

    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Configure console logging
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(SecureBotLogFormatter())
    logger.addHandler(stream_handler)

    return logger
