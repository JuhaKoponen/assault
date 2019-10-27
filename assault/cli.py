from assault.stats import Results
import click
import json
import sys
from typing import TextIO

from .http import assault
from .stats import Results


@click.command()
@click.option("--requests", "-r", default=500, help="Number of requests")
@click.option("--concurrency", "-c", default=1, help="Number of concurrent requests")
@click.option("--json-file", "-j", default=None, help="path to JSON file")
@click.option(
    "--include_data", "-d", is_flag=True, help="Includes data to results JSON file"
)
@click.argument("url")
def cli(requests, concurrency, json_file, include_data, url):
    if json_file:
        try:
            output_file = open(json_file, "w")
        except:
            print(f"Unable to open file {json_file}")
            sys.exit(1)
    total_time, requests_dicts = assault(url, requests, concurrency)
    results = Results(total_time, requests_dicts)
    if json_file:
        results_to_file(results, output_file, include_data)
    else:
        display(results)


def results_to_file(results: Results, output_file: TextIO, include_data: bool):

    # create object to dump into

    dump_object = {
        "successful_requests": results.successful_requests(),
        "slowest": results.slowest(),
        "fastest": results.fastest(),
        "total_time": results.total_time,
        "requests_per_minute": results.requests_per_minute(),
        "requests_per_second": results.requests_per_second(),
    }

    if include_data:
        dump_object["data"] = results.requests

    # write to file
    json.dump(dump_object, output_file)
    output_file.close()
    print("...Done")


def display(results: Results):

    # Print to screen
    print("...Done")
    print("--- Results ---")
    print(f"Successful requests     {results.successful_requests()}")
    print(f"Slowest                 {results.slowest()}")
    print(f"Fastest                 {results.fastest()}")
    print(f"Average                 {results.average_time()}")
    print(f"Total time              {results.total_time}")
    print(f"Requests Per Minute     {results.requests_per_minute()}")
    print(f"Requests Per Second     {results.requests_per_second()}")
