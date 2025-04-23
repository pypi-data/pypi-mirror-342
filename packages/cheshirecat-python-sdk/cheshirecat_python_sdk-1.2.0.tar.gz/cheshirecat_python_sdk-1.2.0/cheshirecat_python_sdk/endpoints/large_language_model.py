from typing import Dict, Any

from cheshirecat_python_sdk.endpoints.base import AbstractEndpoint
from cheshirecat_python_sdk.models.api.factories import FactoryObjectSettingsOutput, FactoryObjectSettingOutput


class LargeLanguageModelEndpoint(AbstractEndpoint):
    def __init__(self, client: "CheshireCatClient"):
        super().__init__(client)
        self.prefix = "/llm"

    def get_large_language_models_settings(self, agent_id: str | None = None) -> FactoryObjectSettingsOutput:
        """
        Get all large language model settings for the agent specified by agent_id
        :param agent_id: The agent id
        :return: FactoryObjectSettingsOutput, a list of large language model settings
        """
        return self.get(
            self.format_url("/settings"),
            FactoryObjectSettingsOutput,
            agent_id,
        )

    def get_large_language_model_settings(self, llm: str, agent_id: str | None = None) -> FactoryObjectSettingOutput:
        """
        Get the large language model settings for the large language model specified by llm and agent_id
        :param llm: The name of the large language model
        :param agent_id: The agent id
        :return: FactoryObjectSettingOutput, the large language model settings
        """
        return self.get(
            self.format_url(f"/settings/{llm}"),
            FactoryObjectSettingOutput,
            agent_id,
        )

    def put_large_language_model_settings(
        self, llm: str, values: Dict[str, Any], agent_id: str | None = None
    ) -> FactoryObjectSettingOutput:
        """
        Update the large language model settings for the large language model specified by llm and agent_id
        :param llm: The name of the large language model
        :param values: The new settings
        :param agent_id: The agent id
        :return: FactoryObjectSettingOutput, the updated large language model settings
        """
        return self.put(
            self.format_url(f"/settings/{llm}"),
            FactoryObjectSettingOutput,
            values,
            agent_id,
        )
