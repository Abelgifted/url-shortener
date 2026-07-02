from auth import hash_password, verify_password, create_token, verify_token


def test_password_hashing_and_verification():
    password = "super-secret"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong-password", hashed) is False


def test_token_creation_and_verification():
    token = create_token(42)

    assert isinstance(token, str)
    assert verify_token(token) == 42
