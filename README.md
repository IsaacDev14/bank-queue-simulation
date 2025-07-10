# Smart Queue Simulator – Stress Test & Optimization Tool

A configurable bank queue simulation system with visual feedback, built using Python, Tkinter, and Matplotlib. It models customer arrivals, service times, wait durations, and provides performance insights based on configurable parameters.

## Features

- GUI interface to adjust simulation settings:
  - Simulation duration (minutes)
  - Maximum customer arrival interval
  - Maximum service time per customer
- Real-time summary log and output panel
- Interactive bar graph showing customer wait times
- Insight analysis on performance under load (e.g. congestion, stress level)
- Red stress indicators for customers with long wait times

## Purpose

This tool was built to simulate real-world queuing behavior and provide a way to:

- Understand how customer wait time increases under traffic stress
- Visualize the effect of changing arrival rates or service durations
- Demonstrate the importance of balancing resource capacity with demand

It is also a learning project for system modeling, data visualization, and decision support tooling.

## Technologies

- Python 3.x
- Tkinter (for GUI)
- Matplotlib & Seaborn (for graphs)
- Object-Oriented Programming (Customer class, modular code)

## How to Run

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/smart-queue-simulator.git
   ```

2. Create a virtual environment and activate it:

   ```
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install required packages:

   ```
   pip install matplotlib seaborn
   ```

4. Run the application:

   ```
   python main.py
   ```

## Folder Structure

```
.
├── gui.py               # Tkinter GUI
├── simulation.py        # Core simulation logic
├── graph.py             # Graph drawing logic
├── main.py              # Entry point
├── README.md            # This file
└── requirements.txt     # Optional: dependencies
```

## Sample Insight

> Simulation ran for 60 minutes.  
> Total customers served: 17  
> 9 of them waited over 10 minutes.  
> System overloaded: Consider reducing arrival rate or adding more tellers.

## License

This project is open for learning and personal use.
