import pytest
from mm_crypto_utils.proxy import fetch_proxies_or_fatal_sync
from mm_std import get_dotenv
from typer.testing import CliRunner


@pytest.fixture()
def mnemonic() -> str:
    return "hub blur cliff taste afraid master game milk nest change blame code"


@pytest.fixture
def passphrase() -> str:
    return "my-secret"


@pytest.fixture()
def mainnet_bip44_address_0() -> str:
    return "1Men3kiujJH7H5NXyKpFtWWtni1cTfSk48"


@pytest.fixture
def binance_address() -> str:
    return "34xp4vRoCGJym3xR7yCVPFHoCNxv4Twseo"


@pytest.fixture
def proxies() -> list[str]:
    return fetch_proxies_or_fatal_sync(get_dotenv("PROXIES_URL"))


@pytest.fixture
def cli_runner() -> CliRunner:
    return CliRunner()
