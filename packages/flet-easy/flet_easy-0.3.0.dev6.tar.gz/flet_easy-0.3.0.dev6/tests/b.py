import functools
import time


def benchmark(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        benchmark_name = func.__name__.replace("test_", "").replace("_", " ")
        print(f"-> Benchmarking: {benchmark_name}", end=" ", flush=True)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        elapsed_ms = round((end - start) * 1000, 5)
        print(f"Execution time: {elapsed_ms} ms")

        return result, elapsed_ms

    return wrapper


@benchmark
def test_benchmarkx():
    x = []
    for i in range(10):
        x.append(i)
    return "Done", x


if __name__ == "__main__":
    result, elapsed = test_benchmarkx()
    print("Resultado:", result)
    print("Tiempo de ejecución:", elapsed, "ms")
