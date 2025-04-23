from cheshirecat_python_sdk.endpoints.base import AbstractEndpoint
from cheshirecat_python_sdk.models.api.nested.plugins import PluginSettingsOutput
from cheshirecat_python_sdk.models.api.plugins import PluginCollectionOutput, PluginToggleOutput, PluginsSettingsOutput


class PluginsEndpoint(AbstractEndpoint):
    def __init__(self, client: "CheshireCatClient"):
        super().__init__(client)
        self.prefix = "/plugins"

    def get_available_plugins(
        self, plugin_name: str | None = None, agent_id: str | None = None
    ) -> PluginCollectionOutput:
        """
        This endpoint returns the available plugins, either for the agent identified by the agent_id parameter
        (for multi-agent installations) or for the default agent (for single-agent installations).
        :param plugin_name: The name of the plugin to get
        :param agent_id: The id of the agent
        :return: PluginCollectionOutput, the available plugins
        """
        return self.get(
            self.prefix,
            PluginCollectionOutput,
            agent_id,
            query={"query": plugin_name} if plugin_name else {},
        )

    def put_toggle_plugin(self, plugin_id: str, agent_id: str | None = None) -> PluginToggleOutput:
        """
        This endpoint toggles a plugin, either for the agent identified by the agent_id parameter (for multi-agent
        installations) or for the default agent (for single-agent installations).
        :param plugin_id: The id of the plugin to toggle
        :param agent_id: The id of the agent
        :return: PluginToggleOutput, the toggled plugin
        """
        return self.put(
            self.format_url(f"/toggle/{plugin_id}"),
            PluginToggleOutput,
            {},
            agent_id,
        )

    def get_plugins_settings(self, agent_id: str | None = None) -> PluginsSettingsOutput:
        """
        This endpoint retrieves the plugins settings, either for the agent identified by the agent_id parameter
        (for multi-agent installations) or for the default agent (for single-agent installations).
        :param agent_id: The id of the agent
        :return: PluginsSettingsOutput, the plugins settings
        """
        return self.get(
            self.format_url("/settings"),
            PluginsSettingsOutput,
            agent_id,
        )

    def get_plugin_settings(self, plugin_id: str, agent_id: str | None = None) -> PluginSettingsOutput:
        """
        This endpoint retrieves the plugin settings, either for the agent identified by the agent_id parameter
        (for multi-agent installations) or for the default agent (for single-agent installations).
        :param plugin_id: The id of the plugin
        :param agent_id: The id of the agent
        :return: PluginSettingsOutput, the plugin settings
        """
        return self.get(
            self.format_url(f"/settings/{plugin_id}"),
            PluginSettingsOutput,
            agent_id,
        )

    def put_plugin_settings(self, plugin_id: str, values: dict, agent_id: str | None = None) -> PluginSettingsOutput:
        """
        This endpoint updates the plugin settings, either for the agent identified by the agent_id parameter
        (for multi-agent installations) or for the default agent (for single-agent installations).
        :param plugin_id: The id of the plugin
        :param values: The values to update
        :param agent_id: The id of the agent
        :return: PluginSettingsOutput, the updated plugin settings
        """
        return self.put(
            self.format_url(f"/settings/{plugin_id}"),
            PluginSettingsOutput,
            values,
            agent_id,
        )
