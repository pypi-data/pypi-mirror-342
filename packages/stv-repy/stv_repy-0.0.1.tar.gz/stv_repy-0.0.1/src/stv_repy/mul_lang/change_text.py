from stv_utils import is_ch

from stv_repy.utils.lang_utils import language_config

def parse_text(check = True):
    check = language_config() if check else check
    if is_ch() or check:
        rh_help = '      显示工具帮助信息'
        ram_help = '      允许通配符匹配多个目录层级'
        rv_help = '      显示项目版本并退出'
        rl_help = '      显示项目许可证并退出'
    else:
        rh_help = '      Display help information for the tool'
        ram_help = '      Allow wildcard matching to match multiple directory levels'
        rv_help = '      Display the project version and exit'
        rl_help = '      Display the project license and exit'

    rsl_help = "      设置参数语言为中文"
    rcls_help = " clear the language setting"

    array = [rh_help, ram_help, rv_help, rl_help, rsl_help, rcls_help]

    return array


def help_content(check = True):
    check = language_config() if check else check
    if is_ch() or check:
        text1 = [
            "Regular Python (repy) 执行工具",
            "版本：0.0.1+dev",
            "用法：",
            "  repy [rp-选项] <路径模式>... [-- Python参数]",
            "",
            "核心功能：",
            "  通过通配符模式匹配Python文件并执行",
            "",
            "选项："
        ]
        text2 = [
            "",
            "路径模式示例：",
            "  *.py                   当前目录所有Python文件",
            "  your_test/*/*Test.py         your_test下两级目录的测试文件",
            "  D:/project/**/util*.py 跨盘符的多级匹配（需启用--rp-allow-multiple）",
            "",
            "典型用法：",
            "  repy --rp-help",
            "  repy --rp-allow-multiple your_test/**/*.py -- -v",
            "  repy tests/*_test.py -- -m pytest"
        ]
    else: # 英文
        text1 = [
            "Regular Python (repy) execution tool",
            "Version: 0.0.1+dev",
            "Usage:",
            "  repy [rp-options] <path-pattern>... [-- Python parameters]",
            "",
            "Core function:",
            "  Match and execute Python files through wildcard patterns",
            "",
            "Options:"
        ]
        text2 = [
            "",
            "Path pattern examples:",
            "  *.py                   All Python files in the current directory",
            "  your_test/*/*Test.py         Test files in two levels of your_test",
            "  D:/project/**/util*.py Multi-level matching across disk drives (requires enabling --rp-allow-multiple)",
            "",
            "Typical usage:",
            "  repy --rp-help",
            "  repy --rp-allow-multiple your_test/**/*.py -- -v",
            "  repy tests/*_test.py -- -m pytest"
        ]
    return [text1, text2]