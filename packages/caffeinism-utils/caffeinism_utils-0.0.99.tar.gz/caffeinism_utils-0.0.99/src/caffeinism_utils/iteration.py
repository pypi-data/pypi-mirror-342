import time
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from typing import Generator, Iterator, TypeVar, Union

T = TypeVar("T")


def rate_limit_iterator(
    iterator: Iterator[T], iters_per_second: float, start: float | None = None
) -> Generator[T, None, None]:
    start = start or time.time()
    for i, it in enumerate(iterator):
        yield it
        time.sleep(max(0, (i / iters_per_second) - (time.time() - start)))


def fcfs_iterator(*iterators: Iterator[T]) -> Generator[tuple[int, T], None, None]:
    with ThreadPoolExecutor(len(iterators)) as p:
        iterators = {i: iter(it) for i, it in enumerate(iterators)}
        futures = {p.submit(next, it): i for i, it in iterators.items()}

        while futures:
            complete, _ = wait(futures.keys(), return_when=FIRST_COMPLETED)

            for future in complete:
                try:
                    ret = future.result()
                    i = futures[future]
                    futures[p.submit(next, iterators[i])] = i
                    yield i, ret
                except StopIteration:
                    pass
                finally:
                    del futures[future]
