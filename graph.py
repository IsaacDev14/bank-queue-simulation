import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plot_wait_times(customers):
    served_customers = [c for c in customers if c.wait_time is not None]
    ids = [c.id for c in served_customers]
    waits = [c.wait_time for c in served_customers]

    
    STRESS_THRESHOLD = 10

    
    colors = [
        "#e74c3c" if wait > STRESS_THRESHOLD else "#3498db"  # red if too long, blue otherwise
        for wait in waits
    ]

    plt.style.use('seaborn-v0_8-darkgrid')
    sns.set_palette("husl")

    fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
    bars = ax.bar(ids, waits, color=colors, edgecolor='white', linewidth=0.5)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontsize=9)

    ax.set_title("Customer Wait Times Analysis", fontsize=14, pad=20, fontweight='bold')
    ax.set_xlabel("Customer ID", fontsize=12, labelpad=10)
    ax.set_ylabel("Wait Time (Minutes)", fontsize=12, labelpad=10)

    avg_wait = np.mean(waits)
    ax.axhline(avg_wait, color='orange', linestyle='--', alpha=0.8)
    ax.text(len(ids)+0.5, avg_wait, f'Avg: {avg_wait:.1f} min',
            color='orange', va='center', ha='left')

    ax.set_xlim(left=0.5, right=len(ids)+0.5)
    ax.grid(axis='y', alpha=0.4)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_alpha(0.4)
    ax.spines['bottom'].set_alpha(0.4)

    plt.figtext(0.98, 0.02, "Stress ≥ 10 mins shown in red", ha='right', va='bottom', alpha=0.6)
    plt.tight_layout()
    plt.show()
