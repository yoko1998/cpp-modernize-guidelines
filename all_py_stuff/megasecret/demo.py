def generate_secret(yourname: str) -> str:
    """Generates very secret password based on your name

    Args:
        yourname (str): user name

    Returns:
        str: secret password
    """
    return "secret" + yourname


def generate_hello() -> str:
    """Generates hello from the binary depth

    Returns:
        str: appreciation message
    """
    import sys
    return f"Hello, World! From {sys.executable}"


if __name__ == "__main__":
    """Welcome from the binary depth of config hell
    """
    print("-" * 50)
    print(generate_hello())
