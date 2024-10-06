# Imports
import os
import inspect
from enum import Enum
from Utilities.data_manager import save_data, load_data



# GuiState enumeration
class GuiState(Enum):
    NORMAL = 0
    ERROR  = 1



# GuiType enumeration
class GuiType(Enum):
    SETTINGS = 0
    OUTPUT   = 1



# Decorator for the main functionality of the module
def lupin_module(function):

    def wrapper(*args, **kwargs):
        result = function(*args, **kwargs)
        save_data(result, f'{function.__module__}')
        return result
    
    return wrapper



# Decorator for the user interface of the module
def lupin_gui(gui_type : GuiType):
    
    def lupin_gui_decorator(function):
        if GuiType.OUTPUT == gui_type:
            data = load_data(f'{function.__module__}')
            
        def wrapper(*args, **kwargs):
            return function(*args, **kwargs)
        return wrapper
    
    return lupin_gui_decorator



# Decorator for the documentation of the module
def lupin_doc(function):

    def wrapper(*args, **kwargs):
        return function(*args, **kwargs)
    
    return wrapper