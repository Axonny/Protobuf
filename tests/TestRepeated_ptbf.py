from protobuf.protobuf_types import Message
from protobuf.protobuf_types import Int32Serializer
from TestInner2_ptbf import TestInner2


class TestRepeated(Message):
    def _get_d(self):
        return self.d

    def _set_d(self, val):
        self.d.append(val)

    def _get_f(self):
        return self.f

    def _set_f(self, val):
        self.f.append(val)

    def __init__(self, d=[], f=[]):
        super().__init__()
        self.d = []
        self.f = []
        self.fields = \
            {
                4: [self._get_d, self._set_d, Int32Serializer, True],
                10: [self._get_f, self._set_f, TestInner2, True]
            }
