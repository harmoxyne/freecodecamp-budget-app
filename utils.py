def right_pad(text: str, length: int = 23, pad: str = ' ') -> str:
    return text[:23] + pad * (length - len(text))


def left_pad(text: str, length: int = 7, pad: str = ' ') -> str:
    return pad * (length - len(text)) + text
