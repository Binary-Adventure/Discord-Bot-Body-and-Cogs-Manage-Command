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

def writing(text):
    with open("./logs/logs.log", encoding="utf-8") as file:
        file.write(f"{text}\n")

def INFO(text, arg=None) -> None:
    init()
    timenow = strftime("%H:%M:%S", gmtime())
    if not arg:
        print(f"[{Fore.GREEN} INFO {Style.RESET_ALL}] {Style.DIM}({timenow}) {Style.RESET_ALL}: {text}")
        writing(f"[ INFO ] ({timenow}) : {text}")
    else:
        print(f"[{Fore.GREEN} INFO {Style.RESET_ALL}] {Style.DIM}({timenow}){Style.RESET_ALL}  —  [{Style.BRIGHT} {arg} {Style.RESET_ALL}] : {text}")
        writing(f"[ INFO ] ({timenow})  —  {arg} : {text}")


def ERROR(text, err=None) -> None:
    init()
    timenow = strftime("%H:%M:%S", gmtime())
    if not err:
        writing(f"[ ERROR ] ({timenow}) : {text}")
        raise NameError(f"[{Fore.RED} ERROR {Style.RESET_ALL}] {Style.DIM}({timenow}) {Style.RESET_ALL}: {text}")
    else:
        writing(f"[ ERROR ] ({timenow})  —  {err} : {text}")
        raise NameError(f"[{Fore.RED} ERROR {Style.RESET_ALL}] {Style.DIM}({timenow}){Style.RESET_ALL}  —  [{Style.BRIGHT} {err} {Style.RESET_ALL}] : {text}")


def WARNING(text, warn=None) -> None:
    init()
    timenow = strftime("%H:%M:%S", gmtime())
    if not warn:
        print(f"[{Fore.YELLOW} WARNING {Style.RESET_ALL}] {Style.DIM}({timenow}) {Style.RESET_ALL}: {text}")
        writing(f"[ WARNING ] ({timenow}) : {text}")
    else:
        print(f"[{Fore.YELLOW} WARNING {Style.RESET_ALL}] {Style.DIM}({timenow}){Style.RESET_ALL}  —  [{Style.BRIGHT} {warn} {Style.RESET_ALL}] : {text}")
        writing(f"[ WARNING ] ({timenow})  —  {warn} : {text}")