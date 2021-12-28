import argparse

default_values = \
    {
        "int32": 0,
        "string": "\"\""
    }

serializers = \
    {
        "int32": "Int32Serializer()",
        "string": "StringSerializer()"
    }


def gen_imports(fields):
    ans = "from protobuf_types import Message\n"
    set_types = set()
    for f in fields.values():
        set_types.add(serializers[f[0]][:-2])
    for t in set_types:
        ans += f"from protobuf_types import {t}\n"
    return ans + "\n\n"


def gen_init(fields):
    ans = (" " * 4) + "def __init__(cls):\n"
    ans += (" " * 8) + "super().__init__()\n"
    for f in fields.values():
        ans += f"" + (" " * 4) + f"" + (" " * 4) + f"cls.{f[1]} = {default_values[f[0]]}\n"

    ans += (" " * 8) + "cls.fields = \\\n"
    ans += (" " * 12) + "{\n"
    for k, v in fields.items():
        ans += (" " * 16) + f"{k}: [cls._get_{v[1]}, cls._set_{v[1]}, {serializers[v[0]]}],\n"
    ans = ans[:-2] + "\n"
    ans += (" " * 12) + "}\n"
    return ans


def gen_getters_setters(fields):
    ans = ""
    for f in fields.values():
        ans += f"" + (" " * 4) + f"def _get_{f[1]}(cls):\n" \
                                 f"" + (" " * 4) + f"" + (" " * 4) + f"return cls.{f[1]}\n\n"
        ans += f"" + (" " * 4) + f"def _set_{f[1]}(cls, val):\n" \
                                 f"" + (" " * 4) + f"" + (" " * 4) + f"cls.{f[1]} = val\n\n"

    return ans


def gen_class(file_name, class_name, fields):
    with open(file_name, "w") as f:
        f.write(gen_imports(fields))
        f.write(f"class {class_name}(Message):\n")
        f.write(gen_getters_setters(fields))
        f.write(gen_init(fields))


def generate(source):
    with open(source, "r") as f:
        data = f.readlines()
        started = False
        finished = False
        fields = {}
        class_name = ""
        for i, line in enumerate(data):
            if finished:
                break
            line = line.strip()
            if not started:
                if line.startswith("message"):
                    cur_data = line.split()
                    if len(cur_data) > 3:
                        raise RuntimeError(f"wrong format in line {i + 1}")
                    started = True
                    class_name = cur_data[1]
            else:
                if line == "":
                    continue
                if line == "}":
                    finished = True
                    continue
                cur_data = line[:-1].split()
                print(cur_data)
                if len(cur_data) != 5 or line[-1] != ";":
                    raise RuntimeError(f"wrong format in line {i + 1}")

                type_ = cur_data[1]
                name_ = cur_data[2]
                index = int(cur_data[4])

                if fields.get(index) is not None:
                    raise RuntimeError(f"repeated number in line {i + 1}")
                fields[index] = (type_, name_)
        if len(fields) == 0:
            return
        file_name = source.split(".")[0] + "_ptbf.py"
        gen_class(file_name, class_name, fields)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument("-s", "--source", type=str, required=True, help="proto file base on which generate class")

    generate(p.parse_args().source)
