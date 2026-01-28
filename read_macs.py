from proxmoxapi import api
import csv

CSV_FILE = 'applied.csv'
OUTPUT_CSV_FILE = 'applied-ips.csv'
OUTPUT_DCHP_CONFIG_FILE = 'applied.conf'

NODE = 'proxmoxedu3'
def get_list(filename = CSV_FILE):
    with open(filename,'r') as f:
        reader = csv.DictReader(f , delimiter = ',')
        vm_list = list(reader)
    
    for vm in vm_list:
        print(vm)
        vm['vm'] = vm['name']
        vm['vmid'] = vm['vmid']
    return vm_list

vms = get_list()

a = api()
MAC_addresses={}
start = 30
IP_RANGE = '10.100.52.{x}'

for vm in vms:
    print(vm)
    info = a.get_vm_params(NODE,vm['vmid'])
    net = info['net0']
    mac = net.split('=')[1].split(',')[0]
    ip = IP_RANGE.format(x=start)
    MAC_addresses[vm['vm']]={
        'mac' : mac,
        'ip' : ip
    }
    vm['mac'] = mac
    vm['ip'] = ip
    start+=1

dhcp_config = ''
for k, vm in vms:
    dhcp_config += """
host {k} {{
hardware ethernet {mac};
fixed-address {ip};
option routers {gateway};
}}
""".format(mac = vm['mac'],
           ip = vm['ip'],
           gateway = '10.100.52.1',
           k = vm['vm'])

print(dhcp_config)

with open(OUTPUT_CSV_FILE,'w') as f:
    writer = csv.writer(f)
    writer.writerow(['vm','user','vmid','mac','ip'])
    for vm in vms:        
        writer.writerow(vm['vm'],vm['user'],vm['id'],vm['mac'],vm['ip'])

with open(OUTPUT_DCHP_CONFIG_FILE,'w') as f:
    f.write(dhcp_config)





