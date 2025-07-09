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

    current_customer = None
    service_end_time = 0

    print("== Simulations Begins ===")


    # Add Customer Arrival Logic to the Loop
    while time < simulation_time:
        if time == next_arrival:
            service_time = random.randint(1, max_service_time)

            # create a new customer and add to the queue
            customer = Customer(id=id_counter, arrival_time=time, service_time=service_time)
            queue.append(customer)
            Customers.append(customer)

            print(f"[{time}] Customer {id_counter} arrived (needs {service_time} mins)")

            #schedule the next customer arrival
            next_arrival = time + random.randint(1, max_arrival_interval)
            id_counter += 1

        # if no one is being served and there's someone  in the queue
        if current_customer is None and queue:
            current_customer = queue.pop(0)
            current_customer.start_time = time
            current_customer.wait_time = time - current_customer.arrival_time
            service_end_time = time + current_customer.service_time

            print(f"{time} Servinf Customer {current_customer.id} (waited {current_customer.wait_time} mins)")

        if current_customer and time == service_end_time:
            print(f"[{time}] Finished with Customer {current_customer.id}")
            current_customer = None

        time += 1

# Teller Service Logic



