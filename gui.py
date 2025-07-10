# gui.py
#
# Role: Manages the Graphical User Interface (GUI)
#
# This module uses Tkinter to build the application window, including all the
# controls (sliders, buttons) and output areas (log, summary, chart).
# It acts as the "controller" that connects user actions to the simulation
# logic and visual feedback.

import tkinter as tk
from tkinter import ttk
from simulation import Simulation, SimulationState
from plotting import SimulationPlot
import datetime # For timestamps in the log

# --- Constants for Styling ---
BG_COLOR = "#e0e7ee"  # Light grey-blue background
CONTROLS_BG = "#ffffff"  # White for control and summary panels
LOG_BG = "#263238"    # Dark blue-grey for log
LOG_FG = "#eceff1"    # Light grey for log text
PRIMARY_ACCENT = "#4f46e5" # Indigo for primary buttons/highlights
SECONDARY_ACCENT = "#6366f1" # Lighter indigo for active states
FONT_FAMILY = "Inter" # Modern font choice

class Application(tk.Frame):
    """Main application class for the simulation GUI."""

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Dynamic Queueing System Simulation")
        self.master.geometry("1200x800")
        self.master.configure(bg=BG_COLOR)
        self.pack(fill="both", expand=True, padx=15, pady=15) # Add padding to the main frame

        self.simulation = None
        self.simulation_plot = None
        self.simulation_speed_ms = 50  # Speed of the simulation loop in milliseconds

        self._create_widgets()
        self._layout_widgets()

    def _create_widgets(self):
        """Create all the UI widgets for the application."""
        # --- Control Frame ---
        self.controls_frame = tk.Frame(self, bg=CONTROLS_BG, padx=25, pady=25, relief="flat", bd=0)
        self.controls_frame.columnconfigure(1, weight=1)

        # --- Output Frame ---
        self.output_frame = tk.Frame(self, bg=BG_COLOR, padx=0, pady=0) # Padding handled by main frame
        self.output_frame.rowconfigure(0, weight=3) # Chart row - more space
        self.output_frame.rowconfigure(1, weight=1) # Log/Summary row
        self.output_frame.columnconfigure(0, weight=3) # Chart/Log column
        self.output_frame.columnconfigure(1, weight=1) # Summary column

        # --- Control Widgets ---
        self._create_control_widgets()

        # --- Plotting Widget ---
        # The SimulationPlot needs to be initialized with its parent frame
        self.simulation_plot = SimulationPlot(self.output_frame)

        # --- Log Widget ---
        self._create_log_widgets()
        
        # --- Summary Widget ---
        self._create_summary_widgets()


    def _create_control_widgets(self):
        """Create the widgets for the control panel."""
        ttk.Label(self.controls_frame, text="Simulation Controls", 
                  font=(FONT_FAMILY, 18, "bold"), background=CONTROLS_BG, 
                  foreground=PRIMARY_ACCENT).grid(row=0, column=0, columnspan=3, pady=(0, 30), sticky="w")
        
        self.duration_var = self._create_slider("Simulation Duration (mins)", 30, 300, 120, 1)
        self.arrival_var = self._create_slider("Max Arrival Interval (mins)", 1, 10, 4, 2)
        self.service_var = self._create_slider("Max Service Time (mins)", 1, 20, 8, 3)
        self.stress_var = self._create_slider("High Wait Threshold (mins)", 1, 30, 10, 4)

        # Buttons with improved styling
        self.run_button = ttk.Button(self.controls_frame, text="Run Simulation", command=self.run_simulation, style="Accent.TButton")
        self.reset_button = ttk.Button(self.controls_frame, text="Reset", command=self.reset_simulation, state="disabled", style="TButton")

    def _create_log_widgets(self):
        """Create the widgets for the simulation log."""
        log_frame = tk.Frame(self.output_frame, bg=BG_COLOR, relief="flat")
        log_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 15), pady=(15, 0))
        
        ttk.Label(log_frame, text="Simulation Log", font=(FONT_FAMILY, 16, "bold"), 
                  background=BG_COLOR, foreground=PRIMARY_ACCENT).pack(anchor="w", pady=(0, 10))
        
        # Use a scrolled text widget for better UX
        self.log_box = tk.Text(log_frame, height=15, width=80, bg=LOG_BG, fg=LOG_FG, 
                               font=(FONT_FAMILY, 10), wrap="word", relief="flat", bd=0,
                               insertbackground="white") # Cursor color
        self.log_box.pack(fill="both", expand=True, pady=(0,0))
        
        # Add a scrollbar
        log_scrollbar = ttk.Scrollbar(self.log_box, command=self.log_box.yview)
        log_scrollbar.pack(side="right", fill="y")
        self.log_box.config(yscrollcommand=log_scrollbar.set)

        self.log_box.tag_configure("arrival", foreground="#81d4fa") # Light Blue
        self.log_box.tag_configure("service", foreground="#ffe082") # Light Yellow
        self.log_box.tag_configure("finish", foreground="#a7d9b5") # Light Green
        self.log_box.tag_configure("summary", foreground="#ffffff", font=(FONT_FAMILY, 10, "bold"))
        self.log_box.tag_configure("timestamp", foreground="#9e9e9e", font=(FONT_FAMILY, 9)) # Grey for timestamps
        
        self.log(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Adjust controls and click 'Run Simulation'.", "summary")

    def _create_summary_widgets(self):
        """Create the widgets for the summary panel."""
        summary_frame = tk.Frame(self.output_frame, bg=CONTROLS_BG, relief="flat", bd=0)
        summary_frame.grid(row=1, column=1, sticky="nsew", padx=(15, 0), pady=(15, 0))
        summary_frame.grid_propagate(False) # Prevent frame from shrinking to content size
        
        ttk.Label(summary_frame, text="Live Summary", font=(FONT_FAMILY, 16, "bold"), 
                  background=CONTROLS_BG, foreground=PRIMARY_ACCENT).pack(pady=(15, 10))
        
        # Use a grid for metrics for better alignment
        metrics_container = tk.Frame(summary_frame, bg=CONTROLS_BG)
        metrics_container.pack(pady=10, padx=20, fill="x")
        metrics_container.columnconfigure(0, weight=1)
        metrics_container.columnconfigure(1, weight=1)

        self.metrics = {
            "Avg. Wait": self._create_metric(metrics_container, "Avg. Wait", "0.0", row=0),
            "Max Wait": self._create_metric(metrics_container, "Max Wait", "0", row=1),
            "Served": self._create_metric(metrics_container, "Served", "0", row=2),
            "Utilization": self._create_metric(metrics_container, "Utilization", "0%", row=3)
        }

        self.insight_label = ttk.Label(summary_frame, text="Run simulation for insights.", 
                                       wraplength=250, background=CONTROLS_BG, justify="center", 
                                       font=(FONT_FAMILY, 11, "italic"), foreground="#616161") # Dark grey italic
        self.insight_label.pack(pady=(20, 20), padx=15, fill="x", expand=True)

    def _layout_widgets(self):
        """Layout the main frames of the application."""
        self.grid_columnconfigure(0, weight=0) # Controls frame fixed width
        self.grid_columnconfigure(1, weight=1) # Output frame expands
        self.grid_rowconfigure(0, weight=1)
        
        self.controls_frame.grid(row=0, column=0, sticky="nsw", padx=(0, 15), pady=0)
        self.output_frame.grid(row=0, column=1, sticky="nsew", padx=(15, 0), pady=0)
        
        # Plotting widget takes full width at the top of the output frame
        self.simulation_plot.get_tk_widget().grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(0, 15))
        
        # Place buttons at the bottom of the controls frame
        self.run_button.grid(row=5, column=0, columnspan=3, pady=(30, 10), sticky="ew", padx=10)
        self.reset_button.grid(row=6, column=0, columnspan=3, sticky="ew", padx=10)

    def run_simulation(self):
        """Starts the simulation process."""
        self.reset_simulation() # Clear previous state
        self.set_controls_state("disabled")

        self.simulation = Simulation(
            duration=self.duration_var.get(),
            max_arrival=self.arrival_var.get(),
            max_service=self.service_var.get()
        )
        self.log_box.delete("1.0", tk.END)
        self.log(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] === Simulation Begins ===", "summary")
        self.log(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Duration: {self.simulation.duration} mins | Arrival: 1-{self.simulation.max_arrival} mins | Service: 1-{self.simulation.max_service} mins")
        
        self.update_simulation() # Start the loop

    def update_simulation(self):
        """The main simulation loop, called repeatedly."""
        if self.simulation is None or self.simulation.state != SimulationState.RUNNING:
            return

        events = self.simulation.step()
        for event in events:
            self.log(event['message'], event['type'])
            if event['type'] == 'finish':
                self.simulation_plot.update_plot(event['customer'], self.stress_var.get())
        
        self.update_summary_metrics()

        if self.simulation.state == SimulationState.FINISHED:
            self.finish_simulation()
        else:
            self.master.after(self.simulation_speed_ms, self.update_simulation)

    def finish_simulation(self):
        """Finalizes the simulation and displays summary insights."""
        self.log(f"\n[{datetime.datetime.now().strftime('%H:%M:%S')}] === Simulation Summary ===", "summary")
        summary = self.simulation.get_summary(self.stress_var.get())
        
        for msg in summary['messages']:
            self.log(msg)
            
        self.insight_label.config(text=summary['insight']['text'], foreground=summary['insight']['color'], font=(FONT_FAMILY, 12, "bold"))
        self.set_controls_state("normal")
        self.reset_button.config(state="normal")
    
    def reset_simulation(self):
        """Resets the UI and simulation state to the beginning."""
        if self.simulation:
            self.simulation.state = SimulationState.STOPPED
            self.simulation = None
            
        self.simulation_plot.clear()
        self.log_box.delete("1.0", tk.END)
        self.log(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Adjust controls and click 'Run Simulation'.", "summary")
        
        for key, var in self.metrics.items():
            var.set("0" if key != "Avg. Wait" else "0.0")
        self.metrics["Utilization"].set("0%")
        
        self.insight_label.config(text="Run simulation for insights.", foreground="#616161", font=(FONT_FAMILY, 11, "italic"))
        self.set_controls_state("normal")
        self.run_button.config(state="normal") # Ensure run button is enabled on reset
        self.reset_button.config(state="disabled")

    def update_summary_metrics(self):
        """Updates the live summary panel during the simulation."""
        if not self.simulation: return

        summary = self.simulation.get_summary(self.stress_var.get())
        self.metrics["Avg. Wait"].set(f"{summary['avg_wait']:.1f}")
        self.metrics["Max Wait"].set(f"{summary['max_wait']}")
        self.metrics["Served"].set(f"{summary['total_served']}")
        self.metrics["Utilization"].set(f"{summary['utilization']:.0f}%")

    # --- Helper methods for creating widgets ---
    def _create_slider(self, text, from_, to, default, row):
        """Creates a labeled slider and returns its variable."""
        ttk.Label(self.controls_frame, text=text, background=CONTROLS_BG, 
                  font=(FONT_FAMILY, 11, "bold")).grid(row=row, column=0, sticky="w", pady=(15,5))
        var = tk.IntVar(value=default)
        
        slider_frame = tk.Frame(self.controls_frame, bg=CONTROLS_BG)
        slider_frame.grid(row=row, column=1, columnspan=2, sticky="ew", pady=(15,5))
        
        slider = ttk.Scale(slider_frame, from_=from_, to=to, orient="horizontal", variable=var, 
                           command=lambda s, v=var: v.set(int(float(s))), style="Custom.Horizontal.TScale")
        slider.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        value_label = ttk.Label(slider_frame, textvariable=var, background=CONTROLS_BG, 
                                font=(FONT_FAMILY, 11, "bold"), width=4, anchor="e")
        value_label.pack(side="right")
        
        return var

    def _create_metric(self, parent, label_text, default_value, row):
        """Creates a single metric display for the summary panel."""
        frame = tk.Frame(parent, bg=CONTROLS_BG)
        frame.grid(row=row, column=0, columnspan=2, pady=5, padx=0, sticky="ew")
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        
        ttk.Label(frame, text=f"{label_text}:", background=CONTROLS_BG, 
                  font=(FONT_FAMILY, 11)).grid(row=0, column=0, sticky="w")
        var = tk.StringVar(value=default_value)
        ttk.Label(frame, textvariable=var, background=CONTROLS_BG, 
                  font=(FONT_FAMILY, 13, "bold"), foreground=PRIMARY_ACCENT).grid(row=0, column=1, sticky="e")
        return var

    def set_controls_state(self, state):
        """Enable or disable all control widgets."""
        for child in self.controls_frame.winfo_children():
            # Check if it's a label or a frame holding a slider, and skip if it's the title label
            if isinstance(child, ttk.Label) and child.cget("text") == "Simulation Controls":
                continue
            if isinstance(child, (ttk.Scale, ttk.Button)):
                child.config(state=state)
            elif isinstance(child, tk.Frame): # Handle slider frames
                for sub_child in child.winfo_children():
                    if isinstance(sub_child, (ttk.Scale, ttk.Button)):
                        sub_child.config(state=state)
        # Explicitly handle buttons as they are laid out separately
        self.run_button.config(state="disabled" if state == "disabled" else "normal")
        # Reset button state is managed by run/reset functions, not this general function

    def log(self, message, tag=None):
        """Logs a message to the text box with an optional style tag and timestamp."""
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        self.log_box.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.log_box.insert(tk.END, message + '\n', tag)
        self.log_box.see(tk.END)


def launch_gui():
    """Initializes and runs the Tkinter application."""
    root = tk.Tk()
    
    # --- Style Configuration ---
    style = ttk.Style(root)
    style.theme_use('clam') # 'clam' theme provides a more modern base

    # General Label Style
    style.configure("TLabel", background=BG_COLOR, font=(FONT_FAMILY, 10), foreground="#333333") # Darker text
    
    # Frame Styles
    style.configure("TFrame", background=BG_COLOR)
    # Specific frame background for controls and summary
    style.configure("Controls.TFrame", background=CONTROLS_BG)

    # Button Styles
    style.configure("Accent.TButton", 
                    font=(FONT_FAMILY, 12, "bold"), 
                    foreground="white", 
                    background=PRIMARY_ACCENT,
                    relief="flat", # Flat button look
                    padding=10, # More padding
                    borderwidth=0,
                    focusthickness=0) # Remove focus border
    style.map("Accent.TButton", 
              background=[('active', SECONDARY_ACCENT)], # Lighter on hover
              foreground=[('disabled', '#cccccc')], # Grey out text when disabled
              bordercolor=[('!disabled', PRIMARY_ACCENT)]) # Border color for consistency
    
    style.configure("TButton", 
                    font=(FONT_FAMILY, 12), 
                    background="#e0e0e0", # Light grey for default buttons
                    foreground="#333333",
                    relief="flat",
                    padding=10,
                    borderwidth=0,
                    focusthickness=0)
    style.map("TButton", 
              background=[('active', '#d0d0d0')],
              foreground=[('disabled', '#999999')])

    # Scale (Slider) Styles
    style.configure("Horizontal.TScale", background=CONTROLS_BG, troughcolor="#e0e0e0", sliderrelief="flat")
    style.map("Horizontal.TScale", 
              background=[('active', PRIMARY_ACCENT)], # Slider thumb color on active
              troughcolor=[('active', "#d0d0d0")]) # Trough color on active

    # Custom style for sliders to ensure consistent appearance
    style.configure("Custom.Horizontal.TScale", 
                    background=CONTROLS_BG, 
                    troughcolor="#e0e0e0", # Light grey trough
                    sliderrelief="flat",
                    sliderthickness=18) # Make slider thumb a bit thicker
    style.map("Custom.Horizontal.TScale", 
              background=[('active', PRIMARY_ACCENT), ('!disabled', PRIMARY_ACCENT)], # Active and enabled thumb color
              troughcolor=[('active', "#d0d0d0"), ('!disabled', "#d0d0d0")]) # Active and enabled trough color


    app = Application(master=root)
    root.mainloop()
