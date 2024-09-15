# Imports
from docx import Document
import Utilities.output_parser as op
import Utilities.documentation_formatter as doc
from Utilities.command_execution import execute_command, CommandExecutionError
from Utilities.decorators import lupin_module, lupin_gui, lupin_doc, GuiType, GuiState



# Configuration and prerequisites of the module
module_config = {
    'priority' : 10,
    'display_name' : 'Ping Sweep',
    'category' : 'Discovery',
    'required_apps' : [
        'nmap'
    ],
    'required_modules' : [],
    'is_network_required' : True,
    'is_wifi_adapter_required' : False,
    'is_bluetooth_adapter_required' : False
}



# This data model should be returned by the function `core`
output_data_model = {
    'up' : [],
    'down' : [],
    'targets' : []
}



# This data model should be set by the user in the settings of the module
settings_data_model = {
    'targets' : []
}



# Main functionality of the module
@lupin_module
def core(settings : dict) -> dict:
    try:
        targets = ' '.join(settings['targets'])

        stdout, stderr, returncode = execute_command(f'nmap -sL {targets} -oG -')
        data_list = op.output_to_list(stdout)
        clean_data_list = op.clean_data(data_list)
        filtered_data = op.keep_filtered(clean_data_list, r'Host: \d+\.\d+\.\d+\.\d+')
        all_ips = op.get_nth_word(filtered_data, 2)

        stdout, stderr, returncode = execute_command(f'nmap -sn {targets} -oG -')
        data_list = op.output_to_list(stdout)
        clean_data_list = op.clean_data(data_list)
        filtered_data = op.keep_filtered(clean_data_list, r'Host: \d+\.\d+\.\d+\.\d+')
        up_ips = op.get_nth_word(filtered_data, 2)
        
        for ip in all_ips:
            if ip in up_ips:
                output_data_model['up'].append(ip)
            else:
                output_data_model['down'].append(ip)

        output_data_model['targets'] = settings['targets']

        return output_data_model

    except CommandExecutionError as e:
        return e



# Settings user interface of the module
@lupin_gui(GuiType.SETTINGS)
def settings_gui(settings : dict):
    pass



# Output user interface of the module
@lupin_gui(GuiType.OUTPUT)
def output_gui(output : dict):
    pass



# Documentation of the module
@lupin_doc
def documentation(document: Document, results: dict) -> None:
    doc.heading(document, 'Ping Sweep')
    doc.paragraph(document, 'The Ping Sweep module is used to scan the network for live hosts.')

    doc.subheading(document, 'Targets')
    doc.unordered_list(document, results['targets'])

    doc.subheading(document, 'Up hosts')
    doc.ordered_list(document, results['up'])
