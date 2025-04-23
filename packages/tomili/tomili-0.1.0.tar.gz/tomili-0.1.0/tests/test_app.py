import pytest

from tomili import rtoml


def test_read_toml(get_toml):
    assert rtoml(get_toml) is not None


def test_read_toml_author(get_toml):
    assert (
        rtoml(get_toml)['project']['authors'][0]['email']
        == 'machadoah@proton.me'
    )


@pytest.mark.parametrize(
    ('key', 'value'),
    [
        ('name', 'Antonio Henrique Machado'),
        ('email', 'machadoah@proton.me'),
    ],
)
def test_author_project(get_toml, key, value):
    autor = rtoml(get_toml)['project']['authors'][0]
    assert autor[key] == value


@pytest.mark.parametrize(
    ('key', 'sub_key', 'value'),
    [
        ('project', 'name', 'example'),
        ('project', 'version', '0.1.0'),
        (
            'information',
            'formation-school',
            {'institution': 'etec', 'course': 'adm', 'year': '2021'},
        ),
        (
            'information',
            'formation-college',
            {'institution': 'fatec', 'course': 'ads', 'year': '2024'},
        ),
    ],
)
def test_campos_toml(get_toml, key, sub_key, value):
    toml = rtoml(get_toml)
    assert toml[key][sub_key] == value
