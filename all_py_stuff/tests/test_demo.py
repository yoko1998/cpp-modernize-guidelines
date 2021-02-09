import pytest

from context import megasecret # type: ignore


def test_secret_empty():
    assert megasecret.generate_secret("") == "secret"


def test_secret_something():
    assert megasecret.generate_secret("something") == "secretsomething"
