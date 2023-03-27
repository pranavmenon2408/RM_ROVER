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
    flex_range: t.Final[float] = 0.2
    MAX_SPEED: t.Final[int] = 255

    def update(self, x_axis: float, y_axis: float) -> None:
        self.x_axis = x_axis
        self.y_axis = y_axis

    def get_mapping(self, joystick: bool) -> tuple[int, int]:
        if joystick:
            return self.motor_speed
        else:
            speed = self.MAX_SPEED * self.speed_factor
            if self.direction == DirectionsMixin.FORWARD:
                return int(speed), int(speed)
            elif self.direction == DirectionsMixin.BACKWARD:
                return -int(speed), -int(speed)
            elif self.direction == DirectionsMixin.LEFT:
                return int(speed), -int(speed)
            elif self.direction == DirectionsMixin.RIGHT:
                return -int(speed), int(speed)
            elif self.direction == DirectionsMixin.FORWARD_LEFT:
                return int(speed * 0.5), int(speed)
            elif self.direction == DirectionsMixin.FORWARD_RIGHT:
                return int(speed), int(speed * 0.5)
            elif self.direction == DirectionsMixin.BACKWARD_LEFT:
                return -int(speed * 0.5), -int(speed)
            elif self.direction == DirectionsMixin.BACKWARD_RIGHT:
                return -int(speed), -int(speed * 0.5)
            else:
                return 0, 0

    def __repr__(self) -> str:
        return (
            f"JoyStick(x_axis={self.x_axis:.1f}, y_axis={self.y_axis:.1f},"
            f" direction={self.direction:.1f}, speed_factor={self.speed_factor:.1f},"
            f" motor_speed={self.motor_speed:.1f}, angle={self.angle:.1f})"
        )

    @property
    def motor_speed(self) -> tuple[int, int]:
        if self.direction == DirectionsMixin.STOP:
            return 0, 0
        angle = (
            math.degrees(math.atan2(math.fabs(self.y_axis), math.fabs(self.x_axis)))
            / 90
        )
        speed = int(self.MAX_SPEED * self.speed_factor)
        vertical = -1 if self.y_axis > 0 else 1
        if self.direction in (DirectionsMixin.FORWARD, DirectionsMixin.BACKWARD):
            return speed * vertical, speed * vertical
        elif self.direction in (DirectionsMixin.LEFT, DirectionsMixin.RIGHT):
            return speed * vertical, speed * -vertical
        else:
            if self.direction in (
                DirectionsMixin.FORWARD_LEFT,
                DirectionsMixin.BACKWARD_LEFT,
            ):
                return int(speed * (1 - angle)) * vertical, speed * vertical
            else:
                return speed * vertical, int(speed * (1 - angle)) * vertical

    @property
    def angle(self) -> float:
        return math.degrees(math.atan2(self.y_axis, self.x_axis))

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
        return math.sqrt(distance)
