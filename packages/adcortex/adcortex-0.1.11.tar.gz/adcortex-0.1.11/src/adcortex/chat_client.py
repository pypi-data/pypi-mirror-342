"""Chat Client for ADCortex API with sequential message processing"""

import os
import uuid
from datetime import datetime, timezone, timedelta
import logging
from typing import Any, Dict, List, Optional
from enum import Enum, auto

import httpx
from dotenv import load_dotenv
from pydantic import ValidationError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from .types import Ad, AdResponse, Message, Role, SessionInfo
from .state import ClientState, CircuitBreaker

# Load environment variables from .env file
load_dotenv()

DEFAULT_CONTEXT_TEMPLATE = "Here is a product the user might like: {ad_title} - {ad_description}: here is a sample way to present it: {placement_template}"
AD_FETCH_URL = "https://adcortex.3102labs.com/ads/matchv2"

# Configure logging
logger = logging.getLogger(__name__)

class AdcortexChatClient:
    def __init__(
        self,
        session_info: SessionInfo,
        context_template: Optional[str] = DEFAULT_CONTEXT_TEMPLATE,
        api_key: Optional[str] = None,
        timeout: Optional[int] = 3,
        log_level: Optional[int] = logging.ERROR,
        disable_logging: bool = False,
        max_queue_size: int = 100,
        circuit_breaker_threshold: int = 5,
        circuit_breaker_timeout: int = 120,  # 2 minutes
    ):
        self._session_info = session_info
        self._context_template = context_template
        self._api_key = api_key or os.getenv("ADCORTEX_API_KEY")
        self._headers = {
            "Content-Type": "application/json",
            "X-API-KEY": self._api_key,
        }
        self._timeout = timeout
        self.latest_ad = None
        self._disable_logging = disable_logging
        
        # Queue management
        self._message_queue: List[Message] = []
        self._max_queue_size = max_queue_size
        
        # State management
        self._state = ClientState.IDLE
        
        # Circuit breaker
        self._circuit_breaker = CircuitBreaker(
            threshold=circuit_breaker_threshold,
            timeout=circuit_breaker_timeout,
            disable_logging=disable_logging
        )
        
        # Configure logging
        if not disable_logging:
            logger.setLevel(log_level)
            if not logger.handlers:
                handler = logging.StreamHandler()
                formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                handler.setFormatter(formatter)
                logger.addHandler(handler)

        if not self._api_key:
            raise ValueError("ADCORTEX_API_KEY is not set and not provided")

    def _log_info(self, message: str) -> None:
        """Log info message if logging is enabled."""
        if not self._disable_logging:
            logger.info(message)

    def _log_error(self, message: str) -> None:
        """Log error message if logging is enabled."""
        if not self._disable_logging:
            logger.error(message)

    def __call__(self, role: Role, content: str) -> None:
        """Add a message to the queue and process it."""
        current_message = Message(
            role=role,
            content=content,
            timestamp=datetime.now(timezone.utc).timestamp()
        )
            
        # Always add message to queue, remove oldest if full
        if len(self._message_queue) >= self._max_queue_size:
            self._message_queue.pop(0)  # Remove oldest message
            self._log_info("Queue full, removed oldest message")
        
        self._message_queue.append(current_message)
        self._log_info(f"Message queued: {role} - {content}")

        # Process queue if not already processing, role is user, and circuit breaker is closed
        if self._state == ClientState.IDLE and role == Role.user and not self._circuit_breaker.is_open():
            self._state = ClientState.PROCESSING
            try:
                self._process_queue()
            except Exception as e:
                self._log_error(f"Processing failed: {e}")
                self._circuit_breaker.record_error()
            finally:
                self._state = ClientState.IDLE

    def _process_queue(self) -> None:
        """Process all messages in the queue in a single batch."""
        if not self._message_queue:
            return

        # Take a snapshot of current messages
        messages_to_process = list(self._message_queue)
        self._log_info(f"Processing {len(messages_to_process)} messages in batch")
        
        try:
            self._fetch_ad_batch(messages_to_process)
            # Only remove messages that were successfully processed
            self._message_queue = self._message_queue[len(messages_to_process):]
        except httpx.TimeoutException as e:
            self._log_error(f"Batch request timed out: {e}")
            self._circuit_breaker.record_error()
            raise
        except httpx.RequestError as e:
            self._log_error(f"Batch request failed: {e}")
            self._circuit_breaker.record_error()
            raise
        except ValidationError as e:
            self._log_error(f"Invalid response format: {e}")
            self._circuit_breaker.record_error()
            raise
        except Exception as e:
            self._log_error(f"Unexpected error processing batch: {e}")
            self._circuit_breaker.record_error()
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.RequestError))
    )
    def _fetch_ad_batch(self, messages: List[Message]) -> None:
        """Fetch an ad based on all messages in a batch."""
        payload = self._prepare_batch_payload(messages)
        print(payload)
        self._send_request(payload)

    def _prepare_batch_payload(self, messages: List[Message]) -> Dict[str, Any]:
        """Prepare the payload for the batch ad request."""
        # Convert session info to dict and handle enum values
        session_info_dict = self._session_info.model_dump()
        user_info_dict = session_info_dict["user_info"]
        user_info_dict["interests"] = [interest.value for interest in session_info_dict["user_info"]["interests"]]
        
        # Convert messages to dict and handle enum values
        messages_dict = []
        for msg in messages:
            msg_dict = msg.model_dump()
            msg_dict["role"] = msg_dict["role"].value
            messages_dict.append(msg_dict)
        
        return {
            "RGUID": str(uuid.uuid4()),
            "session_info": {
                "session_id": session_info_dict["session_id"],
                "character_name": session_info_dict["character_name"],
                "character_metadata": session_info_dict["character_metadata"],
            },
            "user_data": user_info_dict,
            "messages": messages_dict,
            "platform": session_info_dict["platform"]
        }

    def _send_request(self, payload: Dict[str, Any]) -> None:
        """Send the request to the ADCortex API synchronously."""
        try:
            with httpx.Client(timeout=self._timeout) as client:
                response = client.post(
                    AD_FETCH_URL,
                    headers=self._headers,
                    json=payload
                )
                response.raise_for_status()
                self._handle_response(response.json())
        except httpx.TimeoutException:
            self._log_error("Request timed out")
            raise
        except httpx.RequestError as e:
            self._log_error(f"Error fetching ad: {e}")
            raise

    def _handle_response(self, response_data: Dict[str, Any]) -> None:
        """Handle the response from the ad request."""
        try:
            parsed_response = AdResponse(**response_data)
            if parsed_response.ads:
                self.latest_ad = parsed_response.ads[0]
                self._log_info(f"Ad fetched: {self.latest_ad.ad_title}")
                return parsed_response.ads[0]
            else:
                self._log_info("No ads returned")
                return {}
        except ValidationError as e:
            self._log_error(f"Invalid ad response format: {e}")
            return {}

    def create_context(self, latest_ad: Ad) -> str:
        """Create a context string for the last seen ad."""
        return self._context_template.format(**latest_ad.model_dump())

    def get_latest_ad(self) -> Optional[Ad]:
        """Get the latest ad and clear it from memory."""
        latest = self.latest_ad
        self.latest_ad = None
        return latest

    def get_state(self) -> ClientState:
        """Get current client state."""
        return self._state

    def is_healthy(self) -> bool:
        """Check if the client is in a healthy state."""
        return (
            not self._circuit_breaker.is_open()
            and len(self._message_queue) < self._max_queue_size
        )
