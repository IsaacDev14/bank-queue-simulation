# exporter.py

import csv
import json
from datetime import datetime

def export_summary_csv(summaries, filepath="summary.csv"):
    if not summaries:
        return

    keys = ['Run', 'Avg Wait', 'Max Wait', 'Total Served', 'Utilization']
    with open(filepath, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(keys)
        for i, summary in enumerate(summaries, 1):
            writer.writerow([
                i,
                f"{summary['avg_wait']:.2f}",
                summary['max_wait'],
                summary['total_served'],
                f"{summary['utilization']:.2f}"
            ])

def export_alerts_json(patterns, suggestions, filepath="alerts.json"):
    data = {
        "generated_at": datetime.now().isoformat(),
        "patterns": patterns,
        "suggestions": suggestions
    }
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)

def print_console_dashboard(summary, pattern, suggestions):
    print("\n=== Simulation Summary ===")
    for msg in summary['messages']:
        print(f"- {msg}")
    print(f"\nInsight: {summary['insight']['text']}")

    print("\n=== Detected Pattern Across Runs ===")
    for k, v in pattern.items():
        print(f"- {k.replace('_', ' ').capitalize()}: {v}")

    print("\n=== Suggested Improvements ===")
    for s in suggestions:
        print(f"• {s}")
