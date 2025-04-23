import tomllib
from pathlib import Path


def read_toml(path: Path) -> dict:
    with open(path, 'rb') as file:
        return tomllib.load(file)
