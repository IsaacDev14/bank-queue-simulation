from collections import defaultdict
from typing import List, Dict, Any
from simulation import Customer

def analyze_hourly(customers: List[Customer], total_duration: int, stress_threshold: int) -> Dict[str, Any]:
    """
    Analyzes customer data to provide an hourly breakdown of key metrics.
    """
    hourly_summary = defaultdict(lambda: {
        'arrivals': 0, 'served': 0, 'total_wait': 0, 'stressed': 0
    })

    for customer in customers:
        hour = customer.arrival_time // 60
        hourly_summary[hour]['arrivals'] += 1
        if customer.wait_time is not None:
            hourly_summary[hour]['served'] += 1
            hourly_summary[hour]['total_wait'] += customer.wait_time
            if customer.wait_time > stress_threshold:
                hourly_summary[hour]['stressed'] += 1

    avg_waits = {
        hour: data['total_wait'] / data['served'] if data['served'] > 0 else 0
        for hour, data in hourly_summary.items()
    }
    
    peak_arrival_hour = None
    if hourly_summary:
        peak_arrival_hour = max(hourly_summary.items(), key=lambda item: item[1]['arrivals'])[0]

    return {
        'total_hours': total_duration // 60,
        'peak_arrival_hour': peak_arrival_hour,
        'hourly_breakdown': dict(hourly_summary),
        'average_waits_per_hour': avg_waits
    }