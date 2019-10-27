from typing import List, Dict
from statistics import mean


class Results:
    """
    Results handles calculating statistics based on a list of requests were made
    Here's ans example of what the information will look like:
    
    Successful requests     500
    Slowest                 0.010s
    Fastest                 0.001s
    Average                 0.003s
    Total time              0.620s
    Requests Per Minute     48360
    Requests Per Second     806
    """

    def __init__(self, total_time: float, requests: List[Dict]):
        self.total_time = total_time
        self.requests = sorted(requests, key=lambda r: r["response_time"])

    def slowest(self) -> float:
        """
        Returns the slowest request's completion time

        >>> requests = Results(10.6, [{
        ...     'status_code': 200,
        ...     'response_time': 3.4
        ... }, {
        ...     'status_code': 500,
        ...     'response_time': 6.1
        ... }, {
        ...     'status_code': 200,
        ...     'response_time': 1.04
        ... }])
        >>> requests.slowest()
        6.1
        """
        return self.requests[-1]["response_time"]

    def fastest(self) -> float:
        """
        Returns the fastest request's completion time

        >>> requests = Results(10.6, [{
        ...     'status_code': 200,
        ...     'response_time': 3.4
        ... }, {
        ...     'status_code': 500,
        ...     'response_time': 6.1
        ... }, {
        ...     'status_code': 200,
        ...     'response_time': 1.04
        ... }])
        >>> requests.fastest()
        1.04
        """
        return self.requests[0]["response_time"]

    def average_time(self) -> float:
        """
        Returns the average request completion time

        >>> requests = Results(10.6, [{
        ...     'status_code': 200,
        ...     'response_time': 3.4
        ... }, {
        ...     'status_code': 500,
        ...     'response_time': 6.1
        ... }, {
        ...     'status_code': 200,
        ...     'response_time': 1.04
        ... }])
        >>> requests.average_time()
        3.513333333333333
        """
        return mean([r["response_time"] for r in self.requests])

    def successful_requests(self) -> int:
        """
        Returns the average request completion time

        >>> requests = Results(10.6, [{
        ...     'status_code': 200,
        ...     'response_time': 3.4
        ... }, {
        ...     'status_code': 500,
        ...     'response_time': 6.1
        ... }, {
        ...     'status_code': 200,
        ...     'response_time': 1.04
        ... }])
        >>> requests.successful_requests()
        2
        """
        return len([r for r in self.requests if r["status_code"] in range(200, 299)])

    def requests_per_minute(self) -> int:
        """
        Returns the number of requests made per minute

        >>> results = Results(10.6, [{
        ...     'status_code': 200,
        ...     'response_time': 3.4
        ... }, {
        ...     'status_code': 500,
        ...     'response_time': 6.1
        ... }, {
        ...     'status_code': 200,
        ...     'response_time': 1.04
        ... }])
        >>> results.requests_per_minute()
        17
        """
        # 3 / 10.6 = x / 60
        # 60 * 3 / 10.6 = x
        return round(60 * len(self.requests) / self.total_time)

    def requests_per_second(self) -> int:
        """
        Returns the number of requests made per second

        >>> results = Results(3.5, [{
        ...     'status_code': 200,
        ...     'response_time': 3.4
        ... }, {
        ...     'status_code': 500,
        ...     'response_time': 2.9
        ... }, {
        ...     'status_code': 200,
        ...     'response_time': 1.04
        ... }, {
        ...     'status_code': 200,
        ...     'response_time': 0.4
        ... }])
        >>> results.requests_per_second()
        1
        """
        # 4 / 3.5 = x / 1
        return round(len(self.requests) / self.total_time)
