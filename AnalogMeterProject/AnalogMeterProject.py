import GPUtil
import time 
import socket
import psutil
import json

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 12000))

message, address = server_socket.recvfrom(1024)

while(1):
    Gpus = GPUtil.getGPUs()
    CpuCores = psutil.cpu_percent(interval=1, percpu=True) 

    systemStatJson = {
        "CpuStat":[],
        "GpuStat":[],
        "MemStat":[]
    }

    #FETCH CPU CORE STATS AND ADD TO JSON
    print('CPU Stats:')
    for cpu in CpuCores:
        roundedCoreUtil = round(cpu)
        systemStatJson["CpuStat"].append(roundedCoreUtil)

    #FETCH GPU STATS AND ADD TO JSON
    for gpu in Gpus:
        gpu_info = {
            "Gpu_Usage": round(gpu.load*100),
            "Gpu_Mem_Usage": round(gpu.memoryUtil*100)
        }
        systemStatJson["GpuStat"].append(gpu_info)

    #FETCH MEMORY UTIL AND ADD TO JSON
    roundedMemPercentUsage = round(psutil.virtual_memory()[2])
    systemStatJson["MemStat"].append(roundedMemPercentUsage)


    message = json.dumps(systemStatJson, indent=4)
    server_socket.sendto(message.encode(), address)
    print(systemStatJson)

    time.sleep(10)