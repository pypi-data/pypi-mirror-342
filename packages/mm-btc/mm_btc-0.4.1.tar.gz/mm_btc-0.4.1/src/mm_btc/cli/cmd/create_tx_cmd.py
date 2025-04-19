from pathlib import Path

from bit import PrivateKey, PrivateKeyTestnet
from mm_std import BaseConfig, print_console

from mm_btc.wallet import is_testnet_address


class Config(BaseConfig):
    class Output(BaseConfig):
        address: str
        amount: int

    from_address: str
    private: str
    outputs: list[Output]


def run(config_path: Path) -> None:
    config = Config.read_toml_config_or_exit(config_path)
    testnet = is_testnet_address(config.from_address)
    key = PrivateKeyTestnet(config.private) if testnet else PrivateKey(config.private)

    outputs = [(o.address, o.amount, "satoshi") for o in config.outputs]

    tx = key.create_transaction(outputs)
    print_console(tx)
