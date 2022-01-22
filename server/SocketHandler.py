from socket import *
import threading
import datetime

class Client:
    def __init__(self, name: str, connection: tuple) -> None:
        self.name = name
        self._connection,self._addred = connection


class Socket_handler:

    def __init__(self, client: Client) -> None:
        self._client = client
        self._in, self._address = client._connection,client._addred

    def __call__(self) -> None:
        while True:
            print("Hello")
            serverTimeNow = "%s" % datetime.datetime.now()

            self._in.send(serverTimeNow.encode())

            print("Sent %s to %s" % (serverTimeNow, self._address))
            x = self._in.recvfrom(1024)
            ip = x[1][0]
            data = x[0].decode()
            print(ip, " : ", data)

    def __del__(self):
        print("Socket destroyed")
