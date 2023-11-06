from os import get_terminal_size
from os import getpid
from requests.structures import CaseInsensitiveDict

import os
import psutil
import requests
import json
import socket
import netifaces as ni


nic_ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
ram = psutil.virtual_memory()

#print("=======================================")
#my_process = psutil.Process(getpid())
#print("Name:", my_process.name())
#print("PID:", my_process.pid)
#print("Executable:", my_process.exe())
#print("CPU%:", my_process.cpu_percent(interval=1))
#print("MEM%:", my_process.memory_percent())
#print("=======================================")
    
hostname=socket.gethostname()    
totalcup = psutil.cpu_count()
cpu_percent = psutil.cpu_percent(interval=0.5)  
 
####-- RAM Caltulation ---####
total = round(ram.total/(1024**3), 2)
available = round(ram.available/(1024**3), 2)
used = (total - available)
free = (total - used)
percent =  round(((total - available) / total * 100), 2)

####-- end ---####

location = ''

##print("**************************")

path = '/root/system-resource-viewer/iplocation.txt'
check_file = os.path.isfile(path)

if check_file:
    f = open(path, "r")
    location = f.read()
    if(len(location) == 0):
      c = requests.get(f'https://api.iplocation.net/?ip={nic_ip}')
      rs = c.json()
      f= open("iplocation.txt","w+")
      f.write(rs["country_name"])
      f.close()
      location = rs["country_name"]
else:
  c = requests.get(f'https://api.iplocation.net/?ip={nic_ip}')
  rs = c.json()
  f= open("iplocation.txt","w+")
  f.write(rs["country_name"])
  f.close()
  location = rs["country_name"]
  
  
#
#print("**************************")
#
url = "https://ops.copaccount.com/api/ServerList"

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"

data = {
  "serverName"   : hostname,
  "ipAddress"    : nic_ip,
  "countryName"  : location,
  "totalMemory"  : total,
  "memoryUsed"   : used,
  "memoryFree"   : free,
  "cpuUsed"      : cpu_percent
  }

resp = requests.post(url, headers=headers, data=json.dumps(data))

print(resp.status_code)
#print(total, used, free, percent, '|', cpu_percent, totalcup)
