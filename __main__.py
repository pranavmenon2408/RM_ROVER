from client import BluetoothClient

if __name__ == "__main__":
    client = BluetoothClient()

    @client.controller.listener
    def main() -> None:
        client.send(client.controller.joystick.direction)

    try:
        while True:
            main()
    except KeyboardInterrupt:
        client.disconnect()
        client.controller._joystick.quit()
        client.logger.flair("Client terminated")
