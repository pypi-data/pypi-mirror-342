from stv_repy.mul_lang.change_text import help_content

def print_help(parser):
    """定制化帮助信息"""
    content = help_content()
    help_text = content[0]
    for action in parser._actions:
        if action.dest != 'help':
            help_text.append(f"  {', '.join(action.option_strings):<25} {action.help}")

    help_text += content[1]
    print('\n'.join(help_text))