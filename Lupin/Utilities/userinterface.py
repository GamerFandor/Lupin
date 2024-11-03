# Imports
import customtkinter as ctk
from Utilities.documentation_formatter import generate_documentation
from Utilities.data_manager import get_all_sessions, new_session, delete_session, load_data, get_data_files
from Utilities.module_handler import get_modules, call_module_function
from Utilities.command_execution import is_program_installed, is_connected, has_wifi_adapter
import Utilities.ui_components as ui_comps

CURRENT_SESSION = None
CURRENT_MODULE = None

# Create the main window of the application
def create_window() -> ctk.CTk:
    ctk.set_appearance_mode('system')
    ctk.set_default_color_theme('green')

    app = ctk.CTk()
    app.title('Lupin')
    app.geometry('1280x720')
    app.minsize(640, 450)

    create_session_frame(app)

    return app



# Create the session frame
def create_session_frame(app : ctk.CTk) -> ctk.CTkFrame:
    frame = ctk.CTkFrame(app)
    frame.pack(fill="both", expand=True)

    # First Block (Create new session)
    first_block = ctk.CTkFrame(frame)
    first_block.pack(pady=5, padx=5, fill="both", expand=True)

    create_session_btn = ctk.CTkButton(first_block, text="Create New Session", command=lambda: create_new_session(app, frame))
    create_session_btn.place(relx=0.5, rely=0.5, anchor="center")

    sessions = get_all_sessions()
    if sessions != []:
        # Second Block (Continue session with list of sessions)
        second_block = ctk.CTkFrame(frame)
        second_block.pack(pady=5, padx=5, fill="both", expand=True)

        # Label to print 'Continue a session'
        continue_label = ctk.CTkLabel(second_block, text="Continue a session", font=ctk.CTkFont(size=16, weight="bold") )
        continue_label.pack(pady=5)

        # Display the list of sessions
        for session in sessions:
            session_button = ctk.CTkButton(second_block, text=session, command=lambda: load_existing_session(app, frame, session))
            session_button.pack(pady=2)

    return frame



# Create new session and open the main window
def create_new_session(app, current_frame) -> None:
    global CURRENT_SESSION
    session = new_session()
    print(CURRENT_SESSION)
    current_frame.destroy()
    create_main_frame(app)



# Load a session and open the main window
def load_existing_session(app, current_frame, session) -> None:
    global CURRENT_SESSION
    CURRENT_SESSION = session
    current_frame.destroy()
    create_main_frame(app)


# Create the main window frame
def create_main_frame(app : ctk.CTk) -> ctk.CTkFrame:
    frame = ctk.CTkFrame(app)
    frame.pack(fill="both", expand=True)

    # Create side panel
    side_panel = ctk.CTkFrame(frame)
    side_panel.pack(side="left", fill="y")
    menu_panel = ctk.CTkFrame(side_panel, width=200)
    menu_panel.pack(fill="both", expand=True, padx=5, pady=5)

    main_button_panel = ctk.CTkFrame(side_panel, height=76)
    main_button_panel.pack(fill="both", padx=5, pady=5)

    docs_button = ctk.CTkButton(main_button_panel, text="Generate documentation", width=190, command=lambda: generate_documentation(CURRENT_SESSION))
    docs_button.pack(side="top", fill="y", expand=True, padx=5, pady=5)

    global CURRENT_SESSION
    delete_button = ctk.CTkButton(main_button_panel, text="Delete session", width=190, command=lambda: remove_session(CURRENT_SESSION, frame, app))
    delete_button.pack(side="top", fill="y", expand=True, padx=5, pady=5)

    # Create main panel
    main_panel = ctk.CTkFrame(frame)
    main_panel.pack(side="right", fill="both", expand=True)

    settings_panel = ctk.CTkFrame(main_panel)
    settings_panel.pack(fill="both", expand=True, padx=5, pady=5)

    button_container = ctk.CTkFrame(main_panel, height=38)
    button_container.pack(side="bottom", fill="x", expand=False, padx=5, pady=5)

    settings_panel_button = ctk.CTkButton(button_container, text="Settings", width=70, command=lambda: swtich_to_settings(settings_panel))
    settings_panel_button.pack(side="left", padx=5, pady=5)

    output_panel_button = ctk.CTkButton(button_container, text="Output", width=70, command=lambda: switch_to_output(settings_panel))
    output_panel_button.pack(side="left", padx=5, pady=5)

    execute_button = ctk.CTkButton(button_container, text="Execute", width=70, command=lambda: execute_module(settings_panel))
    execute_button.pack(side="right", padx=5, pady=5)

    for i in get_modules():
        menu_button = ctk.CTkButton(menu_panel, text=i[1], width=190, command=lambda i=i: open_module(i[0], settings_panel))
        menu_button.pack(side="top", padx=5, pady=5)

    open_module(get_modules()[0][0], settings_panel)
    global CURRENT_MODULE
    CURRENT_MODULE = get_modules()[0][0]

    return frame



# Load module related interface
def load_module_interface(panel : ctk.CTkFrame, modul : str, interface : str) -> ctk.CTkFrame:
    frame = ctk.CTkFrame(panel)
    frame.pack(fill="both", expand=True)


def remove_session(session_name, frame, app):
    delete_session(session_name)
    frame.destroy()
    create_session_frame(app)


def open_module(module_name, frame):
    global CURRENT_MODULE, CURRENT_PAGE
    CURRENT_MODULE = module_name
    for widget in frame.winfo_children():
        widget.destroy()
    module_name = get_modules()
    for module in module_name:
        if module[0] == CURRENT_MODULE:
            ui_comps.title(frame, module[1])
            break
    data = load_data(CURRENT_SESSION, module_name)
    if data == {}:
        swtich_to_settings(frame)
    else:
        switch_to_output(frame)

def swtich_to_settings(frame):
   

    for widget in frame.winfo_children():
        widget.destroy()
    module_name = get_modules()
    for module in module_name:
        if module[0] == CURRENT_MODULE:
            ui_comps.title(frame, module[1])
            break
    if not check_module_dependencies(CURRENT_MODULE):
        ui_comps.text(frame, 'Module dependencies are not met.')
        return
    call_module_function(CURRENT_MODULE, 'settings_gui', frame)

def switch_to_output(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    module_name = get_modules()
    for module in module_name:
        if module[0] == CURRENT_MODULE:
            ui_comps.title(frame, module[1])
            break
    if not check_module_dependencies(CURRENT_MODULE):
        ui_comps.text(frame, 'Module dependencies are not met.')
        return
    data = load_data(CURRENT_SESSION, CURRENT_MODULE)
    if data == {}:
        ui_comps.text(frame, 'No data to display, you have to run the module first.')
    else:
        call_module_function(CURRENT_MODULE, 'output_gui', frame)

def execute_module(frame):
    if not check_module_dependencies(CURRENT_MODULE):
        return

    call_module_function(CURRENT_MODULE, 'read_input')

    for widget in frame.winfo_children():
        widget.destroy()
    module_name = get_modules()
    for module in module_name:
        if module[0] == CURRENT_MODULE:
            ui_comps.title(frame, module[1])
            break
    
    call_module_function(CURRENT_MODULE, 'core')
    switch_to_output(frame)


def check_module_dependencies(module_name):
    current_module_data = None
    for i in get_modules():
        if i[0] == module_name:
            current_module_data = i
            break
    
    required_apps = current_module_data[3]
    required_modules = current_module_data[4]
    is_network_required = current_module_data[5]
    is_wifi_adapter_required = current_module_data[6]

    for app in required_apps:
        if not is_program_installed(app):
            return False
    
    runned_modules = [module.replace('.json', '') for module in get_data_files(CURRENT_SESSION)]
    for module in required_modules:
        if module not in runned_modules:
            return False

    if is_network_required and not is_connected():
        return False
    
    if is_wifi_adapter_required and not has_wifi_adapter():
        return False

    return True