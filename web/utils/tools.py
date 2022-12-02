import requests
import random,psutil

def getNickName(uid):
    try:
        a = requests.get(f"https://v.api.aa1.cn/api/qqnicheng/?qq={uid}",timeout=1)
        return a.text[5:-10]
    except:
        return "未知"

def generate_random_str(randomlength=8):
  random_str =''
  base_str ='ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
  length =len(base_str) -1
  for i in range(randomlength):
    random_str +=base_str[random.randint(0, length)]
  return random_str

def getPidbyPort(port):
    net_con = psutil.net_connections()
    for con_info in net_con:
        if con_info.laddr.port == port:
            return con_info.pid
    return False

def getPidbyName(name):
    for proc in psutil.process_iter():
        if proc.name() == name:
            return proc.pid
    return False

def getVPSStatus():
    cpupersent = psutil.cpu_percent()
    vmempersent = psutil.virtual_memory().percent
    swappersent = psutil.swap_memory().percent
    return cpupersent,vmempersent,swappersent

def getNonebotStatus():
    pid = getPidbyPort(23345)
    if pid == False:
        return False
    nbtcpu = psutil.Process(pid).cpu_percent()
    nbtmem = psutil.Process(pid).memory_percent()
    return nbtcpu,nbtmem

def getCQHttpStatus():
    pid = getPidbyName("go-cqhttp")
    if pid == False:
        return False
    cqhcpu = psutil.Process(pid).cpu_percent()
    cqhmem = psutil.Process(pid).memory_percent()
    return cqhcpu,cqhmem