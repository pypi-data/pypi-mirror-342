from typing import Dict, Any

from cheshirecat_python_sdk.endpoints.base import AbstractEndpoint
from cheshirecat_python_sdk.models.api.factories import FactoryObjectSettingsOutput, FactoryObjectSettingOutput


class ChunkerEndpoint(AbstractEndpoint):
    def __init__(self, client: "CheshireCatClient"):
        super().__init__(client)
        self.prefix = "/chunking"

    def get_chunkers_settings(self, agent_id: str | None = None) -> FactoryObjectSettingsOutput:
        """
        Get all chunker settings for the agent specified by agent_id
        :param agent_id: The agent id
        :return: FactoryObjectSettingsOutput, a list of chunker settings
        """
        return self.get(
            self.format_url("/settings"),
            FactoryObjectSettingsOutput,
            agent_id,
        )

    def get_chunker_settings(self, chunker: str, agent_id: str | None = None) -> FactoryObjectSettingOutput:
        """
        Get the chunker settings for the chunker specified by chunker and agent_id
        :param chunker: The name of the chunker
        :param agent_id: The agent id
        :return: FactoryObjectSettingOutput, the large language model settings
        """
        return self.get(
            self.format_url(f"/settings/{chunker}"),
            FactoryObjectSettingOutput,
            agent_id,
        )

    def put_chunker_settings(
        self, chunker: str, values: Dict[str, Any], agent_id: str | None = None
    ) -> FactoryObjectSettingOutput:
        """
        Update the chunker settings for the chunker specified by chunker and agent_id
        :param chunker: The name of the chunker
        :param values: The new settings
        :param agent_id: The agent id
        :return: FactoryObjectSettingOutput, the updated chunker settings
        """
        return self.put(
            self.format_url(f"/settings/{chunker}"),
            FactoryObjectSettingOutput,
            values,
            agent_id,
        )
