from protobuf.protobuf_types import Message
from protobuf.protobuf_types import Int32Serializer


class TestInner2(Message):
    def _get_c(cls):
        return cls.c

    def _set_c(cls, val):
        cls.c.append(val)

    def __init__(cls):
        super().__init__()
        cls.c = []
        cls.fields = \
            {
                1: [cls._get_c, cls._set_c, Int32Serializer(), True]
            }
