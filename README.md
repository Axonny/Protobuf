# Protobuf

## How To Use

1. Create `simple.proto` file

```protobuf
message Simple {
  optional int32 simple_int = 1;
}
```

2. Call `python3.10 generate_class.py simple.proto`. You will get `Simple_ptbf.py` file

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

```
usage: generate_class.py [-h] -s SOURCE

options:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        proto file base on which generate class
```