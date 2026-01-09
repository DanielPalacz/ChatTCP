import socket
from utils import get_timestamp
from sys import argv
from time import sleep

# Konfiguracja połączenia
HOST = "localhost"  # lub "127.0.0.1"
PORT = 10001        # port, na którym działa Twój serwer
CLIENT_NAME = "TCP_Client-" + get_timestamp()


if len(argv) == 2:
    sleep_time = int(argv[1])
else:
    sleep_time = 0

print("Running client: ", CLIENT_NAME, " which will connect to: ", f"{HOST}:{PORT}. Sleep time: ", sleep_time, ".\n", sep="")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Tworzymy gniazdo TCP (IPv4, stream)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # 1. Połączenie z serwerem
    s.connect((HOST, PORT))
    print("Server:", (HOST, PORT), "- Client connected to server")
    sleep(sleep_time)

    # 2. Wysyłanie danych
    laddr = s.__str__().split("laddr=(")[1].split("raddr=(")[0]
    print("Server: ", (HOST, PORT), " - Client will send request to server (Client address: ", laddr[:-2], ".", sep="")
    request_msg = "boom\n"
    s.sendall(request_msg.encode("utf-8"))
    print("Server: ", (HOST, PORT), " - Client just sent request to server (Message:", repr(request_msg), ").", sep="")

    # [Test] - Send message and close socket immediately.
    import os
    os._exit(0)

    # 3. Socket kliencki sygnalizuje: "nie będę już nic wysyłał"
    #  - bez tego Deadlock:
    s.shutdown(socket.SHUT_WR)

    # 4. Odbiór odpowiedzi z serwera.
    response = b""
    while True:
        # print("Server: ", (HOST, PORT), "- Client may receive data from server.")
        data = s.recv(1024)
        if not data:
            print("Server:", (HOST, PORT), "- Client stopped to receive data from server. Closing connection.")
            break
        response += data
        print("Server:", (HOST, PORT), "- Client received data from server:", str(response))


print(" - Full server response:", repr(response.decode("utf-8")))