from proxmoxapi import api
import csv

CSV_FILE = 'users2.csv'
NODE = 'proxmoxedu2'
def get_list(filename = CSV_FILE):
    with open(filename,'r') as f:
        reader = csv.DictReader(f , delimiter = ';')
        vm_list = list(reader)

    return vm_list

vms_list = get_list()
a = api()
vms = a.get_vms_net()

# ips = []
# for vm in vms:
#     ips.append(vm['ip'])
        



