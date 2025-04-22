from Crypto.Cipher import AES
import logging

logger = logging.getLogger(__name__)


class TC66Decryptor:
    # TC66 packets are encrypted using AES in ECB mode using the following static key:
    AES_KEY_SROUCE = (
        0x58, 0x21, 0xfa, 0x56, 0x01, 0xb2, 0xf0, 0x26,
        0x87, 0xff, 0x12, 0x04, 0x62, 0x2a, 0x4f, 0xb0,
        0x86, 0xf4, 0x02, 0x60, 0x81, 0x6f, 0x9a, 0x0b,
        0xa7, 0xf1, 0x06, 0x61, 0x9a, 0xb8, 0x72, 0x88,
    )
    AES_KEY = bytes(b & 0xFF for b in AES_KEY_SROUCE)
    CHIPER = AES.new(AES_KEY, AES.MODE_ECB)

    def __call__(self, *, crypted_data: bytearray) -> bytes:
        raw_data = self.CHIPER.decrypt(crypted_data)
        return raw_data


tc66_decryptor = TC66Decryptor()
