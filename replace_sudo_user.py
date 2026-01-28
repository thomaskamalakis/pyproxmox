from proxmoxapi import api
import csv

CSV_FILE = 'applied.out.csv'
START_ID = 400
DEFAULT_USER = 'stud'

with open(CSV_FILE,'r') as f:
    reader = csv.DictReader(f , delimiter = ',')
    vm_list = list(reader)

a = api()

for vm in vm_list:
    print(vm['ip'],vm['sudo_user'])
    a.create_sudo_user(vm['ip'],vm['sudo_user'],vm['sudo_user'])
    a.remove_vm_user(vm['ip'],DEFAULT_USER)
    
 