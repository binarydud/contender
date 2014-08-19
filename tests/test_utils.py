import pytest
from contender.utils import (
    validate_config,
)


def test_validate_config():
    config = {}
    with pytest.raises(AssertionError):
        validate_config(config)

    config['user'] = 'user'
    config['owner'] = 'owner'
    config['repository'] = 'repository'
    config['token'] = 'token'
    validate_config(config)
