import functools
import timeit
from statistics import mean


def benchmark(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        benchmark_name = func.__name__.replace("test_", "").replace("_", " ")
        print(f"-> Benchmarking: {benchmark_name}", end=" ", flush=True)

        # Measure time (1 run, repeat 100 times, take average)
        times = timeit.repeat(
            lambda: func(*args, **kwargs),
            number=1,
            repeat=100,
            globals=globals(),
            timer=timeit.default_timer,  # Usamos timeit.default_timer que es time.perf_counter
        )

        avg_time = round(mean(times) * 1000, 5)  # Convert to milliseconds
        print(f"Average execution time: {avg_time} ms")

        # Ejecutar la función una vez más para obtener el valor de retorno
        result = func(*args, **kwargs)
        return result  # Devolver el valor de retorno de la función decorada

    return wrapper


@benchmark
def test_benchmarkx():
    x = []
    for i in range(10):
        x.append(i)
    return "Done", x


if __name__ == "__main__":
    t = test_benchmarkx()
    print(t)
