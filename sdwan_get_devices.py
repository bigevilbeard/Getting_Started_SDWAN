#Example Only
import json

device_url = 'https://10.10.20.90/dataservice/device'

response = session.get(url=device_url, verify=False)
response = json.loads(response.content)

for device in response['data']:
    print(device['host-name'], device['local-system-ip'], device['uuid'])