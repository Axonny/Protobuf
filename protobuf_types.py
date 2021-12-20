from abc import ABC, abstractmethod
from typing import Any


class Serializer(ABC):

    @abstractmethod
    def dump(self, value: Any):
        pass

    @abstractmethod
    def load(self):
        pass


class VarintSerializer(Serializer):
    wire_type = 0

    @classmethod
    def dump(cls, value: int) -> bytes:
        b = bin(value)[2:]
        count_zeros = (7 - len(b) % 7) % 7
        b = "0" * count_zeros + b
        _bytes = ["1" + b[i:i+7] for i in range(0, len(b), 7)]
        _bytes = _bytes[::-1]
        _bytes[-1] = "0" + _bytes[-1][1:]
        bin_str = "".join(_bytes)
        return bytes(int(bin_str[i:i+8], 2) for i in range(0, len(bin_str), 8))

    def load(self):
        pass


class Int32Serializer(VarintSerializer):
    @classmethod
    def dump(cls, value: int) -> bytes:
        return super().dump(value)

    def load(self):
        pass


class SignedInt32Serializer(VarintSerializer):
    @classmethod
    def dump(cls, value: Any):
        return super().dump((value << 1) ^ (value >> 31))

    def load(self):
        pass


class SignedInt64Serializer(VarintSerializer):
    @classmethod
    def dump(cls, value: Any):
        return super().dump((value << 1) ^ (value >> 63))

    def load(self):
        pass


class StringSerializer(Serializer):
    wire_type = 2

    @classmethod
    def dump(cls, value: str) -> bytes:
        return bytes([len(value)]) + value.encode('utf-8')


    def load(self):
        pass


class MessageSerializer(VarintSerializer):
    @classmethod
    def dump(cls, values: list[Any]):
        result = bytes()
        for i, v in enumerate(values):
            if isinstance(v, int):
                result += bytes([int(f'{bin(i+1)[2:]:0>5}{bin(VarintSerializer.wire_type)[2:]:0>3}', 2)])\
                          + VarintSerializer.dump(v)
            if isinstance(v, str):
                result += bytes([int(f'{bin(i + 1)[2:]:0>5}{bin(StringSerializer.wire_type)[2:]:0>3}', 2)]) \
                          + StringSerializer.dump(v)
        return result

    def load(self):
        pass
