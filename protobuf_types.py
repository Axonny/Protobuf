from abc import ABC, abstractmethod
from typing import Any
from io import BytesIO


class Serializer(ABC):
    wire_type = -1

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

    @classmethod
    def load(cls, io: BytesIO) -> int:
        return super().load(io)


class Int64Serializer(Int32Serializer):
    max_value = 1 << 64


class SignedInt32Serializer(VarintSerializer):
    shift = 31

    @classmethod
    def dump(cls, value: int) -> bytes:
        return super().dump((value << 1) ^ (value >> cls.shift))

    @classmethod
    def load(cls, io: BytesIO) -> int:
        value = super().load(io)
        return (value >> 1) ^ (-(value & 1))


class SignedInt64Serializer(SignedInt32Serializer):
    shift = 63


class BoolSerializer(VarintSerializer):
    @classmethod
    def dump(cls, value: bool) -> bytes:
        return super().dump(int(value))

    @classmethod
    def load(cls, io: BytesIO) -> bool:
        value = super().load(io)
        return value == 1


class StringSerializer(Serializer):
    wire_type = 2

    @classmethod
    def dump(cls, value: str) -> bytes:
        return bytes([len(value)]) + value.encode('utf-8')

    @classmethod
    def load(cls, io: BytesIO) -> str:
        return io.read().decode('utf-8')


class BytesSerializer(Serializer):
    wire_type = 2

    @classmethod
    def dump(cls, value: bytes) -> bytes:
        return bytes([len(value)]) + value

    @classmethod
    def load(cls, io: BytesIO) -> bytes:
        return io.read()


class RepeatedSerializer(Serializer):
    wire_type = 2

    def __init__(self, serializer: Serializer):
        self.serializer = serializer

    def dump(self, values: list) -> bytes:
        result = bytes()
        for value in values:
            result += self.serializer.dump(value)
        return result

    def load(self, bytes_io: BytesIO) -> list:
        result = []
        with bytes_io as io:
            if self.serializer.wire_type == 1:
                result.append(self.serializer.load(io))
            elif self.serializer.wire_type == 2:
                length = int.from_bytes(io.read(1), "big")
                result.append(self.serializer.load(BytesIO(io.read(length))))
        return result


class Message:
    def __init__(self):
        self.fields = {}

    def dump(self):
        result = bytes()
        for k, v in self.fields.items():
            result += bytes([v[2].wire_type + (k << 3)]) + v[2].dump(v[0]())
        return result

    def load(self, bytes_io: BytesIO) -> None:
        fields = {}
        with bytes_io as io:
            while _byte := io.read(1):
                b = int.from_bytes(_byte, "big")
                number, wire_type = b >> 3, b % 8
                data = None
                if wire_type == 1:
                    data = self.fields[number][2].load(io)
                if wire_type == 2:
                    length = int.from_bytes(io.read(1), "big")
                    data = self.fields[number][2].load(BytesIO(io.read(length)))
                fields[number] = data

        for k, v in fields.items():
            self.fields[k][1](v)
