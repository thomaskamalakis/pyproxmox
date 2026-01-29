from proxmoxapi import api
import csv

NODE = 'proxmoxedu3'
POOL = 'applied'
START_ID = 400
INTERFACE_NAME = 'ens18'

a = api()
vms = a.get_pool_vms(POOL)['members']
for vm in vms:
    vmid = vm['vmid']
    if vmid > START_ID:
        nets = a.get_vm_net(NODE, vmid)['result']        
        for net in nets:
            if net['name'] == INTERFACE_NAME:
                ip_address = net['ip-addresses'][0]['ip-address']
                print('Shutting down VM with id', vmid, 'and ip address',ip_address)
                a.ansible_shut_down(ip_address)


        



