import logging

from resume_cli.config import get_settings

_configured = False


def setup_logging() -> logging.Logger:
    global _configured
    logger = logging.getLogger("resume_cli")
    if not _configured:
        settings = get_settings()
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(getattr(logging, settings.log_level, logging.WARNING))
        _configured = True
    return logger
