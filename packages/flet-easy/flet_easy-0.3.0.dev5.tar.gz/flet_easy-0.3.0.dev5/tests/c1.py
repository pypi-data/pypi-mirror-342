class y:
    def __init__(self):
        self.y1 = x


class x:
    a: y = 1

    def __init__(self):
        self.aa = x.a

    def get_name(self):
        return self.aa

    def set_name(self, name):
        self.aa = name


x.a = 15
j = x()
k = y()

print(j.a)
print(j.get_name())

j.set_name(k)

print("y1", k.y1)
j.aa.y1 = 2
print("y2", k.y1)

print(j.get_name())


def aeaae(a):
    print(a)


print(type(x) is type)
print(isinstance(x, type))
print(issubclass(x, y))
