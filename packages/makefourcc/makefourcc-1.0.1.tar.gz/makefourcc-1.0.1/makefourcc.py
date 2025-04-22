def MAKEFOURCC(ch0: str, ch1: str, ch2: str, ch3: str) -> int:
    """
    Creates a 32-bit unsigned integer FOURCC (Four-Character Code)
    from four single-character strings.

    Arguments:
        ch0, ch1, ch2, ch3 (str): Single string characters.

    Returns:
        int: 32-bit integer FOURCC code.
    """
    return (
        ord(ch0) |
        (ord(ch1) << 8) |
        (ord(ch2) << 16) |
        (ord(ch3) << 24)
    )
