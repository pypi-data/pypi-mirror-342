from unittest import TestCase

from tc66c2mqtt.tc66_decryptor import tc66_decryptor
from tc66c2mqtt.tests.fixtures import RAW_TC66_DATA, get_dectyped_data


class TC66DecryptorTestCase(TestCase):
    def test_tc66_decryptor(self):
        result: bytes = tc66_decryptor(crypted_data=RAW_TC66_DATA)
        dectyped_data: bytes = get_dectyped_data()
        self.assertEqual(result.hex(), dectyped_data.hex())
