import time

from client import BluetoothClient

if __name__ == "__main__":
    client = BluetoothClient()

    @client.controller.listener
    def main() -> None:
        client.send(client.controller.joystick.direction)
        time.sleep(0.01)
    try:
        while True:
            main()
    except KeyboardInterrupt:
        client.disconnect()
        client.controller._joystick.quit()
        client.logger.flair("Client terminated")
