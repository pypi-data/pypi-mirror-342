from argparse import ArgumentParser
from stv_repy.mul_lang.change_text import parse_text

def stv_parse():
    pt = parse_text()

    parser = ArgumentParser(add_help=False)

    parser.add_argument('-rh', '--rp-help', action='store_true',
                        help=pt[0])
    parser.add_argument('-ram', '--rp-allow-multiple', action='store_true',
                        help=pt[1])
    parser.add_argument('-rv', '--rp-version', action='store_true',
                        help=pt[2])
    parser.add_argument('-rl', '--rp-license', action='store_true',
                        help=pt[3])
    parser.add_argument('-rsl', '--rp-set-lang', action='store_true',
                        help=pt[4])
    parser.add_argument('-rcls', '--rp-clear-lang-setting', action='store_true',
                        help=pt[5])

    args, remaining = parser.parse_known_args()

    return parser, args, remaining