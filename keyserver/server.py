import socket
import struct
import threading

from keyserver.settings import BUFFER_SIZE, STRUCT_FORMAT,\
    TCP_PORT, TCP_IP, SERVER_TYPE, UDP_IP, UDP_PORT


key = 0


def run_udp(ip=UDP_IP, port=UDP_PORT):
    global key
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))

    while True:
        data, addr = sock.recvfrom(1)
        sock.sendto(struct.pack(STRUCT_FORMAT, key), addr)
        key += 1
        if key % 10000 == 0:
            print('generated: {}'.format(key))


def run_tcp(ip=TCP_IP, port=TCP_PORT):
    global key

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip, port))
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    s.listen(1)

    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=run_tcp_handle_client, args=(addr, conn,))
        t.start()
    s.close()


def run_tcp_handle_client(addr, conn):
    global key
    print('Connection address: {}'.format(addr))
    while 1:
        data = conn.recv(1)
        if not data:
            break
        conn.send(struct.pack(STRUCT_FORMAT, key))
        key += 1
        if key % 10000 == 0:
            print('generated: {}'.format(key))
    conn.close()


if __name__ == "__main__":
    if SERVER_TYPE == 'udp':
        run_udp(UDP_IP, UDP_PORT)
    else:
        run_tcp(TCP_IP, TCP_PORT)
    print('Generated {} keys'.format(key))
