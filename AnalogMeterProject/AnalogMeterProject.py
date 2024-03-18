from tkinter import ROUND
import GPUtil
import time 
import socket
import psutil
import json

#SETTINGS
#Internet speed in MB/s
NETWORK_MAX_DOWNLOAD = 5
NETWORK_MAX_UPLOAD = 5
_last_net_io_meta = None

def net_io_usage():
    global _last_net_io_meta

    net_counters = psutil.net_io_counters()
    tst = time.time()

    send_bytes = net_counters.bytes_sent
    recv_bytes = net_counters.bytes_recv
    err_in = net_counters.errin
    err_out = net_counters.errout
    
    if _last_net_io_meta is None:
        _last_net_io_meta = (send_bytes, recv_bytes, tst)
        return [0,0,0,0]

    last_send_bytes, last_recv_bytes, last_time = _last_net_io_meta
    delta_time = tst - last_time
    recv_speed = (recv_bytes - last_recv_bytes) / delta_time
    send_speed = (send_bytes - last_send_bytes) / delta_time

    _last_net_io_meta = (send_bytes, recv_bytes, tst)
    return [recv_speed, send_speed, err_in, err_out]

def Fetch_Net_Usage(): 
    net_stat = net_io_usage()
    net_in_1 = net_stat[0]
    net_out_1 = net_stat[1]
    net_in_error = net_out_error = net_in_percent = net_out_percent = 0
    
    #round to MB/s with 0 decimals
    net_in = round((net_in_1) / 1024 / 1024)
    net_out = round((net_out_1) / 1024 / 1024)

    #convert to a percentage based on the users internet package
    if(net_in != 0):    
        net_in_percent = Percent_Safety_Check(round((net_in / NETWORK_MAX_DOWNLOAD) * 100))
    if(net_out != 0):    
        net_out_percent = Percent_Safety_Check(round((net_out / NETWORK_MAX_UPLOAD) * 100))
    if(net_stat[2] > 0):
        net_in_error = 100
    if(net_stat[3] > 0):
        net_out_error = 100
        
    return [ net_in_percent, net_in_error, net_out_percent, net_out_error]

def Percent_Safety_Check(percent):
    if(percent > 100):
        return 100
    else:
        return percent

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 12000))

while(1):
    message, address = server_socket.recvfrom(1024)
    Gpus = GPUtil.getGPUs()
    CpuCores = psutil.cpu_percent(interval=1, percpu=True) 
    MemSwap = psutil.swap_memory()

    systemStatJson = {
        "Data":[], 
    }

    #FETCH CPU CORE STATS AND ADD TO JSON
    print("CPU Data")
    for cpu in range(0, int(len(CpuCores)/2)):
        #we dont have enough meters to display all threads. Lets do some averages and merge
        roundedCoreUtil = round((CpuCores[cpu*2] + CpuCores[cpu*2+1])/2)
        print(roundedCoreUtil)
        systemStatJson["Data"].append(roundedCoreUtil)

    #FETCH GPU STATS AND ADD TO JSON
    print("GPU Data")
    for gpu in Gpus:
        load = round(gpu.load*100)
        memoryUtil = round(gpu.memoryUtil*100)
        print(load)
        print(memoryUtil)
        systemStatJson["Data"].append(load)
        systemStatJson["Data"].append(memoryUtil)

    #FETCH MEMORY UTIL AND ADD TO JSON
    print("Memory Data")
    memPercentUsage = round(psutil.virtual_memory()[2])
    memSwap = round(MemSwap.percent)
    print(memPercentUsage)
    print(memSwap)
    systemStatJson["Data"].append(memPercentUsage)
    systemStatJson["Data"].append(memSwap)

    #FETCH DISK STATS AND ADD TO JSON
    print("Storage Data")
    for part in psutil.disk_partitions(all=False):
        usage = psutil.disk_usage(part.mountpoint)
        roundedUsage = round(usage.percent)
        print(roundedUsage)
        systemStatJson["Data"].append(roundedUsage)
        
    #FETCH NETWORK STATS AND ADD TO JSON
    print("Network Data")
    networkUsage = Fetch_Net_Usage()
    for networkStat in networkUsage:
        print(networkStat)
        systemStatJson["Data"].append(networkStat)

    #ENCODE JSON AND SEND TO CLIENT
    message = json.dumps(systemStatJson, indent=4)
    server_socket.sendto(message.encode(), address)
    print(systemStatJson)
    