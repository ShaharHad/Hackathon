import scapy
import socket
import struct


udp_port = 13117

while True:

    # create udp socket
    broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # listen to udp port 13117
    print("Client started, listening for offer requests...")
    broadcast.bind(("", udp_port))
    data, addr = broadcast.recvfrom(1024)
    msg = struct.unpack('!IbH', data) # change the format ????????????
    print(f"Received offer from {addr[0]}, attempting to connect...")
    #connect to server with TCP port



    # close port and return to listening
