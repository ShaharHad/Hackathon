import socket
import struct
import sys
import time
import scapy.all as scapy
from concurrent.futures import ThreadPoolExecutor as pool
import multiprocessing
import threading
import random

udp_port = 13117
tcp_port = 13000
server_ip = scapy.get_if_addr("eth1")
encoded = "utf-8"
clients_ans = []


def send_broadcast(udp_socket):
    msg = struct.pack("Ibh", 2882395322, 2, tcp_port)
    udp_socket.sendto(msg, ("<broadcast>", udp_port))
    # time.sleep(1)


def thread_broadcast(udp):
    threading.Timer(1, thread_broadcast, [udp]).start()
    send_broadcast(udp_socket)


def create_random_equation():
    operator_list = ["+", "-"]
    equation_numbers = random.randint(2, 4)
    eq = str(random.randint(1, 20))
    for i in range(1, equation_numbers):
        oper_index = random.randint(0, 1)
        print(f"oper_index: {oper_index}")
        eq += operator_list[oper_index]
        eq += str(random.randint(1, 10))
    return eq


# get item (group name, socket) from the socket list and update the client answer in the global list
def listening_to_client(item):
    global clients_ans
    num_from_client = item[1].recv(1024).decode(encoded)
    clients_ans.append((item[0], num_from_client))


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
    tcp_socket_clients = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket_clients.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    tcp_socket_clients.bind(("", tcp_port))
    tcp_socket_clients.listen(2)
    tcp_socket_list = []
    # with pool(max_workers=2):
    while len(tcp_socket_list) < 2:
        (tcp_socket, addr) = tcp_socket_clients.accept()
        group_name = tcp_socket.recv(1024).decode(encoded)
        tcp_socket_list.append((group_name, tcp_socket))
        print("************************")
        print(addr)

    udp_socket.close()
    # (tcp_socket2, addr2) = tcp_socket_clients.accept()
    # group_name2 = tcp_socket2.recv(1024).decode(encoded)
    # tcp_socket_list.append((group_name2, tcp_socket2))
    # print("************************")
    # print(group_name2)
    welcome_msg = f"Welcome to Quick Maths.\nPlayer 1: {tcp_socket_list[0][0]}Player 2: {tcp_socket_list[1][0]}==\nPlease answer the following question as fast as you can:\n"
    eq = create_random_equation()
    eq_ans = eval(eq)
    print(eq_ans)
    welcome_msg += eq
    print(welcome_msg)
    welcome_msg_bytes = bytes(welcome_msg, encoded)

    tcp_socket_list[0][1].send(welcome_msg_bytes)
    tcp_socket_list[1][1].send(welcome_msg_bytes)
    t_client1 = threading.Thread(target=listening_to_client, args=[tcp_socket_list[0]])
    t_client2 = threading.Thread(target=listening_to_client, args=[tcp_socket_list[1]])
    start_game_time = time.time()
    # without this sleep it will terminated
    time.sleep(0.5)
    t_client1.start()
    t_client2.start()

    while True:
        # without this sleep it will terminated
        time.sleep(0.2)
        if len(clients_ans) > 0 or time.time() - start_game_time > 10:
            break

    end_game_msg = f"Game over!\nThe correct answer was {eq_ans}!\n\n"

    if len(clients_ans) == 0:
        msg = "The game ended with a draw"
        print(msg)
    else:
        if int(clients_ans[0][1]) == eq_ans:
            winner = clients_ans[0][0]
        else:
            for item in tcp_socket_list:
                if item[0] != clients_ans[0][0]:
                    winner = item[0]
        print(f"the winnder team is: {winner}")
        msg = f"Congratulations to the winner: {winner}"
    end_game_msg += msg
    print(end_game_msg)

    # else:
    #     # need to implement it
    #     winner = check_ans(clients_ans, tcp_socket_list)
    #     msg = winner

    # num_from_client1 = tcp_socket_list[0][1].recv(1024).decode(encoded)
    # num_from_client2 = tcp_socket_list[1][1].recv(1024).decode(encoded)

    # print(f"client1 number is: {num_from_client1} and client2 number is: {num_from_client2}")

    # if eval == int(num_from_client1):
    #     print(f"{tcp_socket_list[0][0]} wins")
    # else:
    #     print(f"{tcp_socket_list[1][0]} wins")
