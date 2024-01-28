# GPU information
import GPUtil
import time 
import socket


server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 12000))

message, address = server_socket.recvfrom(1024)

while(1):
    gpu = GPUtil.getGPUs()[0]
    gpu_usage = round(gpu.load*100)
    gpu_mem_usage = round(gpu.memoryUtil*100)

    message = f'{gpu_usage} {gpu_mem_usage}'.encode()
    print(f'Sending GPU Usage and GPU Mem Usage. {gpu_usage} : {gpu_mem_usage}')
    server_socket.sendto(message, address)

    time.sleep(1)