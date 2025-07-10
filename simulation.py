# simulation.py
#
# Role: Core Simulation Logic
#
# This module contains the "engine" of the simulation. It's a class that
# manages the state (time, queue, customers) and progression of the simulation.
# Crucially, it contains NO GUI code (Tkinter, plotting). This separation means
# you could run this simulation from a command line, a web server, or any
# other interface, making it highly reusable.

import random
from enum import Enum, auto

class SimulationState(Enum):
    """Represents the current state of the simulation."""
    READY = auto()
    RUNNING = auto()
    FINISHED = auto()
    STOPPED = auto()

class Customer:
    """Represents a single customer with their timing details."""
    def __init__(self, id, arrival_time, service_time):
        self.id = id
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.start_time = None  # Time service begins
        self.wait_time = None   # Time spent in queue

class Simulation:
    """Manages the entire state and logic of the queueing simulation."""

    def __init__(self, duration, max_arrival, max_service):
        self.duration = duration
        self.max_arrival = max_arrival
        self.max_service = max_service
        self.reset()

    def reset(self):
        """Resets the simulation to its initial state."""
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
        """Schedules the arrival time of the next customer."""
        self.next_arrival = self.time + random.randint(1, self.max_arrival)

    def step(self):
        """
        Advances the simulation by a single time step and returns events.
        This is the heart of the simulation engine.
        """
        if self.time >= self.duration:
            self.state = SimulationState.FINISHED
            return []

        events = []

        # Event 1: A new customer arrives
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

        # Event 2: The server is free and can serve the next customer
        if self.current_customer is None and self.queue:
            self.current_customer = self.queue.pop(0)
            self.current_customer.start_time = self.time
            self.current_customer.wait_time = self.time - self.current_customer.arrival_time
            self.service_end_time = self.time + self.current_customer.service_time
            events.append({
                'type': 'service',
                'message': f"[T={self.time}] Serving Customer {self.current_customer.id} (waited {self.current_customer.wait_time} mins). Queue: {len(self.queue)}"
            })

        # Event 3: The server finishes with the current customer
        if self.current_customer and self.time >= self.service_end_time:
            events.append({
                'type': 'finish',
                'message': f"[T={self.time}] Finished with Customer {self.current_customer.id}.",
                'customer': self.current_customer
            })
            self.current_customer = None

        # Update server busy time metric
        if self.current_customer:
            self.total_busy_time += 1
            
        # Advance the simulation clock
        self.time += 1
        return events

    def get_summary(self, stress_threshold):
        """Calculates and returns summary statistics of the simulation."""
        served = [c for c in self.all_customers if c.wait_time is not None]
        
        if not served:
            return {
                'avg_wait': 0, 'max_wait': 0, 'total_served': 0,
                'utilization': 0, 'messages': ["No customers were served."],
                'insight': {'text': 'N/A', 'color': 'black'}
            }

        wait_times = [c.wait_time for c in served]
        avg_wait = sum(wait_times) / len(served)
        max_wait = max(wait_times) if wait_times else 0
        utilization = (self.total_busy_time / self.time) * 100 if self.time > 0 else 0
        
        stressed_customers = [c for c in served if c.wait_time > stress_threshold]
        stress_percent = (len(stressed_customers) / len(served)) * 100

        # Generate summary messages for the log
        summary_messages = [
            f"Total customers served: {len(served)}",
            f"Average wait time: {avg_wait:.2f} minutes",
            f"Maximum wait time: {max_wait} minutes",
            f"Server utilization: {utilization:.2f}%"
        ]

        # Generate a qualitative insight based on performance
        if stress_percent == 0:
            insight = {'text': "Excellent Performance: All customers were served quickly.", 'color': "#2e7d32"} # Green
        elif stress_percent < 25:
            insight = {'text': f"Good Performance: System is mostly smooth, though {len(stressed_customers)} customer(s) experienced long waits.", 'color': "#f9a825"} # Yellow
        elif stress_percent < 50:
            insight = {'text': f"Under Pressure: Almost half of customers waited longer than {stress_threshold} minutes.", 'color': "#ef6c00"} # Orange
        else:
            insight = {'text': "System Overloaded: A majority of customers faced unacceptable wait times.", 'color': "#c62828"} # Red

        return {
            'avg_wait': avg_wait,
            'max_wait': max_wait,
            'total_served': len(served),
            'utilization': utilization,
            'messages': summary_messages,
            'insight': insight
        }
