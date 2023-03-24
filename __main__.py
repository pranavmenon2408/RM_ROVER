from client import BluetoothClient

if __name__ == "__main__":
    """
    from client.controller import Controller

    controller = Controller()


    @controller.listener
    def main() -> None:
        print(f"DIRECTION: {controller.joystick.direction} | SPEED: {controller.joystick.speed}")


    while True:
        main()
    """
    client = BluetoothClient()

    @client.controller.listener
    def main() -> None:
        client.send(
            f"DIRECTION: {client.controller.joystick.direction} | SPEED: {client.controller.joystick.speed}"
        )

    try:
        while True:
            main()
    except KeyboardInterrupt:
        client.disconnect()
        client.controller._joystick.quit()
        client.logger.flair("Client terminated")
