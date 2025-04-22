import asyncio
import time


from cli_base.cli_tools.verbosity import setup_logging
from cli_base.tyro_commands import TyroVerbosityArgType
from rich import print  # noqa
from rich.live import Live
from rich.progress import BarColumn, Progress, TaskID, TextColumn

from tc66c2mqtt.cli_app import app
from tc66c2mqtt.data_classes import TC66PollData
from tc66c2mqtt.tc66c_bluetooth import poll
from tc66c2mqtt.types import TyroDeviceNameArgType


class StatsOut:
    def __init__(self):
        self.live = None
        self.progress = Progress(
            '{task.description}',
            BarColumn(bar_width=None),
            TextColumn('{task.completed}'),
            TextColumn('{task.fields[unit]}'),
        )

        self.voltage_task_id: TaskID = self.progress.add_task(
            description='[green]Voltage',
            total=30,
            unit='V',
        )
        self.current_task_id: TaskID = self.progress.add_task(
            description='[green]Current',
            total=5,
            unit='A',
        )
        self.power_task_id: TaskID = self.progress.add_task(
            description='[green]Power',
            total=30 * 5,
            unit='W',
        )

        self.resistor_task_id: TaskID = self.progress.add_task(
            description='[green]Resistor',
            total=1000,
            unit='Ω',
        )

        self.group0Ah_task_id: TaskID = self.progress.add_task(
            description='[green]Group 0 Ah',
            total=10000,
            unit='Ah',
        )
        self.group0Wh_task_id: TaskID = self.progress.add_task(
            description='[green]Group 0 Wh',
            total=10000,
            unit='Wh',
        )
        self.group1Ah_task_id: TaskID = self.progress.add_task(
            description='[green]Group 1 Ah',
            total=10000,
            unit='Ah',
        )
        self.group1Wh_task_id: TaskID = self.progress.add_task(
            description='[green]Group 1 Wh',
            total=10000,
            unit='Wh',
        )

        self.temperature_task_id: TaskID = self.progress.add_task(
            description='[green]Temperature',
            total=60,
            unit='°C',
        )

        self.data_plus_task_id: TaskID = self.progress.add_task(
            description='[green]Data +',
            total=5,
            unit='V',
        )
        self.data_minus_task_id: TaskID = self.progress.add_task(
            description='[green]Data -',
            total=5,
            unit='V',
        )

    def __enter__(self):
        return self

    def __call__(self, *, crypted_data: bytes, decoded_data: bytes, parsed_data: TC66PollData):
        if self.live is None:
            print(
                f'\n\n{parsed_data.product_name} v{parsed_data.version}'
                f' Serial: {parsed_data.serial} (Number of runs: {parsed_data.number_of_runs})'
            )
            self.live = Live(self.progress, refresh_per_second=10)
            self.live.__enter__()

        self.progress.update(self.voltage_task_id, completed=parsed_data.voltage)
        self.progress.update(self.current_task_id, completed=parsed_data.current)
        self.progress.update(self.power_task_id, completed=parsed_data.power)

        self.progress.update(self.resistor_task_id, completed=parsed_data.resistor)

        self.progress.update(self.group0Ah_task_id, completed=parsed_data.group0Ah)
        self.progress.update(self.group0Wh_task_id, completed=parsed_data.group0Wh)

        self.progress.update(self.group1Ah_task_id, completed=parsed_data.group1Ah)
        self.progress.update(self.group1Wh_task_id, completed=parsed_data.group1Wh)

        self.progress.update(self.temperature_task_id, completed=parsed_data.temperature)

        self.progress.update(self.data_plus_task_id, completed=parsed_data.data_plus)
        self.progress.update(self.data_minus_task_id, completed=parsed_data.data_minus)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.live is not None:
            self.live.__exit__(exc_type, exc_val, exc_tb)


@app.command
def print_data(verbosity: TyroVerbosityArgType, device_name: TyroDeviceNameArgType):
    """
    Print TC66C data to console
    """
    setup_logging(verbosity=verbosity)

    with StatsOut() as stats_out:
        while True:
            try:
                asyncio.run(poll(device_name=device_name, poll_callback=stats_out))
            except Exception as e:
                print(f'Error: {e}')
                print('Retrying in 1 second...')
                time.sleep(1)
