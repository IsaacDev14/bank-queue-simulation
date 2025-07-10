import random
from graph import plot_wait_times


# class to represent each customer in the simulation
class Customer:
    def __init__(self, id, arrival_time, service_time):
        self.id = id
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.start_time = None
        self.wait_time = None
    
# Simulation Time Loop
def run_simulation(max_arrival_interval=5, max_service_time=10, simulation_time=60):
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

    while time < simulation_time:
        if time == next_arrival:
            service_time = random.randint(1, max_service_time)
            customer = Customer(id=id_counter, arrival_time=time, service_time=service_time)
            queue.append(customer)
            Customers.append(customer)
            print(f"[{time}] Customer {id_counter} arrived (needs {service_time} mins)")
            next_arrival = time + random.randint(1, max_arrival_interval)
            id_counter += 1

        if current_customer is None and queue:
            current_customer = queue.pop(0)
            current_customer.start_time = time
            current_customer.wait_time = time - current_customer.arrival_time
            service_end_time = time + current_customer.service_time
            print(f"{time} Serving Customer {current_customer.id} (waited {current_customer.wait_time} mins)")

        if current_customer and time == service_end_time:
            print(f"[{time}] Finished with Customer {current_customer.id}")
            current_customer = None

        time += 1  


    print("\n=== Simulation Summary ===")
    total_wait_time = 0
    total_served = 0

    for customer in Customers:
        if customer.wait_time is not None:
            total_wait_time += customer.wait_time
            total_served += 1
            print(
                f"Customer {customer.id}: Arrived at {customer.arrival_time}, "
                f"Started at {customer.start_time}, "
                f"Waited {customer.wait_time} mins, "
                f"Service time: {customer.service_time} mins"
            )

    average_wait = total_wait_time / total_served if total_served > 0 else 0
    print(f"\nTotal customers served: {total_served}")
    print(f"Average wait time: {average_wait:.2f} minutes")

    plot_wait_times(Customers)