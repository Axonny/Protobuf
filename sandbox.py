
from protobuf_types import MessageSerializer, Message
from simple_ptbf import Test1


def format_output(hex_str: str) -> None:
    print(*[hex_str[i: i + 2] for i in range(0, len(hex_str), 2)])


if __name__ == '__main__':
    qq = Test1()
    qq.a = 150
    qq.b = "testing"
    format_output(qq.dump().hex())
    q = Message()
    q.a = 150
    format_output(q.dump().hex())
    format_output(MessageSerializer.dump([150]).hex())
    format_output(MessageSerializer.dump([150, "testing"]).hex())
