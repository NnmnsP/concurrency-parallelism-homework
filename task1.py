import time
import multiprocessing
import concurrent.futures
import threading
from queue import Queue

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def sum_primes(N):
    total = 0
    for i in range(2, N+1):
        if is_prime(i):
            total += i
    return total

def sum_primes_multi_threaded(N):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        primes = list(executor.map(is_prime, range(2, N + 1)))
    return sum(i for i, prime in enumerate(primes, 2) if prime)

def sum_primes_multiprocess(N):
    num_cores = multiprocessing.cpu_count()

    with multiprocessing.Pool(num_cores) as pool:
        terms = pool.map(is_prime, range(2, N + 1))

    return sum(filter(None, terms))

if __name__ == '__main__':
    N = 1000000
    
    start_time = time.time()
    total = sum_primes_multiprocess(N)
    multi_process_time = time.time() - start_time
    print(f"Multi-process time: {multi_process_time:.3f} seconds")

    start_time = time.time()
    total = sum_primes_multi_threaded(N)
    multi_threaded_time = time.time() - start_time
    print(f"Multi-threaded time: {multi_threaded_time:.3f} seconds")
    
# So in Python, using multiprocessing is way faster than threading because you can use more than one CPU core, 
# while threads are stuck with just one. And on top of that, multiprocessing dodges the Global Interpreter Lock
# that stops Python code from running simultaneously in multiple threads.