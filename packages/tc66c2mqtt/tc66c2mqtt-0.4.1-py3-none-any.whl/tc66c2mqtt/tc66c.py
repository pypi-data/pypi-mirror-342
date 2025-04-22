# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception(
        f"Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have {kaitaistruct.__version__}"
    )


class Tc66c(KaitaiStruct):
    """Poll data is returned as 3x 64 byte blocks of data, a total of 192 bytes.
    Each block is prefixed by pacX with X as 1, 2, or 3.
    The returned data is encrypted using AES in ECB mode.
    All integers are little endian.

    Missing information:
     - Information about "Quick charge" / "PD" mode
     - Recording status/data
     - Time since the device has been switched on

    .. seealso::
       Source - https://sigrok.org/wiki/RDTech_TC66C#Protocol_response_format_(%22Poll_data%22)
    """

    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic = self._io.read_bytes(4)
        if not self.magic == b"\x70\x61\x63\x31":
            raise kaitaistruct.ValidationNotEqualError(b"\x70\x61\x63\x31", self.magic, self._io, "/seq/0")
        self.product_name = (self._io.read_bytes(4)).decode("ASCII")
        self.version = (self._io.read_bytes(4)).decode("ASCII")
        self.serial = self._io.read_u4le()
        self.unknown = self._io.read_bytes(28)
        self.number_of_runs = self._io.read_s4le()
        self.raw_voltage = self._io.read_s4le()
        self.raw_current = self._io.read_s4le()
        self.raw_power = self._io.read_s4le()
        self.crc16_pac1 = self._io.read_u4le()
        self.pac2 = self._io.read_bytes(4)
        if not self.pac2 == b"\x70\x61\x63\x32":
            raise kaitaistruct.ValidationNotEqualError(b"\x70\x61\x63\x32", self.pac2, self._io, "/seq/10")
        self.raw_resistor = self._io.read_s4le()
        self.raw_group0ah = self._io.read_s4le()
        self.raw_group0wh = self._io.read_s4le()
        self.raw_group1ah = self._io.read_s4le()
        self.raw_group1wh = self._io.read_s4le()
        self.temperature_sign = self._io.read_u4le()
        self.raw_temperature = self._io.read_u4le()
        self.raw_data_plus = self._io.read_s4le()
        self.raw_data_minus = self._io.read_s4le()
        self.unused = self._io.read_bytes(20)
        self.crc16_pac2 = self._io.read_u4le()
        self.pac3 = self._io.read_bytes(4)
        if not self.pac3 == b"\x70\x61\x63\x33":
            raise kaitaistruct.ValidationNotEqualError(b"\x70\x61\x63\x33", self.pac3, self._io, "/seq/22")

    @property
    def resistor(self):
        if hasattr(self, '_m_resistor'):
            return self._m_resistor

        self._m_resistor = self.raw_resistor / 10.0
        return getattr(self, '_m_resistor', None)

    @property
    def group0ah(self):
        if hasattr(self, '_m_group0ah'):
            return self._m_group0ah

        self._m_group0ah = self.raw_group0ah / 1000.0
        return getattr(self, '_m_group0ah', None)

    @property
    def temperature(self):
        if hasattr(self, '_m_temperature'):
            return self._m_temperature

        self._m_temperature = self.raw_temperature if self.temperature_sign == 0 else -(self.raw_temperature)
        return getattr(self, '_m_temperature', None)

    @property
    def data_plus(self):
        if hasattr(self, '_m_data_plus'):
            return self._m_data_plus

        self._m_data_plus = self.raw_data_plus / 100.0
        return getattr(self, '_m_data_plus', None)

    @property
    def voltage(self):
        if hasattr(self, '_m_voltage'):
            return self._m_voltage

        self._m_voltage = self.raw_voltage / 10000.0
        return getattr(self, '_m_voltage', None)

    @property
    def group1wh(self):
        if hasattr(self, '_m_group1wh'):
            return self._m_group1wh

        self._m_group1wh = self.raw_group1wh / 1000.0
        return getattr(self, '_m_group1wh', None)

    @property
    def data_minus(self):
        if hasattr(self, '_m_data_minus'):
            return self._m_data_minus

        self._m_data_minus = self.raw_data_minus / 100.0
        return getattr(self, '_m_data_minus', None)

    @property
    def group0wh(self):
        if hasattr(self, '_m_group0wh'):
            return self._m_group0wh

        self._m_group0wh = self.raw_group0wh / 1000.0
        return getattr(self, '_m_group0wh', None)

    @property
    def power(self):
        if hasattr(self, '_m_power'):
            return self._m_power

        self._m_power = self.raw_power / 10000.0
        return getattr(self, '_m_power', None)

    @property
    def group1ah(self):
        if hasattr(self, '_m_group1ah'):
            return self._m_group1ah

        self._m_group1ah = self.raw_group1ah / 1000.0
        return getattr(self, '_m_group1ah', None)

    @property
    def current(self):
        if hasattr(self, '_m_current'):
            return self._m_current

        self._m_current = self.raw_current / 100000.0
        return getattr(self, '_m_current', None)
