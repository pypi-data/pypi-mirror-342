from typing import Annotated, Protocol

import tyro

from tc66c2mqtt.constants import DEFAULT_DEVICE_NAME
from tc66c2mqtt.data_classes import TC66PollData


class PollCallbackProtocol(Protocol):
    def __call__(
        self,
        *,
        crypted_data: bytes,
        decoded_data: bytes,
        parsed_data: TC66PollData,
    ) -> None: ...


TyroDeviceNameArgType = Annotated[
    str,
    tyro.conf.arg(
        # aliases=['-v'],
        default=DEFAULT_DEVICE_NAME,
        help='Bluetooth device name',
    ),
]
