import socket
import os
import subprocess
import sys
import random

print("CS421 testing program, FALL 2018 BILKENT UNIVERSITY")

port1 = "10000"
port2 = "10001"
port3 = "10002"
port4 = "10003"
port5 = "10004"

if(len(sys.argv) == 7):
    port1 = sys.argv[2]
    port2 = sys.argv[3]
    port3 = sys.argv[4]
    port4 = sys.argv[5]
    port5 = sys.argv[6]

p = subprocess.Popen([sys.executable, 'Junction.py'], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

p2 = subprocess.Popen([sys.executable, 'Operator.py', "A", port1], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
p3 = subprocess.Popen([sys.executable, 'Operator.py', "B", port2], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
p4 = subprocess.Popen([sys.executable, 'Operator.py', "C", port3], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
p5 = subprocess.Popen([sys.executable, 'Operator.py', "D", port4], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
p5 = subprocess.Popen([sys.executable, 'Operator.py', "E", port5], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)


addr = sys.argv[1]

addr,port = addr.split(':')

port = int(port)
print(addr, port)
TCP_IP = addr
TCP_PORT = port

BUFFER_SIZE = 1024

number = random.randint(1,50)

number_data = f'{number:08}'
print(number_data)

MESSAGE = "DATA:"+number_data+" OPS:A,B,A,D,D,C,E\n" #DATA:0000OPS:ABCDEF...

MESSAGE = MESSAGE.encode()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
print(data.decode())

s.close()

data = data.decode().split("DATA:")[1]
print("received data:", data)
print("expected data:", ((number*17+13)*17-7-7)*11*13)
