from protobuf.protobuf_types import Message
from protobuf.protobuf_types import Int32Serializer
from protobuf.protobuf_types import StringSerializer
from Test2_ptbf import Test2


class Test1(Message):
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
        cls.d.append(val)

    def __init__(cls):
        super().__init__()
        cls.a = 0
        cls.b = None
        cls.c = None
        cls.d = []
        cls.fields = \
            {
                1: [cls._get_a, cls._set_a, Int32Serializer(), False],
                2: [cls._get_b, cls._set_b, StringSerializer(), False],
                3: [cls._get_c, cls._set_c, Test2(), False],
                4: [cls._get_d, cls._set_d, Int32Serializer(), True]
            }
