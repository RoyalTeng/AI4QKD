"""Structured logging via structlog."""
from __future__ import annotations

import logging
import structlog


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Return a structlog bound logger for *name*."""
    logging.basicConfig(level=logging.WARNING)
    return structlog.get_logger(name)
