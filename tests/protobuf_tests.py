import unittest
from protobuf.protobuf_types import *

from tests.TestInner_ptbf import TestInner
from tests.TestRepeated_ptbf import TestRepeated
from tests.Test2_ptbf import Test2
from tests.TestComplex_ptbf import TestComplex
from tests.TestInner2_ptbf import TestInner2


class LoadDumpTestCase(unittest.TestCase):
    def test_repeated(self):
        s = TestRepeated(d=[2, 100, 1000])
        in1 = TestInner2(c=[100, 10000])
        in2 = TestInner2(c=[9, 99999])
        s.f = [in1, in2]
        f = TestRepeated.loads(s.dumps())

        self.assertEqual(s.d, f.d)
        self.assertEqual(s.f[0].c, f.f[0].c)
        self.assertEqual(s.f[1].c, f.f[1].c)

    def test_int(self):
        numbers = [1, 2, 10, 20, 100, 1000]
        encoded = [b'\x01', b'\x02', b'\n', b'\x14', b'd', b'\xe8\x07']
        for n, e in zip(numbers, encoded):
            cur_e32 = Int32Serializer.dump_inner(n)
            self.assertEquals(e, cur_e32)
            cur_e64 = Int64Serializer.dump_inner(n)
            self.assertEquals(e, cur_e64)

    def test_signed_int(self):
        numbers = [-1, 1, -5, 5, -100, 100]
        encoded32 = [b'\x01', b'\x02', b'\t', b'\n', b'\xc7\x01', b'\xc8\x01']
        for n, e in zip(numbers, encoded32):
            cur_e32 = SignedInt32Serializer.dump_inner(n)
            self.assertEquals(e, cur_e32)

        encoded64 = [b'\x01', b'\x02', b'\t', b'\n', b'\xc7\x01', b'\xc8\x01']
        for n, e in zip(numbers, encoded64):
            cur_e64 = SignedInt32Serializer.dump_inner(n)
            self.assertEquals(e, cur_e64)

    def test_float(self):
        numbers = [1.1, -2.2, 1/3]
        encoded_f = [b'\xcd\xcc\x8c?', b'\xcd\xcc\x0c\xc0', b'\xab\xaa\xaa>']
        encoded_d = [b'\x9a\x99\x99\x99\x99\x99\xf1?', b'\x9a\x99\x99\x99\x99\x99\x01\xc0', b'UUUUUU\xd5?']

        for n, e in zip(numbers, encoded_f):
            cur_e = FloatSerializer.dump_inner(n)
            self.assertEquals(e, cur_e)

        for n, e in zip(numbers, encoded_d):
            cur_e = DoubleSerializer.dump_inner(n)
            self.assertEquals(e, cur_e)

    def test_simple_proto(self):
        t = Test2(c=150)
        dump = t.dumps()
        self.assertEquals(dump, b'\x08\x96\x01')
        t2 = Test2.loads(dump)
        self.assertEquals(t.c, t2.c)

    def test_embedded_message(self):
        tc = TestComplex(a=150, b=300, c=400, d=800, e=-100, f=-2.2, i="test")
        embedded = TestInner(a=250, e=-200, f=-3.2, i="test2")
        tc.t = embedded
        dump = tc.dumps()
        new_tc = TestComplex.loads(dump)
        self.assertEquals(tc.a, new_tc.a)
        self.assertEquals(tc.b, new_tc.b)
        self.assertEquals(tc.d, new_tc.d)
        self.assertEquals(tc.i, new_tc.i)
        self.assertEquals(embedded.a, new_tc.t.a)
        self.assertEquals(embedded.i, new_tc.t.i)


if __name__ == '__main__':
    unittest.main()
