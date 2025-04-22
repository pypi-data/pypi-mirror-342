import json
import os
from contextlib import contextmanager

import pytest
from uun_iot import Gateway
from uun_iot.UuAppClient import UuAppClient

# set correct server credentials in tests/config.json and set this to True to enable server testing
TEST_SERVER_COMM = False


# @pytest.fixture(scope="class")
def _config_location(tmpdir_factory, config_object):
    path = str(tmpdir_factory.mktemp("data").join("config.json"))
    with open(path, "w") as f:
        json.dump(config_object, f)

    return path


# @pytest.fixture(scope="class")
def _config_object():
    """Overwrite with custom configuration."""
    #return json.load(open("tests/config.json"))
    return {}


# @pytest.fixture(scope="class")
def _config_gateway(config_object):
    """Return a gateway subkey of configuration."""
    return config_object["gateway"]


# @pytest.fixture(scope="class")
def _init_modules():
    """Overwrite with custom init function."""
    return None

def _init_events():
    """Overwrite with custom event init function."""
    return None


# @pytest.fixture(scope="class")
def _gateway(config_location, init_modules, init_events):
    """Supply a config_object fixture in given module to overwite default file configuration."""

    if init_events:
        yield Gateway(config_location, None, init_events)
    else:
        yield Gateway(config_location, init_modules)

    try:
        os.remove("oidc-token")  # delete cached token
    except FileNotFoundError:
        pass

    try:
        os.remove("dummy")  # delete created files
    except FileNotFoundError:
        pass


# @pytest.fixture(scope="class")
def _started_gateway(gateway):
    with gateway as g:
        yield g


# @pytest.fixture(scope="class")
def _fileconfig(config_location):
    # return current configuration
    with open(config_location) as f:
        config = json.load(f)
    return config


# @pytest.fixture(scope="class")
def _uuappclient(fileconfig):
    return UuAppClient(fileconfig)


##### FIXTURES ######


@pytest.fixture(scope="class")
def config_location(tmpdir_factory, config_object):
    return _config_location(tmpdir_factory, config_object)


@pytest.fixture(scope="class")
def config_location_fn(tmpdir_factory_fn, config_object_fn):
    return _config_location(tmpdir_factory_fn, config_object_fn)


@pytest.fixture(scope="class")
def config_object():
    return _config_object()


@pytest.fixture(scope="function")
def config_object_fn():
    return _config_object()


@pytest.fixture(scope="class")
def config_gateway(config_object):
    return _config_gateway(config_object)


@pytest.fixture(scope="function")
def config_gateway_fn(config_object_fn):
    return _config_gateway(config_object_fn)


@pytest.fixture(scope="class")
def init_modules():
    return _init_modules()


@pytest.fixture(scope="function")
def init_modules_fn():
    return _init_modules()

@pytest.fixture(scope="class")
def init_events():
    return _init_events()


@pytest.fixture(scope="function")
def init_events_fn():
    return _init_events()


@pytest.fixture(scope="class")
def gateway(config_location, init_modules, init_events):
    yield from _gateway(config_location, init_modules, init_events)


@pytest.fixture(scope="function")
def gateway_fn(config_location_fn, init_modules_fn):
    yield from _gateway(config_location_fn, init_modules_fn, init_events_fn)


@pytest.fixture(scope="class")
def started_gateway(gateway):
    yield from _started_gateway(gateway)

@pytest.fixture(scope="function")
def started_gateway_fn(gateway_fn):
    yield from _started_gateway(gateway_fn)


@pytest.fixture(scope="class")
def fileconfig(config_location):
    return _fileconfig(config_location)


@pytest.fixture(scope="function")
def fileconfig_fn(config_location_fn):
    return _fileconfig(config_location_fn)


@pytest.fixture(scope="class")
def uuappclient(fileconfig):
    return _uuappclient(fileconfig)


@pytest.fixture(scope="function")
def uuappclient_fn(fileconfig_fn):
    return uuappclient(fileconfig_fn)
