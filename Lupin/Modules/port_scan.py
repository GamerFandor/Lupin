# Imports
from docx import Document
import Utilities.output_parser as op
import Utilities.ui_components as ui_comps
from Utilities.data_manager import load_data
import Utilities.documentation_formatter as doc
from Utilities.userinterface import CURRENT_SESSION
from Utilities.command_execution import execute_command, CommandExecutionError
from Utilities.decorators import lupin_module, lupin_gui, lupin_doc, GuiType, GuiState



# Configuration and prerequisites of the module
module_config = {
    'order' : 20,
    'display_name' : 'Port Scan',
    'category' : 'Discovery',
    'required_apps' : [
        'nmap'
    ],
    'required_modules' : [
        'ping_sweep'
    ],
    'is_network_required' : True,
    'is_wifi_adapter_required' : False
}



# This data model should be returned by the function `core`
output_data_model = {
    'open_ports' : {},
    'targets' : [],
    'target_ports' : []
}



# This data model should be set by the user in the settings of the module
settings_data_model = {
    'targets' : [],
    'attack_all_ports' : False,
    'target_ports' : []
}



# Input components
targets_checkboxes = []
attack_all_ports_checkbox = None
target_ports_textbox = None



# Main functionality of the module
@lupin_module
def core() -> dict:
    global output_data_model, settings_data_model
    try:
        targets = ' '.join(settings_data_model['targets'])
        target_ports = ','.join(settings_data_model['target_ports'])

        if settings_data_model['attack_all_ports']:
            stdout, stderr, returncode = execute_command(f'nmap -p- {targets}')
        else:
            stdout, stderr, returncode = execute_command(f'nmap -p {target_ports} {targets}')

        data_list = op.output_to_list(stdout)
        block_data =[[]]
        index = 0
        for i in data_list:
            if i == '':
                block_data.append([])
                index += 1
            else:
                block_data[index].append(i)

        for i in block_data:
            if len(i) == 0 or len(i) == 1:
                continue
            ports = op.keep_filtered(i, r'^\d+')
            filtered_ports = []
            for port in ports:
                filtered_ports.append(port.split(' ')[0])
            host = op.keep_filtered(i, r'Nmap scan report for')[0].split(' ')[-1]
            if len(filtered_ports) > 0:
                output_data_model['open_ports'][host] = filtered_ports
        print(output_data_model['open_ports'])
        print("---")
        print(block_data)


        output_data_model['targets'] = settings_data_model['targets']
        output_data_model['target_ports'] = settings_data_model['target_ports']

        return output_data_model

    except CommandExecutionError as e:
        return e



# This function is used to read the input from the user
def read_input():
    global settings_data_model, targets_checkboxes, attack_all_ports_checkbox, target_ports_textbox
    for i in range(len(targets_checkboxes)):
        if ui_comps.get_checkbox_value(targets_checkboxes[i]):
            settings_data_model['targets'].append(targets_checkboxes[i].cget('text'))
    settings_data_model['attack_all_ports'] = ui_comps.get_checkbox_value(attack_all_ports_checkbox)
    settings_data_model['target_ports'] = ui_comps.get_multiline_input_value(target_ports_textbox)



# Settings user interface of the module
@lupin_gui(GuiType.SETTINGS)
def settings_gui(root):
    global targets_textbox, attack_all_ports_checkbox, target_ports_textbox
    ui_comps.subtitle(root, 'Ports to scan')
    ui_comps.text(root, 'Enter the ports to scan. If you chose attack all ports you don\'t have to enter anything.')
    attack_all_ports_checkbox = ui_comps.create_checkbox(root, 'Attack all ports (1 - 65535)')
    target_ports_textbox = ui_comps.create_multiline_input(root)

    ui_comps.subtitle(root, 'Targets')
    ui_comps.text(root, 'Enter the targets (each target should be in a new line). You also can use CIDR notation for mutliple targets.')
    ping_sweep_output = load_data(CURRENT_SESSION, 'ping_sweep')
    for ip in ping_sweep_output['up']:
        targets_checkboxes.append(ui_comps.create_checkbox(root, ip))



# Output user interface of the module
@lupin_gui(GuiType.OUTPUT)
def output_gui(root, data: dict):
    ui_comps.subtitle(root, 'Targets')
    ui_comps.create_unordered_list(root, data['targets'])

    ui_comps.subtitle(root, 'Target ports')
    if len(data['target_ports']) == 65535:
        ui_comps.text(root, 'All ports (1 - 65535)')
    else:
        ui_comps.create_unordered_list(root, data['target_ports'])

    for key, value in data['open_ports'].items():
        ui_comps.subtitle(root, f"{key}'s open ports")
        ui_comps.create_unordered_list(root, value)



# Documentation of the module
@lupin_doc
def documentation(document: Document, data: dict) -> None:
    doc.heading(document, 'Port Scan')
    doc.paragraph(document, 'The Port Scan module is used to scan the host for open ports.')

    doc.subheading(document, 'Targets')
    doc.unordered_list(document, data['targets'])

    doc.subheading(document, 'Target ports')
    if len(data['target_ports']) == 65535:
        doc.paragraph(document, 'All ports (1 - 65535)')
    else:
        doc.unordered_list(document, data['target_ports'])

    table_data = []
    for key, value in data['open_ports'].items():
        table_data.append([key, "\n".join(value)])
        
    doc.table(document, ['Host', 'Open ports'], table_data)