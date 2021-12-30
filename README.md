# Protobuf

## How To Use

1. Create `simple.proto` file

```protobuf
message Simple {
  optional int32 simple_int = 1;
}
```

2. Call `python3.10 -m protobuf -c simple.proto`. You will get `Simple_ptbf.py` file

```python
from protobuf.protobuf_types import Message
from protobuf.protobuf_types import Int32Serializer


class Simple(Message):
    def _get_simple_int(self):
        return self.simple_int

    def _set_simple_int(self, val):
        self.simple_int = val

    def __init__(self, simple_int=0):
        super().__init__()
        self.simple_int = simple_int
        self.fields = \
            {
                1: [self._get_simple_int, self._set_simple_int, Int32Serializer, False]
            }

```

3. Import generated class to your code

```python
from Simple_ptbf import Simple
```

### How to dump 
```python
from Simple_ptbf import Simple

s = Simple(simple_int=42)
print(s.dumps())  # Return bytes
#  Or
s.dump(open('proto_dump', 'wb'))
```

### How to load

```python
from Simple_ptbf import Simple

dump = Simple(simple_int=42).dumps()

s = Simple.loads(dump)  # Return new instance of class
print(s.simple_int)  # 42
#  Or
s = Simple.load(open('proto_dump', 'rb'))
```

## Generate

```text
usage: generate_class.py [-h] -c COMPILE

options:
  -h, --help            show this help message and exit
  -c COMPILE, --compile COMPILE
                        path to proto file base on which generate class
```

### Example
```text
python3.10 -m protobuf -c simple.proto
```