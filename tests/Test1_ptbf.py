from protobuf.protobuf_types import Message
from protobuf.protobuf_types import Int32Serializer
from protobuf.protobuf_types import StringSerializer
from Test2_ptbf import Test2


class Test1(Message):
    def _get_a(self):
        return self.a

    def _set_a(self, val):
        self.a = val

    def _get_b(self):
        return self.b

    def _set_b(self, val):
        self.b = val

    def _get_c(self):
        return self.c

    def _set_c(self, val):
        self.c = val

    def _get_d(self):
        return self.d

    def _set_d(self, val):
        self.d.append(val)

    def __init__(self):
        super().__init__()
        self.a = 0
        self.b = None
        self.c = None
        self.d = []
        self.fields = \
            {
                1: [self._get_a, self._set_a, Int32Serializer, False],
                2: [self._get_b, self._set_b, StringSerializer, False],
                3: [self._get_c, self._set_c, Test2, False],
                4: [self._get_d, self._set_d, Int32Serializer, True]
            }
