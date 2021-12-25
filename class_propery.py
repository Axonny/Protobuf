

class TestProperty:

    def __init__(self, a):
        self._a = a

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):
        self._a = value


if __name__ == "__main__":
    t = TestProperty(123)
    print(t.a)
    t.a = 1234
    print(t.a)
