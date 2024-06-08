import Logger
import ipaddress
import subprocess

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
    
    common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3389, 3306, 5432, 5900, 8080, 8443]
    common_ports_str = ','.join(map(str, common_ports))

    for host in live_hosts:
        Logger.Info(f'Scanning {host}...')
        output = subprocess.check_output(['nmap', '-p', common_ports_str, '-O', host])
        print(output.decode())