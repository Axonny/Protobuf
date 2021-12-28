from tests.simple_ptbf import Test1
from io import BytesIO


def format_output(hex_str: str) -> None:
    print(*[hex_str[i: i + 2] for i in range(0, len(hex_str), 2)])


if __name__ == '__main__':

    q = Test1()
    q.a = 150
    q.b = "testing"
    format_output(q.dump().hex())
    qq = Test1()
    qq.load(BytesIO(q.dump()))
    print(qq.a)
    print(qq.b)
