from cheshirecat_python_sdk.endpoints.base import AbstractEndpoint
from cheshirecat_python_sdk.models.api.settings import SettingsOutputCollection, SettingOutputItem


class SettingsEndpoint(AbstractEndpoint):
    def __init__(self, client: "CheshireCatClient"):
        super().__init__(client)
        self.prefix = "/settings"

    def get_settings(self, agent_id: str | None = None) -> SettingsOutputCollection:
        """
        This endpoint returns the settings of the agent identified by the agent_id parameter (multi-agent installations)
        You can omit the agent_id parameter in a single-agent installation. In this case, the settings of the default
        agent are returned.
        :param agent_id: The id of the agent to get settings for (optional)
        :return: SettingsOutputCollection, the settings of the agent
        """
        return self.get(self.prefix, SettingsOutputCollection, agent_id)

    def post_setting(self, values: dict, agent_id: str | None = None) -> SettingOutputItem:
        """
        This method creates a new setting for the agent identified by the agent_id parameter (multi-agent installations).
        You can omit the agent_id parameter in a single-agent installation. In this case, the setting is created for the
        default agent.
        :param values: The values of the setting to create
        :param agent_id: The id of the agent to create the setting for (optional)
        :return: SettingOutputItem, the created setting
        """
        return self.post_json(self.prefix, SettingOutputItem, values, agent_id)

    def get_setting(self, setting_id: str, agent_id: str | None = None) -> SettingOutputItem:
        """
        This endpoint returns the setting identified by the setting_id parameter. The setting must belong to the agent
        identified by the agent_id parameter (multi-agent installations). You can omit the agent_id parameter in a
        single-agent installation. In this case, the setting is looked up in the default agent.
        :param setting_id: The id of the setting to get
        :param agent_id: The id of the agent to get the setting for (optional)
        :return: SettingOutputItem, the setting
        """
        return self.get(self.format_url(setting_id), SettingOutputItem, agent_id)

    def put_setting(self, setting_id: str, values: dict, agent_id: str | None = None) -> SettingOutputItem:
        """
        This method updates the setting identified by the setting_id parameter. The setting must belong to the agent
        identified by the agent_id parameter (multi-agent installations). You can omit the agent_id parameter in a
        single-agent installation. In this case, the setting is updated in the default agent.
        :param setting_id: The id of the setting to update
        :param values: The values to update the setting with
        :param agent_id: The id of the agent to update the setting for (optional)
        :return: SettingOutputItem, the updated setting
        """
        return self.put(self.format_url(setting_id), SettingOutputItem, values, agent_id)

    def delete_setting(self, setting_id: str, agent_id: str | None = None) -> SettingOutputItem:
        """
        This endpoint deletes the setting identified by the setting_id parameter. The setting must belong to the agent
        identified by the agent_id parameter (multi-agent installations). You can omit the agent_id parameter in a
        single-agent installation. In this case, the setting is deleted from the default agent.
        :param setting_id: The id of the setting to delete
        :param agent_id: The id of the agent to delete the setting for (optional)
        :return: SettingOutputItem, the deleted setting
        """
        return self.delete(self.format_url(setting_id), SettingOutputItem, agent_id)
