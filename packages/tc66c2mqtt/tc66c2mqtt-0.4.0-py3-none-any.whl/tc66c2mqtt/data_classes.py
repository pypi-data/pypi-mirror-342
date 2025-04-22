import dataclasses


@dataclasses.dataclass
class TC66PollData:
    product_name: str  # e.g.: 'TC66'
    version: str  # e.g., '1.14'
    serial: int
    number_of_runs: int
    #
    voltage: float  # in Volts
    current: float  # in Amperes
    power: float  # in Watts
    #
    resistor: float  # in Ohms
    #
    group0Ah: float  # in Ampere-hours
    group0Wh: float  # in Watt-hours
    group1Ah: float  # in Ampere-hours
    group1Wh: float  # in Watt-hours
    #
    temperature: int  # in Celsius
    #
    data_plus: float  # in Volts
    data_minus: float  # in Volts
