import random

# Define a class to represent each customer in the simulation
class Customer:
    def __init__(self, id, arrival_time, service_time):
        self.id = id
        self.arrival_time = arrival_time
        self.serrvice_time = service_time
        self.start_time = None
        self.wait_time = None
    
# Simulation Time Loop
    def run_simulation():
        simulation_time = 60
        max_arrival_interval = 5
        max_service_time = 10

        time = 0
        next_arrival = random.randint(1, max_arrival_interval) 

        queue = []
        Customer = []
        id_counter = 1

        print("== Simulations Begins ===")

