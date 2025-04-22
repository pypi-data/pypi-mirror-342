import asyncio
from pprint import pprint

from bleak import AdvertisementData, BleakClient, BLEDevice
from cli_base.cli_tools.verbosity import setup_logging
from cli_base.tyro_commands import TyroVerbosityArgType
from rich import print  # noqa

from tc66c2mqtt.cli_app import app


@app.command
def scan(verbosity: TyroVerbosityArgType):
    """
    Discover Bluetooth devices and there services/descriptors
    """
    setup_logging(verbosity=verbosity)

    async def device_info(device: BLEDevice):
        print(f'Connect to {device}...', flush=True, end='')

        async with BleakClient(device) as client:
            print('connected.')

            for service in client.services:
                print('_' * 79)
                print('Service:', service)

                for char in service.characteristics:
                    print(f'{char.properties=}')
                    if 'read' in char.properties:
                        try:
                            value = await client.read_gatt_char(char.uuid)
                        except Exception as err:
                            print('\tERROR:', err)
                        else:
                            print(f'\tread: {value=}')

                    for descriptor in char.descriptors:
                        print('Descriptor:', descriptor)
                        try:
                            value = await client.read_gatt_descriptor(descriptor.handle)
                        except Exception as err:
                            print(f'\tError: {err}')
                        else:
                            print(f'\t{value=}')

                print()

    async def main():
        from collections.abc import Sequence

        from bleak import BleakClient, BleakScanner
        from bleak.backends.device import BLEDevice

        print('Discovering devices...')
        devices: Sequence[BLEDevice] = await BleakScanner.discover(timeout=5.0)
        print('Discovered:')
        pprint(devices)

        for d in devices:
            try:
                async with BleakClient(d) as client:
                    print(client.services)
            except TimeoutError as err:
                print('Timeout:', err)

        print('-' * 79)

        async with BleakScanner(scanning_mode='active') as scanner:
            seen_addresses = set()
            print('Scanning...\n')

            async for device, advertisement_data in scanner.advertisement_data():
                device: BLEDevice
                advertisement_data: AdvertisementData

                if device.address in seen_addresses:
                    return
                seen_addresses.add(device.address)

                print('New device found:', device)
                print()
                print(advertisement_data)
                print()
                try:
                    await device_info(device)
                except TimeoutError as err:
                    print('Timeout:', err)

    asyncio.run(main())
