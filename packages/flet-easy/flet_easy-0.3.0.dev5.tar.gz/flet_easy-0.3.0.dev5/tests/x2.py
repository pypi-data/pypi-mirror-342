import asyncio
import threading
import time


class Tx:
    def __init__(self):
        self.x = 1
        self.y = 2

    def __str__(self):
        return f"Tx(x={self.x}, y={self.y})"


def test(t: Tx):
    print("test: Hello, world!", t)
    t.y = 4

    # Creamos un contenedor para almacenar el resultado
    result_container = {"result": None, "done": False}

    # Función para ejecutar test2 en un bucle separado
    def run_test2_in_thread(r):
        # Ejecutamos test2 en un nuevo bucle
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result_container["result"] = loop.run_until_complete(test2(t, r))
        result_container["done"] = True
        loop.close()

    # Creamos un hilo para ejecutar test2
    thread = threading.Thread(target=run_test2_in_thread(5))
    thread.start()
    threadx = threading.Thread(target=run_test2_in_thread(2))
    threadx.start()

    # Esperamos a que termine
    while not result_container["done"]:
        time.sleep(0.01)

    x = result_container["result"]
    print(x)
    return x


async def test2(t: Tx, time: int = 5):
    print("use test2:", time)
    await asyncio.sleep(time)
    t.x = 3
    return "test 2:", time


async def main(t: Tx):
    print("Initializing...")
    # Ejecutamos test en el bucle principal
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, lambda: test(t))
    print("Done!", t)
    return result


# Creamos una instancia de Tx y la pasamos a main
asyncio.run(main(Tx()))
