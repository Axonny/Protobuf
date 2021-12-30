import argparse
import os

default_values = \
    {
        "int32": 0,
        "uint32": 0,
        "sint32": 0,
        "fixed32": 0.0,
        "sfixed32": 0.0,
        "int64": 0,
        "uint64": 0,
        "sint64": 0,
        "fixed64": 0,
        "sfixed64": 0,
        "bool": 0,
        "string": None,
        "repeated": [],
        "float": 0.0,
        "double": 0.0
    }

serializers = \
    {
        "int32": "Int32Serializer",
        "uint32": "Int32Serializer",
        "sint32": "SignedInt32Serializer",
        "fixed32": "FloatSerializer",
        "sfixed32": "FloatSerializer",
        "int64": "Int64Serializer",
        "uint64": "Int64Serializer",
        "sint64": "SignedInt64Serializer",
        "fixed64": "DoubleSerializer",
        "sfixed64": "DoubleSerializer",
        "bool": "BoolSerializer",
        "string": "StringSerializer",
        "float": "FloatSerializer",
        "double": "DoubleSerializer"
    }
messages = {}


def gen_imports(fields, messages):
    ans = "from protobuf.protobuf_types import Message\n"
    set_types = set()
    set_message_types = set()
    for f in fields.values():
        type_name = f[0]
        if (type_val := serializers.get(type_name)) is None:
            if messages.get(type_name) is not None:
                set_message_types.add(type_name)
        else:
            set_types.add(type_val)
    for t in set_types:
        ans += f"from protobuf.protobuf_types import {t}\n"
    for t in set_message_types:
        ans += f"from {t}_ptbf import {t}\n"

    return ans + "\n\n"


def gen_init(fields):
    init_default = ""

    for f in fields.values():
        if (default := default_values.get(f[0])) is None:
            default = "None"
        if f[2]:
            default = "None"
        init_default += f"{f[1]}={default}, "
    init_default = init_default[:-2]
    ans = (" " * 4) + f"def __init__(self, {init_default}):\n"
    ans += (" " * 8) + "super().__init__()\n"
    for f in fields.values():
        default = f[1]
        if f[2]:
            default = f"[] if {f[1]} is None else {f[1]}"
        ans += f"" + (" " * 4) + f"" + (" " * 4) + f"self.{f[1]} = {default}\n"

    ans += (" " * 8) + "self.fields = \\\n"
    ans += (" " * 12) + "{\n"
    for k, v in fields.items():
        if (serializer := serializers.get(v[0])) is None:
            serializer = v[0]
        ans += (" " * 16) + f"{k}: [self._get_{v[1]}, self._set_{v[1]}, {serializer}, {v[2]}],\n"
    ans = ans[:-2] + "\n"
    ans += (" " * 12) + "}\n"
    return ans


def gen_getters_setters(fields):
    ans = ""
    for f in fields.values():
        ans += f"" + (" " * 4) + f"def _get_{f[1]}(self):\n" \
                                 f"" + (" " * 4) + f"" + (" " * 4) + f"return self.{f[1]}\n\n"
        if f[2]:
            ans += f"" + (" " * 4) + f"def _set_{f[1]}(self, val):\n" \
                                     f"" + (" " * 4) + f"" + (" " * 4) + f"self.{f[1]}.append(val)\n\n"
        else:
            ans += f"" + (" " * 4) + f"def _set_{f[1]}(self, val):\n" \
                                     f"" + (" " * 4) + f"" + (" " * 4) + f"self.{f[1]} = val\n\n"

    return ans


def gen_class(messages, source):
    for k, v in messages.items():
        file_name = k + "_ptbf.py"
        next_class = os.path.join(os.path.split(os.path.abspath(source))[0], file_name)
        with open(next_class, "w") as f:
            f.write(gen_imports(v, messages))
            f.write(f"class {k}(Message):\n")
            f.write(gen_getters_setters(v))
            f.write(gen_init(v))


def parse_message(data, current_line):
    fields = {}

    for i, line in enumerate(data[current_line + 1:]):
        line = line.strip()
        if line == "":
            continue
        if line == "}":
            return fields, i
        repeated = False
        cur_data = line[:-1].split()
        if len(cur_data) != 5 or line[-1] != ";":
            raise RuntimeError(f"wrong format in line {i + 1}")
        if cur_data[0] == "repeated":
            repeated = True
        type_ = cur_data[1]
        name_ = cur_data[2]
        index = int(cur_data[4])
        if fields.get(index) is not None:
            raise RuntimeError(f"repeated number in line {i + 1}")
        fields[index] = (type_, name_, repeated)


def generate(source):
    with open(source, "r") as f:
        data = f.readlines()
        end = 0
        for i, line in enumerate(data):
            if i < end:
                continue
            line = line.strip()
            if line.startswith("import"):
                next_source = os.path.join(os.path.split(os.path.abspath(source))[0], line.split()[1][1:-2])
                generate(next_source)
            if line.startswith("message"):
                cur_data = line.split()
                if len(cur_data) > 3:
                    raise RuntimeError(f"wrong format in line {i + 1}")
                messages[cur_data[1]], end = parse_message(data, i)
                class_name = cur_data[1]

        if len(messages) == 0:
            return

        return messages


def main():
    p = argparse.ArgumentParser()
    p.add_argument("-c", "--compile", type=str, required=True, help="path to proto file base on which generate class")
    generate(p.parse_args().compile)
    gen_class(messages, p.parse_args().compile)


if __name__ == '__main__':
    main()
