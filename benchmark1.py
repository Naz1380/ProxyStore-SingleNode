 
"""Globus Compute and ProxyStore example."""
from __future__ import annotations

import time
from typing import Any
from proxystore.connectors.file import FileConnector
from proxystore.store import register_store
from proxystore.store.base import Store
from globus_compute_sdk import Client

def something(x):
    from proxystore import proxy
    return proxy.is_resolved(x)

if __name__ == '__main__':
    ### Client implementation
    store: Store[Any] | None = None
    store = Store('file', FileConnector(store_dir='benchmark_temp'))
    register_store(store)
    gcc = Client()

    personal_endpoint = 'c1e8bbd8-5714-40fe-aeb8-6b933d792c8f'
    print(gcc.get_endpoint_status(personal_endpoint))
    x = store.proxy(1)

    func_uuid = gcc.register_function(something)
    task_id = gcc.run(x, endpoint_id=personal_endpoint, function_id=func_uuid)

    start_time = time.perf_counter()

    while True:
        try:
            result = gcc.get_result(task_id)
            break
        except Exception as e:
            continue

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Benchmark completed in {elapsed_time:.2f} seconds.")

    if store is not None:
        store.close()