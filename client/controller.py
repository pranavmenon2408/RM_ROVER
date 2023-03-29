import typing as t

import pygame

from .models import ControlPad, DirectionsMixin, JoyStick

__all__: tuple[str, ...] = ("Controller",)
CallbackT = t.Callable[..., t.Any]


class Controller:
    def __new__(cls, *args: t.Any, **kwargs: t.Any) -> "Controller":
        pygame.init()
        pygame.joystick.init()
        return super().__new__(cls, *args, **kwargs)

    def __init__(self, index: int = 0) -> None:
        self._joystick = pygame.joystick.Joystick(index)
        self._joystick.init()
        self._joystick.rumble(0.5, 1000, 1000)
        self.joystick = JoyStick(0.0, 0.0)
        self.control_pad = ControlPad(direction=DirectionsMixin.STOP, speed_factor=1.0)

    def listener(self, func: CallbackT) -> CallbackT:
        def wrapper(*args: t.Any, **kwargs: t.Any) -> t.Any:
            self.listen()
            return func(*args, **kwargs)

        return wrapper

    def listen(self) -> None:
        joystick_events = pygame.event.get(pygame.JOYAXISMOTION)
        if joystick_events:
            self.joystick.update(
                x_axis=self._joystick.get_axis(0), y_axis=self._joystick.get_axis(1)
            )
        l_1, r_1 = self._joystick.get_button(9), self._joystick.get_button(10)
        if l_1 or r_1:
            speed_factor = (
                min(
                    (
                        1,
                        self.control_pad.speed_factor + 0.1,
                    )
                )
                if r_1
                else max(
                    (
                        0,
                        self.control_pad.speed_factor - 0.1,
                    )
                )
            )
            self.control_pad.update_speed_factor(speed_factor=speed_factor)
        if self._joystick.get_button(11):
            self.control_pad.update_direction(direction=DirectionsMixin.FORWARD)
        elif self._joystick.get_button(12):
            self.control_pad.update_direction(direction=DirectionsMixin.BACKWARD)
        elif self._joystick.get_button(13):
            self.control_pad.update_direction(direction=DirectionsMixin.LEFT)
        elif self._joystick.get_button(14):
            self.control_pad.update_direction(direction=DirectionsMixin.RIGHT)
        else:
            self.control_pad.update_direction(direction=DirectionsMixin.STOP)
