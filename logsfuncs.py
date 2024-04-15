"""
$ Module for logs for bot

functions: 
INFO(text, arg=None) [text - Text for print in log; arg=None - Argument for the informativeness of the log]
ERROR(text, err=None) []
"""

from time import gmtime, strftime
from colorama import init
from colorama import Fore, Style



def INFO(text, arg=None) -> None:
    print("1")
    init()
    print("2")
    timenow = strftime("%H:%M:%S", gmtime())
    if not arg:
        print(f"[{Fore.GREEN} INFO {Style.RESET_ALL}] {Style.DIM}({timenow}) {Style.RESET_ALL}: {text}")
    else:
        print(f"[{Fore.GREEN} INFO {Style.RESET_ALL}] {Style.DIM}({timenow}){Style.RESET_ALL}  —  [{Style.BRIGHT} {arg} {Style.RESET_ALL}]: {text}")


def ERROR(text) -> None:
    pass
