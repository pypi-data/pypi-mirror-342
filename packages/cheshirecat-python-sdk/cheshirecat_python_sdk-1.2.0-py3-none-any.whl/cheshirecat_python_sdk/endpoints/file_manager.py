from typing import Dict, Any

from cheshirecat_python_sdk.endpoints.base import AbstractEndpoint
from cheshirecat_python_sdk.models.api.factories import FactoryObjectSettingOutput, FactoryObjectSettingsOutput


class FileManagerEndpoint(AbstractEndpoint):
    def __init__(self, client: "CheshireCatClient"):
        super().__init__(client)
        self.prefix = "/file_manager"

    def get_file_managers_settings(self) -> FactoryObjectSettingsOutput:
        """
        Get all file managers settings
        :return: FactoryObjectSettingsOutput, the settings of all file managers
        """
        return self.get(
            self.format_url("/settings"),
            FactoryObjectSettingsOutput,
            self.system_id,
        )

    def get_file_manager_settings(self, file_manager: str) -> FactoryObjectSettingOutput:
        """
        Get the settings of a file manager by name
        :param file_manager: str, the name of the file manager
        :return: FactoryObjectSettingOutput, the settings of the file manager
        """
        return self.get(
            self.format_url(f"/settings/{file_manager}"),
            FactoryObjectSettingOutput,
            self.system_id,
        )

    def put_file_manager_settings(self, file_manager: str, values: Dict[str, Any]) -> FactoryObjectSettingOutput:
        """
        Update the settings of a file manager by name with the given values
        :param file_manager: str, the name of the file manager
        :param values: Dict[str, Any], the values to update
        :return: FactoryObjectSettingOutput, the updated settings of the file manager
        """
        return self.put(
            self.format_url(f"/settings/{file_manager}"),
            FactoryObjectSettingOutput,
            values,
            self.system_id,
        )
