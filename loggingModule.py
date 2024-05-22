"""
$ Module for logs for bot

functions: 
INFO(text, arg=None) -> None [text - Text for print in log; arg=None - Argument for the informativeness of the log]
ERROR(text, err=None) -> None [text - Text for print in log; err=None - Argument for the error info of the log]
WARNING(text, warn=Nonw) -> None [text - Text for print in log; warn=None - Argument for the warning info of the log]
"""

import colorama
from time import gmtime, strftime
from colorama import Fore, Style



colorama.init()


class LoggingModule():
    @property
    def timenow(self):
        return strftime("%H:%M:%S", gmtime())


    def writing(self, text):
        with open("./logs/logs.log", 'a') as file:
            file.write(f"{text}\n")


    def INFO(self, text, arg=None) -> None:
        if arg == None:
            print(f"[{Fore.GREEN} INFO {Style.RESET_ALL}] {Style.DIM}({self.timenow}) {Style.RESET_ALL}: {text}")
            self.writing(f"[ INFO ] ({self.timenow}) : {text}")
        
        else:
            print(f"[{Fore.GREEN} INFO {Style.RESET_ALL}] {Style.DIM}({self.timenow}){Style.RESET_ALL}  —  [{Style.BRIGHT} {arg} {Style.RESET_ALL}] : {text}")
            self.writing(f"[ INFO ] ({self.timenow})  —  {arg} : {text}")


    def ERROR(self, text, err=None) -> None:
        if err == None:
            self.writing(f"[ ERROR ] ({self.timenow}) : {text}")
            raise NameError(f"[{Fore.RED} ERROR {Style.RESET_ALL}] {Style.DIM}({self.timenow}) {Style.RESET_ALL}: {text}")
        
        else:
            self.writing(f"[ ERROR ] ({self.timenow})  —  {err} : {text}")
            raise NameError(f"[{Fore.RED} ERROR {Style.RESET_ALL}] {Style.DIM}({self.timenow}){Style.RESET_ALL}  —  [{Style.BRIGHT} {err} {Style.RESET_ALL}] : {text}")


    def WARNING(self, text, warn=None) -> None:
        if warn == None:
            print(f"[{Fore.YELLOW} WARNING {Style.RESET_ALL}] {Style.DIM}({self.timenow}) {Style.RESET_ALL}: {text}")
            self.writing(f"[ WARNING ] ({self.timenow}) : {text}")
        
        else:
            print(f"[{Fore.YELLOW} WARNING {Style.RESET_ALL}] {Style.DIM}({self.timenow}){Style.RESET_ALL}  —  [{Style.BRIGHT} {warn} {Style.RESET_ALL}] : {text}")
            self.writing(f"[ WARNING ] ({self.timenow})  —  {warn} : {text}")


logs = LoggingModule()