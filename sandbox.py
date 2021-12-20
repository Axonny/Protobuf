
from protobuf_types import MessageSerializer


def format_output(hex_str: str) -> None:
    print(*[hex_str[i: i + 2] for i in range(0, len(hex_str), 2)])


if __name__ == '__main__':
    format_output(MessageSerializer.dump([150]).hex())
    format_output(MessageSerializer.dump(["testing"]).hex())
