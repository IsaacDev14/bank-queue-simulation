# plotting.py

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SimulationPlot:
    
    def __init__(self, master):
        plt.style.use('seaborn-v0_8-whitegrid')
        self.fig, self.ax = plt.subplots(figsize=(8, 4), dpi=100)
        self.fig.patch.set_facecolor('#ffffff') # Match control panel background

        #Embed the Figure in a Tkinter Canvas 
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        
        self.customer_ids = []
        self.wait_times = []
        
        self.clear() # Set initial state

    def get_tk_widget(self):
        return self.canvas.get_tk_widget()

    def clear(self):
        self.customer_ids.clear()
        self.wait_times.clear()
        self.ax.clear()
        self.ax.set_title("Customer Wait Time Analysis", fontsize=14, fontweight='bold')
        self.ax.set_xlabel("Customer ID", fontsize=10)
        self.ax.set_ylabel("Wait Time (Minutes)", fontsize=10)
        self.ax.text(0.5, 0.5, "Waiting for simulation data...", 
                     ha='center', va='center', transform=self.ax.transAxes, fontsize=12, color='gray')
        self.canvas.draw()

    def update_plot(self, customer, stress_threshold):
        # If this is the first data point, clear the "waiting" message
        if not self.customer_ids:
            self.ax.clear()
            self.ax.set_title("Customer Wait Time Analysis", fontsize=14, fontweight='bold')
            self.ax.set_xlabel("Customer ID", fontsize=10)
            self.ax.set_ylabel("Wait Time (Minutes)", fontsize=10)

        # Add new data
        self.customer_ids.append(customer.id)
        self.wait_times.append(customer.wait_time)
        
        color = '#c62828' if customer.wait_time > stress_threshold else '#4f46e5' # Red or Indigo
        
        # Add the new bar to the plot
        self.ax.bar(customer.id, customer.wait_time, color=color)
        self.ax.set_xlim(left=0.5, right=max(self.customer_ids) + 0.5)
        
        self.canvas.draw_idle()
