from tkinter import ROUND
import GPUtil
import time 
import socket
import psutil
import json

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 12000))

while(1):
    message, address = server_socket.recvfrom(1024)
    Gpus = GPUtil.getGPUs()
    CpuCores = psutil.cpu_percent(interval=1, percpu=True) 
    MemSwap = psutil.swap_memory()

    systemStatJson = {
        "Cpu":[],
        "Gpu":[],
        "Mem":[],
        "Storage":[]
    }

    #FETCH CPU CORE STATS AND ADD TO JSON
    for cpu in CpuCores:
        roundedCoreUtil = round(cpu)
        systemStatJson["Cpu"].append(roundedCoreUtil)

    #FETCH GPU STATS AND ADD TO JSON
    for gpu in Gpus:
        gpu_info = {
            "Gpu_Usage": round(gpu.load*100),
            "Gpu_Mem_Usage": round(gpu.memoryUtil*100)
        }
        systemStatJson["Gpu"].append(gpu_info)

    #FETCH MEMORY UTIL AND ADD TO JSON
    mem_info = {
        "Mem_Percent_Usage": round(psutil.virtual_memory()[2]),
        "Mem_Swap": round(MemSwap.percent)
    }
    systemStatJson["Mem"].append(mem_info)

    #FETCH DISK STATS AND ADD TO JSON
    for part in psutil.disk_partitions(all=False):
        usage = psutil.disk_usage(part.mountpoint)
        systemStatJson["Storage"].append(round(usage.percent))

    #ENCODE JSON AND SEND TO CLIENT
    message = json.dumps(systemStatJson, indent=4)
    server_socket.sendto(message.encode(), address)
    print(systemStatJson)

    time.sleep(.1)