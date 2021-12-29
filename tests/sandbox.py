from tests.Test1_ptbf import Test1

from io import BytesIO

from tests.Test2_ptbf import Test2


def format_output(hex_str: str) -> None:
    print(*[hex_str[i: i + 2] for i in range(0, len(hex_str), 2)])


if __name__ == '__main__':
    q = Test1()
    q.a = 150
    q.b = "testing"
    q.c = Test2()
    q.c.c = 150
    q.d = [1, 2, 3, 4]
    format_output(q.dump().hex())
    qq = Test1()
    qq.load(BytesIO(q.dump()))
    print(qq.a)
    print(qq.b)
    print(qq.d)
    print(qq.c.c)















