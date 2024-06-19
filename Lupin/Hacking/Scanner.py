import Logger
import ipaddress
import subprocess
from enum import Enum



class ScanType(Enum):
    COMMON = 0
    FULL = 1



class Port:
    def __init__(self, port_number, protocol, state, service):
        self.port_number = port_number
        self.protocol = protocol
        self.state = state
        self.service = service

    def __str__(self):
        return f'{self.port_number}/{self.protocol}\t{self.state}\t{self.service}'



class Host:
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.ports = []
        self.mac_address = 'Unknown'



    def scan(self, ScanType=ScanType.FULL):
        Logger.Info(f'Scanning {self.ip_address}...')
        self.scan_level = ScanType

        if ScanType == ScanType.COMMON:
            common_ports = [20, 21, 22, 23, 25, 53, 80, 110, 143, 443, 3389, 3306, 5432, 5900, 8080, 8443]
            common_ports_str = ','.join(map(str, common_ports))
            output = subprocess.check_output(['nmap', '--min-parallelism', '5', '-T5', '-p', common_ports_str, self.ip_address])

        elif ScanType == ScanType.FULL:
            output = subprocess.check_output(['nmap', '--min-parallelism', '5', '-T5', '-p-', self.ip_address])
        
        Logger.Success(f'{self.ip_address} scanned.')
        
        decoded_output = output.decode().split('\n')
        for i in range(len(decoded_output)):
            decoded_output[i] = decoded_output[i].rstrip('\r')
        
        decoded_output = list(filter(None, decoded_output))

        for i in decoded_output:
            if '/tcp' in i or '/udp' in i:
                test = i.split(' ')
                test = list(filter(None, test))
                if 'open' in test:
                    print(f'\t{test}')
            #print(f'\t{i}')
          


    def __str__(self):
        return f'{self.ip_address}'



def is_nmap_installed():
    try:
        subprocess.check_output(['nmap', '--version'])
        return True
    except FileNotFoundError:
        return False
    


def ping_sweep(network):
    try:
        output = subprocess.check_output(['nmap', '-sn', network, '-oG', '-'])
        output_lines = output.decode().split('\n')

        alive_hosts = []
        for line in output_lines:
            if 'Up' in line:
                ip_address = line.split()[1]
                alive_hosts.append(ip_address)

        return sorted(alive_hosts, key=lambda ip: ipaddress.ip_address(ip))
    
    except subprocess.CalledProcessError as e:
        return None
    

    
def scan():
    if not is_nmap_installed():
        Logger.Error('Nmap is not installed.')
        return

    Logger.Info('Scanning the network...')
    live_hosts = ping_sweep('192.168.1.0/24')
    if live_hosts is None:
        Logger.Error('Failed to scan the network.')
        return
    Logger.Success('Live hosts determined.')

    hosts = [Host(ip) for ip in live_hosts]

    for host in hosts:
        host.scan()

    return hosts