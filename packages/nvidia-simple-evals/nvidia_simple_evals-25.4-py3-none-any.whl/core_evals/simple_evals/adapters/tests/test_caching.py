import json
from typing import cast
from unittest.mock import MagicMock, patch

import pytest
import requests
from flask import Request
from requests.utils import CaseInsensitiveDict

from ..interceptors import (
    AdapterMetadata,
    AdapterRequest,
    AdapterResponse,
    CachingInterceptor,
)


@pytest.fixture
def mock_requests():
    with patch("requests.request") as mock_req:
        yield mock_req


@pytest.mark.parametrize(
    "data1,data2",
    [
        (
            {"prompt": "test", "parameters": {"temp": 0.7}},
            {"parameters": {"temp": 0.7}, "prompt": "test"},
        ),
        (
            {
                "prompt": "test",
                "parameters": {"temp": 0.7, "options": {"a": 1, "b": 2}},
            },
            {
                "parameters": {"options": {"b": 2, "a": 1}, "temp": 0.7},
                "prompt": "test",
            },
        ),
    ],
)
def test_generate_cache_key(data1, data2):
    # Given: Two differently ordered but equivalent data structures

    # When: Cache keys are generated for both
    key1 = CachingInterceptor._generate_cache_key(data1)
    key2 = CachingInterceptor._generate_cache_key(data2)

    # Then: The cache keys should be identical
    assert key1 == key2


@pytest.mark.parametrize(
    "test_data,cached_content,cached_headers",
    [
        (
            {"prompt": "test prompt", "parameters": {"temperature": 0.7}},
            b'{"result": "cached result"}',
            [["Content-Type", "application/json"]],
        ),
        (
            {
                "prompt": "complex prompt",
                "parameters": {"temperature": 0.9, "max_tokens": 100},
            },
            b'{"result": "complex cached result"}',
            [["Content-Type", "application/json"], ["X-Custom-Header", "test-value"]],
        ),
    ],
)
def test_cache_hit(tmp_path, mock_requests, test_data, cached_content, cached_headers):
    interceptor = CachingInterceptor(cache_dir=tmp_path / "cache")
    # Given: A cached response exists for a specific request
    cache_key = interceptor._generate_cache_key(test_data)
    headers_key = f"{cache_key}_headers"

    interceptor.cache[cache_key] = cached_content
    interceptor.cache[headers_key] = cached_headers

    # When: A request is made with the same data
    request = Request.from_values(
        method="POST",
        headers={"Content-Type": "application/json"},
        data=json.dumps(test_data),
    )
    response = interceptor.intercept_request(
        ar=AdapterRequest(r=request, meta=AdapterMetadata())
    )

    # Then: The cached response should be returned without making an API call
    assert isinstance(response, AdapterResponse)
    mock_requests.assert_not_called()
    assert response.r.status_code == 200
    assert response.meta.cache_hit == True


@pytest.fixture
def create_response():
    """Fixture to create paramterized response"""

    def _create_response(status_code, content, headers):
        response = requests.Response()
        response.status_code = status_code
        response._content = content
        response.headers = CaseInsensitiveDict(headers)
        response.raw = MagicMock()
        response.raw.headers = headers
        return response

    return _create_response


@pytest.mark.parametrize(
    "test_data,expected_headers",
    [
        (
            {"prompt": "test prompt", "parameters": {"temperature": 0.7}},
            {"Content-Type": "application/json"},
        ),
        (
            {
                "prompt": "complex prompt",
                "parameters": {"temperature": 0.9, "max_tokens": 100},
            },
            {"Content-Type": "application/json", "X-Custom-Header": "test-value"},
        ),
    ],
)
def test_cache_miss_and_store(
    tmp_path, mock_requests, create_response, test_data, expected_headers
):
    interceptor = CachingInterceptor(cache_dir=tmp_path / "cache")

    # When: A request is made with that data
    request = Request.from_values(
        method="POST",
        headers={"Content-Type": "application/json"},
        data=json.dumps(test_data),
    )
    adapter_request = AdapterRequest(r=request, meta=AdapterMetadata())
    result = interceptor.intercept_request(ar=adapter_request)
    # Then: the interceptor does not intercept, but rather propagates as a request
    assert isinstance(result, AdapterRequest)
    assert result.meta.cache_key

    # On the way back from the endpoint, the request must be cached if the response
    # was not error ==> two branches, failed and success.

    # First, check that the error response is not cached.
    some_error_response = AdapterResponse(
        r=create_response(404, {"error": "bas request"}, expected_headers),
        meta=result.meta,
    )
    interceptor.intercept_response(ar=some_error_response)

    # We assert that the errored response did not result in cachin on the way back.
    assert result.meta.cache_key not in interceptor.cache
    assert result.meta.cache_key + "_headers" not in interceptor.cache

    # Now we model successful response
    some_succesful_reponse = AdapterResponse(
        r=create_response(200, {"result": "success"}, expected_headers),
        meta=result.meta,
    )
    interceptor.intercept_response(ar=some_succesful_reponse)

    assert interceptor.cache[result.meta.cache_key] == {"result": "success"}
    for header in expected_headers:
        assert header in interceptor.cache[result.meta.cache_key + "_headers"]
