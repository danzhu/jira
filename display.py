from __future__ import print_function
from colorama import init, Fore, Back, Style
import sys

def display(fmt = '', *vals, **keys):
    try:
        print(fmt.format(*vals, fore=Fore, back=Back, style=Style, **keys))
    except UnicodeEncodeError as e:
        error('Encoding error: {}', e)

def style(fmt):
    return fmt.format(fore=Fore, back=Back, style=Style)

def error(fmt, *vals, **keys):
    msg = Fore.RED + fmt + Fore.RESET
    print(msg.format(*vals, **keys), file=sys.stderr)
