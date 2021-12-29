import socket
import struct
import sys
import time
import scapy.all as scapy
from concurrent.futures import ThreadPoolExecutor as pool
import multiprocessing
import threading

udp_port = 13117
tcp_port = 13000
server_ip = scapy.get_if_addr("eth1")
encoded = "utf-8"


def start_game():
    pass
    # while (time.time()<10):

    #     try:

    #     except Exception as e:


def send_broadcast(udp_socket):
    msg = struct.pack("Ibh", 2882395322, 2, tcp_port)
    udp_socket.sendto(msg, ("<broadcast>", udp_port))
    # time.sleep(1)


def thread_broadcast(udp):
    threading.Timer(1, thread_broadcast, [udp]).start()
    send_broadcast(udp_socket)


# def send_broadcast(udp_socket):
#     msg = struct.pack("Ibh", 2882395322, 2, tcp_port)
#     udp_socket.sendto(msg, ("<broadcast>", udp_port))
#     time.sleep(1)


if __name__ == "__main__":
    # UDP
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    print(f"Server started, listening on IP address {server_ip}")
    # num_of_clients = 0
    # while num_of_clients < 2:
    #     send_broadcast(udp_socket)
    sending = multiprocessing.Process(target=thread_broadcast, args=(udp_socket,))
    sending.start()

    # TCP
    tcp_socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    tcp_socket_client.bind(("", tcp_port))
    tcp_socket_client.listen(2)
    tcp_socket_list = []
    # with pool(max_workers=2):
    print("here")
    while len(tcp_socket_list) < 2:
        (tcp_socket, addr) = tcp_socket_client.accept()
        group_name = tcp_socket.recv(1024).decode(encoded)
        tcp_socket_list.append((group_name, tcp_socket))
        print("************************")
        print(group_name)

        # (tcp_socket2, addr2) = tcp_socket_client.accept()
        # group_name2 = tcp_socket2.recv(1024).decode(encoded)
        # tcp_socket_list.append((group_name2, tcp_socket2))
        # print("************************")
        # print(group_name2)

    print(tcp_socket_list)










