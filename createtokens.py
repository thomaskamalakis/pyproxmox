from proxmoxapi import api
import csv


CSV_FILE = 'tokens.csv'
CSV_FILE_OUT = 'tokensout.csv'

NODE = 'proxmoxedu2'

def get_list(filename = CSV_FILE):
    with open(filename,'r') as f:
        reader = csv.DictReader(f , delimiter = ';')
        l = list(reader)

    return l

def save_to_csv(l, filename = CSV_FILE_OUT):
    keys = l[0].keys()

    with open(filename, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys, delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(l)

l = get_list()

a = api()

for r in l:
    print(r)
    result = a.create_token(userid=r['userid'],tokenid=r['tokenid'])
    r['secret'] = result['value']
    r['full-tokenid'] = result['full-tokenid']

save_to_csv(l)


