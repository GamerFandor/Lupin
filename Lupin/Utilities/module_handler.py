# Imports
import os
import sys
import importlib
from docx import Document



# Function to get the modules and their names
def get_modules() -> list:
    folder = 'Lupin/Modules'
    sys.path.insert(0, folder)    
    modules = []
    
    for item in os.listdir(folder):
        if item.endswith('.py') and item != '__init__.py':
            module_name = item[:-3]
            try:
                module = importlib.import_module(module_name)
                modules.append((module_name, module.module_config["display_name"], module.module_config["order"], module.module_config["required_apps"], module.module_config["required_modules"], module.module_config["is_network_required"], module.module_config["is_wifi_adapter_required"]))
            except Exception as e:
                print(f"Failed to import {module_name}: {e}")

    sys.path.pop(0)  
    modules.sort(key=lambda x: x[2])  
    return modules



# Function to call a module functions
def call_module_function(module_name: str, function_name: str, *args, **kwargs):
    folder = 'Lupin/Modules'
    sys.path.insert(0, folder)
    
    module = importlib.import_module(module_name)
    function = getattr(module, function_name)
    result = function(*args, **kwargs)

    sys.path.pop(0)
    return result



# Function to get a module variable
def get_module_variable(module_name: str, variable_name: str):
    folder = 'Lupin/Modules'
    sys.path.insert(0, folder)
    
    module = importlib.import_module(module_name)
    variable = getattr(module, variable_name)

    sys.path.pop(0)
    return variable



# Function to get the runned modules
def get_runned_modules() -> list:
    return []



# Create documentation
def create_documentation(document : Document) -> None:
    pass