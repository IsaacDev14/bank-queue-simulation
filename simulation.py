import random
from graph import plot_wait_times

def run_simulation(max_arrival_interval=5, max_service_time=10, simulation_time=60, output_box=None):
    class Customer:
        def __init__(self, id, arrival_time, service_time):
            self.id = id
            self.arrival_time = arrival_time
            self.service_time = service_time
            self.start_time = None
            self.wait_time = None

    def log(msg, tag=None):
        if output_box:
            from gui import tagged_log
            tagged_log(output_box, msg, tag)
        else:
            print(msg)

    time = 0
    next_arrival = random.randint(1, max_arrival_interval)
    queue = []
    Customers = []
    id_counter = 1
    current_customer = None
    service_end_time = 0

    log("=== Simulation Begins ===", "yellow")
    log(f"Duration: {simulation_time} mins | Arrival: 1–{max_arrival_interval} mins | Service: 1–{max_service_time} mins\n")

    while time < simulation_time:
        if time == next_arrival:
            service_time = random.randint(1, max_service_time)
            customer = Customer(id=id_counter, arrival_time=time, service_time=service_time)
            queue.append(customer)
            Customers.append(customer)
            log(f"[{time}] Customer {id_counter} arrived (needs {service_time} mins)")
            next_arrival = time + random.randint(1, max_arrival_interval)
            id_counter += 1

        if current_customer is None and queue:
            current_customer = queue.pop(0)
            current_customer.start_time = time
            current_customer.wait_time = time - current_customer.arrival_time
            service_end_time = time + current_customer.service_time
            log(f"{time} Serving Customer {current_customer.id} (waited {current_customer.wait_time} mins)")

        if current_customer and time == service_end_time:
            log(f"[{time}] Finished with Customer {current_customer.id}")
            current_customer = None

        time += 1

    # Summary
    log("\n=== Simulation Summary ===", "yellow")
    total_wait_time = 0
    total_served = 0
    for customer in Customers:
        if customer.wait_time is not None:
            total_wait_time += customer.wait_time
            total_served += 1
            log(
                f"Customer {customer.id}: Arrived at {customer.arrival_time}, "
                f"Started at {customer.start_time}, "
                f"Waited {customer.wait_time} mins, "
                f"Service time: {customer.service_time} mins"
            )

    average_wait = total_wait_time / total_served if total_served > 0 else 0
    log(f"\nTotal customers served: {total_served}", "yellow")
    log(f"Average wait time: {average_wait:.2f} minutes", "yellow")

    # === Smart Insight
    STRESS_THRESHOLD = 10
    stressed = [c for c in Customers if c.wait_time and c.wait_time > STRESS_THRESHOLD]
    stress_percent = (len(stressed) / total_served) * 100 if total_served > 0 else 0

    log("\n--- System Insights ---", "yellow")
    if stress_percent == 0:
        log("Great performance: All customers were served quickly.", "green")
    elif stress_percent < 25:
        log("Mostly smooth. A few customers experienced long waits.", "yellow")
    elif stress_percent < 50:
        log("Performance under pressure. Almost half waited too long.", "yellow")
    else:
        log("System overloaded: Consider reducing arrival rate or adding more tellers.", "red")

    log(f"{len(stressed)} out of {total_served} customers waited over {STRESS_THRESHOLD} mins ({stress_percent:.1f}%)", "yellow")

    plot_wait_times(Customers)
