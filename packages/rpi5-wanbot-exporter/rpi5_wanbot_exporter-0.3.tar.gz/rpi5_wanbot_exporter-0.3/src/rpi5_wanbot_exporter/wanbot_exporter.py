import argparse
import concurrent.futures
import contextlib
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from rpi5_wanbot_exporter.lib.bbkcli_metrics import get_bbk_metrics
from rpi5_wanbot_exporter.lib.ping_metrics import get_ping_metrics
from rpi5_wanbot_exporter.lib.rpi5_metrics import get_pi5_fan_speed, get_pi5_cpu_temperature, get_memory_utilization, get_memory_free, get_memory_total, get_disk_free_space, get_disk_total_space
from time import sleep


def get_metrics():

    # Get metrics
    metrics = [get_pi5_fan_speed,
               get_pi5_cpu_temperature,
               get_memory_utilization,
               get_memory_free,
               get_memory_total,
               get_disk_free_space,
               get_disk_total_space,
               get_bbk_metrics,
               get_ping_metrics]

    # Using ProcessPoolExecutor to execute tasks concurrently (ideal for CPU-bound tasks)
    jobs = list()
    metric_results = dict()
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:

        for metric in metrics:
            # Submit multiple tasks to the pool and get results
            jobs.append(executor.submit(metric))

        for job in jobs:
            result = job.result()

            if result:
                for metric_name, metric_values in result.items():
                    metric_results[metric_name] = metric_values

    return metric_results


class CustomCollector(object):
    def __init__(self):
        pass

    def collect(self):
        metrics = get_metrics()

        for metric_name, metric_values in metrics.items():

            # for key, value in metric_values.items():
            #     print(f' {key} - {value}')

            yield GaugeMetricFamily(name=metric_values['metric_name'],
                                    documentation=metric_values['help_text'],
                                    value=metric_values['measurement'],
                                    unit=metric_values['unit'])


def run_server(port=8878):
    start_http_server(port)

    # Unregister default collectors
    for name in list(REGISTRY._names_to_collectors.values()):
        with contextlib.suppress(KeyError):
            REGISTRY.unregister(name)

    # Register requested collectors
    REGISTRY.register(CustomCollector())
    while True:
        sleep(1)


def start():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Prometheus Exporter for Raspberry Pi Metrics")
    parser.add_argument("--port", type=int,
                        default=8878, help="Port to run the web server on")
    # parser.add_argument("--speedlimit", type=int,
    #                     default=5, help="Maximum up and download speed in MBit/s")
    # parser.add_argument("--speedtestduration", type=int,
    #                     default=2, help="Measurement time in seconds")

    args = parser.parse_args()

    # Start server
    run_server(port=args.port)


if __name__ == "__main__":
    start()
