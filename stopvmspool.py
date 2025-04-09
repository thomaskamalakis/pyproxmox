from proxmoxapi import api
NODE_ID='proxmoxedu1'

a = api()
vms = a.get_pool_vms('mscit')
for vm in vms['members']:
    print('Stopping ', vm['vmid'])
    a.stop_vm(vm['node'],vm['vmid'])
