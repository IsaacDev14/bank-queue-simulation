# reporting.py
"""
Handles exporting simulation results to various formats and printing summaries.
"""
import csv
import json
from datetime import datetime
from typing import List, Dict, Any

def export_summary_to_csv(summaries: List[Dict], filepath: str):
    """Exports a list of run summaries to a CSV file."""
    if not summaries:
        return
    
    keys = ['Run', 'Total Served', 'Avg Wait (min)', 'Max Wait (min)', 'Server Utilization (%)']
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(keys)
        for i, summary in enumerate(summaries, 1):
            writer.writerow([
                i,
                summary['total_served'],
                f"{summary['avg_wait']:.2f}",
                f"{summary['max_wait']:.2f}",
                f"{summary['utilization']:.2f}"
            ])
    print(f"Summary exported to {filepath}")

def export_patterns_to_json(patterns: Dict, suggestions: List[str], filepath: str):
    """Exports detected patterns and suggestions to a JSON file."""
    data = {
        "report_generated_at": datetime.now().isoformat(),
        "detected_patterns": patterns,
        "actionable_suggestions": suggestions
    }
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Alerts and suggestions exported to {filepath}")

def print_console_dashboard(
    last_summary: Dict,
    patterns: Dict,
    suggestions: List[str],
    run_count: int
):
    """Prints a formatted dashboard of the latest run and overall patterns."""
    print("\n" + "="*50)
    print("QUEUING SIMULATION DASHBOARD")
    print("="*50)

    # --- Last Run Summary ---
    print(f"\n--- Summary of Last Run (Run #{run_count}) ---")
    if last_summary:
        print(f"  - Customers Served:   {last_summary['total_served']}")
        print(f"  - Average Wait Time:  {last_summary['avg_wait']:.2f} minutes")
        print(f"  - Max Wait Time:      {last_summary['max_wait']:.2f} minutes")
        print(f"  - Server Utilization: {last_summary['utilization']:.2f}%")
        print(f"  - Stressed Customers: {last_summary['stressed_customers']} (waited > {last_summary.get('stress_threshold', 'N/A')} min)")
    else:
        print("  No data available for the last run.")

    # --- Cross-Run Pattern Analysis ---
    print("\n--- Patterns Detected Across All Runs ---")
    if patterns:
        print(f"  - Avg. Server Utilization: {patterns.get('avg_utilization', 0):.2f}%")
        print(f"  - Avg. Wait Time:          {patterns.get('avg_wait_time', 0):.2f} minutes")
        print(f"  - Most Common Peak Hour:   {patterns.get('most_common_peak_hour', 'N/A')}")
        print(f"  - Consistent Stress Hour:  {patterns.get('consistently_stressed_hour', 'None')}")
    else:
        print("  No patterns were analyzed.")
        
    # --- Actionable Suggestions ---
    print("\n--- Actionable Suggestions ---")
    if suggestions:
        for suggestion in suggestions:
            print(f"  • {suggestion}")
    else:
        print("  • No specific actions recommended at this time.")
    print("="*50 + "\n")