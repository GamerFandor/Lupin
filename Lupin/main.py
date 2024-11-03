# Imports
from Utilities.data_manager import get_data_files
import Utilities.userinterface as ui
from pathlib import Path



# Create the main window
APP = ui.create_window()



# Main function
def main():
    documents_folder = Path.home() / "Documents" / "Lupin"
    print(documents_folder)
    global APP
    APP.mainloop()



# Run the main function
main()