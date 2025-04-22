meta:
  id: tc66c
  title: TC66C load meter which can measure various properties of USB-C devices
  endian: le
doc: |
  Poll data is returned as 3x 64 byte blocks of data, a total of 192 bytes.
  Each block is prefixed by pacX with X as 1, 2, or 3.
  The returned data is encrypted using AES in ECB mode.
  All integers are little endian.

  Missing information:
   - Information about "Quick charge" / "PD" mode
   - Recording status/data
   - Time since the device has been switched on
doc-ref:
  - https://sigrok.org/wiki/RDTech_TC66C#Protocol_response_format_(%22Poll_data%22)
seq:
  - id: magic
    contents: 'pac1'

  - id: product_name
    type: str
    size: 4
    encoding: ASCII
    doc: Is always 'TC66'

  - id: version
    type: str
    size: 4
    encoding: ASCII

  - id: serial
    type: u4

  - id: unknown
    size: 28
    doc: Contains unknown data

  - id: number_of_runs
    type: s4
    doc: Counter increases by one with every power supply

  - id: raw_voltage
    type: s4
  - id: raw_current
    type: s4
  - id: raw_power
    type: s4

  - id: crc16_pac1
    type: u4

###################################################################################################

  - id: pac2
    contents: 'pac2'

  - id: raw_resistor
    type: s4

  - id: raw_group0ah
    type: s4
  - id: raw_group0wh
    type: s4

  - id: raw_group1ah
    type: s4
  - id: raw_group1wh
    type: s4

  - id: temperature_sign
    type: u4
  - id: raw_temperature
    type: u4

  - id: raw_data_plus
    type: s4
  - id: raw_data_minus
    type: s4

  - id: unused
    size: 20
    doc: Always zero?

  - id: crc16_pac2
    type: u4

###################################################################################################

  - id: pac3
    contents: 'pac3'
    doc: The third block is always zero (with CRC16)

###################################################################################################

instances:
  voltage:
    value: raw_voltage / 10000.0
  current:
    value: raw_current / 100000.0
  power:
    value: raw_power / 10000.0
  resistor:
    value: raw_resistor / 10.0
  group0ah:
    value: raw_group0ah / 1000.0
  group0wh:
    value: raw_group0wh / 1000.0
  group1ah:
    value: raw_group1ah / 1000.0
  group1wh:
    value: raw_group1wh / 1000.0
  temperature:
    value: 'temperature_sign == 0 ? raw_temperature : -raw_temperature'
  data_plus:
    value: raw_data_plus / 100.0
  data_minus:
    value: raw_data_minus / 100.0



