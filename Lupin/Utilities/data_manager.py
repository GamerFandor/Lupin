# Imports
import os
import shutil
import platform
from pathlib import Path
from datetime import datetime



# Global variables
CURRENT_SESSION = None



# Function to get the directory where the saves are stored and create it if it doesn't exist
def get_saves_directory() -> str:
    os_name = platform.system()
    
    save_dir = Path.home() / "Documents" / "Lupin"
    
    # Create the directory if it doesn't exist
    save_dir.mkdir(parents=True, exist_ok=True)
    
    return str(save_dir)



# Function to save the data
def save_data(data: dict, module_name: str, CURRENT_SESSION) -> None:
    try:
        saves_directory = get_saves_directory()
        file = f'{saves_directory}/{CURRENT_SESSION}/{module_name}.json'
        with open(file, 'w') as f:
            f.write(str(data).replace("'", '"'))
    except Exception as e:
        pass



# Function to load the data
def load_data(session: str, module_name: str) -> dict:
    try:
        saves_directory = get_saves_directory()
        file = f'{saves_directory}/{session}/{module_name}.json'
        with open(f'{file}', 'r') as f:
            return eval(f.read())
    except Exception as e:
        return {}
    


# Get the data files
def get_data_files(CURRENT_SESSION) -> list:
    saves_directory = get_saves_directory()
    return [file for file in os.listdir(f'{saves_directory}/{CURRENT_SESSION}') if file.endswith('.json')]
    


# Create new session
def new_session() -> None:
    global CURRENT_SESSION
    CURRENT_SESSION = datetime.now().strftime('%Y-%m-%d [%H-%M-%S]')
    path = Path.home() / "Documents" / "Lupin" / CURRENT_SESSION
    os.makedirs(path, exist_ok = True)
    return path



# Get all sessions and return an empty list if NoneType is encountered
def get_all_sessions() -> list:
    saves_directory = get_saves_directory()
    sessions = [session for session in os.listdir(saves_directory) if os.path.isdir(f'{saves_directory}/{session}')]

    if sessions is None:
        return []

    return sessions[::-1]



def delete_session(session_name: str) -> None:
    saves_directory = get_saves_directory()
    if '\\' in saves_directory:
        session_path = f'{saves_directory}\\{session_name}'
    else:
        session_path = f'{saves_directory}/{session_name}'
    shutil.rmtree(session_path)