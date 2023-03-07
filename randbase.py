import random

def randbase(basefunc=int, start:int=0, end:int=1):
    """
    Return random number in given range in given base.

    basefunc:
        referres to built-in | bin | oct | int | hex | functions
    example:
        randbase(bin, 0b11, 0b1111)\n
        randbase(int, 10, 100)\n
        randbase(oct, 0o2, 0o777)\n
        randbase(hex, 0, 0xff)\n
    """
    return basefunc(random.randint(start, end))


def setDigits(number: str | int, digitCount: int, digit: str = '0', removePrefix = False) -> str:
    if (type(number) == int):
        number = str(number)
        return digit * max(0, digitCount - len(number)) + number
    if (not number[1] in 'box'):
        raise SyntaxWarning("number MUST contain base-prefix: 0b | 0o | 0x")
    # add 2 to account for prefix
    missing = max(0, digitCount - len(number)) + 2
    if (removePrefix):
        return digit * missing + number[2:]
    return number[:2] + digit * missing + number[2:]



if (__name__ == '__main__'):
    pass