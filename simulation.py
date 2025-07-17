import random
from enum import Enum, auto
from collections import deque
from typing import List, Optional, Deque


class SimulationState(Enum):
    READY = auto()
    RUNNING = auto()
    FINISHED = auto()
    STOPPED = auto()


class Customer:
    """Represents a customer with arrival, service, and wait times."""
    def __init__(self, customer_id: int, arrival_time: int, service_time: int):
        self.id = customer_id
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.start_service_time: Optional[int] = None
        self.end_service_time: Optional[int] = None
        self.wait_time: Optional[int] = None


class Server:
    """Represents a server that can serve one customer at a time."""
    def __init__(self, server_id: int):
        self.id = server_id
        self.current_customer: Optional[Customer] = None
        self.service_end_time: Optional[int] = None

    def is_free(self) -> bool:
        return self.current_customer is None

    def start_serving(self, customer: Customer, current_time: int):
        self.current_customer = customer
        self.current_customer.start_service_time = current_time
        self.current_customer.wait_time = current_time - customer.arrival_time
        self.service_end_time = current_time + customer.service_time

    def finish_serving(self) -> Optional[Customer]:
        finished_customer = self.current_customer
        if finished_customer:
            finished_customer.end_service_time = self.service_end_time
        self.current_customer = None
        self.service_end_time = None
        return finished_customer


class Simulation:
    """Manages the discrete-event simulation of a queuing system."""
    def __init__(self, duration: int, num_servers: int, max_arrival: int, max_service: int):
        self.duration = duration
        self.num_servers = num_servers
        self.max_arrival = max_arrival
        self.max_service = max_service
        self.reset()

    def reset(self):
        """Resets the simulation to its initial state."""
        self.time = 0
        self.customer_queue: Deque[Customer] = deque()
        self.all_customers: List[Customer] = []
        self.served_customers: List[Customer] = []
        self.customer_id_counter = 1
        self.servers = [Server(i) for i in range(self.num_servers)]
        self.total_busy_time = 0
        self.state = SimulationState.RUNNING
        self._schedule_next_arrival()

    def _schedule_next_arrival(self):
        """Schedules the arrival time of the next customer."""
        self.next_arrival_time = self.time + random.randint(1, self.max_arrival)

    def step(self) -> List[dict]:
        """Advances the simulation by one time step and returns events."""
        events = []

        if self.time >= self.duration and not any(not s.is_free() for s in self.servers):
            self.state = SimulationState.FINISHED
            return events

        # Event 1: A customer arrives
        if self.time == self.next_arrival_time and self.time < self.duration:
            service_time = random.randint(1, self.max_service)
            customer = Customer(self.customer_id_counter, self.time, service_time)
            self.customer_queue.append(customer)
            self.all_customers.append(customer)
            self.customer_id_counter += 1
            events.append({
                'type': 'arrival',
                'message': f"Customer {customer.id} arrived at {self.time} min",
                'customer': customer
            })
            self._schedule_next_arrival()

        # Event 2: A server finishes serving a customer
        for server in self.servers:
            if not server.is_free() and self.time >= server.service_end_time:
                finished_customer = server.finish_serving()
                if finished_customer:
                    self.served_customers.append(finished_customer)
                    events.append({
                        'type': 'finish',
                        'message': f"Customer {finished_customer.id} finished at {self.time} min",
                        'customer': finished_customer
                    })

        # Event 3: A free server starts serving the next customer in the queue
        for server in self.servers:
            if server.is_free() and self.customer_queue:
                customer_to_serve = self.customer_queue.popleft()
                server.start_serving(customer_to_serve, self.time)
                events.append({
                    'type': 'service',
                    'message': f"Customer {customer_to_serve.id} is being served at {self.time} min",
                    'customer': customer_to_serve
                })

        # Update statistics
        for server in self.servers:
            if not server.is_free():
                self.total_busy_time += 1

        self.time += 1
        return events

    def run(self):
        """Runs the simulation until it is finished."""
        while self.state == SimulationState.RUNNING:
            self.step()

    def get_summary(self, stress_threshold: int) -> dict:
        """Generates a summary of the simulation results."""
        if not self.served_customers:
            return {
                'total_served': 0, 'avg_wait': 0, 'max_wait': 0,
                'utilization': 0, 'customers': [], 'insight': "No customers were served."
            }

        wait_times = [c.wait_time for c in self.served_customers if c.wait_time is not None]
        avg_wait = sum(wait_times) / len(wait_times) if wait_times else 0
        max_wait = max(wait_times) if wait_times else 0

        total_available_time = self.time * self.num_servers
        utilization = (self.total_busy_time / total_available_time) * 100 if total_available_time > 0 else 0

        stressed_customers_count = sum(1 for c in self.served_customers if c.wait_time is not None and c.wait_time > stress_threshold)

        return {
            'total_served': len(self.served_customers),
            'avg_wait': avg_wait,
            'max_wait': max_wait,
            'utilization': utilization,
            'stressed_customers': stressed_customers_count,
            'customers': self.all_customers
        }