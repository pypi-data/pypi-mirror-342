import multiprocessing
import time
from typing import Any, Generator

import pytest
import requests

from ..adapter_config import AdapterConfig
from ..server import AdapterServer


@pytest.fixture
def adapter_server(
    fake_openai_endpoint,
    tmp_path,
) -> Generator[AdapterServer, Any, Any]:
    adapter = AdapterServer(
        api_url="http://localhost:3300/v1/chat/completions",
        adapter_config=AdapterConfig(
            use_request_caching=True,
            request_caching_dir=str(tmp_path / "cache"),
            # TODO(agronskiy): there's bunch of logic in nvcf, would be nice to test
            use_nvcf=False,
            use_response_logging=True,
            use_reasoning=True,
            end_reasoning_token="</think>",
        ),
    )
    p = multiprocessing.Process(target=adapter.run)
    p.start()
    time.sleep(0.1)
    yield adapter

    p.terminate()


def test_adapter_server_post_request(adapter_server, capfd):

    url = f"http://{adapter_server.adapter_host}:{adapter_server.adapter_port}"
    data = {
        "prompt": "This is a test prompt",
        "max_tokens": 100,
        "temperature": 0.5,
    }

    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert "choices" in response.json()
    assert len(response.json()["choices"]) > 0

    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert "choices" in response.json()
    assert len(response.json()["choices"]) > 0
    # We also test that reasoning has gone
    assert "</think>" not in response.json()["choices"][0]["message"]["content"]
