import dataclasses
import math
import typing as t
from enum import Enum

__all__: tuple[str, ...] = ("JoyStick",)


class BaseEnum(Enum):
    def __get__(self, instance: t.Any, owner: t.Any) -> str:
        return self.value


class DirectionsMixin(str, BaseEnum):
    FORWARD = "f"
    BACKWARD = "b"
    LEFT = "l"
    RIGHT = "r"
    FORWARD_LEFT = "g"
    FORWARD_RIGHT = "i"
    BACKWARD_LEFT = "h"
    BACKWARD_RIGHT = "j"
    STOP = "s"


@dataclasses.dataclass
class JoyStick:
    y_axis: float
    x_axis: float
    flex_range: float = 0.3

    @property
    def direction(self) -> str:
        if self.y_axis > 0.0:
            if -self.flex_range <= self.x_axis <= self.flex_range:
                return DirectionsMixin.FORWARD
            elif self.x_axis < -self.flex_range:
                return DirectionsMixin.FORWARD_LEFT
            elif self.x_axis > self.flex_range:
                return DirectionsMixin.FORWARD_RIGHT
        elif self.y_axis < 0.0:
            if -self.flex_range <= self.x_axis <= self.flex_range:
                return DirectionsMixin.BACKWARD
            elif self.x_axis < -self.flex_range:
                return DirectionsMixin.BACKWARD_LEFT
            elif self.x_axis > self.flex_range:
                return DirectionsMixin.BACKWARD_RIGHT
        elif self.y_axis == 0.0:
            if -self.flex_range <= self.x_axis <= self.flex_range:
                return DirectionsMixin.STOP
            elif self.x_axis < -self.flex_range:
                return DirectionsMixin.LEFT
            elif self.x_axis > self.flex_range:
                return DirectionsMixin.RIGHT
        return DirectionsMixin.STOP

    @property
    def speed(self) -> float:
        distance = math.sqrt(self.x_axis**2 + self.y_axis**2)
        radius = math.sqrt(2) / 2
        return distance / radius
