# client 获取 cpu 占用信息
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_addr = ('127.0.0.1', 8090)
s.sendto(b'CPU info', s_addr)
data_b, addr = s.recvfrom(1024)

if addr == s_addr:
    data_s = data_b.decode('utf-8')
    data_list = data_s.split('\n')
    print("Cpu usage rate is ", data_list[0])
    print('% - 20s % -5s % -10s' % ('name', 'pid', 'cpu usage'))
    data_list = data_list[1:-1]
    for xx in data_list:
        yy = xx.split(',')
        print('% - 20s % -5s % -10s' % (yy[0], yy[1], yy[2]))

s.close()
