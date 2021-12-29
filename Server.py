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
# server_ip = scapy.get_if_addr("eth1")
server_ip = scapy.get_if_addr("eth2")
print(server_ip)
encoded = "utf-8"
clients_ans = []



def send_broadcast(udp_socket):
    msg = struct.pack("IbH", 2882395322, 2, tcp_port)
    udp_socket.sendto(msg, ("<broadcast>", udp_port))
    # time.sleep(1)


def thread_broadcast(udp):
    threading.Timer(1, thread_broadcast, [udp]).start()
    send_broadcast(udp_socket)


def create_random_equation():
    operator_list = ["+", "-"]
    # equation_numbers = random.randint(2,4)
    equation_numbers = 2
    eq = str(random.randint(0, 4))
    for i in range(1, equation_numbers):
        eq += "+" + str(random.randint(0, 4))
    return eq


# get item (group name, socket) from the socket list and update the client answer in the global list
def listening_to_client(item):
    global clients_ans
    time.sleep(0.2)
    num_from_client = item[1].recv(1024).decode(encoded)
    clients_ans.append((item[0], num_from_client))

# send end game message to the client in the end of the game
def send_end_game_msg(socket, msg):
    byte_msg = bytes(msg, encoded)
    socket.sendall(byte_msg)


# close all tcp clients
def closed_clients_sockets(tcp_socket_list):
    global clients_ans
    for item in tcp_socket_list:
        item[1].close()
    clients_ans = []


if __name__ == "__main__":
    # UDP
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    print(f"Server started, listening on IP address {server_ip}")
    sending = multiprocessing.Process(target=thread_broadcast, args=(udp_socket,))
    sending.start()

    # TCP
    tcp_socket_clients = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket_clients.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    tcp_socket_clients.bind(("", tcp_port))
    tcp_socket_clients.listen(2)
    while True:
        tcp_socket_list = []
        while len(tcp_socket_list) < 2:
            (tcp_socket, addr) = tcp_socket_clients.accept()
            group_name = tcp_socket.recv(1024).decode(encoded)
            tcp_socket_list.append((group_name, tcp_socket))
        udp_socket.close()
        welcome_msg = f"Welcome to Quick Maths.\nPlayer 1: {tcp_socket_list[0][0]}Player 2: {tcp_socket_list[1][0]}==\nPlease answer the following question as fast as you can:\n"
        eq = create_random_equation()
        eq_ans = eval(eq)
        welcome_msg += eq
        print(welcome_msg)
        welcome_msg_bytes = bytes(welcome_msg, encoded)
        # send walcome message to the clients
        tcp_socket_list[0][1].send(welcome_msg_bytes)
        tcp_socket_list[1][1].send(welcome_msg_bytes)
        t_client1 = threading.Thread(target=listening_to_client, args=[tcp_socket_list[0]])
        t_client2 = threading.Thread(target=listening_to_client, args=[tcp_socket_list[1]])
        start_game_time = time.time()
        while True:
            print(clients_ans)
            # without this sleep it will terminated
            time.sleep(0.2)
            if len(clients_ans) > 0 or time.time() - start_game_time > 10:
                break
            try:
                t_client1.start()
                t_client2.start()
            except Exception as e:
                pass
        end_game_msg = f"Game over!\nThe correct answer was {eq_ans}!\n\n"
        print(clients_ans)
        if len(clients_ans) == 0:
            msg = "The game ended with a draw"
            print(msg)
        else:
            winner = ""
            if clients_ans[0][1] == str(eq_ans):
                winner = clients_ans[0][0]
            else:
                for item in tcp_socket_list:
                    if item[0] != clients_ans[0][0]:
                        winner = item[0]
            print(f"the winnder team is: {winner}")
            msg = f"Congratulations to the winner: {winner}"
        end_game_msg += msg
        print(end_game_msg)
        for (group_name, client) in tcp_socket_list:
            try:
                client.send(bytes(end_game_msg, encoded))
                client.close()
            except Exception as e:
                print(e)
        sending = multiprocessing.Process(target=thread_broadcast, args=(udp_socket,))
        sending.start()
        print(f"Game over, sending out offer requests...")
        time.sleep(0.5)
