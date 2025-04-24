import multiprocessing
from dataclasses import dataclass
from typing import Any, Generator

import pytest
from flask import Flask, jsonify, request


@pytest.fixture
def fake_openai_endpoint() -> Generator[Any, Any, Any]:
    """Fixture to create a Flask app with an OpenAI response.

    Being a "proper" fake endpoint, it responds with a payload which can be
    set via app.config.response.
    """

    app = Flask(__name__)
    fake_response = {
        "object": "chat.completion",
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "This is a fake LLM response</think>This survives reasoning",
                }
            }
        ],
    }

    # In the chat_completion route

    @app.route("/v1/chat/completions", methods=["POST"])
    def chat_completion():
        data = request.json
        if "fake_response" in data:
            response = data["fake_response"]
        else:
            response = fake_response
        return jsonify(response)

    def run_app():
        app.run(host="localhost", port=3300)

    p = multiprocessing.Process(target=run_app)
    p.start()
    yield p

    p.terminate()
