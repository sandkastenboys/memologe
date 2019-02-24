import os
import subprocess
from subprocess import STDOUT, check_output

timeout = 20

def start_bot():
    try:
        check_output(["python3", "main.py"], timeout=timeout)
    except subprocess.TimeoutExpired as timeout_e:
        print("Success")
    except subprocess.CalledProcessError as e:
        raise e


if __name__ == "__main__":
    start_bot()