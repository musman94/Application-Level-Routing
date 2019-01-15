import socket
import sys

TCP_IP = '127.0.0.1'
TCP_PORT = int(sys.argv[2])
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
argument = sys.argv[1]

#print('Connection address:', addr)
while 1:
    conn, addr = s.accept()

    data = conn.recv(BUFFER_SIZE)
    data = data.decode().split("DATA:")[1]
    data = int(data)
    print data
    if(argument == "A"):
        data = data * 17
    elif(argument == "B"):
        data = data + 13
    elif(argument == "C"):
        data = data * 11
    elif(argument == "D"):
        data = data - 7
    elif(argument == "E"):
        data = data * 13

    print("operated " + str(data))
    data = ("DATA:" + str(data)+"\n").encode()
    conn.send(data)