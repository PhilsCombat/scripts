import os
import re
import randbase


commentDict = {
    ".py": '#',
    ".sh": '#',
    ".mcfunction": '#',
    ".ps1": '#',

    ".js": '//',
    ".ts": '//',
    ".java": '//',
    ".c": '//',
    ".cpp": '//',
    ".h": '//',
    ".rs": '//',
    ".go": '//',

    ".lua": '--',

    ".bat": 'REM',
}
CHARS = "#=-_@/."


def generateHeadline(commentChar: str, pre: str, title: str, suf: str, width=80):
    title = title.strip()
    width -= len(commentChar) + 1
    titleIndent = width // 2 - len(title) // 2
    out = ''
    if (pre):
        out = f"{commentChar} {pre * width}\n"
    return out + f"{commentChar} {' ' * titleIndent + title.upper()}\n{commentChar} {suf * width}\n"


def patternByFiletype(suffix: str):
    c = commentDict[suffix]
    return f"^ *{c} *([{CHARS}])?([^{CHARS} ].*)([{CHARS}]) *$"


def headlineFromMatch(commentChar: str, regMatch, width = 80):
    pre = regMatch[1]
    if (pre is None):
        pre = ''
    return generateHeadline(commentChar, pre, regMatch[2], regMatch[3], width)


def formatFile(path: str, width = 80, keepOriginal = False):
    if (not os.path.exists(path)):
        raise Exception(f"File '{path}' not found")
    if (not os.path.isfile(path)):
        raise Exception(f"File '{path}' is not a file")
    
    name, extension = os.path.splitext(path)
    if (not commentDict.get(extension)):
        print(extension + ' files not supported')
        return
    nameEdited = ''    
    original = open(path, 'r')
    edited = None
    while (True):
        id = randbase.randbase(hex, 0, 0xffffff)
        id = randbase.setDigits(id ,6)
        id = randbase.removePrefix(id)
        nameEdited = name + '-' + id
        try:
            edited = open(nameEdited + extension, 'x')
            break
        except:
            continue
    
    reg = re.compile(patternByFiletype(extension))
    for line in original.readlines():
        m = reg.search(line)
        if (not m):
            edited.write(line)
            continue
        edited.write(headlineFromMatch(commentDict[extension], m, width))

    original.close()
    edited.close()
    if (not keepOriginal):
        os.replace(nameEdited + extension, path)


def getFiles(path: str, pattern: str = None, *args):
    """use args for regex options"""
    isfile = lambda p, i: os.path.isfile(os.path.join(p, i))
    if (not pattern):
        return [os.path.join(path, item) for item in os.listdir(path) if (isfile(path, item))]

    filesOnly = []
    reg = re.compile(pattern, *args)
    for item in os.listdir(path):
        if (not isfile(path, item)):
            continue
        if (reg.fullmatch(item)):
            filesOnly.append(os.path.join(path, item))
    return filesOnly


# ==============================================================================
#                                      MAIN
# ==============================================================================


if (__name__ == "__main__"):
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', type=str, help='Path of target file/directory')
    parser.add_argument('-w', '--width', type=int, default=80, help='Headline width')
    parser.add_argument('-k', '--keep', action='store_true', help='Keeps the original file instead of overwriting it')

    sub = parser.add_subparsers(dest='target')
    sub_file = sub.add_parser('file', help='Interprets --path as file')

    sub_dir= sub.add_parser('dir', help='Interprets --path as directory')
    sub_dir.add_argument('-r', '--regex', type=str, default=None, help='Regex-Pattern to filter for files')

    opt = parser.parse_args(sys.argv[1:])
    if (opt.target == 'file'):
        formatFile(opt.path, opt.width, opt.keep)
    else:
        try:
            for file in getFiles(opt.path, opt.regex):
                formatFile(file, opt.width, opt.keep)
        except FileNotFoundError as err:
            print(err.filename + 'not found')
        except Exception as err:
            print(str(err.args) + 'something went wrong')
            
