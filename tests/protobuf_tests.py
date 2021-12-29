import unittest
from io import BytesIO

from tests.TestInner2_ptbf import TestInner2
from tests.TestRepeated_ptbf import TestRepeated


class LoadDumpTestCase(unittest.TestCase):
    def test_repeated(self):
        s = TestRepeated()
        s.d = [2, 100, 1000]
        in1 = TestInner2()
        in1.c = [100, 10000]
        in2 = TestInner2()
        in2.c = [9, 99999]
        s.f = [in1, in2]
        f = TestRepeated()
        f.load(BytesIO(s.dump()))

        self.assertEqual(s.d, f.d)  # add assertion here
        self.assertEqual(s.f[0].c, f.f[0].c)  # add assertion here
        self.assertEqual(s.f[1].c, f.f[1].c)  # add assertion here


if __name__ == '__main__':
    unittest.main()
