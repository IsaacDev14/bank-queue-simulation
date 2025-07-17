# pattern_engine.py
"""
Analyzes results from multiple simulation runs to identify patterns and suggest improvements.
"""
from collections import Counter
from typing import List, Dict, Any

class PatternEngine:
    """Detects cross-run patterns and generates strategic advice."""
    def __init__(self, summaries: List[Dict], hourly_reports: List[Dict], config: Dict):
        self.summaries = summaries
        self.hourly_reports = hourly_reports
        self.config = config
        self.patterns: Dict[str, Any] = {}

    def analyze(self):
        """Analyzes collected data to find meaningful patterns."""
        num_runs = len(self.summaries)
        if num_runs == 0:
            return {}

        utilizations = [s['utilization'] for s in self.summaries]
        avg_waits = [s['avg_wait'] for s in self.summaries]
        peak_hours = [r.get('peak_arrival_hour') for r in self.hourly_reports if r.get('peak_arrival_hour') is not None]

        self.patterns['avg_utilization'] = sum(utilizations) / num_runs
        self.patterns['avg_wait_time'] = sum(avg_waits) / num_runs
        
        most_common_peak = Counter(peak_hours).most_common(1)
        self.patterns['most_common_peak_hour'] = most_common_peak[0][0] if most_common_peak else "N/A"

        # Check for consistent stress during specific hours
        stressed_hour_counts = Counter()
        for report in self.hourly_reports:
            for hour, data in report.get('hourly_breakdown', {}).items():
                if data.get('stressed', 0) > 0:
                    stressed_hour_counts[hour] += 1
        
        self.patterns['consistently_stressed_hour'] = "None"
        for hour, count in stressed_hour_counts.items():
            if (count / num_runs) >= self.config['stress_consistency_threshold']:
                self.patterns['consistently_stressed_hour'] = hour
                break
        
        return self.patterns

    def suggest(self) -> List[str]:
        
        if not self.patterns:
            return ["No patterns detected to generate suggestions."]
            
        suggestions = []
        if self.patterns['avg_utilization'] > self.config['high_utilization_threshold']:
            suggestions.append(
                "System utilization is consistently high. Consider adding another server to reduce wait times."
            )
        elif self.patterns['avg_utilization'] < self.config['low_utilization_threshold']:
            suggestions.append(
                "System is under-utilized. Consider reducing the number of active servers or reallocating resources."
            )

        if self.patterns['avg_wait_time'] > self.config['high_wait_time_threshold']:
            suggestions.append(
                "Average wait times are high. Look into optimizing service time or adding staff."
            )

        stressed_hour = self.patterns.get('consistently_stressed_hour')
        if isinstance(stressed_hour, int):
            suggestions.append(
                f"Hour {stressed_hour} is a recurring bottleneck. "
                f"Consider adding temporary staff or resources during this period."
            )

        if not suggestions:
            return ["The system appears to be operating efficiently under the current configuration."]
            
        return suggestions