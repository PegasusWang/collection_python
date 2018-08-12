import socket
import time


def get(path):
    s = socket.socket()
    s.connect(('localhost', 5000))

    request = 'GET {} HTTP/1.0\r\n\r\n'.format(path)
    s.send(request.encode())

    chunks = []
    while True:
        chunk = s.recv(1000)
        if chunk:
            chunks.append(chunk)
        else:
            body = (b''.join(chunks)).decode()
            print(body)
            return


start = time.time()
get('/1')
get('/2')
print(time.time() - start)
