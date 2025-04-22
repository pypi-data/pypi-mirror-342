import logging

from ha_services.mqtt4homeassistant.components.sensor import Sensor
from ha_services.mqtt4homeassistant.device import MainMqttDevice, MqttDevice
from ha_services.mqtt4homeassistant.mqtt import get_connected_client

import tc66c2mqtt
from tc66c2mqtt.data_classes import TC66PollData
from tc66c2mqtt.user_settings import UserSettings


logger = logging.getLogger(__name__)


class Tc66cMqttHandler:
    def __init__(self, user_settings: UserSettings, verbosity: int):
        self.user_settings = user_settings
        self.device_name = user_settings.device_name

        self.mqtt_client = get_connected_client(settings=user_settings.mqtt, verbosity=verbosity)
        self.mqtt_client.loop_start()

        self.main_device = None

    def init_device(self, *, parsed_data: TC66PollData):
        self.main_device = MainMqttDevice(
            name='TC66C 2 MQTT',
            uid=str(parsed_data.serial),
            manufacturer='tc66c2mqtt',
            sw_version=tc66c2mqtt.__version__,
            config_throttle_sec=self.user_settings.mqtt.publish_config_throttle_seconds,
        )
        self.mqtt_device = MqttDevice(
            main_device=self.main_device,
            name=self.device_name,
            uid=parsed_data.product_name,
            manufacturer='RDTech',
            sw_version=parsed_data.version,
            config_throttle_sec=self.user_settings.mqtt.publish_config_throttle_seconds,
        )

        #################################################################################

        self.number_of_runs = Sensor(
            device=self.mqtt_device,
            name='Number Of Runs',
            uid='number_of_runs',
            state_class='measurement',
            min_value=0,
        )

        #################################################################################

        self.voltage = Sensor(
            device=self.mqtt_device,
            name='Voltage',
            uid='voltage',
            device_class='voltage',
            state_class='measurement',
            unit_of_measurement='V',
            suggested_display_precision=3,
            min_value=0,  # Properly min. 5V, isn't it?
            max_value=30,
        )
        self.current = Sensor(
            device=self.mqtt_device,
            name='Current',
            uid='current',
            device_class='current',
            state_class='measurement',
            unit_of_measurement='A',
            suggested_display_precision=3,
            min_value=0,
            max_value=5,
        )
        self.power = Sensor(
            device=self.mqtt_device,
            name='Power',
            uid='power',
            device_class='power',
            state_class='measurement',
            unit_of_measurement='W',
            suggested_display_precision=3,
            min_value=0,
            max_value=30 * 5,
        )

        #################################################################################

        self.resistor = Sensor(
            device=self.mqtt_device,
            name='Resistor',
            uid='resistor',
            state_class='measurement',
            unit_of_measurement='Ω',
            suggested_display_precision=1,
            min_value=0,
        )
        self.data_plus = Sensor(
            device=self.mqtt_device,
            name='Data +',
            uid='data_plus',
            state_class='measurement',
            unit_of_measurement='V',
            suggested_display_precision=3,
        )
        self.data_minus = Sensor(
            device=self.mqtt_device,
            name='Data -',
            uid='data_minus',
            state_class='measurement',
            unit_of_measurement='V',
            suggested_display_precision=3,
        )

        #################################################################################

        self.group0Ah = Sensor(
            device=self.mqtt_device,
            name='Group 0 Ah',
            uid='group0ah',
            state_class='measurement',
            unit_of_measurement='Ah',
            suggested_display_precision=3,
            min_value=0,
        )
        self.group0Wh = Sensor(
            device=self.mqtt_device,
            name='Group 0 Wh',
            uid='group0wh',
            state_class='measurement',
            unit_of_measurement='Wh',
            suggested_display_precision=3,
            min_value=0,
        )

        self.group1Ah = Sensor(
            device=self.mqtt_device,
            name='Group 1 Ah',
            uid='group1ah',
            state_class='measurement',
            unit_of_measurement='Ah',
            suggested_display_precision=3,
            min_value=0,
        )
        self.group1Wh = Sensor(
            device=self.mqtt_device,
            name='Group 1 Wh',
            uid='group1wh',
            state_class='measurement',
            unit_of_measurement='Wh',
            suggested_display_precision=3,
            min_value=0,
        )

        #################################################################################

        self.temperature = Sensor(
            device=self.mqtt_device,
            name='Temperature',
            uid='temperature',
            state_class='measurement',
            unit_of_measurement='°C',
            suggested_display_precision=1,
            # From the docs, it's only 0-80°C and the device usage temperature is ony 0-45°C
            # But it seems that can be also negative, so guess:
            min_value=-20,
            max_value=80,
        )

    def __call__(self, *, crypted_data: bytes, decoded_data: bytes, parsed_data: TC66PollData):
        logger.info(f'Parsed data: {parsed_data}')

        if self.main_device is None:
            self.init_device(parsed_data=parsed_data)

        self.main_device.poll_and_publish(self.mqtt_client)

        #################################################################################

        self.number_of_runs.set_state(parsed_data.number_of_runs)
        self.number_of_runs.publish(self.mqtt_client)

        #################################################################################

        self.voltage.set_state(parsed_data.voltage)
        self.voltage.publish(self.mqtt_client)

        self.current.set_state(parsed_data.current)
        self.current.publish(self.mqtt_client)

        self.power.set_state(parsed_data.power)
        self.power.publish(self.mqtt_client)

        #################################################################################

        self.resistor.set_state(parsed_data.resistor)
        self.resistor.publish(self.mqtt_client)

        self.data_plus.set_state(parsed_data.data_plus)
        self.data_plus.publish(self.mqtt_client)

        self.data_minus.set_state(parsed_data.data_minus)
        self.data_minus.publish(self.mqtt_client)

        #################################################################################

        self.group0Ah.set_state(parsed_data.group0Ah)
        self.group0Ah.publish(self.mqtt_client)

        self.group0Wh.set_state(parsed_data.group0Wh)
        self.group0Wh.publish(self.mqtt_client)

        self.group1Ah.set_state(parsed_data.group1Ah)
        self.group1Ah.publish(self.mqtt_client)

        self.group1Wh.set_state(parsed_data.group1Wh)
        self.group1Wh.publish(self.mqtt_client)

        #################################################################################

        self.temperature.set_state(parsed_data.temperature)
        self.temperature.publish(self.mqtt_client)
