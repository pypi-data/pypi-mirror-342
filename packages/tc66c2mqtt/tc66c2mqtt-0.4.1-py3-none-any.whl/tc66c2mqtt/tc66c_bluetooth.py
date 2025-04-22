import logging
import time

from bleak import AdvertisementData, BleakClient, BleakGATTCharacteristic, BleakScanner, BLEDevice
from rich import print  # noqa

from tc66c2mqtt.constants import (
    ASK_FOR_VALUES_COMMAND,
    BLEAK_CLIENT_TIMEOUT,
    RX_CHARACTERISTIC_UUID,
    TX_CHARACTERISTIC_UUID,
)
from tc66c2mqtt.tc66 import parse_tc66_packet
from tc66c2mqtt.tc66_decryptor import tc66_decryptor
from tc66c2mqtt.types import PollCallbackProtocol


logger = logging.getLogger(__name__)


class NotificationHandler:
    def __init__(self, poll_callback: PollCallbackProtocol):
        self.poll_callback = poll_callback

    def __call__(self, sender, data: bytearray):
        length = len(data)
        if length != 192:
            logger.error(f'Wrong data: {length=} is not 192!')
            print(data)

        decoded_data = tc66_decryptor(crypted_data=data)
        if parsed_data := parse_tc66_packet(decoded_data):
            self.poll_callback(
                crypted_data=data,
                decoded_data=decoded_data,
                parsed_data=parsed_data,
            )
        else:
            logger.error('Error parsing data: %r', decoded_data)


async def device_info(*, device: BLEDevice, notify_handler):
    print(f'Connect to {device}...', flush=True, end='')

    async with BleakClient(device, timeout=BLEAK_CLIENT_TIMEOUT) as client:
        print('connected.')
        print(f'{client.services.services=}')

        tx_characteristic: BleakGATTCharacteristic = client.services.get_characteristic(
            specifier=TX_CHARACTERISTIC_UUID
        )
        print(f'tx_characteristic: {tx_characteristic}')
        print(f'{tx_characteristic.properties=}')

        rx_characteristic: BleakGATTCharacteristic = client.services.get_characteristic(
            specifier=RX_CHARACTERISTIC_UUID
        )
        print(f'rx_characteristic: {rx_characteristic}')
        print(f'{rx_characteristic.properties=}')

        try:
            while True:
                await client.write_gatt_char(char_specifier=tx_characteristic, data=ASK_FOR_VALUES_COMMAND)
                await client.start_notify(char_specifier=rx_characteristic, callback=notify_handler)
                time.sleep(1)
        finally:
            print('stop notify')
            await client.stop_notify(char_specifier=rx_characteristic)


async def poll(device_name, poll_callback: PollCallbackProtocol):

    notify_handler = NotificationHandler(poll_callback)

    async with BleakScanner() as scanner:
        seen_addresses = set()
        print(f'Scanning for TC66C device named {device_name!r}...\n')

        async for device, advertisement_data in scanner.advertisement_data():
            device: BLEDevice
            advertisement_data: AdvertisementData

            if device.address in seen_addresses:
                continue

            seen_addresses.add(device.address)

            print(f'New device {len(seen_addresses)} found:', device)
            print()
            print(advertisement_data)
            print()

            if device.name != device_name:
                print('skipped.')
            else:
                await device_info(device=device, notify_handler=notify_handler)

        print('Scan complete.')
