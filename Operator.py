import socket
import sys

TCP_IP = '127.0.0.1'
TCP_PORT = int(sys.argv[1])
occupancy = int(sys.argv[2])
num_elements = int(sys.argv[3])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    conn, addr = s.accept()
    f = conn.makefile(buffering=1, encoding="utf-8")
    
    check1, check2 = False, False
    
    l = f.readline()
    message_type, message = l[:-1].split(":")
    
    if message_type == "GETOCC":
        conn.sendall( ("OCC:%d\n" % occupancy).encode("utf-8") )
        
        for l in f:
            message_type, message = l[:-1].split(":")
                
            if message_type == "DATA":
                data = message.split(",")
                
                if len(data) > num_elements + 5:
                    print("1")
                elif len(data) < num_elements - 5:
                    print("2")
                
                check1 = True
            
            elif message_type == "FUNCS":
                func = message
                check2 = True
                
            elif message_type == "END":
                break
                
            if check1 and check2:            
                output = []
                for i in range(len(data)):
                    cur_number = int(data[i])
                    
                    if func == "f1":
                        cur_number = cur_number * 17
                    elif func == "f2":
                        cur_number = cur_number ** 2
                    elif func == "f3":
                        cur_number = cur_number + 53
                        
                    output.append(cur_number)
                
                output = ",".join(map(str, output)) 
                output = ("DATA:" + output + "\n").encode("utf-8")
                conn.sendall(output)
                
                check1, check2 = False, False
except Exception as e:
    print(e)
    
finally:
    s.close()