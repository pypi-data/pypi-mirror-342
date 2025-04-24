import json
from typing import final

import requests
import structlog

from .types import AdapterResponse, ResponseInterceptor


@final
class ResponseLoggingInterceptor(ResponseInterceptor):
    _logger: structlog.BoundLogger

    def __init__(self):
        self._logger = structlog.get_logger(__name__)

    @final
    def intercept_response(self, ar: AdapterResponse) -> AdapterResponse:
        try:
            payload = ar.r.json()
        except requests.exceptions.JSONDecodeError as e:
            self._logger.info(
                "Logging response (non-JSON)",
                raw_content=ar.r.content.decode('utf-8', errors='ignore'),
                cache_hit=ar.meta.cache_hit,
            )
        else:
            # If JSON parsing succeeds, log the parsed JSON
            self._logger.info(
                "Logging response",
                payload=payload,
                cache_hit=ar.meta.cache_hit
            )
        return ar
