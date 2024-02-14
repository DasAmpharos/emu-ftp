from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


@dataclass
class Config:
    n3ds: ConsoleConfig
    switch: ConsoleConfig


@dataclass
class ConsoleConfig:
    host: str
    directory: str
    saves: dict[str, Optional[str]]


class Console(str, Enum):
    N3DS = 'n3ds'
    SWITCH = 'switch'

    def __str__(self) -> str:
        return self.value


class GameType(str, Enum):
    RED = 'red'
    BLUE = 'blue'
    YELLOW = 'yellow'
    GOLD = 'gold'
    SILVER = 'silver'
    CRYSTAL = 'crystal'

    def __str__(self) -> str:
        return self.value
