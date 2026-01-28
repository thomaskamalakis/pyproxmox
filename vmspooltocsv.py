from proxmoxapi import api
import csv

NODE_ID='proxmoxedu3'
POOL_NAME = 'applied'
csv_filename = POOL_NAME + '.csv'
fieldnames = ['vmid', 'name', 'node']

a = api()
vms = a.get_pool_vms(POOL_NAME)['members']
for vm in vms:
    for field in fieldnames:
        print(vm[field])


with open(csv_filename, mode='w') as file:
    writer = csv.writer(file)
    writer.writerow(fieldnames)
    for vm in vms:
        writer.writerow([vm[field] for field in fieldnames])