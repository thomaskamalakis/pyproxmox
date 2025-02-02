from proxmoxapi import api
import csv

CSV_FILE = 'users2.csv'
NODE = 'proxmoxedu2'
def get_list(filename = CSV_FILE):
    with open(filename,'r') as f:
        reader = csv.DictReader(f , delimiter = ';')
        vm_list = list(reader)

    return vm_list

vms = get_list()

a = api()
MAC_addresses={}
start = 65
IP_RANGE = '10.100.52.{x}'

for vm in vms:
    print(vm)
    info = a.get_vm_params(NODE,vm['vmid'])
    net = info['net0']
    mac = net.split('=')[1].split(',')[0]
    MAC_addresses[vm['vm']]={
        'mac' : mac,
        'ip' : IP_RANGE.format(x=start)
    }
    start+=1

print(MAC_addresses)
dhcp_config = ''
for k, vm in MAC_addresses.items():
    dhcp_config += """
host {k} {{
hardware ethernet {mac};
fixed-address {ip};
option routers {gateway};
}}
""".format(mac = vm['mac'],
           ip = vm['ip'],
           gateway = '10.100.52.1',
           k = k)
    



