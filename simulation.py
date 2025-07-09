import random

# Define a class to represent each customer in the simulation
class Customer:
    def __init__(self, id, arrival_time, service_time):
        self.id = id
        self.arrival_time = arrival_time
        self.serrvice_time = service_time
        self.start_time = None
        self.wait_time = None
    
