"""
module for logs for bot
fncs: 
INFO(text) [text - Text for print in log]
ERROR()
"""
from time import gmtime, strftime


def INFO(text, arg=None):
    if not arg:
        print(f"\033[1;32m[ INFO ] \033[4m({strftime("%H:%M:%S", gmtime())}) \033[0m: {text}")
    else:
        print(f"\033[1;32m[ INFO ] \033[4m({strftime("%H:%M:%S", gmtime())}) \033[0m - \033[3m [ {arg} ]: \033[0m {text}")


def ERROR(text):
    pass
