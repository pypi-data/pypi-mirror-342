import json
from unittest.mock import MagicMock, patch

import pytest
import requests
from flask import Request

from ..interceptors import (
    AdapterMetadata,
    AdapterRequest,
    AdapterResponse,
    NvcfEndpointInterceptor,
)


@pytest.fixture
def mock_requests():
    with patch("requests.request") as mock_req:
        yield mock_req


@pytest.fixture
def polling_response():
    mock_response = MagicMock()
    mock_response.status_code = 202
    mock_response.headers = {"NVCF-REQID": "test-request-id"}
    mock_response.raw = MagicMock()
    mock_response.raw.headers = {"NVCF-REQID": "test-request-id"}
    return mock_response


@pytest.fixture
def success_response():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = {"status": "success"}
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.raw = MagicMock()
    mock_response.raw.headers = {"Content-Type": "application/json"}
    return mock_response


@pytest.mark.parametrize(
    "retry_count,expected_calls",
    [
        (1, 2),  # One retry means two calls total
        (2, 3),  # Two retries means three calls total
    ],
)
def test_handle_request_polling(
    mock_requests,
    polling_response,
    success_response,
    retry_count,
    expected_calls,
):
    # Given: A request that will initially return a polling response
    mock_requests.reset_mock()

    # We need to mock both requests.request and requests.get
    with patch("requests.get") as mock_get:
        # Set up the polling sequence
        mock_requests.side_effect = [polling_response] + [
            Exception("Should not be called")
        ] * 10
        mock_get.side_effect = [polling_response] * (retry_count - 1) + [
            success_response
        ]

        test_data = {"prompt": "test prompt"}

        # # When: The request is handled with polling
        # with adapter.app.test_request_context(
        #     "/",
        #     method="POST",
        #     headers={
        #         "Authorization": "Bearer test-token",
        #         "Content-Type": "application/json",
        #     },
        # ):
        #     adapter.app.config["STATUS_URL"] = "https://api.test.com/status"
        #     adapter.app.config["FETCH_RETRIES"] = retry_count + 1

        interceptor = NvcfEndpointInterceptor(api_url="http://some.api.url")
        request = Request.from_values(
            method="POST",
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_data),
        )
        adapter_request = AdapterRequest(r=request, meta=AdapterMetadata())
        response = interceptor.intercept_request(ar=adapter_request)

        # Then: The adapter should poll until receiving a success response
        assert mock_requests.call_count == 1  # Initial request
        assert mock_get.call_count == retry_count  # Status check requests
        assert response.r.status_code == 200

        # And: The get requests should be to the status URL with the request ID
        for call in mock_get.call_args_list:
            assert "status" in call[1]["url"]
            assert "test-request-id" in call[1]["url"]
