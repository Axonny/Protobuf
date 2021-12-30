from protobuf.protobuf_types import Message
from protobuf.protobuf_types import SignedInt32Serializer
from protobuf.protobuf_types import FloatSerializer
from protobuf.protobuf_types import BoolSerializer
from protobuf.protobuf_types import Int64Serializer
from protobuf.protobuf_types import StringSerializer
from protobuf.protobuf_types import Int32Serializer
from protobuf.protobuf_types import DoubleSerializer
from TestInner_ptbf import TestInner


class TestComplex(Message):
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
        self.d = val

    def _get_e(self):
        return self.e

    def _set_e(self, val):
        self.e = val

    def _get_f(self):
        return self.f

    def _set_f(self, val):
        self.f = val

    def _get_g(self):
        return self.g

    def _set_g(self, val):
        self.g = val

    def _get_h(self):
        return self.h

    def _set_h(self, val):
        self.h = val

    def _get_i(self):
        return self.i

    def _set_i(self, val):
        self.i = val

    def _get_t(self):
        return self.t

    def _set_t(self, val):
        self.t = val

    def __init__(self, a=0, b=0, c=0, d=0, e=0, f=0.0, g=0.0, h=0, i=None, t=None):
        super().__init__()
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        self.g = g
        self.h = h
        self.i = i
        self.t = t
        self.fields = \
            {
                1: [self._get_a, self._set_a, Int32Serializer, False],
                2: [self._get_b, self._set_b, Int64Serializer, False],
                3: [self._get_c, self._set_c, Int32Serializer, False],
                4: [self._get_d, self._set_d, Int64Serializer, False],
                5: [self._get_e, self._set_e, SignedInt32Serializer, False],
                7: [self._get_f, self._set_f, DoubleSerializer, False],
                8: [self._get_g, self._set_g, FloatSerializer, False],
                9: [self._get_h, self._set_h, BoolSerializer, False],
                10: [self._get_i, self._set_i, StringSerializer, False],
                12: [self._get_t, self._set_t, TestInner, False]
            }
