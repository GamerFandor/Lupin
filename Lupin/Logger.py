RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"

def Success(message):
    print(f"[{GREEN}+{RESET}] {message}")

def Error(message):
    print(f"[{RED}-{RESET}] {message}")

def Info(message):
    print(f"[{BLUE}i{RESET}] {message}")

def Warning(message):
    print(f"[{YELLOW}!{RESET}] {message}")