import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from simulation import Customer

plt.style.use('seaborn-v0_8-darkgrid')


class SimulationPlot:
    """Manages the Matplotlib plot embedded in the Tkinter UI."""

    VISIBLE_RANGE = 50  # Show only the last 50 customers

    def __init__(self, master):
        self.fig, self.ax = plt.subplots(figsize=(8, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)

        self.customer_ids = []
        self.wait_times = []

        self._setup_initial_plot()
        self.clear()

    def _setup_initial_plot(self):
        """Sets up the static elements of the plot."""
        self.ax.set_title("Customer Wait Time Analysis", fontsize=14, fontweight='bold')
        self.ax.set_xlabel("Customer ID", fontsize=10)
        self.ax.set_ylabel("Wait Time (Minutes)", fontsize=10)
        self.ax.text(
            0.5, 0.5,
            "Waiting for simulation data...",
            ha='center', va='center',
            transform=self.ax.transAxes,
            fontsize=12,
            color='gray'
        )

    def get_tk_widget(self):
        """Returns the Tkinter widget for the plot."""
        return self.canvas.get_tk_widget()

    def clear(self):
        """Clears the plot data and resets it to its initial state."""
        self.customer_ids.clear()
        self.wait_times.clear()
        self.ax.clear()
        self._setup_initial_plot()
        self.canvas.draw()

    def update_plot(self, customer: Customer, average_wait: float, stress_threshold: int):
        """Adds a new data point to the plot and redraws."""
        if self.ax.texts and self.ax.texts[0].get_text() == "Waiting for simulation data...":
            self.ax.texts[0].remove()

        # Store full data
        self.customer_ids.append(customer.id)
        self.wait_times.append(customer.wait_time)

        # Get only the most recent visible range
        ids_to_show = self.customer_ids[-self.VISIBLE_RANGE:]
        waits_to_show = self.wait_times[-self.VISIBLE_RANGE:]

        self.ax.cla()
        self.ax.set_title("Customer Wait Time Analysis", fontsize=14, fontweight='bold')
        self.ax.set_xlabel("Customer ID", fontsize=10)
        self.ax.set_ylabel("Wait Time (Minutes)", fontsize=10)

        # Color bars
        bar_colors = ['#e74c3c' if wt > stress_threshold else '#2ecc71' for wt in waits_to_show]
        bar_heights = [wt if wt > 0 else 0.2 for wt in waits_to_show]
        self.ax.bar(ids_to_show, bar_heights, color=bar_colors)

        if ids_to_show:
            x_min = min(ids_to_show)
            x_max = max(ids_to_show)

            self.ax.axhline(average_wait, color='#3498db', linestyle='--', linewidth=1.5,
                            label=f'Avg. Wait ({average_wait:.1f} min)')
            self.ax.axhline(stress_threshold, color='#e74c3c', linestyle=':', linewidth=2,
                            label=f'Stress Threshold ({stress_threshold} min)')
            self.ax.legend(loc="upper right", fontsize=9)

            self.ax.set_xlim(left=x_min - 1, right=x_max + 2)
            max_wait = max(waits_to_show) if waits_to_show else 1
            self.ax.set_ylim(bottom=0, top=max(1, max_wait * 1.2))

            if all(wt == 0 for wt in waits_to_show):
                self.ax.text(
                    0.5, 0.9,
                    "All recent customers served instantly",
                    transform=self.ax.transAxes,
                    ha='center',
                    va='center',
                    fontsize=10,
                    color='gray'
                )

        self.ax.tick_params(axis='x', rotation=0)
        self.canvas.draw_idle()
