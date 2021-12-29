import scapy
import socket
import struct
import getch
import socket
import time

group_name = "Pytonic"
udp_port = 13117
encoded = "utf-8"
a


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
        time.sleep(0.2)
        # UDP
        udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp_client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_client.bind(("", udp_port))
        print("Client started, listening for offer requests...")
        while True:
            server_address = get_broadcast_message(udp_client)
            print(int(server_address[1]))
            if int(server_address[1]) == 13000:  # and int(server_address[1]) == 13000:
                break

        # udp_client.close()
        print(server_address)

        # TCP
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            tcp_socket.connect(server_address)
        except Exception as e:
            print(e)
            exit(2)
        group_name_bytes = bytes(group_name + "\n", encoded)
        tcp_socket.sendall(group_name_bytes)
        print(tcp_socket.recv(1024).decode(encoded))
        key_num = getch.getch()
        tcp_socket.send(bytes(key_num, encoded))
        print(tcp_socket.recv(1024).decode(encoded))
        print(tcp_socket.recv(1024).decode(encoded))
        tcp_socket.close()
