import requests
import sys
import json
from tabulate import tabulate

# disable warnings from SSL/TLS certificates
requests.packages.urllib3.disable_warnings()

sdwan_url = 'https://10.10.20.90/j_security_check'
sdwan_credentials = {'j_username':'admin', 'j_password':'C1sco12345'}

session = requests.session()
response = session.post(url=sdwan_url, data=sdwan_credentials, verify=False)

if b'<html>' in response.content:
	print(f"Login Failed, {response.status_code}")
	exit(0)
else:
    print(f"Login Success, {response.status_code}")
    print("---")
    print("Getting Token")
    print("---")


token_url = 'https://10.10.20.90/dataservice/client/token'

token = session.get(url=token_url)
# print(token)

if token.status_code != 200:
    if b'<html>' in token_url.content:
        print(token_url)
        print ("Login Token Failed")
        exit(0)
else:
    print("Token Success")

token = token.text
headers = {'X-XSRF-TOKEN':token}
session.headers.update(headers)

print("Getting Attached Devices")

device_url = 'https://10.10.20.90/dataservice/device'

response = session.get(url=device_url, verify=False)
response = json.loads(response.content)

headers = ["Host Name", "Reachability", "Status", "Device IP", "Site-ID", "Host Type", "Version", "Certificate"]
table = list()


for device in response['data']:
    # print(response)
    info = [device['host-name'], device['reachability'], device['status'], device['deviceId'], 
    device['site-id'], device['device-model'], device['version'], device['certificate-validity']]
    table.append(info)

print(tabulate(table, headers, tablefmt="fancy_grid"))

