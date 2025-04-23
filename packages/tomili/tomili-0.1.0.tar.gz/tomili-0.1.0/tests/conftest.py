from pathlib import Path

import pytest


@pytest.fixture
def get_toml() -> Path:
    return Path('tests/pyproject-test.toml')


@pytest.fixture
def user():
    return {
        'name': 'Antonio Henrique Machado',
        'email': 'machadoah@proton.me',
        'linkedin': 'https://linkedin.com/in/machadoah',
    }
