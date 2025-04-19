"""State management for ADCortex chat client."""
from datetime import datetime, timezone, timedelta
from enum import Enum, auto
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class ClientState(Enum):
    """Client operational states."""
    IDLE = auto()
    PROCESSING = auto()

class CircuitBreaker:
    """Circuit breaker for handling error thresholds and timeouts."""
    def __init__(
        self,
        threshold: int = 5,
        timeout: int = 120,  # 2 minutes
        disable_logging: bool = False
    ):
        self._threshold = threshold
        self._timeout = timeout
        self._error_count = 0
        self._reset_time: Optional[datetime] = None
        self._is_open = False
        self._disable_logging = disable_logging

    def _log_error(self, message: str) -> None:
        """Log error message if logging is enabled."""
        if not self._disable_logging:
            logger.error(message)

    def record_error(self) -> None:
        """Record an error and update circuit breaker state."""
        self._error_count += 1
        if self._error_count >= self._threshold and not self._is_open:
            self._is_open = True
            self._reset_time = datetime.now(timezone.utc) + timedelta(seconds=self._timeout)
            self._log_error("Circuit breaker opened due to too many errors")

    def is_open(self) -> bool:
        """Check if circuit breaker is open and update state if needed."""
        if not self._is_open:
            return False

        now = datetime.now(timezone.utc)
        if self._reset_time and now >= self._reset_time:
            self._is_open = False
            self._error_count = 0
            self._reset_time = None
            return False

        return True

    def reset(self) -> None:
        """Reset the circuit breaker state."""
        self._is_open = False
        self._error_count = 0
        self._reset_time = None 