import random

# Define a class to represent each customer in the simulation
class Customer:
    def __init__(self, id, arrival_time, service_time):
        self.id = id
        self.arrival_time = arrival_time
        self.service_time = service_time
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
    Customers = []
    id_counter = 1

    print("== Simulations Begins ===")


    # Add Customer Arrival Logic to the Loop
    while time < simulation_time:
        if time == next_arrival:
            service_time = random.randint(1, max_service_time)

            # create a new customer and add to the queue
            customer = Customer(id=id_counter, arrival_time=time, service_time=service_time)
            queue.append(customer)
            Customers.append(customer)

            print(f"Customer {id_counter} arrived at {time} with service time {service_time}" )

            #schedule the next customer arrival
            next_arrival = time + random.randint(1, max_arrival_interval)
            id_counter += 1

        time += 1



