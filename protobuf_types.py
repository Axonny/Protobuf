from abc import ABC, abstractmethod
from typing import Any
from io import BytesIO


class Serializer(ABC):

    @abstractmethod
    def dump(self, value: Any):
        pass

    @abstractmethod
    def load(self, io: BytesIO):
        pass


class VarintSerializer(Serializer):
    wire_type = 0

    @classmethod
    def get_bytes(cls, value):
        return bin(value)[2:]

    @classmethod
    def dump(cls, value: int) -> bytes:
        b = cls.get_bytes(value=value)
        count_zeros = (7 - len(b) % 7) % 7
        b = "0" * count_zeros + b
        _bytes = ["1" + b[i:i + 7] for i in range(0, len(b), 7)]
        _bytes = _bytes[::-1]
        _bytes[-1] = "0" + _bytes[-1][1:]
        bin_str = "".join(_bytes)
        return bytes(int(bin_str[i:i + 8], 2) for i in range(0, len(bin_str), 8))

    @classmethod
    def load(cls, io: BytesIO) -> int:
        result = 0
        count = 0
        while b := int.from_bytes(io.read(1), "big"):
            is_not_end = b >> 7
            result = result ^ ((b % (2 ** 7)) << (7 * count))
            count += 1
            if is_not_end == 0:
                return result


class Int32Serializer(VarintSerializer):
    max_value = (1 << 32)

    @classmethod
    def get_bytes(cls, value):
        if value > 0:
            return super().get_bytes(value)
        else:
            return super().get_bytes(cls.max_value + value)

    @classmethod
    def dump(cls, value: int) -> bytes:
        return super().dump(value)

    def load(self, io: BytesIO):
        pass


class Int64Serializer(Int32Serializer):
    max_value = 1 << 64


class SignedInt32Serializer(VarintSerializer):
    shift = 31

    @classmethod
    def dump(cls, value: Any):
        return super().dump((value << 1) ^ (value >> cls.shift))

    def load(self, io: BytesIO):
        pass


class SignedInt64Serializer(SignedInt32Serializer):
    shift = 63


class StringSerializer(Serializer):
    wire_type = 2

    @classmethod
    def dump(cls, value: str) -> bytes:
        return bytes([len(value)]) + value.encode('utf-8')

    @classmethod
    def load(cls, io: BytesIO) -> str:
        length = int.from_bytes(io.read(1), "big")
        return io.read(length).decode('utf-8')


class MessageSerializer(VarintSerializer):
    @classmethod
    def dump(cls, values: list[Any]):
        result = bytes()
        for i, v in enumerate(values):
            if isinstance(v, int):
                result += bytes([VarintSerializer.wire_type + ((i + 1) << 3)]) + VarintSerializer.dump(v)
            if isinstance(v, str):
                result += bytes([StringSerializer.wire_type + ((i + 1) << 3)]) + StringSerializer.dump(v)
        return result

    def load(self, io: BytesIO):
        pass


class Message:
    def __init__(self):
        self.fields = {}

    def dump(self):
        result = bytes()
        for k, v in self.fields.items():
            result += bytes([v[2].wire_type + (k << 3)]) + v[2].dump(v[0]())
        return result

    def load(self, bytes_io: BytesIO) -> dict:
        fields = {}
        with bytes_io as io:
            while _byte := io.read(1):
                b = int.from_bytes(_byte, "big")
                number, wire_type = b >> 3, b % 8
                data = None
                if wire_type == 0:
                    data = VarintSerializer.load(io)
                if wire_type == 2:
                    data = StringSerializer.load(io)

                fields[number] = data

        for k, v in fields.items():
            self.fields[k][1](v)

