import socket
import typing as t

from .controller import Controller
from .environment import config
from .logger import Logger

__all__: tuple[str, ...] = ("BluetoothClient",)


class BluetoothClient:
    connected: bool = False

    def __init__(self) -> None:
        self.sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)  # type: ignore
        self.logger = Logger(name="client", file=False)
        self._connect()
        self.controller = Controller()
        self.logger.info("Client initialized")

    def _connect(self) -> None:
        try:
            self.sock.connect((config.MAC_ADDRESS, config.PORT))
            self.logger.flair("Connected to server")
            self.connected = True
        except socket.error as e:
            self.logger.error(f"Failed to connect to server: {e}")

    def disconnect(self) -> None:
        self.sock.close()
        self.logger.flair("Disconnected from server")
        self.connected = False

    def send(self, data: t.Any) -> None:
        if not self.connected:
            self._connect()
        self.sock.send(bytes(data, "utf-8"))
        self.logger.flair(f"Sent data: {data}")
