from protobuf_types import Message
from protobuf_types import StringSerializer
from protobuf_types import Int32Serializer


class Test1(Message):
    def _get_a(self):
        return self.a

    def _set_a(self, val):
        self.a = val

    def _get_b(self):
        return self.b

    def _set_b(self, val):
        self.b = val

    def __init__(self):
        super().__init__()
        self.a = 0
        self.b = ""
        self.fields = \
            {
                1: [self._get_a, self._set_a, Int32Serializer()],
                2: [self._get_b, self._set_b, StringSerializer()]
            }
