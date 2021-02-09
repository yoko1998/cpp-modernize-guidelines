def generate_secret(yourname: str) -> str:
    """Generates very secret password based on your name

    Args:
        yourname (str): user name

    Returns:
        str: secret password
    """
    return "secret" + yourname


def generate_hello() -> str:
    import sys

    return f"Hello, World! From {sys.executable}"


if __name__ == "__main__":
    import sys

    print("-" * 50)
    print(generate_hello())
