"""
$ Module for logs for bot

functions: 
INFO(text, arg=None) -> None [text - Text for print in log; arg=None - Argument for the informativeness of the log]
ERROR(text, err=None) -> None [text - Text for print in log; err=None - Argument for the error info of the log]
WARNING(text, warn=Nonw) -> None [text - Text for print in log; warn=None - Argument for the warning info of the log]
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


def ERROR(text, err=None) -> None:
    init()
    timenow = strftime("%H:%M:%S", gmtime())
    if not arg:
        raise NameError(f"[{Fore.RED} ERROR {Style.RESET_ALL}] {Style.DIM}({timenow}) {Style.RESET_ALL}: {text}")
    else:
        raise NameError(f"[{Fore.RED} ERROR {Style.RESET_ALL}] {Style.DIM}({timenow}){Style.RESET_ALL}  —  [{Style.BRIGHT} {err} {Style.RESET_ALL}]: {text}")


def WARNING(text, warn=None) -> None:
    init()
    timenow = strftime("%H:%M:%S", gmtime())
    if not arg:
        print(f"[{Fore.YELLOW} WARNING {Style.RESET_ALL}] {Style.DIM}({timenow}) {Style.RESET_ALL}: {text}")
    else:
        print(f"[{Fore.YELLOW} WARNING {Style.RESET_ALL}] {Style.DIM}({timenow}){Style.RESET_ALL}  —  [{Style.BRIGHT} {warn} {Style.RESET_ALL}]: {text}")
