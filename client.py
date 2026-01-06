import socket
from utils import get_timestamp

# Konfiguracja połączenia
HOST = "localhost"  # lub "127.0.0.1"
PORT = 10001        # port, na którym działa Twój serwer

CLIENT_NAME = "TCP_Client-" + get_timestamp()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Tworzymy gniazdo TCP (IPv4, stream)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # 1. Połączenie z serwerem
    s.connect((HOST, PORT))
    print("Server:", (HOST, PORT), "- Client connected to server")

    # 2. Wysyłanie danych
    laddr = s.__str__().split("laddr=(")[1].split("raddr=(")[0]
    print("Server: ", (HOST, PORT), " - Client will send request to server (Client address: ", laddr[:-2], ".", sep="")
    request_msg = "Client message 123456789\n"
    s.sendall(request_msg.encode("utf-8"))
    print("Server: ", (HOST, PORT), " - Client just sent request to server (Message:", repr(request_msg), ").", sep="")

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