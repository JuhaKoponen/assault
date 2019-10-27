import asyncio
from codecs import register
import time
import os
import requests

# function to make network call
def fetch(url):
    """
    Make request and return the results
    """
    started_at = time.monotonic()
    response = requests.get(url)
    response_time = time.monotonic() - started_at
    return {"status_code": response.status_code, "response_time": response_time}


# Function to process work from queue
async def worker(name, queue, results):
    """
    A function to take unmake request from a queue and
    perform the work and then add results to the results list.
    """
    loop = asyncio.get_event_loop()
    while True:
        url = await queue.get()
        if os.getenv("DEBUG"):
            print(f"{name} - Fetching {url}")
        future_result = loop.run_in_executor(None, fetch, url)
        result = await future_result
        results.append(result)
        queue.task_done()


# Function to distribute work items to queue
async def distribute_work(url, requests, concurrency, results) -> float:
    """
    Divide up the work into branches and collect the final results
    """
    queue = asyncio.Queue()

    for _ in range(requests):
        queue.put_nowait(url)

    tasks = []
    for i in range(concurrency):
        task = asyncio.create_task(worker(f"worker-{i+1}", queue, results))
        tasks.append(task)

    started_at = time.monotonic()
    await queue.join()
    total_time = time.monotonic() - started_at

    for task in tasks:
        task.cancel()

    return total_time


def assault(url, requests, concurrency):
    """
    Entrypoint to making requests
    """
    results = []
    total_time = asyncio.run(distribute_work(url, requests, concurrency, results))
    return (total_time, results)
