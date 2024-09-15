# Imports
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



# Testing
if __name__ == '__main__':
    stdout, stderr, returncode = execute_command('python --version')
    print(stdout)