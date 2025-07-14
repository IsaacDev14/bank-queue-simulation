# analytics.py

from collections import defaultdict

def analyze_hourly(customers, total_time, stress_threshold):
    """
    Analyzes customer flow and wait times across hourly segments.
    """
    hour_summary = defaultdict(lambda: {'arrivals': 0, 'served': 0, 'stress': 0, 'total_wait': 0})
    stressed_customers = 0

    for customer in customers:
        hour = customer.arrival_time // 60
        hour_summary[hour]['arrivals'] += 1
        if customer.wait_time is not None:
            hour_summary[hour]['served'] += 1
            hour_summary[hour]['total_wait'] += customer.wait_time
            if customer.wait_time > stress_threshold:
                hour_summary[hour]['stress'] += 1
                stressed_customers += 1

    peak_hour = max(hour_summary.items(), key=lambda x: x[1]['arrivals'])[0] if hour_summary else None
    avg_wait_per_hour = {
        hour: (data['total_wait'] / data['served']) if data['served'] > 0 else 0
        for hour, data in hour_summary.items()
    }

    report = {
        'total_hours': total_time // 60,
        'peak_hour_by_arrival': peak_hour,
        'hourly_breakdown': dict(hour_summary),
        'average_waits': avg_wait_per_hour,
        'total_stressed': stressed_customers
    }

    return report
