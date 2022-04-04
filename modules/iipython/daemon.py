# Copyright 2022 iiPython

# Modules
import os
import random
import socket
from threading import Thread
from types import FunctionType
from tempfile import gettempdir
from .socket import Socket, Connection

# Daemon class
class Daemon(object):
    def __init__(self, name: str) -> None:
        self.lock_file = os.path.join(gettempdir(), f"{name}.lock")
        self.cli = os.path.isfile(self.lock_file)

        # Attribs
        self.handlers = {}
        self.main_handler = None

    def _listen(self, conn: Connection) -> None:
        while True:
            try:
                data = conn.recvjson()
                if not data:
                    break

                for msg in data:
                    if msg["emit"] in self.handlers:
                        self.handlers[msg["emit"]](msg["args"])

            except Exception:
                break

    def on(self, event: str) -> FunctionType:
        def cb(fn: FunctionType) -> None:
            self.handlers[event] = fn

        return cb

    def main(self) -> FunctionType:
        def cb(fn: FunctionType) -> None:
            self.main_handler = fn

        return cb

    def connect(self) -> None:
        with open(self.lock_file, "r") as lock:
            raw = lock.read()

        try:
            server_port = int(raw)

        except Exception:
            raise ValueError("Lock file does not contain a valid port!")

        # Connect to daemon
        self.conn = Socket()
        self.conn.connect(("0.0.0.0", server_port))
        if self.main_handler:
            self.main_handler()

    def emit(self, event: str, *args) -> None:
        if not hasattr(self, "conn"):
            raise RuntimeError("Not connected to an existing daemon process!")

        self.conn.sendjson({"emit": event, "args": args})

    def process(self) -> None:
        if os.path.isfile(self.lock_file):
            self.connect()

        else:
            self.start_server()

    def start_server(self) -> None:
        server_port = random.randint(2000, 60000)
        with open(self.lock_file, "w+") as lock:
            lock.write(str(server_port))

        self.srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srv.bind(("0.0.0.0", server_port))
        self.srv.listen(5)

        # Main loop
        try:
            while True:
                conn, addr = self.srv.accept()
                Thread(target = self._listen, args = [Connection(conn)]).start()

        except KeyboardInterrupt:
            os.remove(self.lock_file)

        except Exception as e:
            os.remove(self.lock_file)
            raise e
