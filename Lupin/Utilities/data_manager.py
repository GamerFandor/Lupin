# Imports
import os
import platform
from pathlib import Path
from datetime import datetime



# Global variables
CURRENT_SESSION = None



# Function to get the directory where the saves are stored and create it if it doesn't exist
def get_saves_directory() -> str:
    os_name = platform.system()
    
    if os_name == 'Windows':
        save_dir = Path(os.getenv('APPDATA')) / 'Lupin'
    elif os_name == 'Linux':
        save_dir = Path(os.getenv('XDG_DATA_HOME', Path.home() / '.local/share')) / 'Lupin'
    else:
        raise Exception(f"Unsupported OS: {os_name}")
    
    # Create the directory if it doesn't exist
    save_dir.mkdir(parents=True, exist_ok=True)
    
    return str(save_dir)



# Function to save the data
def save_data(data: dict, module_name: str) -> None:
    try:
        saves_directory = get_saves_directory()
        file = f'{saves_directory}/{CURRENT_SESSION}/{module_name}.json'
        with open(f'{file}', 'w') as f:
            f.write(str(data))
    except Exception as e:
        pass



# Function to load the data
def load_data(module_name: str) -> dict:
    try:
        saves_directory = get_saves_directory()
        file = f'{saves_directory}/{CURRENT_SESSION}/{module_name}.json'
        with open(f'{file}', 'r') as f:
            return eval(f.read())
    except Exception as e:
        return {}
    


# Create new session
def new_session() -> None:
    global CURRENT_SESSION
    CURRENT_SESSION = datetime.now().strftime('%Y-%m-%d [%H-%M-%S]')
    path = f'{get_saves_directory()}\\{CURRENT_SESSION}'
    os.makedirs(path, exist_ok = True)
    print(path)



# Get all sessions and return an empty list if NoneType is encountered
def get_all_sessions() -> list:
    saves_directory = get_saves_directory()
    sessions = [session for session in os.listdir(saves_directory) if os.path.isdir(f'{saves_directory}/{session}')]

    if sessions is None:
        return []

    return sessions[::-1]