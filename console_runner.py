# console_runner.py
"""
This script runs the multi-simulation analysis in the console.
It orchestrates the simulation process, from running multiple simulations
to analyzing the results and generating reports.
"""
from simulation import Simulation
from analytics import analyze_hourly
from pattern_engine import PatternEngine
from reporting import export_summary_to_csv, export_patterns_to_json, print_console_dashboard
from config import SIMULATION_CONFIG, REPORTING_CONFIG, PATTERN_CONFIG

def run_and_analyze():
    """
    Executes the full simulation and analysis pipeline based on configuration.
    """
    summaries = []
    hourly_reports = []

    print(f"Starting simulation with {SIMULATION_CONFIG['runs']} runs...")
    
    for i in range(SIMULATION_CONFIG['runs']):
        print(f"Running simulation #{i + 1}...")
        sim = Simulation(
            duration=SIMULATION_CONFIG['duration'],
            num_servers=SIMULATION_CONFIG['num_servers'],
            max_arrival=SIMULATION_CONFIG['max_arrival_interval'],
            max_service=SIMULATION_CONFIG['max_service_time']
        )
        sim.run()

        # Get results
        summary = sim.get_summary(SIMULATION_CONFIG['stress_threshold'])
        summary['stress_threshold'] = SIMULATION_CONFIG['stress_threshold']
        hourly_report = analyze_hourly(
            summary['customers'],
            SIMULATION_CONFIG['duration'],
            SIMULATION_CONFIG['stress_threshold']
        )
        
        summaries.append(summary)
        hourly_reports.append(hourly_report)
    
    print("\nAll simulations completed. Analyzing patterns...")
    
    # Analyze patterns across all runs
    engine = PatternEngine(summaries, hourly_reports, PATTERN_CONFIG)
    patterns = engine.analyze()
    suggestions = engine.suggest()

    # Generate reports
    if REPORTING_CONFIG['export_csv']:
        export_summary_to_csv(summaries, REPORTING_CONFIG['summary_csv_path'])
        
    if REPORTING_CONFIG['export_json']:
        export_patterns_to_json(patterns, suggestions, REPORTING_CONFIG['alerts_json_path'])

    if REPORTING_CONFIG['show_console']:
        print_console_dashboard(summaries[-1], patterns, suggestions, SIMULATION_CONFIG['runs'])

if __name__ == "__main__":
    # This allows running the console analysis directly if needed
    run_and_analyze()
