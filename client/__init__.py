import socket

from .controller import Controller
from .environment import config
from .logger import Logger

__all__: tuple[str, ...] = ("BluetoothClient",)
PROTOCOL: int = socket.BTPROTO_RFCOMM  # type: ignore


class BluetoothClient:
    connected: bool = False

    def __init__(self) -> None:
        self.sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, PROTOCOL)
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

    def send(self, data: str) -> None:
        if not self.connected:
            self._connect()
        self.sock.send(data.encode())
        self.logger.flair(f"Sent data: {data}")
