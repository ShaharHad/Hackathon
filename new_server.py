import queue
import socket
import struct
import sys
import time
import scapy.all as scapy
from concurrent.futures import ThreadPoolExecutor as pool
import multiprocessing
import threading
import random
import select



udp_port = 13117
tcp_port = 13000
server_ip = scapy.get_if_addr("eth1")
encoded = "utf-8"
inputs = []
outputs = []
error = {}


def send_broadcast(udp_socket):
    msg = struct.pack("IbH", 2882395322, 2, tcp_port)
    udp_socket.sendto(msg, ("<broadcast>", udp_port))


def thread_broadcast(udp):
    threading.Timer(1, thread_broadcast, [udp]).start()
    send_broadcast(udp_socket)



if __name__ == "__main__":
    while True:
        # UDP
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        print(f"Server started, listening on IP address {server_ip}")
        sending = multiprocessing.Process(target=thread_broadcast, args=(udp_socket,))
        sending.start()

        #TCP
        tcp_socket_clients = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket_clients.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        tcp_socket_clients.bind(("", tcp_port))
        tcp_socket_clients.listen(2)
        inputs = [tcp_socket_clients]

        while input:
            readable, writeable, exceptional = select.select(inputs, outputs, inputs)
            for item in readable:
                if item in tcp_socket_clients:
                    tcp_socket, addr = tcp_socket_clients.accept()
                    # configre the socket to be nonblocking mode
                    tcp_socket.setblocking(0)
                    inputs.append(tcp_socket)
                    error[tcp_socket] = queue.Queue()
                else:
                    data = item.recv(1024)
                    if data:
                        error[s].put(data)
                        if s not in outputs:
                            outputs.append(s)
                    else:
                        if s in outputs:
                            outputs.remove(s)
                        inputs.remove(s)
                        s.close()
                        del error[s]

                    for s in writeable:
                        try:
                            next_msg = error[s].get_nowait()
                        except queue.Empty:
                            outputs.remove(s)
                        else:
                            s.send(next_msg)

                    for s in exceptional:
                        inputs.remove(s)
                        if s in outputs:
                            outputs.remove(s)
                        s.close()
                        del error[s]




