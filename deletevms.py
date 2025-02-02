from proxmoxapi import api
VMID=118
NODEID='proxmoxedu3'

a = api()
t = a.stop_vm(NODEID,VMID)
a.wait_for_task(NODEID,t)
a.delete_vm(NODEID,VMID)