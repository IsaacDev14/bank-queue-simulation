# pattern_engine.py

from collections import Counter

class PatternEngine:
    def __init__(self, summary_list, hourly_reports):
        self.summaries = summary_list  # list of summary dicts from simulation
        self.hourly_reports = hourly_reports  # list of analytics dicts
        self.patterns = {}

    def analyze(self):
        total_runs = len(self.summaries)
        peak_hours = [r.get('peak_hour_by_arrival') for r in self.hourly_reports if r.get('peak_hour_by_arrival') is not None]
        total_served = [s['total_served'] for s in self.summaries]
        utilizations = [s['utilization'] for s in self.summaries]
        avg_waits = [s['avg_wait'] for s in self.summaries]

        most_common_peak = Counter(peak_hours).most_common(1)
        self.patterns['most_common_peak_hour'] = most_common_peak[0][0] if most_common_peak else None
        self.patterns['avg_customers_served'] = sum(total_served) / total_runs if total_runs else 0
        self.patterns['avg_utilization'] = sum(utilizations) / total_runs if total_runs else 0
        self.patterns['avg_wait_time'] = sum(avg_waits) / total_runs if total_runs else 0

        # Identify consistency of stress in the same hour
        hour_stress_counts = Counter()
        for report in self.hourly_reports:
            for hour, data in report['hourly_breakdown'].items():
                if data['stress'] >= 3:  # arbitrary stress threshold
                    hour_stress_counts[hour] += 1

        if hour_stress_counts:
            consistent_stress_hour = hour_stress_counts.most_common(1)[0]
            self.patterns['repeated_stress_hour'] = consistent_stress_hour[0]
            self.patterns['stress_consistency'] = consistent_stress_hour[1] / total_runs
        else:
            self.patterns['repeated_stress_hour'] = None
            self.patterns['stress_consistency'] = 0

        return self.patterns

    def suggest(self):
        suggestions = []
        if self.patterns['avg_wait_time'] > 5:
            suggestions.append("Consider reducing customer service time or increasing staff.")
        if self.patterns['avg_utilization'] < 30:
            suggestions.append("System appears under-utilized. Consider adjusting opening hours.")
        if self.patterns['stress_consistency'] >= 0.5:
            hr = self.patterns['repeated_stress_hour']
            suggestions.append(f"Stress repeatedly occurs at hour {hr}. Add a temporary assistant during that period.")

        if not suggestions:
            suggestions.append("System is performing well across all runs.")

        return suggestions
