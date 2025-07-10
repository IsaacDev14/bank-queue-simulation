import tkinter as tk
from simulation import run_simulation

def run_from_gui(arrival_var, service_var, duration_var):
    arrival_rate = int(arrival_var.get())
    max_service = int(service_var.get())
    duration = int(duration_var.get())

    run_simulation(arrival_rate, max_service, duration)

def launch_gui():
    window = tk.Tk()
    window.title("Bank Queue Simulation")
    window.geometry("400x350")
    window.config(bg="#f0f0f0")

    tk.Label(window, text="Bank Queue Simulation", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)

    # Simulation Duration
    tk.Label(window, text="Simulation Duration (mins)", bg="#f0f0f0").pack()
    duration_var = tk.StringVar(value="60")
    tk.Entry(window, textvariable=duration_var, font=("Arial", 12)).pack(pady=5)

    # Max Arrival Interval
    tk.Label(window, text="Customer Arrival Interval (1 = fast, 5 = slow)", bg="#f0f0f0").pack()
    arrival_var = tk.StringVar(value="5")
    tk.OptionMenu(window, arrival_var, "1", "2", "3", "4", "5").pack(pady=5)

    # Max Service Time
    tk.Label(window, text="Max Service Time per Customer", bg="#f0f0f0").pack()
    service_var = tk.StringVar(value="10")
    tk.OptionMenu(window, service_var, "3", "5", "7", "10", "15").pack(pady=5)

    
    tk.Button(window, text="Run Simulation",
              command=lambda: run_from_gui(arrival_var, service_var, duration_var),
              font=("Arial", 12), bg="#4CAF50", fg="white", padx=20, pady=10).pack(pady=20)

    window.mainloop()
