import socket
import struct
import sys
import time
import scapy.all as scapy


udp_port = 13117
tcp_port = 13000
server_ip = scapy.get_if_addr("eth1")

# send message from by UDP protocol with delay of 1 second
def send_broadcast(udp_socket):
    msg = struct.pack("Ibh", 2882395322, 2, tcp_port)
    udp_socket.sendto(msg, ("<broadcast>", udp_port))
    time.sleep(1)


if __name__ == "__main__":
    # create UDP port
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    print(f"Server started, listening on IP address {server_ip}")
    num_of_clients = 0
    while num_of_clients < 2:
        send_broadcast(udp_socket)




