import socket # socketserver
import sys
import threading

from utils import configure_logger
from utils import get_timestamp



class TcpServer:
    # LOGGER = LogProvider()

    HOST = "localhost"  # lub "127.0.0.1"
    PORT = 10001        # port, na którym działa Twój serwer
                        # SERVER_ADDRESS = (HOST, PORT)

    def __init__(self):
        self._server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_name = "TcpServer-" + get_timestamp()
        self._logger = configure_logger(self._server_name)

    # @property
    # def server_sock(self):
    #     return self._server_sock

    @property
    def logger(self):
        return self._logger


    def configure(self) -> None:
        """ Configures/initiates TcpServer

        Returns:
            None
        """
        self.logger.info(f"[TcpServer][configure] Configure TcpServer: binding Server Socket to address: %s",
                        f"({self.HOST}, {self.PORT})")
        self._server_sock.bind((self.HOST, self.PORT))
        self.logger.info("[TcpServer][configure] Configure TcpServer: setting Server Socket to 'listening' state.")
        self._server_sock.listen() # become a server sock

    def handle_connection(self, c_socket, c_address) -> None:
        """ Handle connection

        Returns:
            None
        """
        t_name = threading.current_thread().name
        c_host = c_address[0]
        c_port = c_address[1]
        self.logger.info("[TcpServer][%s] - start handling connection (Client: %s:%s).",
                         t_name, c_host, c_port)

        with c_socket:
            buffer = b""

            try:
                while True:
                    data = c_socket.recv(1024)
                    if data == b"":
                        self.logger.info("[TcpServer][%s] - data sending ended (Client: %s:%s).",
                                         t_name, c_host, c_port)
                        break

                    buffer += data
                    b_delimiter = b"\n"
                    while b_delimiter in buffer:
                        line, buffer = buffer.split(b"\n", 1)
                        message = line.decode("utf-8")
                        self.logger.info("[TcpServer][%s] - server received data from client (%s bytes).",
                                     t_name, sys.getsizeof(data))

                        c_socket.sendall(f"echo: {message}\n".encode("utf-8"))

            except ConnectionResetError:
                self.logger.warning(
                    "[TcpServer][%s] client %s:%s reset connection (ConnectionResetError)",
                    t_name, c_host, c_port
                )

            except BrokenPipeError:
                self.logger.warning(
                    "[TcpServer][%s] broken pipe when sending to client %s:%s",
                    t_name, c_host, c_port
                )

            except Exception as e:
                self.logger.exception("[TcpServer][%s] unexpected error: %r",t_name, e)



        self.logger.debug("[TcpServer][%s] - handle_connection is ending (Client: %s:%s).",t_name, c_host, c_port)


    def run_server(self):
        self.configure()
        print(f"TcpServer waits for connections. Listening on {self.HOST}:{self.PORT}.")

        while True:

            self.logger.debug("[TcpServer][run_server while loop] waits for connection from outside client.")
            (client_socket, s_address) = self._server_sock.accept()

            self.logger.debug("[TcpServer][run_server while loop] accepts new connection from outside client "
                             "(Address of the client: %s; New socket representing the connection: %s).",
                              s_address, client_socket)

            client_socket.settimeout(5)
            # client_socket.settimeout(50)

            t = threading.Thread(target=self.handle_connection, args=(client_socket, s_address))
            t.start()


if __name__ == "__main__":
    TcpServer().run_server()
