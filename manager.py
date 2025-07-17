# manager.py

from simulation import Simulation
from analytics import analyze_hourly
from pattern_engine import PatternEngine
from reporting import export_summary_csv, export_alerts_json, print_console_dashboard

def run_simulations(
    runs=6,
    duration=360,           # 6 hours
    max_arrival=5,
    max_service=10,
    stress_threshold=5,
    export=True,
    show_console=True
):
    summaries = []
    hourly_reports = []

    for i in range(runs):
        sim = Simulation(duration, max_arrival, max_service)
        while sim.state == sim.state.RUNNING:
            sim.step()

        summary = sim.get_summary(stress_threshold)
        report = analyze_hourly(summary['customers'], duration, stress_threshold)

        summaries.append(summary)
        hourly_reports.append(report)

    engine = PatternEngine(summaries, hourly_reports)
    patterns = engine.analyze()
    suggestions = engine.suggest()

    if export:
        export_summary_csv(summaries)
        export_alerts_json(patterns, suggestions)

    if show_console:
        print_console_dashboard(summaries[-1], patterns, suggestions)


if __name__ == "__main__":
    run_simulations()
