from datetime import datetime
from pytz import timezone
from colorama import Fore,Style,Back

def currentTimeDXB():
    dubai = timezone('Asia/Dubai')
    sa_time = datetime.now(dubai)
    return sa_time.strftime(f'{Fore.CYAN}{Style.BRIGHT}(INFO)\t[%Y-%m-%d %H:%M:%S]{Style.RESET_ALL}')

def currentTimeErrorDXB(crit=False):
    dubai = timezone('Asia/Dubai')
    sa_time = datetime.now(dubai)
    if crit == False:
        return sa_time.strftime(f'{Fore.RED}{Style.BRIGHT}(ERROR)\t[%Y-%m-%d %H:%M:%S]{Style.RESET_ALL}')
    elif crit == True:
        return sa_time.strftime(f'{Fore.WHITE}{Style.BRIGHT}{Back.RED}(CRIT){Back.RESET}{Fore.RED}\t[%Y-%m-%d %H:%M:%S]{Style.RESET_ALL}')

def currentTimeSuccessDXB():
    dubai = timezone('Asia/Dubai')
    sa_time = datetime.now(dubai)
    return sa_time.strftime(f'{Fore.GREEN}{Style.BRIGHT}(PASS)\t[%Y-%m-%d %H:%M:%S]{Style.RESET_ALL}')