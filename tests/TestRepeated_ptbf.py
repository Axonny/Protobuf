from protobuf.protobuf_types import Message
from protobuf.protobuf_types import Int32Serializer
from TestInner2_ptbf import TestInner2


class TestRepeated(Message):
    def _get_d(cls):
        return cls.d

    def _set_d(cls, val):
        cls.d.append(val)

    def _get_f(cls):
        return cls.f

    def _set_f(cls, val):
        cls.f.append(val)

    def __init__(cls):
        super().__init__()
        cls.d = []
        cls.f = []
        cls.fields = \
            {
                4: [cls._get_d, cls._set_d, Int32Serializer, True],
                10: [cls._get_f, cls._set_f, TestInner2, True]
            }
