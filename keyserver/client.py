import socket
import struct

from keyserver.settings import BUFFER_SIZE, STRUCT_FORMAT,\
    TCP_PORT, TCP_IP, SERVER_TYPE, UDP_IP, UDP_PORT


def run_udp(ip=UDP_IP, port=UDP_PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        message = "C"
        sock.sendto(message, (ip, port))
        data, addr = sock.recvfrom(BUFFER_SIZE)
        key = struct.unpack(STRUCT_FORMAT, data)[0]
        if key % 10000 == 0:
            print('received: {}'.format(key))


def run_tcp(ip=TCP_IP, port=TCP_PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    s.connect((ip, port))
    while True:
        s.send('C')
        data = s.recv(BUFFER_SIZE)
    s.close()


if __name__ == "__main__":
    if SERVER_TYPE == 'udp':
        run_udp(UDP_IP, UDP_PORT)
    else:
        run_tcp(TCP_IP, TCP_PORT)
