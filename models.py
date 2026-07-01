ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

BASE = len(ALPHABET)


def encode_base62(number: int) -> str:
    """
    Convert an integer into a Base62 string.
    Result is padded to at least 6 characters.
    """

    if number < 0:
        raise ValueError("Number cannot be negative")

    if number == 0:
        code = ALPHABET[0]
    else:
        code = ""

        while number > 0:
            number, remainder = divmod(number, BASE)
            code = ALPHABET[remainder] + code

    return code.rjust(6, "0")


def decode_base62(code: str) -> int:
    """
    Convert a Base62 string back into an integer.
    """

    number = 0

    for character in code:

        try:
            value = ALPHABET.index(character)

        except ValueError:
            raise ValueError(f"Invalid Base62 character: {character}")

        number = number * BASE + value

    return number


if __name__ == "__main__":

    print(encode_base62(1))

    print(encode_base62(1000))

    encoded = encode_base62(1000)

    print(decode_base62(encoded))