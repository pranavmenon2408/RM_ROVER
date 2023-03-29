import time

from client import BluetoothClient

if __name__ == "__main__":
    client = BluetoothClient()

    @client.controller.listener
    def main() -> None:
        client.send(
            s
            if 0 not in (s := client.controller.control_pad.motor_speed)
            else client.controller.joystick.motor_speed
        )
        time.sleep(0.1)

    try:
        while True:
            main()
    except KeyboardInterrupt:
        client.disconnect()
        client.controller._joystick.quit()
        client.logger.flair("Client terminated")
