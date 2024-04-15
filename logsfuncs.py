"""
$ Module for logs for bot

functions: 
INFO(text, arg=None) [text - Text for print in log; arg=None - Argument for the informativeness of the log]
ERROR(text, err=None) []
"""

from time import gmtime, strftime
from os import system


def INFO(text, arg=None) -> None:
    system("")
    timenow = strftime("%H:%M:%S", gmtime())
    if not arg:
        print(f"\033[1;32m[ INFO ] \033[4m({timenow}) \033[0m: {text}")
    else:
        print(f"\033[1;32m[ INFO ] \033[4m({timenow}) \033[0m - \033[3m [ {arg} ]: \033[0m {text}")


def ERROR(text) -> None:
    pass
