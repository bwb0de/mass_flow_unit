import time

from .paths import log_file

def escrever(string):
    with open(log_file, 'a') as f:
        f.write(f"[{time.ctime()}] => {string}\n")