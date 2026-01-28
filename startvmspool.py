from proxmoxapi import api
NODE_ID='proxmoxedu1'
POOL = 'applied'
a = api()
vms = a.get_pool_vms(POOL)
for vm in vms['members']:
    print('Starting ', vm['vmid'])
    a.start_vm(vm['node'],vm['vmid'])
