import demo


def test_secret_empty():
    assert demo.generate_secret("") == "secret"


def test_secret_something():
    assert demo.generate_secret("something") == "secretsomething"
