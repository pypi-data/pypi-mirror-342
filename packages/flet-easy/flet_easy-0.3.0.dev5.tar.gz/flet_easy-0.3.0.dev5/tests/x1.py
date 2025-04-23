import asyncio


class Tx:
    def __init__(self):
        self.x = 1
        self.y = 2

    def __str__(self):
        return f"Tx(x={self.x}, y={self.y})"


def test(t: Tx):
    print("test: Hello, world!", t)
    t.y = 4
    x = test2(t)
    print(x)
    return x


async def test2(t: Tx):
    print("use test2")
    t.x = 3
    return "test 2"


async def main(t: Tx):
    print("Initializing...")
    test(t)
    print("Done!", t)
    # test2()


asyncio.run(main(Tx()))
