from __future__ import annotations

import dataclasses
import os
import typing as t

from dotenv import load_dotenv

__all__: tuple[str, ...] = (
    "config",
    "ENVIRONMENT",
)
load_dotenv()
MISSING = object()


@dataclasses.dataclass
class EnvironmentVariable:
    name: str
    default: t.Any = MISSING
    cast: type = str
    required: bool = True

    def __post_init__(self) -> None:
        self.default = os.getenv(self.name, self.default)
        if self.required and self.default is MISSING:
            raise ValueError(f"Missing required environment variable {self.name}")
        try:
            self.default = self.cast(self.default)
        except Exception as e:
            raise ValueError(
                f"Failed to cast {self.name} to {self.cast.__name__}"
            ) from e

    def __get__(self, instance: t.Any, owner: t.Any) -> t.Any:
        return self.default

    def __repr__(self) -> str:
        return f"EnvironmentVariable(name={self.name}, default={self.default}, cast={self.cast.__name__}, required={self.required})"


class ENVIRONMENT:
    _instance: t.Optional["ENVIRONMENT"] = None
    PORT: EnvironmentVariable = EnvironmentVariable("PORT", cast=int, required=True)
    MAC_ADDRESS: EnvironmentVariable = EnvironmentVariable("MAC_ADDRESS", required=True)

    def __new__(cls, *args: t.Any, **kwargs: t.Any) -> "ENVIRONMENT":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


config = ENVIRONMENT()
