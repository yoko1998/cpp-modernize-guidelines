from context import megasecret # type: ignore


def test_hello():
    assert megasecret.generate_hello() != "Hello, World! From "

