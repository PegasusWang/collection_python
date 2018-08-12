
# Echo server program
import socket

HOST = '127.0.0.1'    # The remote host
PORT = 8888 # Arbitrary non-privileged port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        print('Connected by', addr)
        with conn:
            while 1:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)



"""
# Echo server program
import socket
HOST = '127.0.0.1'    # The remote host
PORT = 50007              # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
while 1:
    conn, addr = s.accept()
    print('Connected by', addr)
    while 1:
        data = conn.recv(1024)
        if not data:
            break
        conn.sendall(data)
    conn.close()
"""
