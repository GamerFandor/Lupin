# Imports
import customtkinter as ctk


def create_multiline_input(frame : ctk.CTkFrame) -> ctk.CTkTextbox:
    input = ctk.CTkTextbox(frame, height=150)
    input.pack(fill="x", expand=False, padx=30, pady=10)
    return input

def get_multiline_input_value(input : ctk.CTkTextbox) -> str:
    return input.get("0.0", "end").split("\n")[:-1]

def create_singleline_input(frame: ctk.CTkFrame) -> ctk.CTkEntry:
    input = ctk.CTkEntry(frame)
    input.pack(fill="x", expand=False, padx=30, pady=10)
    return input

def get_singleline_input_value(input: ctk.CTkEntry) -> str:
    return input.get()

def create_checkbox(frame: ctk.CTkFrame, label : str) -> ctk.CTkCheckBox:
    checkbox = ctk.CTkCheckBox(frame, text=label)
    checkbox.pack(fill="x", expand=False, padx=30, pady=10)
    return checkbox

def get_checkbox_value(checkbox: ctk.CTkCheckBox) -> bool:
    return checkbox.get() == 1

def create_radiobutton_group(frame: ctk.CTkFrame, values: list) -> list:
    selected_value = ctk.StringVar(value=values[0])

    radio_buttons = []
    for value in values:
        radio_button = ctk.CTkRadioButton(frame, text=value, variable=selected_value, value=value)
        radio_button.pack(fill="x", expand=False, padx=30, pady=5)
        radio_buttons.append(radio_button)

    return selected_value

def get_radiobutton_value(selected_value: ctk.StringVar) -> str:
    return selected_value.get()

def title(frame: ctk.CTkFrame, text: str) -> ctk.CTkLabel:
    title_label = ctk.CTkLabel(frame, text=text, font=("Helvetica", 32, "bold"))
    title_label.pack(padx=20, pady=5, anchor="w")

def subtitle(frame: ctk.CTkFrame, text: str) -> ctk.CTkLabel:
    subtitle_label = ctk.CTkLabel(frame, text=text, font=("Helvetica", 24, "bold"))
    subtitle_label.pack(padx=20, pady=5, anchor="w")

def text(frame: ctk.CTkFrame, text: str) -> ctk.CTkLabel:
    label = ctk.CTkLabel(frame, text=text)
    label.pack(padx=20, pady=5, anchor="w")

def create_table(frame: ctk.CTkFrame, header: list, content: list):
    for i in range(len(content) + 1):
        row_frame = ctk.CTkFrame(frame)
        row_frame.pack(fill="x", expand=False, padx=20, pady=5)
        if i == 0:
            current_content = header
            is_header = True
        else:
            current_content = content[i - 1]
            is_header = False
        for j, label_text in enumerate(current_content):
            if is_header:
                label = ctk.CTkLabel(row_frame, text=label_text, font=("Helvetica", 16, "bold"))
            else:
                label = ctk.CTkLabel(row_frame, text=label_text, font=("Helvetica", 11))
            label.grid(row=0, column=j, padx=10, pady=10, sticky="w")
            row_frame.grid_columnconfigure(j, weight=1)

def create_unordered_list(frame: ctk.CTkFrame, items: list):
    for item in items:
        label = ctk.CTkLabel(frame, text="• " + item)
        label.pack(padx=20, anchor="w")

def create_ordered_list(frame: ctk.CTkFrame, items: list):
    for i, item in enumerate(items):
        label = ctk.CTkLabel(frame, text=f"{i + 1}. {item}")
        label.pack(padx=20, anchor="w")