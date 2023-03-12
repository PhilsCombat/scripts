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


def setDigits(number: str | int, digitCount: int, digit: str = "0") -> str:
    if (type(number) == int):
        tmp = str(number)
        return (max(0, digitCount - len(tmp)) * digit) + tmp
    # add 2 to account for prefix
    missing = max(0, digitCount - len(number)) - 2
    return number[:2] + digit * missing + number[2:]

def removePrefix(number: str):
    if (not number[1] in 'box'):
        raise SyntaxWarning("number MUST contain base-prefix: 0b | 0o | 0x")
    return number[2:]

# ##############################################################################
#                                      MAIN
# ##############################################################################

if (__name__ == '__main__'):
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(
        description="Genrate random number as integer, binary, octal, hexadecimal",
        usage='randbase.py [options] [bin|oct|int|hex]'
    )
    parser.add_argument('-s', '--start', type=int, default=0, help='Minimum value')
    parser.add_argument('-e', '--end', type=int, required=True, help='Maximum value (inclusive)')
    parser.add_argument('-d', '--digits', type=int, default=0, help='Minimum digit count')
    parser.add_argument('-l', '--list', action='store_true', help='Make a list of random numbers')  # must be set with --items
    parser.add_argument('-i', '--items', type=int, default=1, help='Item count of list (default: 1)')  # must be set with --list
    parser.add_argument('-c', '--clip', action='store_true', help='Put result into clipboard')
    parser.add_argument('--no-prefix', action='store_true', help='Remove pythons prefix (0x 0o 0b)')

    sub_parser = parser.add_subparsers(dest="base")
    sub_hex = sub_parser.add_parser('hex', help='Return as hex number')
    sub_int = sub_parser.add_parser('int', help='Return as int number')
    sub_oct = sub_parser.add_parser('oct', help='Return as oct number')
    sub_bin = sub_parser.add_parser('bin', help='Return as bin number')

    opt = parser.parse_args(sys.argv[1:])

    func=None
    match(opt.base):
        case 'hex':
            func = hex
        case 'bin':
            func = bin
        case 'oct':
            func = oct
        case _:
            func = int
    

    def generate(): 
        out = None
        if (opt.digits > 2):
            out = setDigits(randbase(func, opt.start, opt.end), opt.digits, '0')
        else:
            out = randbase(func, opt.start, opt.end)
        if (opt.no_prefix):
            out = removePrefix(out)
        return out

# ==============================================================================
#                                    GENERATE
# ==============================================================================

    val=None
    if (opt.list):
        val = []
        for i in range(opt.items):
            val.append(generate())
    else:
        val = generate()

# ==============================================================================
#                                      CLIP
# ==============================================================================

    if (opt.clip):
        try:
            import pyperclip
            pyperclip.copy(str(val))
        except:
            print("Copy to clipboard failed due to module pyperclip missing")

    print(val)
