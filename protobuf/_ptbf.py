from protobuf.protobuf_types import Message
from protobuf.protobuf_types import Int32Serializer
from protobuf.protobuf_types import StringSerializer


class Test1(Message):
    def _get_a(cls):
        return cls.a

    def _set_a(cls, val):
        cls.a = val

    def _get_b(cls):
        return cls.b

    def _set_b(cls, val):
        cls.b = val

    def __init__(cls):
        super().__init__()
        cls.a = 0
        cls.b = ""
        cls.fields = \
            {
                1: [cls._get_a, cls._set_a, Int32Serializer()],
                2: [cls._get_b, cls._set_b, StringSerializer()]
            }
