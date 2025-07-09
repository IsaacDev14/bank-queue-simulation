import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plot_wait_times(customers):
    served_customers = [c for c in customers if c.wait_time is not None]
    ids = [c.id for c in served_customers]
    waits = [c.wait_time for c in served_customers]
    
    
    plt.style.use('seaborn-v0_8-darkgrid')
    sns.set_palette("husl")
    
    fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
    
    colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(ids)))
    bars = ax.bar(ids, waits, color=colors, edgecolor='white', linewidth=0.5)
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=9)
    
    
    ax.set_title("Customer Wait Times Analysis", 
                fontsize=14, pad=20, fontweight='bold')
    ax.set_xlabel("Customer ID", fontsize=12, labelpad=10)
    ax.set_ylabel("Wait Time (Minutes)", fontsize=12, labelpad=10)
    
    ax.grid(axis='y', alpha=0.4)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_alpha(0.4)
    ax.spines['bottom'].set_alpha(0.4)
    
    # average line
    avg_wait = np.mean(waits)
    ax.axhline(avg_wait, color='red', linestyle='--', alpha=0.7)
    ax.text(len(ids)+0.5, avg_wait, f'Avg: {avg_wait:.1f} min', 
            color='red', va='center', ha='left')
    
    ax.set_xlim(left=0.5, right=len(ids)+0.5)
    
    plt.figtext(0.95, 0.02, "Queue Simulation Analysis", 
               ha='right', va='bottom', alpha=0.5)
    
    plt.tight_layout()
    plt.show()