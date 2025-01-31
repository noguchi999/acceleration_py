import timeit, math
from multiprocessing import Process
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

WORKER_INDEXES = [0,1,2,3]
PROC_LIST = list(range(10000000))

def sample_fnc(process_index):
    print(f"process index: {process_index} started.")
    num = 0

    for i in PROC_LIST:
        num += 1
    print(f"process index: {process_index} ended. {num}")

def task(process_index):
    print(f"process index: {process_index} started.")
    num = 0

    chunk_size = math.floor(len(PROC_LIST) / len(WORKER_INDEXES))
    if process_index == 0:
        chunk = PROC_LIST[0:chunk_size]
    else:
        chunk = PROC_LIST[chunk_size * process_index - 1: chunk_size * (process_index + 1)]
    for i in chunk:
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
    with ProcessPoolExecutor(max_workers=len(WORKER_INDEXES)) as e:
        e.map(task, WORKER_INDEXES)

def threadpool():
    with ThreadPoolExecutor(max_workers=len(WORKER_INDEXES)) as e:
        e.map(task, WORKER_INDEXES)

if __name__ == '__main__':
    loop = 1

    result = timeit.timeit(lambda: singleprocess(), number=loop)
    print(f"single {result / loop}")

    # result = timeit.timeit(lambda: multiprocess(), number=loop)
    # print(f"multiprocess {result / loop}")

    result = timeit.timeit(lambda: processpool(), number=loop)
    print(f"processpool {result / loop}")

    # result = timeit.timeit(lambda: threadpool(), number=loop)
    # print(f"threadpool {result / loop}")