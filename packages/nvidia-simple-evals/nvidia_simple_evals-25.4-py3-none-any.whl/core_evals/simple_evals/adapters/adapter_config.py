"""Submodule responsible for the configuration related specifically to adapters.

For the visibility reasons, we don't expose adapter configuration via CLI. All the
adaptor config comes from the framework configuration yaml under
```yaml
target:
  api_endpoint:
    adapter_config:
      use_response_logging: true
      use_reasoning: true
      use_nvcf: true
      use_request_caching: true
      request_caching_dir: /some/dir
```

This module merely takes such a dict and translates it into a typed dataclass.
"""

from typing import Any

from pydantic import BaseModel, Field


class AdapterConfig(BaseModel):

    @staticmethod
    def get_validated_config(run_config: dict[str, Any]) -> "AdapterConfig | None":
        """Factory. Shall return `None` if the adapter_config is not passed, or validate the schema.

        Args:
            run_config: is the main dict of a configuration run, see `api_dataclasses`.
        """
        # TODO(agronskiy, jira/COML1KNX-475), CAVEAT: adaptor will be bypassed alltogether in a rare
        # case when streaming is requested. See https://nvidia.slack.com/archives/C06QX6WQ30U/p1742451700506539 and
        # jira issue.
        if run_config.get("target", {}).get("api_endpoint", {}).get("stream", False):
            return None
        
        # TODO mbien: adaptors need to be bypassed for embedding use cases as they don't work
        if run_config.get("target", {}).get("api_endpoint", {}).get("type", "") == "embedding":
            return None

        adapter_config = (
            run_config.get("target", {}).get("api_endpoint", {}).get("adapter_config")
        )
        if not adapter_config:
            return None
        return AdapterConfig.model_validate(adapter_config)

    use_response_logging: bool = Field(
        description="Whether to log endpoint responses",
        default=False,
    )

    use_reasoning: bool = Field(
        description="Whether to use the reasoning adapter",
        default=False,
    )

    end_reasoning_token: str = Field(
        description="Token that singifies the end of reasoning output",
        default="</think>",
    )

    use_nvcf: bool = Field(
        description="Whether to use the NVCF endpoint adapter",
        default=False,
    )

    use_request_caching: bool = Field(
        description="Whether to use the request caching adapter",
        default=False,
    )

    request_caching_dir: str = Field(
        description="Directory for adapter cache storage (optional)",
        default="cache",
    )

    use_system_prompt: bool = Field(
        description="Whether to use custom system prompt adapter",
        default=False
    )

    custom_system_prompt: str = Field(
        description="A custom system prompt to replace original one",
        default=""
    )
