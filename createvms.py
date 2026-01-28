from proxmoxapi import api
import csv

CSV_FILE = 'applied.csv'
CSV_FILE_OUTPUT = 'applied.out.csv'
DHCP_CONFIG_FILE = 'dhcp.conf'

VM_TEMPLATE = 118
START_ID = 400
NODE = 'proxmoxedu3'
ISO_STORAGE = 'isostorage1'
IP_RANGE = '10.100.52.{x}'
IP_START = 30
GATEWAY = '10.100.52.1'

def get_list(filename = CSV_FILE):
    vm_id = START_ID
    with open(filename,'r') as f:
        reader = csv.DictReader(f , delimiter = ',')
        vm_list = list(reader)
    
    for vm in vm_list:
        vm['sudo_user'] = vm['user']
        vm['vm'] = vm['user'] + 'vm'
        vm['user'] = vm['user'] + '@HUA'
        vm['vmid'] = vm_id
        
        vm_id += 1

    return vm_list

def clone_vm(user, newvmid, node = NODE, vmid = VM_TEMPLATE, name = None, **kwargs):
    a = api()
    if not a.user_exists(user):
        a.create_user(user, **kwargs)
    t = a.clone_vm(node, vmid, newvmid)    
    print(t)
    a.wait_for_task(node, t)                       
        
    a.set_vm_user(user, newvmid)
    a.change_vm_config(node, newvmid, name=name)
    # a.set_storage_user(user,ISO_STORAGE)

vms = get_list()
a = api()
x = IP_START
dhcp_config = ''

for vm in vms:
    password = vm.get('password')
    firstname = vm.get('firstname')
    lastname = vm.get('lastname')
    email = vm.get('email')
    
    clone_vm(vm['user'], int(vm['vmid']), 
             name = vm['vm'],
             password = password,
             firstname = firstname,
             lastname = lastname,
             email = email)
    info = a.get_vm_params(NODE,vm['vmid'])
    net = info['net0']
    mac = net.split('=')[1].split(',')[0]
    ip = IP_RANGE.format(x=x)
    vm['mac'] = mac
    vm['ip'] = ip

    dhcp_config += """
    host {name} {{
    hardware ethernet {mac};
    fixed-address {ip};
    option routers {gateway};
    }}
    """.format(mac = vm['mac'],
           ip = vm['ip'],
           gateway = GATEWAY,
           name = vm['vm'])
    
    x += 1

with open(CSV_FILE_OUTPUT, "w") as f:
    writer = csv.DictWriter(f, fieldnames=vms[0].keys())
    writer.writeheader()
    writer.writerows(vms)

with open(DHCP_CONFIG_FILE, 'w') as f:
    f.write(dhcp_config)
    









