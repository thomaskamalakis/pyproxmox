from proxmoxapi import api
VMIDS=[401, 402, 403, 404, 405, 
       406, 407, 408, 409, 410, 
       411, 412, 413, 414, 415,
       416, 417, 418, 419, 420,
       421, 422, 423, 424, 425]
NODEID='proxmoxedu3'


a = api()
for vmid in VMIDS:
    t = a.stop_vm(NODEID,vmid)
    a.wait_for_task(NODEID,t)
    a.delete_vm(NODEID,vmid)