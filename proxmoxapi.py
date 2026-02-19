import requests
import datetime
import time
import subprocess
import sys
import configparser


requests.packages.urllib3.disable_warnings() 
config = configparser.ConfigParser()
config.read('defaults.txt')
defaults = config['defaults']

SECRET = defaults['secret']
TOKENID = defaults['tokenid']
URL = defaults['url']
TIMEOUT = int(defaults['timeout'])
CHECK_INTERVAL = int(defaults['check_interval'])
ANSIBLE_SCRIPTS = {'sudo' : 'sudo.yml', 
                   'shutdown' : 'shutdown.yml',
                   'remove_user' : 'remove_user.yml'}

def elapsed(t0):
    t1 = datetime.datetime.now()
    return (t1-t0).total_seconds()

class api:

    def __init__(self, 
                 secret = SECRET,
                 tokenid = TOKENID,
                 url = URL,
                 verify = False,
                 check_interval = CHECK_INTERVAL,
                 timeout = TIMEOUT,
                 ansible_scripts = ANSIBLE_SCRIPTS):
        
        self.secret = secret
        self.tokenid = tokenid
        self.url = url
        self.verify = verify
        self.timeout = timeout
        self.check_interval = check_interval
        self.ansible_scripts = ansible_scripts

        self.headers = {
            'Authorization' : 'PVEAPIToken=%s=%s' %(self. tokenid, self.secret)
        }

    def get(self, suburl):
        url = self.url + suburl
        return requests.get(url, 
                            headers = self.headers, 
                            verify = self.verify).json()['data']

    def post(self, suburl, params):
        url = self.url + suburl
        print(url)
        r = requests.post(url,
                          json = params, 
                          headers = self.headers, 
                          verify = self.verify)
        print(r.status_code)
        print(r.text)
        return r.json()['data']
    
    def delete(self, suburl):
        url = self.url + suburl
        return requests.delete(url, headers=self.headers, verify = self.verify)

    def put(self, suburl, params):
        url = self.url + suburl
        print(url)
        r = requests.put(url,
                         json = params, 
                         headers = self.headers, 
                         verify = self.verify)
        print(r.status_code)
        print(r.text)
        return r.json()['data']

    def get_version(self):
        return self.get('version')   
     
    def get_nodes(self):
        return self.get('nodes')
    
    def get_users(self):
        return self.get('users')
        
    def get_node_vms(self, nodeid):
        suburl = 'nodes/{node}/qemu'.format(node=nodeid)
        print(suburl)
        return self.get(suburl)
    
    def get_vms(self):
        nodes = self.get_nodes()
        nodeids = [n['node'] for n in nodes]
        vms = []
        for nodeid in nodeids:
            vms_node = self.get_node_vms(nodeid)
            for vm in vms_node:
                vm['nodeid'] = nodeid
            vms += vms_node
        
        return vms

    def get_vm_params(self, nodeid, vmid):
        suburl = 'nodes/{node}/qemu/{vmid}/config'.format(node=nodeid, 
                                                          vmid=vmid)
        return self.get(suburl)
    
    def create_vm(self, nodeid, **kwargs):
        suburl = 'nodes/{node}/qemu'.format(node=nodeid)
        return self.post(suburl, params=kwargs)
    
    def create_disk(self, nodeid, storageid, **kwargs):
        suburl = 'nodes/{node}/storage/{storage}/content'.format(node=nodeid,
                                                                 storage=storageid)
        return self.post(suburl, params=kwargs)
    
    def clone_vm(self, nodeid, vmid, newid, full=True):
        suburl = 'nodes/{node}/qemu/{vmid}/clone'.format(node=nodeid, 
                                                          vmid=vmid)
        params = {'newid' : newid, 'full' : full }
        return self.post(suburl, params=params)
    
    def get_task_status(self, nodeid, upid):
        suburl = 'nodes/{node}/tasks/{upid}/status'.format(node=nodeid, 
                                                           upid=upid)
        return self.get(suburl)
    
    def change_vm_config(self, nodeid, vmid, **params):
        suburl = 'nodes/{node}/qemu/{vmid}/config'.format(node=nodeid, 
                                                          vmid=vmid)
        return self.post(suburl, params = params)

    def get_vm_status(self, nodeid, vmid):
        suburl = 'nodes/{node}/qemu/{vmid}/status/current'.format(node=nodeid, 
                                                                  vmid=vmid)
        return self.get(suburl)

    def get_vm_net(self, nodeid, vmid):
        suburl = 'nodes/{node}/qemu/{vmid}/agent/network-get-interfaces'.format(node=nodeid, 
                                                                  vmid=vmid)
        return self.get(suburl)

    def delete_vm(self, nodeid, vmid):
        suburl = 'nodes/{node}/qemu/{vmid}'.format(node=nodeid,vmid=vmid)
        return self.delete(suburl)

    def get_vms_net(self):
        vms = self.get_vms()
        for vm in vms:
            vm['net'] = self.get_vm_net(vm['nodeid'], vm['vmid'])
        return vms 

    def get_pool_vms(self, pool_id):
        suburl = 'pools/{pool_id}'.format(pool_id=pool_id)
        return self.get(suburl)

    def wait_for_task(self, nodeid, upid, timeout = None, echodot=True):
        t0 = datetime.datetime.now()

        if not timeout:
            timeout=self.timeout

        while elapsed(t0) < timeout:
            s = self.get_task_status(nodeid, upid)
            if s['status'] == 'stopped':
                print()
                return elapsed(t0)
            time.sleep(self.check_interval)
            if echodot:
                print('.', end='', flush=True)
        
        return -1  

    def stop_vm(self, nodeid, vmid):
        suburl = 'nodes/{node}/qemu/{vmid}/status/stop'.format(node=nodeid, vmid=vmid)
        params = {'node' : nodeid, 'vmid' : vmid}
        headers = self.headers
        return self.post(suburl, params=params)
    
    def start_vm(self, nodeid, vmid):
        suburl = 'nodes/{node}/qemu/{vmid}/status/start'.format(node=nodeid, vmid=vmid)
        params = {'node' : nodeid, 'vmid' : vmid}
        headers = self.headers
        return self.post(suburl, params=params)

    def create_user(self, userid, **params):
        suburl = 'access/users'
        params['userid'] = userid
        return self.post(suburl, params = params)
    
    def get_users(self):
        suburl = 'access/users'
        return self.get(suburl)
        
    def get_user(self, userid):
        suburl = 'access/users/{userid}'.format(userid=userid)
        return self.get(suburl)
    
    def user_exists(self, userid):
        users = [ u['userid'] for u in self.get_users() ]
        return userid in users
    
    def get_acl(self):
        suburl = 'access/acl'
        return self.get(suburl)
    
    def set_vm_user(self, userid, vmid):
        suburl = 'access/acl'
        path = '/vms/{vmid}'.format(vmid=vmid)
        params = {
            'roles' : ['PVEVMUser'],
            'users' : [ userid ],
            'path' : path,
            'propagate' : 1
        }
        return self.put(suburl, params=params)
    
    def set_storage_user(self, userid, storageid):
        suburl = 'access/acl'        
        params = {
            'path': '/storage/'+storageid, 
            'propagate': 1, 
            'users': [userid], 
            'roles': ['PVEDatastoreUser']
        }
        return self.put(suburl, params=params)
    
    def create_sudo_user(self, ip, user, password):
        extra_vars = 'username={user} password={password}'.format(user=user, password=password)
        ip += ','
        print(extra_vars)
        subprocess.run(['ansible-playbook', '-i', ip, 
                        self.ansible_scripts['sudo'],'--extra-vars', extra_vars],
                        stderr = sys.stderr, stdout = sys.stdout)
        
    def remove_vm_user(self, ip, user):
        extra_vars = 'username={user}'.format(user=user)
        ip += ','
        print(extra_vars)
        subprocess.run(['ansible-playbook', '-i', ip, 
                        self.ansible_scripts['remove_user'],'--extra-vars', extra_vars],
                        stderr = sys.stderr, stdout = sys.stdout)
        
        
    def ansible_shut_down(self, ip):
        ip += ','
        subprocess.run(['ansible-playbook', '-i', ip, self.ansible_scripts['shutdown']],
                        stderr = sys.stderr, stdout = sys.stdout)
    
        
    def create_token(self, userid, tokenid):
        suburl = 'access/users/{userid}/token/{tokenid}'.format(userid=userid, tokenid=tokenid)
        params = {'privsep' : False}
        return self.post(suburl, params = params) 

    def migrate_vm(self, source_node, target_node, vmid):
        suburl = f'nodes/{source_node}/qemu/{vmid}/migrate'
        params = { 'target' : target_node }
        return self.post(suburl, params = params) 

            





    

    
