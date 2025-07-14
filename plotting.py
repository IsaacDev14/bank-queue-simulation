# plotting.py
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from simulation import Customer

plt.style.use('seaborn-v0_8-darkgrid') # A style that works well with dark/light themes

class SimulationPlot:
    """Manages the Matplotlib plot embedded in the Tkinter UI."""
    def __init__(self, master):
        self.fig, self.ax = plt.subplots(figsize=(8, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)

        self.customer_ids = []
        self.wait_times = []
        
        self.avg_line = None
        self.stress_line = None

        self.clear()

    def get_tk_widget(self):
        """Returns the Tkinter widget for the plot."""
        return self.canvas.get_tk_widget()

    def clear(self):
        """Clears the plot and resets it to its initial state."""
        self.customer_ids.clear()
        self.wait_times.clear()
        self.ax.clear()

        self.ax.set_title("Customer Wait Time Analysis", fontsize=14, fontweight='bold')
        self.ax.set_xlabel("Customer ID", fontsize=10)
        self.ax.set_ylabel("Wait Time (Minutes)", fontsize=10)
        self.ax.text(0.5, 0.5, "Waiting for simulation data...", ha='center', va='center', transform=self.ax.transAxes, fontsize=12, color='gray')
        
        self.avg_line = self.ax.axhline(0, color='#3498db', linestyle='--', linewidth=1.5, label='Avg. Wait')
        self.stress_line = self.ax.axhline(0, color='#e74c3c', linestyle=':', linewidth=2, label='Stress Threshold')
        
        self.canvas.draw()

    def update_plot(self, customer: Customer, average_wait: float, stress_threshold: int):
        """Adds a new data point to the plot and redraws."""
        if not self.customer_ids: # First data point
            self.ax.clear()
            self.ax.set_title("Customer Wait Time Analysis", fontsize=14, fontweight='bold')
            self.ax.set_xlabel("Customer ID", fontsize=10)
            self.ax.set_ylabel("Wait Time (Minutes)", fontsize=10)

        self.customer_ids.append(customer.id)
        self.wait_times.append(customer.wait_time)

        # Determine bar color based on stress threshold
        color = '#e74c3c' if customer.wait_time > stress_threshold else '#2ecc71'
        self.ax.bar(customer.id, customer.wait_time, color=color)
        
        # Update horizontal lines
        self.avg_line.set_ydata([average_wait, average_wait])
        self.stress_line.set_ydata([stress_threshold, stress_threshold])
        self.ax.legend(handles=[self.avg_line, self.stress_line])
        
        # Adjust plot limits
        self.ax.set_xlim(left=0.5, right=max(self.customer_ids) + 5.5) # Add padding
        self.ax.set_ylim(bottom=0, top=max(self.wait_times) * 1.15) # Add top margin
        
        self.canvas.draw_idle()