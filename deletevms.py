from proxmoxapi import api
#VMIDS=[301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319]
#VMIDS = [113, 114, 115,117]
NODEID='proxmoxedu3'


a = api()
for vmid in VMIDS:
    t = a.stop_vm(NODEID,vmid)
    a.wait_for_task(NODEID,t)
    a.delete_vm(NODEID,vmid)