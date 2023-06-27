from __future__ import annotations

import time
from typing import Any
from proxystore.connectors.file import FileConnector
from proxystore.store import register_store
from proxystore.store.base import Store
from globus_compute_sdk import Client
from kafka import KafkaProducer, KafkaConsumer

def something(x):
    from kafka import KafkaProducer, KafkaConsumer
    from proxystore import proxy
    return proxy.is_resolved(x)

if __name__ == '__main__':
    
    bootstrap_servers = 'localhost:9092'
    topic = 'benchmark_topic'
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
    consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_servers, group_id='benchmark_group')

    store: Store[Any] | None = None
    store = Store('file', FileConnector(store_dir='benchmark_temp'))
    register_store(store)
    gcc = Client()

    personal_endpoint = 'c1e8bbd8-5714-40fe-aeb8-6b933d792c8f'
    print(gcc.get_endpoint_status(personal_endpoint))
    x = store.proxy(1)

    func_uuid = gcc.register_function(something)

    producer.send(topic, b'start_benchmark')

    start_time = time.perf_counter()

    task_id = gcc.run(x, endpoint_id=personal_endpoint, function_id=func_uuid)

    while True:
        for message in consumer:
            if message.value == b'start_benchmark':
                break

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"Benchmark completed in {elapsed_time:.2f} seconds.")

        producer.send(topic, b'benchmark_completed')

        break

    if store is not None:
        store.close()



    ### Same with Executor over Client
    #personal_endpoint = '692646d4-63f2-4e9e-866f-3085b0fb220e'
    # with Executor(endpoint_id=personal_endpoint) as gce:
    #     fut = gce.submit(something)
    #     print(fut.result())
    #end = time.perf_counter()
    #elapsed_time = end - start
#print("Time taken to send data:", elapsed_time, "seconds")





#create a function for the uuid for proxy
#add proxy to the function argument
#pass proxy from my computer to the globus comp
#call proxy
#time the amount that it takes to pass proxy from my comp to globus


#ask about libaries/packages
#gcc clinet authorization
