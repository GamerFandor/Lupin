# Imports
import customtkinter as ctk
from Utilities.data_manager import new_session
from Utilities.data_manager import get_all_sessions
from Lupin.Utilities.module_handler import get_modules



# Create the main window of the application
def create_window() -> ctk.CTk:
    ctk.set_appearance_mode('system')
    ctk.set_default_color_theme('green')

    app = ctk.CTk()
    app.title('Lupin')
    app.geometry('1280x720')
    app.minsize(640, 450)

    create_main_frame(app)

    return app



# Create the session frame
def create_session_frame(app : ctk.CTk) -> ctk.CTkFrame:
    frame = ctk.CTkFrame(app)
    frame.pack(fill="both", expand=True)

    # First Block (Create new session)
    first_block = ctk.CTkFrame(frame)
    first_block.pack(pady=5, padx=5, fill="both", expand=True)

    create_session_btn = ctk.CTkButton(first_block, text="Create New Session", command=new_session)
    create_session_btn.place(relx=0.5, rely=0.5, anchor="center")

    sessions = get_all_sessions()
    if sessions != []:
        # Second Block (Continue session with list of sessions)
        second_block = ctk.CTkFrame(frame)
        second_block.pack(pady=5, padx=5, fill="both", expand=True)

        # Label to print 'Continue a session'
        continue_label = ctk.CTkLabel(second_block, text="Continue a session", font=ctk.CTkFont(size=16, weight="bold"))
        continue_label.pack(pady=5)

        # Display the list of sessions
        for session in sessions:
            session_button = ctk.CTkButton(second_block, text=session)
            session_button.pack(pady=2)

    return frame



# Create the main window frame
def create_main_frame(app : ctk.CTk) -> ctk.CTkFrame:
    frame = ctk.CTkFrame(app)
    frame.pack(fill="both", expand=True)

    # Create side panel
    side_panel = ctk.CTkFrame(frame)
    side_panel.pack(side="left", fill="y")
    menu_panel = ctk.CTkFrame(side_panel, width=200)
    menu_panel.pack(fill="both", expand=True, padx=5, pady=5)

    main_button_panel = ctk.CTkFrame(side_panel, height=114)
    main_button_panel.pack(fill="both", padx=5, pady=5)

    for i in get_modules():
        menu_button = ctk.CTkButton(menu_panel, text=i[1], width=190)
        menu_button.pack(side="top", padx=5, pady=5)

    docs_button = ctk.CTkButton(main_button_panel, text="Generate documentation", width=190)
    docs_button.pack(side="top", fill="y", expand=True, padx=5, pady=5)

    auto_button = ctk.CTkButton(main_button_panel, text="Automatize execution", width=190)
    auto_button.pack(side="top", fill="y", expand=True, padx=5, pady=5)

    delete_button = ctk.CTkButton(main_button_panel, text="Delete session", width=190)
    delete_button.pack(side="top", fill="y", expand=True, padx=5, pady=5)

    # Create main panel
    main_panel = ctk.CTkFrame(frame)
    main_panel.pack(side="right", fill="both", expand=True)

    settings_panel = ctk.CTkFrame(main_panel)
    settings_panel.pack(fill="both", expand=True, padx=5, pady=5)

    button_container = ctk.CTkFrame(main_panel, height=38)
    button_container.pack(side="bottom", fill="x", expand=False, padx=5, pady=5)

    settings_panel_button = ctk.CTkButton(button_container, text="Settings", width=70)
    settings_panel_button.pack(side="left", padx=5, pady=5)

    output_panel_button = ctk.CTkButton(button_container, text="Output", width=70)
    output_panel_button.pack(side="left", padx=5, pady=5)

    execute_button = ctk.CTkButton(button_container, text="Execute", width=70)
    execute_button.pack(side="right", padx=5, pady=5)


    return frame



# Load module related interface
def load_module_interface(panel : ctk.CTkFrame, modul : str, interface : str) -> ctk.CTkFrame:
    frame = ctk.CTkFrame(panel)
    frame.pack(fill="both", expand=True)