import typing as t

import pygame

from .models import JoyStick

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

    def listener(self, func: CallbackT) -> CallbackT:
        def wrapper(*args: t.Any, **kwargs: t.Any) -> t.Any:
            self.listen()
            return func(*args, **kwargs)

        return wrapper

    def listen(self) -> None:
        joystick_events = pygame.event.get(pygame.JOYAXISMOTION)
        if joystick_events:
            self.joystick = JoyStick(
                x_axis=self._joystick.get_axis(0), y_axis=self._joystick.get_axis(1)
            )
