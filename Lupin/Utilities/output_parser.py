# Imports
import re



# Convert the executed command's output into a list that contains the lines separatedly
def output_to_list(output : str) -> list:
    return output.split('\n')



# Clean the data from unvanted parts
def clean_data(data : list, should_replace_tab : bool = True) -> list:
    output = []
    
    for d in data:
        d = d.strip()
        if should_replace_tab:
            d = d.replace('\t', ' ')
        d = re.sub(r'\s+', ' ', d)
        
        output.append(d)

    return output



# Keeps the lines that match the regex expression
def keep_filtered(data : list, regex_expression : str) -> list:
    regex = re.compile(regex_expression)
    return [line for line in data if regex.search(line)]



# Discards the lines that match the regex expression
def discard_filtered(data : list, regex_expression : str) -> list:
    regex = re.compile(regex_expression)
    return [line for line in data if not regex.search(line)]



# Returns only the n-th word from every line
def get_nth_word(data : list, n : int, separator : str = ' ') -> list:
    output = []
    for d in data:
        output.append(d.split(separator)[n - 1])
    return output



# Testing
if __name__ == '__main__':
    test_data = [
        'Nmap scan report for 192.168.1.1',
        'Hello',
        'Nmap scan report for 192.168.1.2',
        'Nmap scan report for 192.168.1.3',
        'Nmap scan report for 192.168.1.4',
        'Hello',
        'Hello',
        'Nmap scan report for 192.168.1.5',
        'Nmap scan report for 192.168.1.6',
        'Nmap scan report for 192.168.1.7',
        'Hello',
        'Nmap scan report for 192.168.1.8',
        'Nmap scan report for 192.168.1.9',
        'Nmap scan report for 192.168.1.10',
    ]

    filtered_data = keep_filtered(test_data, r'\d+\.\d+\.\d+\.\d+')
    up_hosts = get_nth_word(filtered_data, 5)

    for host in up_hosts:
        print(host)