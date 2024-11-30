from proxmoxapi import api
import csv

CSV_FILE = 'users.csv'
VM_TEMPLATE = 106
NODE = 'proxmoxedu1'

def get_list(filename = CSV_FILE):
    with open(filename,'r') as f:
        reader = csv.DictReader(f , delimiter = ';')
        vm_list = list(reader)

    return vm_list

def clone_vm(user, newvmid, node = NODE, vmid = VM_TEMPLATE, name = None):
    a = api()
    t = a.clone_vm(node, vmid, newvmid)
    print(t)
    a.wait_for_task(node, t)
    if not a.user_exists(user):
        a.create_user(user)
        
    a.set_vm_user(user, newvmid)
    a.change_vm_config(node, newvmid, name=name)

vms = get_list()
for vm in vms:
    print(vm)
    clone_vm(vm['user'], vm['vmid'], name = vm['vm'])
