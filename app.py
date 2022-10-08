import timeit
from multiprocessing import Process
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

def sample_fnc(process_index):
    print(f"process index: {process_index} started.")
    num = 0

    for i in range(100000000):
        num += 1
    print(f"process index: {process_index} ended. {num}")

def singleprocess():
    sample_fnc(process_index=0)

def multiprocess():
    process_list = []
    for i in range(1):
        process = Process(
            target=sample_fnc,
            kwargs={'process_index': i})
        process.start()
        process_list.append(process)

    for process in process_list:
        process.join()

def processpool():
    with ProcessPoolExecutor(max_workers=4) as e:
        e.submit(sample_fnc, 1)

def threadpool():
    with ThreadPoolExecutor(max_workers=4) as e:
        e.submit(sample_fnc, 1)

if __name__ == '__main__':
    loop = 1

    result = timeit.timeit(lambda: singleprocess(), number=loop)
    print(f"single {result / loop}")

    result = timeit.timeit(lambda: multiprocess(), number=loop)
    print(f"multiprocess {result / loop}")

    result = timeit.timeit(lambda: processpool(), number=loop)
    print(f"processpool {result / loop}")

    result = timeit.timeit(lambda: threadpool(), number=loop)
    print(f"threadpool {result / loop}")