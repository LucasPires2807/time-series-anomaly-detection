import asyncio
import random
import time

import httpx
import psutil

async def monitor_system(metrics_log: list):
    """A task that runs in parallel to log CPU and memory."""
    try:
        while True:
            metrics_log.append(
                    {
                        "timestamp": time.time(),
                        "cpu_percent": psutil.cpu_percent(interval=None),
                        "memory_percent": psutil.virtual_memory().percent,
                    }
            )
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Monitoring stopped.")
    except Exception as e:
        print(f"Error in monitor: {e}")

class LoadTest:
    def __init__(
        self,
        base_url: str,
        requests_per_user: int,
        concurrent_requests: int
    ):
        self._base_url = base_url
        self._requests_per_user = requests_per_user
        self._concurrent_requests = concurrent_requests

    async def _predict_worker(
        self,
        client: httpx.AsyncClient,
        worker_id: int,
    ):
        """A single worker that sends multiple predict requests."""
        print(f"Worker {worker_id} started...")
        for i in range(self._requests_per_user):
            series_id = f"series_{worker_id}"
            model_version = "v1"
            
            payload = {
                "timestamp": int(time.time()),
                "value": random.uniform(0, 100)
            }
            
            try:
                url = f"{self._base_url}/predict/{series_id}?version={model_version}"
                response = await client.post(url, json=payload, timeout=10.0)
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                print(f"Error for worker {worker_id}: {e.response.status_code} with error message {e.response.content} on request {i}")
            except httpx.RequestError as e:
                print(f"Request failed for worker {worker_id}: {e}")
            else:
                print(f"Successful request.")


    async def _fit_worker(
        self,
        client: httpx.AsyncClient,
        worker_id: int,
    ):
        """A single worker that sends multiple predict requests."""
        print(f"Worker {worker_id} started...")
        for i in range(self._requests_per_user):
            series_id = f"series_{worker_id}"
            base_time = int(time.time()) + worker_id * 1000
            payload = {
                "data": [
                    {
                        "timestamp": base_time + i,
                        "value": random.uniform(0, 100)
                    }
                    for i in range(100)
                ]
            }

            try:
                url = f"{self._base_url}/fit/{series_id}"
                response = await client.post(url, json=payload, timeout=10.0)
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                print(f"Error for worker {worker_id}: {e.response.status_code} with error message {e.response.content} on request {i}")
            except httpx.RequestError as e:
                print(f"Request failed for worker {worker_id}: {e}")
            else:
                print(f"Successful request.")


    async def load_test(self):
        system_metrics_log = []
        
        monitor_task = asyncio.create_task(monitor_system(system_metrics_log))
        
        start_time = time.time()
        
        async with httpx.AsyncClient() as client:
            predict_tasks = [self._predict_worker(client, i) for i in range(self._concurrent_requests)]
            fit_tasks = [self._fit_worker(client, i) for i in range(self._concurrent_requests)]
            all_tasks = [*predict_tasks, *fit_tasks]
            
            await asyncio.gather(*all_tasks)
            
        end_time = time.time()

        monitor_task.cancel()
        await asyncio.sleep(0)

        duration = end_time - start_time
        total_requests = 2 * self._concurrent_requests * self._requests_per_user
        rps = total_requests / duration if duration > 0 else 0
        
        return {
            "duration_seconds": duration,
            "total_requests": total_requests,
            "requests_per_second": rps,
            "system_metrics": system_metrics_log,
        }
