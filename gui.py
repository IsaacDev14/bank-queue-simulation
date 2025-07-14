# gui.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sv_ttk
import csv
from simulation import Simulation, SimulationState
from plotting  import SimulationPlot
from config import SIMULATION_CONFIG

# --- UI Constants ---
FONT_FAMILY = "Inter"

class Application(tk.Frame):
    """The main GUI application for the simulation."""
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Multi-Server Queueing System Simulation")
        self.master.geometry("1400x900")

        # --- Style Configuration ---
        sv_ttk.set_theme("dark")
        self.pack(fill="both", expand=True, padx=20, pady=20)

        # --- Instance Variables ---
        self.simulation = None
        self.simulation_speed_ms = 25  # Faster update interval

        self._create_widgets()
        self._layout_widgets()

    def _create_widgets(self):
        """Create all the UI widgets."""
        # --- Frames ---
        self.controls_frame = ttk.Frame(self, padding=25)
        self.output_frame = ttk.Frame(self)
        self.plot_frame = ttk.Frame(self.output_frame)
        self.info_frame = ttk.Frame(self.output_frame)
        self.log_frame = ttk.LabelFrame(self.info_frame, text="Simulation Log", padding=15)
        self.summary_frame = ttk.LabelFrame(self.info_frame, text="Live Summary", padding=15)
        self.status_frame = ttk.LabelFrame(self.controls_frame, text="Live Status", padding=15)

        # --- Control Widgets ---
        self._create_control_sliders()
        self.run_button = ttk.Button(self.controls_frame, text="Run Simulation", command=self.run_simulation, style='Accent.TButton')
        self.reset_button = ttk.Button(self.controls_frame, text="Reset", command=self.reset_simulation, state="disabled")
        self.export_button = ttk.Button(self.controls_frame, text="Export Customer Data", command=self.export_to_csv, state="disabled")
        self.theme_switch = ttk.Checkbutton(self.controls_frame, text="Dark Mode", style="Switch.TCheckbutton", command=sv_ttk.toggle_theme)
        self.theme_switch.state(['selected']) # Default to dark theme

        # --- Output Widgets ---
        self.simulation_plot = SimulationPlot(self.plot_frame)
        self.progress_bar = ttk.Progressbar(self.plot_frame, orient="horizontal", mode="determinate")
        
        self._create_log_widgets()
        self._create_summary_widgets()
        self._create_status_widgets()
        
    def _create_control_sliders(self):
        """Create the sliders for simulation parameters."""
        ttk.Label(self.controls_frame, text="Simulation Controls", font=(FONT_FAMILY, 18, "bold"), style='Accent.TLabel').grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")
        
        self.duration_var = self._create_slider("Duration (mins)", 60, 720, SIMULATION_CONFIG['duration'], 1)
        self.servers_var = self._create_slider("Number of Servers", 1, 10, SIMULATION_CONFIG['num_servers'], 2)
        self.arrival_var = self._create_slider("Max Arrival Interval", 1, 15, SIMULATION_CONFIG['max_arrival_interval'], 3)
        self.service_var = self._create_slider("Max Service Time", 5, 25, SIMULATION_CONFIG['max_service_time'], 4)
        self.stress_var = self._create_slider("Stress Threshold (wait)", 1, 30, SIMULATION_CONFIG['stress_threshold'], 5)

    def _create_log_widgets(self):
        """Create the text box for logging events."""
        self.log_box = tk.Text(self.log_frame, height=10, font=(FONT_FAMILY, 10), wrap="word", relief="flat", bd=0)
        log_scrollbar = ttk.Scrollbar(self.log_frame, orient="vertical", command=self.log_box.yview)
        self.log_box.config(yscrollcommand=log_scrollbar.set)
        
        self.log_box.pack(side="left", fill="both", expand=True)
        log_scrollbar.pack(side="right", fill="y")
        
        # Log message tags for color-coding
        self.log_box.tag_configure("arrival", foreground="#3498db")
        self.log_box.tag_configure("service", foreground="#f1c40f")
        self.log_box.tag_configure("finish", foreground="#2ecc71")
        self.log_box.tag_configure("summary", font=(FONT_FAMILY, 10, "bold"))

    def _create_summary_widgets(self):
        """Create the labels for displaying summary metrics."""
        self.metrics = {
            "Avg. Wait": self._create_metric("Avg. Wait Time", "0.0 min"),
            "Max Wait": self._create_metric("Max Wait Time", "0 min"),
            "Served": self._create_metric("Customers Served", "0"),
            "Utilization": self._create_metric("Avg. Utilization", "0%")
        }
        self.insight_label = ttk.Label(self.summary_frame, text="Run simulation to see insights.", wraplength=280, justify="center", font=(FONT_FAMILY, 11, "italic"))

    def _create_status_widgets(self):
        """Create the live status indicators for queue and servers."""
        self.queue_label_var = tk.StringVar(value="Queue: 0")
        ttk.Label(self.status_frame, textvariable=self.queue_label_var, font=(FONT_FAMILY, 14, "bold")).pack(pady=5)
        self.server_status_frame = ttk.Frame(self.status_frame)
        self.server_status_frame.pack(pady=10)
        self.server_labels = []

    def _layout_widgets(self):
        """Arrange all widgets in the main window."""
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.controls_frame.grid(row=0, column=0, sticky="nsw", padx=(0, 20))
        self.output_frame.grid(row=0, column=1, sticky="nsew")

        # Layout within controls_frame
        self.status_frame.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(20, 10))
        self.run_button.grid(row=7, column=0, columnspan=2, pady=(20, 10), sticky="ew")
        self.reset_button.grid(row=8, column=0, columnspan=2, pady=5, sticky="ew")
        self.export_button.grid(row=9, column=0, columnspan=2, pady=5, sticky="ew")
        self.theme_switch.grid(row=10, column=0, columnspan=2, pady=(20, 0), sticky="w")
        
        # Layout within output_frame
        self.output_frame.rowconfigure(0, weight=3)
        self.output_frame.rowconfigure(1, weight=1)
        self.output_frame.columnconfigure(0, weight=1)

        self.plot_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        self.plot_frame.rowconfigure(0, weight=1)
        self.plot_frame.columnconfigure(0, weight=1)
        self.simulation_plot.get_tk_widget().pack(fill="both", expand=True)
        self.progress_bar.pack(fill="x", pady=(5,0))
        
        self.info_frame.grid(row=1, column=0, sticky="nsew")
        self.info_frame.columnconfigure(0, weight=2)
        self.info_frame.columnconfigure(1, weight=1)
        self.info_frame.rowconfigure(0, weight=1)
        
        self.log_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        self.summary_frame.grid(row=0, column=1, sticky="nsew")

        for i, (key, var) in enumerate(self.metrics.items()):
            var['frame'].pack(fill="x", padx=10, pady=5)
        self.insight_label.pack(pady=15, padx=10, fill="x", expand=True)

    def run_simulation(self):
        """Starts a new simulation run."""
        self.reset_simulation()
        self.set_controls_state("disabled")
        
        self.simulation = Simulation(
            duration=self.duration_var.get(),
            num_servers=self.servers_var.get(),
            max_arrival=self.arrival_var.get(),
            max_service=self.service_var.get()
        )
        self.update_server_display(self.servers_var.get())

        self.log_box.delete("1.0", tk.END)
        self.log("=== Simulation Starting ===", "summary")
        self.update_simulation()
        
    def update_simulation(self):
        """The main simulation loop, called repeatedly."""
        if self.simulation.state != SimulationState.RUNNING:
            return

        events = self.simulation.step()
        for event in events:
            self.log(event['message'], event['type'])
            if event['type'] == 'finish':
                summary = self.simulation.get_summary(self.stress_var.get())
                self.simulation_plot.update_plot(
                    event['customer'],
                    summary.get('avg_wait', 0),
                    self.stress_var.get()
                )

        self.update_live_data()
        
        if self.simulation.state == SimulationState.FINISHED:
            self.finish_simulation()
        else:
            self.master.after(self.simulation_speed_ms, self.update_simulation)

    def finish_simulation(self):
        """Finalizes the simulation and displays results."""
        self.log("\n=== Simulation Finished ===", "summary")
        summary = self.simulation.get_summary(self.stress_var.get())
        
        insight_text = "System appears balanced."
        if summary['utilization'] > 90:
            insight_text = "High server utilization may lead to long waits. Consider adding servers."
        elif summary['utilization'] < 40:
            insight_text = "Low server utilization. Consider reducing servers if wait times are low."
        if summary['avg_wait'] > self.stress_var.get():
            insight_text = "Average wait time is above the stress threshold. System is under pressure."

        self.insight_label.config(text=insight_text, font=(FONT_FAMILY, 11, "bold"))
        self.set_controls_state("normal")
        self.reset_button.config(state="normal")
        self.export_button.config(state="normal")

    def reset_simulation(self):
        """Resets the UI and simulation to the initial state."""
        if self.simulation:
            self.simulation.state = SimulationState.STOPPED
        
        self.simulation_plot.clear()
        self.log_box.delete("1.0", tk.END)
        self.log("Adjust controls and click 'Run Simulation'.")
        
        self.update_metric_vars(avg_wait="0.0 min", max_wait="0 min", served="0", util="0%")
        self.insight_label.config(text="Run simulation to see insights.", font=(FONT_FAMILY, 11, "italic"))
        
        self.set_controls_state("normal")
        self.reset_button.config(state="disabled")
        self.export_button.config(state="disabled")
        self.progress_bar['value'] = 0
        self.queue_label_var.set("Queue: 0")

    def update_live_data(self):
        """Updates all live metrics, progress, and status indicators."""
        if not self.simulation or self.simulation.time == 0:
            return

        summary = self.simulation.get_summary(self.stress_var.get())
        self.update_metric_vars(
            avg_wait=f"{summary['avg_wait']:.1f} min",
            max_wait=f"{summary['max_wait']:.0f} min",
            served=f"{summary['total_served']}",
            util=f"{summary['utilization']:.1f}%"
        )
        
        # Update progress bar
        self.progress_bar['value'] = (self.simulation.time / self.simulation.duration) * 100
        
        # Update queue and server status
        self.queue_label_var.set(f"Queue: {len(self.simulation.customer_queue)}")
        for i, server in enumerate(self.simulation.servers):
            state = "Busy" if not server.is_free() else "Free"
            color = "red" if state == "Busy" else "green"
            self.server_labels[i].config(text=f"S{i+1}: {state}", foreground=color)
            
    def export_to_csv(self):
        """Exports detailed customer data to a CSV file."""
        if not self.simulation or not self.simulation.all_customers:
            messagebox.showwarning("No Data", "There is no customer data to export.")
            return

        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not path:
            return
            
        try:
            with open(path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Arrival Time", "Service Time", "Wait Time", "Served"])
                for cust in self.simulation.all_customers:
                    writer.writerow([
                        cust.id, cust.arrival_time, cust.service_time,
                        f"{cust.wait_time:.0f}" if cust.wait_time is not None else "N/A",
                        "Yes" if cust.end_service_time is not None else "No"
                    ])
            messagebox.showinfo("Success", f"Data successfully exported to {path}")
        except IOError as e:
            messagebox.showerror("Export Failed", f"An error occurred: {e}")

    # --- Helper Methods ---
    
    def _create_slider(self, text, from_, to, default, row):
        ttk.Label(self.controls_frame, text=text).grid(row=row, column=0, sticky="w", padx=(0, 10))
        var = tk.IntVar(value=default)
        slider_frame = ttk.Frame(self.controls_frame)
        slider_frame.grid(row=row, column=1, sticky="ew")
        slider = ttk.Scale(slider_frame, from_=from_, to=to, orient="horizontal", variable=var, command=lambda s, v=var: v.set(int(float(s))))
        slider.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Label(slider_frame, textvariable=var, width=4).pack(side="right")
        return var

    def _create_metric(self, label_text, default_value):
        frame = ttk.Frame(self.summary_frame)
        ttk.Label(frame, text=f"{label_text}:").pack(side="left")
        var = tk.StringVar(value=default_value)
        ttk.Label(frame, textvariable=var, font=(FONT_FAMILY, 12, "bold"), style='Accent.TLabel').pack(side="right")
        return {'frame': frame, 'var': var}
    
    def update_server_display(self, num_servers):
        """Clears and recreates the server status labels."""
        for widget in self.server_status_frame.winfo_children():
            widget.destroy()
        self.server_labels = []
        
        cols = 5 # max servers per row
        for i in range(num_servers):
            label = ttk.Label(self.server_status_frame, text=f"S{i+1}: Free", font=(FONT_FAMILY, 11, "bold"), foreground="green")
            label.grid(row=i//cols, column=i%cols, padx=5, pady=2)
            self.server_labels.append(label)

    def update_metric_vars(self, avg_wait, max_wait, served, util):
        self.metrics["Avg. Wait"]['var'].set(avg_wait)
        self.metrics["Max Wait"]['var'].set(max_wait)
        self.metrics["Served"]['var'].set(served)
        self.metrics["Utilization"]['var'].set(util)

    def set_controls_state(self, state):
        for child in self.controls_frame.winfo_children():
            widget_type = child.winfo_class()
            if widget_type in ('TScale', 'TButton'):
                child.config(state=state)
        # Ensure run button is disabled during run, and reset is enabled after
        self.run_button.config(state="disabled" if state == "disabled" else "normal")
        self.reset_button.config(state="normal" if state == "disabled" else "disabled")

    def log(self, message, tag=None):
        self.log_box.insert(tk.END, f"[{self.simulation.time if self.simulation else 0:03d}] {message}\n", tag)
        self.log_box.see(tk.END)