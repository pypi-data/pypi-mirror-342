import unicodedata

def gcw(char):
    width_category = unicodedata.east_asian_width(char)
    if width_category in ('F', 'W'):
        return 2
    else:
        return 1


#cmd = ['python'] + matches + python_args
def output(cmd):
    title = 'DEBUG cmd: '
    seps = gcw(',') + gcw(' ')
    bracket = gcw('[')
    quota = gcw('\'')
    width = 0
    for i in cmd:
        for j in i:
            width += gcw(j)
            if j == '\\':
                width += gcw('\\')
    width += (len(cmd) - 1) * seps + 2 * len(cmd) * quota + 2 * bracket
    for i in range(width+11):
        print("\033[96m-", end='\033[0m')
    print(f"\n\033[31m{title}\033[33m{cmd}\033[0m")
    for i in range(width+11):
        print("\033[96m-", end='\033[0m')
    print()