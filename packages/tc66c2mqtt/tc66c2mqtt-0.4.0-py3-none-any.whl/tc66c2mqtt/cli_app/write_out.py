import asyncio
import dataclasses
import datetime
import json
import time
from pathlib import Path
from typing import Annotated

import tyro
from cli_base.cli_tools.verbosity import setup_logging
from cli_base.tyro_commands import TyroVerbosityArgType
from rich import print  # noqa

from tc66c2mqtt.cli_app import app
from tc66c2mqtt.data_classes import TC66PollData
from tc66c2mqtt.tc66c import Tc66c
from tc66c2mqtt.tc66c_bluetooth import poll
from tc66c2mqtt.types import TyroDeviceNameArgType


class FileWriter:
    def __init__(self, count: int):
        self.count = count

    def __enter__(self):
        return self

    def __call__(self, *, crypted_data: bytes, decoded_data: bytes, parsed_data: TC66PollData):
        tc66c = Tc66c.from_bytes(decoded_data)

        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')

        raw_out_path = Path(f'tc66c_{timestamp}_raw.bin')
        raw_out_path.write_bytes(crypted_data)

        decoded_out_path = Path(f'tc66c_{timestamp}_decoded.bin')
        decoded_out_path.write_bytes(decoded_data)

        parsed_out_path = Path(f'tc66c_{timestamp}_parsed.json')
        parsed_data = dataclasses.asdict(parsed_data)
        json_data = json.dumps(parsed_data, indent=4, sort_keys=True)
        parsed_out_path.write_text(json_data)

        print(f'{self.count:02} wrote {timestamp} files...', tc66c.unknown.hex())
        self.count -= 1
        if self.count <= 0:
            print('Done writing files')
            raise SystemExit(0)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            return False


TyroCountArgType = Annotated[
    int,
    tyro.conf.arg(
        default=10,
        help='Number of files to write',
    ),
]


@app.command
def write(verbosity: TyroVerbosityArgType, device_name: TyroDeviceNameArgType, count: TyroCountArgType):
    """
    Write files from TC66C data to disk.
    """
    setup_logging(verbosity=verbosity)

    with FileWriter(count=count) as file_writer:
        while file_writer.count > 0:
            try:
                asyncio.run(poll(device_name=device_name, poll_callback=file_writer))
            except Exception as e:
                print(f'Error: {e}')
                print('Retrying in 1 second...')
                time.sleep(1)
