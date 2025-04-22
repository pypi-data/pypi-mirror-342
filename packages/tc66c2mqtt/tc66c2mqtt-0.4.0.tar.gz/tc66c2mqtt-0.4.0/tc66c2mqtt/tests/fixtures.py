from pathlib import Path


BASE_PATH = Path(__file__).parent

RAW_TC66_DATA = bytearray.fromhex(
    '006630928cdbb01e307647693bac80b012a60ec3c8645b9af0ead3c57ae5a0628f330593ff8f836a2a36d60f8709fc4fc5ec277ef1'
    'b0dbb4815a9497d8646eb206f404f8061c1177e994f37dfc6f4dab07385ea4d05c1e32616e88527b57d3106babf8c170d31db582db'
    '234384fa559313e92b412f6af4e16e09168c608fba0a4231f411e56f5c203c590b4a68fd5b092aca6ec4a4554d5542e8674b097e25'
    '9c2aca6ec4a4554d5542e8674b097e259ce09c4004c92da948c3165eebdb8b9ec2'
)


def get_dectyped_data() -> bytes:
    # V: 5.1609       I: 0.0199       W: 0.1026
    # Ω: 259.3        mAh: 0.0        mWh: 5.0        mAh: 0.0        mWh: 0.0
    # Temp: 27.0      D+: 2.81        D-: 2.8
    return Path(BASE_PATH, 'tc66c_decrypted.data').read_bytes()
