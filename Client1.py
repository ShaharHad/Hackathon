import scapy
import socket
import struct
import getch
import socket

group_name = "Pytonic"
udp_port = 13117



# listening to broadcast port and return the TCP port in the message
def get_broadcast_message(udp_client):
    tcp_port = -1
    # udp_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        data, addr = udp_client.recvfrom(1024)
        msg = struct.unpack('Ibh', data)
    except:
        return tcp_port
    # IP of the server
    ip_host = addr[0]
    tcp_port = msg[2]
    print(f"Received offer from {ip_host}, attempting to connect...")
    return tcp_port



if __name__ == "__main__":
    # create UDP port
    udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp_client.bind(("", udp_port))
    print("Client started, listening for offer requests...")
    while True:
        tcp_port = get_broadcast_message(udp_client)
        if tcp_port < 1024:
            continue
        print(tcp_port)
        # udp_client.close()