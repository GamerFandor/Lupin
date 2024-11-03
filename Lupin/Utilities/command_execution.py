# Imports
import socket
import subprocess
from typing import Tuple



# Command execution error
class CommandExecutionError(Exception):
    def __init__(self, command, returncode, stderr):
        super().__init__(f"Command '{command}' failed with return code {returncode}. Error: {stderr}")
        self.command = command
        self.returncode = returncode
        self.stderr = stderr



# Execute a terminal command
def execute_command(command: str) -> Tuple[str, str, int]:
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout, result.stderr, result.returncode
    except subprocess.CalledProcessError as e:
        raise CommandExecutionError(command, e.returncode, e.stderr)



# Check if a program is installed
def is_program_installed(program):
    try:
        subprocess.run([program, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False



# Check if the program is connected to the internet
def is_connected():
    try:
        socket.create_connection(("8.8.8.8", 53))
        return True
    except OSError:
        return False



# CHeck if the computer has a wifi adapter
def has_wifi_adapter():
    try:
        result = subprocess.run(["netsh", "wlan", "show", "interfaces"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return "Wireless Network Connection" in result.stdout or "Wi-Fi" in result.stdout
    except Exception as e:
        return False



# Testing
if __name__ == '__main__':
    stdout, stderr, returncode = execute_command('python --version')
    print(stdout)