# simulation.py
import random
from enum import Enum, auto

class SimulationState(Enum):
    READY = auto()
    RUNNING = auto()
    FINISHED = auto()
    STOPPED = auto()

class Customer:
    def __init__(self, id, arrival_time, service_time):
        self.id = id
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.start_time = None
        self.wait_time = None

class Simulation:
    def __init__(self, duration, max_arrival, max_service, log_events=False):
        self.duration = duration
        self.max_arrival = max_arrival
        self.max_service = max_service
        self.log_events = log_events
        self.reset()

    def reset(self):
        self.time = 0
        self.queue = []
        self.all_customers = []
        self.id_counter = 1
        self.current_customer = None
        self.service_end_time = 0
        self.total_busy_time = 0
        self.state = SimulationState.RUNNING
        self._set_next_arrival()

    def _set_next_arrival(self):
        self.next_arrival = self.time + random.randint(1, self.max_arrival)

    def step(self):
        if self.time >= self.duration:
            self.state = SimulationState.FINISHED
            return []

        events = []

        # 1. Customer arrives
        if self.time == self.next_arrival:
            service_time = random.randint(1, self.max_service)
            customer = Customer(self.id_counter, self.time, service_time)
            self.queue.append(customer)
            self.all_customers.append(customer)
            events.append({
                'type': 'arrival',
                'message': f"[T={self.time}] Customer {self.id_counter} arrived (needs {service_time} mins). Queue: {len(self.queue)}"
            })
            self.id_counter += 1
            self._set_next_arrival()

        # 2. Start serving next in queue
        if self.current_customer is None and self.queue:
            self.current_customer = self.queue.pop(0)
            self.current_customer.start_time = self.time
            self.current_customer.wait_time = self.time - self.current_customer.arrival_time
            self.service_end_time = self.time + self.current_customer.service_time
            events.append({
                'type': 'service',
                'message': f"[T={self.time}] Serving Customer {self.current_customer.id} (waited {self.current_customer.wait_time} mins). Queue: {len(self.queue)}"
            })

        # 3. Finish serving
        if self.current_customer and self.time >= self.service_end_time:
            events.append({
                'type': 'finish',
                'message': f"[T={self.time}] Finished with Customer {self.current_customer.id}.",
                'customer': self.current_customer
            })
            self.current_customer = None

        if self.current_customer:
            self.total_busy_time += 1

        if self.log_events:
            for e in events:
                print(e['message'])

        self.time += 1
        return events

    def run(self):
        while self.state == SimulationState.RUNNING:
            self.step()

    def get_summary(self, stress_threshold=5):
        served = [c for c in self.all_customers if c.wait_time is not None]

        if not served:
            return {
                'avg_wait': 0, 'max_wait': 0, 'total_served': 0,
                'utilization': 0, 'messages': ["No customers were served."],
                'insight': {'text': 'N/A', 'color': 'black'}
            }

        wait_times = [c.wait_time for c in served]
        avg_wait = sum(wait_times) / len(served)
        max_wait = max(wait_times)
        utilization = (self.total_busy_time / self.time) * 100 if self.time > 0 else 0

        stressed_customers = [c for c in served if c.wait_time > stress_threshold]
        stress_percent = (len(stressed_customers) / len(served)) * 100

        summary_messages = [
            f"Total customers served: {len(served)}",
            f"Average wait time: {avg_wait:.2f} minutes",
            f"Maximum wait time: {max_wait} minutes",
            f"Server utilization: {utilization:.2f}%"
        ]

        if stress_percent == 0:
            insight = {'text': "Excellent: All customers served promptly.", 'color': "#2e7d32"}
        elif stress_percent < 25:
            insight = {'text': f"Good: Only {len(stressed_customers)} had long waits.", 'color': "#f9a825"}
        elif stress_percent < 50:
            insight = {'text': "Fair: Nearly half waited too long.", 'color': "#ef6c00"}
        else:
            insight = {'text': "Poor: System overloaded.", 'color': "#c62828"}

        return {
            'avg_wait': avg_wait,
            'max_wait': max_wait,
            'total_served': len(served),
            'utilization': utilization,
            'messages': summary_messages,
            'insight': insight,
            'customers': self.all_customers  # For analytics
        }
