import hashlib
import json
from typing import Any, final

import flask
import requests
import requests.structures
from urllib3 import HTTPHeaderDict

from ..caching.diskcaching import Cache
from .types import (
    AdapterRequest,
    AdapterResponse,
    RequestInterceptor,
    ResponseInterceptor,
)


@final
class CachingInterceptor(RequestInterceptor, ResponseInterceptor):
    """Caching interceptor is speical in the sense that it intercepts both requests and responses."""

    cache: Cache

    def __init__(self, cache_dir: str):
        self.cache = Cache(directory=cache_dir)

    @staticmethod
    def _generate_cache_key(data: Any) -> str:
        """
        Generate a hash for the request data to be used as the cache key.

        Args:
            data: Data to be hashed

        Returns:
            str: Hash of the data
        """
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode("utf-8")).hexdigest()

    def _get_from_cache(self, cache_key: str) -> tuple[Any, Any] | None:
        """
        Attempt to retrieve content and headers from cache.

        Args:
            cache_key (str): Cache key to lookup

        Returns:
            Optional[tuple[Any, Any]]: Tuple of (content, headers) if found, None if not
        """

        headers_key = f"{cache_key}_headers"
        try:
            cached_content = self.cache[cache_key]
            cached_headers = self.cache[headers_key]
            return cached_content, cached_headers
        except KeyError:
            return None

    def _save_to_cache(self, cache_key: str, content: Any, headers: Any) -> None:
        """
        Save content and headers to cache.

        Args:
            cache_key (str): Cache key to store under
            content: Content to cache
            headers: Headers to cache
        """
        self.cache[cache_key] = content

        # NOTE(# TODO(agronskiy): headers are `CaseInsensitiveDict()` which is not serializable
        # by `Cache` class. If this is the case, transform to a normal dict.
        if isinstance(headers, requests.structures.CaseInsensitiveDict):
            cached_headers = dict(headers)
        else:
            cached_headers = headers
        self.cache[f"{cache_key}_headers"] = cached_headers

    @final
    def intercept_request(self, ar: AdapterRequest) -> AdapterResponse | AdapterRequest:
        """Shall return request if no cache hit, and response if it is."""
        request_data = ar.r.get_json()

        # Check cache. Create cache key that will be used everywhere (also if no cache hit)
        ar.meta.cache_key = self._generate_cache_key(request_data)
        cached_result = self._get_from_cache(ar.meta.cache_key)
        if cached_result:
            content, headers = cached_result

            requests_response = requests.Response()
            requests_response._content = content
            requests_response.status_code = 200
            requests_response.reason = "OK"
            requests_response.headers = requests.utils.CaseInsensitiveDict(headers)
            requests_response.request = request_data

            # Make downstream know
            ar.meta.cache_hit = True

            return AdapterResponse(r=requests_response, meta=ar.meta)

        return ar

    @final
    def intercept_response(self, ar: AdapterResponse) -> AdapterResponse:
        """"""
        # first, if caching was used, we do nothing
        if ar.meta.cache_hit:
            return ar

        if ar.r.status_code == 200:
            # Save both content and headers to cache
            try:
                assert ar.meta.cache_key, "cache key is unset, this is a bug"
                self._save_to_cache(
                    cache_key=ar.meta.cache_key,
                    content=ar.r.content,
                    headers=ar.r.headers,
                )
            except Exception as e:
                print(f"Warning: Could not cache response: {e}")

        # And just propagate
        return ar
