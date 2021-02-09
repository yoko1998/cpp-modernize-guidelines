from _context import megasecret


def test_hello():
    assert megasecret.generate_hello() != "Hello, World! From "

