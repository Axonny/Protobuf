import struct

from io import BytesIO
from typing import Any
from abc import ABC, abstractmethod


class Serializer(ABC):
    wire_type = -1

    @abstractmethod
    def dump_inner(self, value: Any):
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
    def dump_inner(cls, value: int) -> bytes:
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
    def dump_inner(cls, value: int) -> bytes:
        return super().dump_inner(value)

    @classmethod
    def load(cls, io: BytesIO) -> int:
        return super().load(io)


class Int64Serializer(Int32Serializer):
    max_value = 1 << 64


class SignedInt32Serializer(VarintSerializer):
    shift = 31

    @classmethod
    def dump_inner(cls, value: int) -> bytes:
        return super().dump_inner((value << 1) ^ (value >> cls.shift))

    @classmethod
    def load(cls, io: BytesIO) -> int:
        value = super().load(io)
        return (value >> 1) ^ (-(value & 1))


class SignedInt64Serializer(SignedInt32Serializer):
    shift = 63


class BoolSerializer(VarintSerializer):
    @classmethod
    def dump_inner(cls, value: bool) -> bytes:
        return super().dump_inner(int(value))

    @classmethod
    def load(cls, io: BytesIO) -> bool:
        value = super().load(io)
        return value == 1


class FloatSerializer(Serializer):
    wire_type = 5
    format = '<f'
    size = 4

    @classmethod
    def dump_inner(cls, value: float) -> bytes:
        return struct.pack(cls.format, value)

    @classmethod
    def load(cls, io: BytesIO) -> float:
        return struct.unpack(cls.format, io.read(cls.size))[0]


class DoubleSerializer(FloatSerializer):
    wire_type = 1
    format = '<d'
    size = 8


class StringSerializer(Serializer):
    wire_type = 2

    @classmethod
    def dump_inner(cls, value: str) -> bytes:
        return VarintSerializer.dump_inner(len(value)) + value.encode('utf-8')

    @classmethod
    def load(cls, io: BytesIO) -> str:
        return io.read().decode('utf-8')


class BytesSerializer(Serializer):
    wire_type = 2

    @classmethod
    def dump_inner(cls, value: bytes) -> bytes:
        return VarintSerializer.dump_inner(len(value)) + value

    @classmethod
    def load(cls, io: BytesIO) -> bytes:
        return io.read()


class RepeatedSerializer(Serializer):
    wire_type = 2

    def __init__(self, serializer: callable):
        self.serializer = serializer

    def dump_inner(self, values: list) -> bytes:
        result = VarintSerializer.dump_inner(len(values))
        for value in values:
            s = self.serializer()
            s._embedded = True
            result += s.dump_inner(value)
        return result

    def load(self, bytes_io: BytesIO) -> list:
        result = []
        with bytes_io as io:
            if self.serializer.wire_type in [0, 1, 5]:
                result.append(self.serializer.load(io))
            elif self.serializer.wire_type == 2:
                length = VarintSerializer.load(io)
                result.append(self.serializer().load(BytesIO(io.read(length))))
        return result


class Message:
    wire_type = 2

    def __init__(self):
        self.fields = {}
        self._embedded = False

    def dump(self):
        result = bytes()
        for k, v in self.fields.items():
            if v[3]:
                for v2 in v[0]():
                    v[2]._embedded = True
                    result += bytes([v[2].wire_type + (k << 3)]) + v[2]().dump_inner(v2)
            else:
                val = v[0]()
                if val is not None:
                    v[2]._embedded = True
                    result += bytes([v[2].wire_type + (k << 3)]) + v[2]().dump_inner(val)
        if self._embedded:
            result = VarintSerializer.dump_inner(len(result)) + result
        return result

    def dump_inner(self, value):
        value._embedded = self._embedded
        return value.dump()

    def load(self, bytes_io: BytesIO):
        with bytes_io as io:
            while _byte := io.read(1):
                b = int.from_bytes(_byte, "big")
                number, wire_type = b >> 3, b % 8
                data = None
                if wire_type in [0, 1, 5]:
                    data = self.fields[number][2].load(io)
                if wire_type == 2:
                    length = VarintSerializer.load(io)
                    data = self.fields[number][2]().load(BytesIO(io.read(length)))
                self.fields[number][1](data)
        return self
