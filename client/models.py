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
    flex_range: float = 0.1
    max_speed: int = 255

    def __repr__(self) -> str:
        return (
            f"JoyStick(x_axis={self.x_axis},"
            f" y_axis={self.y_axis},"
            f" direction={self.direction},"
            f" speed_factor={self.speed_factor},"
            f" angle={self.angle},"
            f" motor_speed={self.motor_speed})"
        )

    def update(self, x_axis: float, y_axis: float) -> None:
        self.x_axis = round(x_axis, 1)
        self.y_axis = round(y_axis, 1)

    @property
    def motor_speed(self) -> tuple[int, int]:
        if self.direction == DirectionsMixin.STOP:
            return 0, 0
        angle = round(
            math.degrees(math.atan2(math.fabs(self.y_axis), math.fabs(self.x_axis)))
            / 90,
            1,
        )
        speed = int(self.max_speed * self.speed_factor)
        vertical = -1 if self.y_axis > 0 else 1
        if self.direction in (DirectionsMixin.FORWARD, DirectionsMixin.BACKWARD):
            return speed * vertical, speed * vertical
        if self.direction in (DirectionsMixin.LEFT, DirectionsMixin.RIGHT):
            return speed * vertical, speed * -vertical
        if self.direction in (
            DirectionsMixin.FORWARD_LEFT,
            DirectionsMixin.BACKWARD_LEFT,
        ):
            return int(speed * (1 - angle)) * vertical, speed * vertical
        if self.direction in (
            DirectionsMixin.FORWARD_RIGHT,
            DirectionsMixin.BACKWARD_RIGHT,
        ):
            return speed * vertical, int(speed * (1 - angle)) * vertical
        return 0, 0

    @property
    def angle(self) -> float:
        return round(math.degrees(math.atan2(self.y_axis, self.x_axis)), 1)

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
    def speed_factor(self) -> float:
        distance = max(abs(self.x_axis), abs(self.y_axis))
        return round(math.sqrt(distance), 1)
