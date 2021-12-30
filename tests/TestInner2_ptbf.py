from protobuf.protobuf_types import Message
from protobuf.protobuf_types import Int32Serializer


class TestInner2(Message):
    def _get_c(self):
        return self.c

    def _set_c(self, val):
        self.c.append(val)

    def __init__(self, c=[]):
        super().__init__()
        self.c = []
        self.fields = \
            {
                1: [self._get_c, self._set_c, Int32Serializer, True]
            }
