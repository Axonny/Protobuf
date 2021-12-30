from protobuf.protobuf_types import Message
from protobuf.protobuf_types import Int32Serializer


class Test2(Message):
    def _get_c(self):
        return self.c

    def _set_c(self, val):
        self.c = val

    def __init__(self, c=0):
        super().__init__()
        self.c = c
        self.fields = \
            {
                1: [self._get_c, self._set_c, Int32Serializer, False]
            }
