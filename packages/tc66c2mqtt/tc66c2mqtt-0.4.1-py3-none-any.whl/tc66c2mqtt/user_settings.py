import dataclasses
import logging
import sys

from cli_base.systemd.data_classes import BaseSystemdServiceInfo, BaseSystemdServiceTemplateContext
from cli_base.toml_settings.api import TomlSettings
from cli_base.tyro_commands import TyroVerbosityArgType
from ha_services.mqtt4homeassistant.data_classes import MqttSettings
from rich import print  # noqa

from tc66c2mqtt.constants import DEFAULT_DEVICE_NAME


logger = logging.getLogger(__name__)


@dataclasses.dataclass
class SystemdServiceTemplateContext(BaseSystemdServiceTemplateContext):
    """
    Context values for the systemd service file content.
    """

    verbose_service_name: str = 'tc66c2mqtt'
    exec_start: str = f'{sys.argv[0]} publish-loop'


@dataclasses.dataclass
class SystemdServiceInfo(BaseSystemdServiceInfo):
    """
    Information for systemd helper functions.
    """

    template_context: SystemdServiceTemplateContext = dataclasses.field(default_factory=SystemdServiceTemplateContext)


@dataclasses.dataclass
class UserSettings:
    """
    TC66C -> MQTT - settings

    Note: Insert at least device address + key and your MQTT settings.

    See README for more information.
    """

    device_name: str = DEFAULT_DEVICE_NAME

    # Information about the MQTT server:
    mqtt: dataclasses = dataclasses.field(default_factory=MqttSettings)

    systemd: dataclasses = dataclasses.field(default_factory=SystemdServiceInfo)


def get_toml_settings() -> TomlSettings:
    return TomlSettings(
        dir_name='tc66c2mqtt',
        file_name='tc66c2mqtt',
        settings_dataclass=UserSettings(),
    )


def get_user_settings(verbosity: TyroVerbosityArgType) -> UserSettings:
    toml_settings: TomlSettings = get_toml_settings()
    user_settings: UserSettings = toml_settings.get_user_settings(debug=verbosity > 0)
    return user_settings
