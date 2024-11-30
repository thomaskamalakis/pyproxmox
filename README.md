# pyproxmox
This repo shows an example of using the Proxmox API to automate VM creation. It is used in the postgraduate course "Cloud Infrastructures" of the MSc program of the Department of Informatics and Telematics of Harokopio University of Athens.

### Initialization
You start by cloning the repo:
```
git clone https://github.com/thomaskamalakis/pyproxmox
```
You need to create a virtual environment and install the required Python modules from `requirements.txt`. This can be done using the `venv` module
```
cd pyproxmox
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
### Create an API key
To use pyproxmox you need to create an API key in your Proxmox environment. Go to Datacenter>Permissions>API Tokens and Click 'Add'

![image](https://github.com/user-attachments/assets/66a480e7-2c1a-4cbd-a873-42248063bf26)

Create an API token unchecking 'Privilege Separation' textbox and copy/paste it in a text editor (you will not be able to see its value again!). 

### Using pyproxmox
To use the `pyproxmox` you need to create the default values in `defaults.txt`
```
cp defaults.txt.example defaults.txt
```
You can edit the `defaults.txt` in order to reflect your Proxmox enviroment. In the file make sure to replace the `secret` parameter value with the API key you created earlier and update the proxmox API endpoint in the `url` parameter. You can test your connectivity in a Python shell using something like:
```
>>> import proxmoxapi as papi
>>> a = papi.api()
>>> a.get_version()
```
If all works correctly you should see the version of your Proxmox environment!

### An example use case
The `createmulvm.py` is an example where a number of VMs are created and assigned to users. Use the `users.csv` file to assign each VM to a new or existing user (if the user does not exist, it will be created). Make sure to include the realm after the username, e.g. `myuser@MYREALM` refers to a user with username `myuser` at realm `MYREALM`

In the script code you need to set the `CSV_FILE` to the name of the `csv` file containing the VM/user assignments, the `VM_TEMPLATE` to the ID of the template VM and the `NODE` to the name of the proxmox node where the cloning will take place.






