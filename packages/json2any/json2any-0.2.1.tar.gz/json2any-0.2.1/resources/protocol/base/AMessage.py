from abc import ABC
from enum import Enum
from typing import Type


class AMessage(ABC):
    def from_bytes(self, data: bytes):
        raise NotImplementedError()

    def to_bytes(self, data: bytes):
        raise NotImplementedError()

    def min_len(self) -> int:
        raise NotImplementedError()

    def max_len(self) -> int:
        raise NotImplementedError()


class DataTypes(Enum):
    UINT8 = 1, int, 'B'
    UINT16 = 2, int, 'H'

    def __new__(cls, *args, **kwds):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: int, type_: Type, decode_format: str):
        self._type = type_
        self._format = decode_format

    def __str__(self):
        return f'{self.value} - {self.name}'

    def __repr__(self):
        return self.__str__()

    # this makes sure that the description is read-only
    @property
    def type(self) -> Type:
        return self._type

    @property
    def format(self) -> str:
        return self._format
