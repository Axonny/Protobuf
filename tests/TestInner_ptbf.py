from protobuf.protobuf_types import Message
from protobuf.protobuf_types import Int32Serializer
from protobuf.protobuf_types import BoolSerializer
from protobuf.protobuf_types import StringSerializer
from protobuf.protobuf_types import Int64Serializer
from protobuf.protobuf_types import SignedInt64Serializer
from protobuf.protobuf_types import VarintSerializer
from protobuf.protobuf_types import SignedInt32Serializer


class TestInner(Message):
    def _get_a(cls):
        return cls.a

    def _set_a(cls, val):
        cls.a = val

    def _get_b(cls):
        return cls.b

    def _set_b(cls, val):
        cls.b = val

    def _get_c(cls):
        return cls.c

    def _set_c(cls, val):
        cls.c = val

    def _get_d(cls):
        return cls.d

    def _set_d(cls, val):
        cls.d = val

    def _get_e(cls):
        return cls.e

    def _set_e(cls, val):
        cls.e = val

    def _get_e(cls):
        return cls.e

    def _set_e(cls, val):
        cls.e = val

    def _get_f(cls):
        return cls.f

    def _set_f(cls, val):
        cls.f = val

    def _get_g(cls):
        return cls.g

    def _set_g(cls, val):
        cls.g = val

    def _get_h(cls):
        return cls.h

    def _set_h(cls, val):
        cls.h = val

    def _get_i(cls):
        return cls.i

    def _set_i(cls, val):
        cls.i = val

    def __init__(cls):
        super().__init__()
        cls.a = 0
        cls.b = 0
        cls.c = 0
        cls.d = 0
        cls.e = 0
        cls.e = 0
        cls.f = None
        cls.g = None
        cls.h = 0
        cls.i = None
        cls.fields = \
            {
                1: [cls._get_a, cls._set_a, Int32Serializer(), False],
                2: [cls._get_b, cls._set_b, Int64Serializer(), False],
                3: [cls._get_c, cls._set_c, VarintSerializer(), False],
                4: [cls._get_d, cls._set_d, VarintSerializer(), False],
                5: [cls._get_e, cls._set_e, SignedInt32Serializer(), False],
                6: [cls._get_e, cls._set_e, SignedInt64Serializer(), False],
                7: [cls._get_f, cls._set_f, double(), False],
                8: [cls._get_g, cls._set_g, float(), False],
                9: [cls._get_h, cls._set_h, BoolSerializer(), False],
                10: [cls._get_i, cls._set_i, StringSerializer(), False]
            }
