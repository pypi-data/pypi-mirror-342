from unittest import TestCase

from tc66c2mqtt.data_classes import TC66PollData
from tc66c2mqtt.tc66 import parse_tc66_packet
from tc66c2mqtt.tests.fixtures import get_dectyped_data


class Tc66TestCase(TestCase):
    def test_parse_tc66_packet(self):
        # V: 5.1609       I: 0.0199       W: 0.1026
        # Ω: 259.3        mAh: 0.0        mWh: 5.0        mAh: 0.0        mWh: 0.0
        # Temp: 27.0      D+: 2.81        D-: 2.8
        tc66_packet: bytes = get_dectyped_data()
        data: TC66PollData = parse_tc66_packet(tc66_packet)
        self.assertEqual(data.product_name, 'TC66')
        self.assertEqual(
            data,
            TC66PollData(
                product_name='TC66',
                version='1.18',
                serial=48724,
                number_of_runs=40,
                voltage=5.1609,
                current=0.0199,
                power=0.1026,
                resistor=259.3,
                group0Ah=0.0,
                group0Wh=0.005,
                group1Ah=0.0,
                group1Wh=0.0,
                temperature=27,
                data_plus=2.81,
                data_minus=2.8,
            ),
        )

        with self.assertLogs() as cm:
            self.assertIsNone(parse_tc66_packet(b'invalid'))
        self.assertIn('Failed to parse TC66 packet data', cm.output[0])
