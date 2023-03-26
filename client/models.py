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

    def __repr__(self) -> str:
        return f"JoyStick(x_axis={self.x_axis}," \
               f" y_axis={self.y_axis}," \
               f" direction={self.direction}," \
               f" speed={self.speed})"

    def update(self, x_axis: float, y_axis: float) -> None:
        self.x_axis = round(x_axis, 1)
        self.y_axis = round(y_axis, 1)

    @property
    def direction(self) -> str:
        if -self.flex_range <= self.y_axis <= self.flex_range:
            if -self.flex_range <= self.x_axis <= self.flex_range:
                return DirectionsMixin.STOP
            elif self.x_axis < -self.flex_range:
                return DirectionsMixin.LEFT
            elif self.x_axis > self.flex_range:
                return DirectionsMixin.RIGHT
        if self.y_axis > 0.0:
            if -self.flex_range <= self.x_axis <= self.flex_range:
                return DirectionsMixin.BACKWARD
            elif self.x_axis < -self.flex_range:
                return DirectionsMixin.BACKWARD_LEFT
            elif self.x_axis > self.flex_range:
                return DirectionsMixin.BACKWARD_RIGHT
        if self.y_axis < 0.0:
            if -self.flex_range <= self.x_axis <= self.flex_range:
                return DirectionsMixin.FORWARD
            elif self.x_axis < -self.flex_range:
                return DirectionsMixin.FORWARD_LEFT
            elif self.x_axis > self.flex_range:
                return DirectionsMixin.FORWARD_RIGHT
        return DirectionsMixin.STOP

    @property
    def speed(self) -> float:
        distance = max(abs(self.x_axis), abs(self.y_axis))
        return round(math.sqrt(distance), 1)
