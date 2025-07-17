# config.py
"""
Centralized configuration for the simulation.
"""

from typing import Dict, Any

# Simulation settings
SIMULATION_CONFIG: Dict[str, Any] = {
    "runs": 5,                  # Number of simulation runs to perform
    "duration": 480,            # Duration of each simulation in minutes (e.g., 8 hours)
    "num_servers": 2,           # Number of available servers
    "max_arrival_interval": 4,  # Maximum time between customer arrivals (uniform distribution)
    "max_service_time": 12,     # Maximum time required to serve a customer (uniform distribution)
    "stress_threshold": 5,      # Wait time in minutes beyond which a customer is considered "stressed"
}

# Reporting settings
REPORTING_CONFIG: Dict[str, Any] = {
    "export_csv": True,
    "export_json": True,
    "show_console": True,
    "summary_csv_path": "simulation_summary.csv",
    "alerts_json_path": "simulation_alerts.json"
}

# Pattern analysis settings
PATTERN_CONFIG: Dict[str, Any] = {
    "high_utilization_threshold": 90.0, # Percentage
    "low_utilization_threshold": 40.0,  # Percentage
    "high_wait_time_threshold": 7,      # Average minutes
    "stress_consistency_threshold": 0.6 # 60% of runs showing stress at the same hour
}