import logging

from kaitaistruct import KaitaiStructError

from tc66c2mqtt.data_classes import TC66PollData
from tc66c2mqtt.tc66c import Tc66c


logger = logging.getLogger(__name__)


def parse_tc66_packet(data: bytes) -> TC66PollData | None:
    """
    Parse TC66 packet data via Python parser generated
    from Kaitai Struct YAML file `tc66c.ksy`.

    https://sigrok.org/wiki/RDTech_TC66C#Protocol_response_format_(%22Poll_data%22)
    """
    try:
        tc66c = Tc66c.from_bytes(data)
    except KaitaiStructError as err:
        logger.exception(f'Failed to parse TC66 packet data: {err}')
        return None

    return TC66PollData(
        product_name=tc66c.product_name,
        version=tc66c.version,
        serial=tc66c.serial,
        number_of_runs=tc66c.number_of_runs,
        #
        voltage=tc66c.voltage,
        current=tc66c.current,
        power=tc66c.power,
        #
        resistor=tc66c.resistor,
        #
        group0Ah=tc66c.group0ah,
        group0Wh=tc66c.group0wh,
        group1Ah=tc66c.group1ah,
        group1Wh=tc66c.group1wh,
        #
        temperature=tc66c.temperature,
        #
        data_plus=tc66c.data_plus,
        data_minus=tc66c.data_minus,
    )
