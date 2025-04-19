import os
import re
import subprocess

from stv_repy.core.stv_parse import stv_parse
from stv_repy.core.traverser import traverse_dirs
from stv_repy.utils.diyhelp import print_help
from stv_repy.utils.lang_utils import set_cn
from stv_repy.utils.utils import output
from stv_utils import system_check, is_ch

__version__ = '0.0.1'
def main(__version__ = __version__):

    parser, args, remaining = stv_parse()

    if args.rp_help:
        print_help(parser)
        return

    if args.rp_version:
        print(__version__)
        return

    if args.rp_license:
        try:
            from stv_repy.utils.lic import return_mit
            print(f"\033[33m{return_mit}\033[0m")
        except ImportError:
            print(f"\033[96mThis Project Follow MIT License\033[0m")
        return

    if args.rp_set_lang:
        print("Success") if set_cn("chinese") else print("Failed")
        return

    if args.rp_clear_lang_setting:
        print("Success!") if set_cn("rm") else print("Failed")
        return

    # 分离路径模式与Python参数
    python_args = []
    if '--' in remaining:
        idx = remaining.index('--')
        patterns = remaining[:idx]
        python_args = remaining[idx+1:]
    else:

        split_index = next((i for i, v in enumerate(remaining) if v.startswith('-')), None)
        if split_index is not None:
            patterns = remaining[:split_index]
            python_args = remaining[split_index:]
        else:
            patterns = remaining

    compiled_patterns = []
    for raw_pattern in patterns:
        abs_pattern = os.path.abspath(raw_pattern)
        drive, path = os.path.splitdrive(abs_pattern)
        path = path.replace('\\', '/').lstrip('/')
        layers = [p for p in path.split('/') if p]

        regex_layers = []
        for layer in layers:
            regex_str = '^'
            for c in layer:
                if c == '*':
                    regex_str += '[^/]*'
                else:
                    regex_str += re.escape(c)
            regex_str += '$'
            regex = re.compile(regex_str, re.IGNORECASE)
            regex_layers.append(regex)

        start_dir = os.path.join(drive, '/') if drive else os.getcwd()
        compiled_patterns.append((start_dir, regex_layers))

    # 文件匹配和命令执行
    matches = []
    for start_dir, regex_layers in compiled_patterns:
        traverse_dirs(start_dir, regex_layers, 0, args, matches)

    if not matches:
        print("未找到匹配文件。") if is_ch() else print("No matching file found.")
        print("Not Support Unix-Like, Just Support Windows") if not system_check() else print(end='')
        return

    cmd = ['python'] + matches + python_args
    output(cmd)

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        return