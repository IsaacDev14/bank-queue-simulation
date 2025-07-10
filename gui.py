import tkinter as tk
from simulation import run_simulation
import sys
import io


class OutputRedirector(io.StringIO): # redirect print() output to GUI text box
    def __init__(self, output_widget):
        super().__init__()
        self.output_widget = output_widget

    def write(self, text):
        self.output_widget.insert(tk.END, text)
        self.output_widget.see(tk.END)

    def flush(self):
        pass

# tag color
def tagged_log(widget, message, tag=None):
    widget.insert(tk.END, message + '\n', tag)
    widget.see(tk.END)

# Function called when "Run Simulation" button is clicked
def run_from_gui(arrival_var, service_var, duration_var, output_box):
    output_box.delete("1.0", tk.END)  
    sys.stdout = OutputRedirector(output_box)  # Redirect stdout to GUI

    try:
        arrival_rate = int(arrival_var.get())
        max_service = int(service_var.get())
        duration = int(duration_var.get())

        run_simulation(arrival_rate, max_service, duration, output_box)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        sys.stdout = sys.__stdout__  # Restore after run


def launch_gui():
    window = tk.Tk()
    window.title("Bank Queue Simulation")
    window.geometry("500x550")
    window.config(bg="#f0f0f0")

    tk.Label(window, text="Bank Queue Simulation", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)

    # Duration
    tk.Label(window, text="Simulation Duration (minutes)", bg="#f0f0f0").pack()
    duration_var = tk.StringVar(value="60")
    tk.Entry(window, textvariable=duration_var, font=("Arial", 12)).pack(pady=5)

    # Arrival Interval
    tk.Label(window, text="Max Arrival Interval (1 = fast, 5 = slow)", bg="#f0f0f0").pack()
    arrival_var = tk.StringVar(value="5")
    tk.OptionMenu(window, arrival_var, "1", "2", "3", "4", "5").pack(pady=5)

    # Max Service Time
    tk.Label(window, text="Max Service Time (minutes)", bg="#f0f0f0").pack()
    service_var = tk.StringVar(value="10")
    tk.OptionMenu(window, service_var, "3", "5", "7", "10", "15").pack(pady=5)

    # Output box
    output_box = tk.Text(window, height=12, width=65, font=("Courier", 10), wrap="word")
    output_box.pack(pady=10)

    # Scrollbar
    scrollbar = tk.Scrollbar(window, command=output_box.yview)
    output_box.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    
    output_box.tag_configure("green", foreground="green")
    output_box.tag_configure("yellow", foreground="orange")
    output_box.tag_configure("red", foreground="red")

    
    tk.Button(
        window, text="Run Simulation",
        command=lambda: run_from_gui(arrival_var, service_var, duration_var, output_box),
        font=("Arial", 12), bg="#4CAF50", fg="white", padx=20, pady=10
    ).pack(pady=10)

    window.mainloop()
