import scapy
import socket
import struct
import getch
import socket
import time

group_name = "Pytonic1"
udp_port = 13117
encoded = "utf-8"


# UDP process
def get_broadcast_message(udp_client):
    # tcp_port = -1
    # udp_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        data, addr = udp_client.recvfrom(1024)
        msg = struct.unpack('IbH', data)
    except Exception as e:
        # print(e)
        return (-1, -1)
    server_ip = addr[0]
    tcp_port = msg[2]
    print(f"Received offer from {server_ip}, attempting to connect...")
    # print(f"port number {tcp_port}")
    return (server_ip, tcp_port)


if __name__ == "__main__":
    while True:
        # UDP
        udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        udp_client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_client.bind(("", udp_port))
        print("Client started, listening for offer requests...")
        while True:
            server_address = get_broadcast_message(udp_client)
            print(int(server_address[1]))
            if int(server_address[1]) > 1024 and int(server_address[1]) != 13000:
                break

        #    print(server_address)

        # TCP
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            tcp_socket.connect(server_address)
        except Exception as e:
            print(e)
            udp_client.close()
            continue
        udp_client.close()
        # send the group name to server
        group_name_bytes = bytes(group_name + "\n", encoded)
        tcp_socket.sendall(group_name_bytes)
        print(tcp_socket.recv(1024).decode(encoded))
        # get a key input
        key_num = getch.getch()
        tcp_socket.sendall(bytes(key_num, encoded))
        # tcp_socket.settimeout(0.01)
        print(tcp_socket.recv(1024).decode(encoded))
        print(tcp_socket.recv(1024).decode(encoded))

        tcp_socket.close()

# udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# udp_client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# udp_client.bind(("", udp_port))
# # udp_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# print("Client started, listening for offer requests...")
# data, addr = udp_client.recvfrom(1024)
# msg = struct.unpack('Ibh', data)
# ip_host = addr[0]
# tcp_port = msg[2]
# print(f"address: {addr}")
# print(f"tcp_port: {tcp_port}")
# print(f"Received offer from {ip_host}, attempting to connect...")
# udp_client.close()