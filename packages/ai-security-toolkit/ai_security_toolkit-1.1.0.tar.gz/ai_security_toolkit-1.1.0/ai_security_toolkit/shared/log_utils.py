import pandas as pd
import matplotlib.pyplot as plt
import os
import csv

def save_report(data: dict, filepath: str):
    """
    Save a dictionary or list of dicts to a CSV file.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False)
    print(f"[✓] Report saved to {filepath}")

def append_report_row(row: list, header: list, filepath: str):
    import csv, os
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    file_exists = os.path.isfile(filepath)
    with open(filepath, "a", newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(header)
        writer.writerow(row)
    print(f"[✓] Row logged to {filepath}")


def save_plot(fig, filepath: str):
    """
    Save a matplotlib figure to PNG.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    fig.savefig(filepath, bbox_inches='tight')
    print(f"[✓] Plot saved to {filepath}")

def log_metrics(accuracy=None, precision=None, recall=None):
    """
    Print evaluation metrics in a readable format.
    """
    print("\n📊 Metrics Summary")
    if accuracy is not None:
        print(f"  Accuracy:  {accuracy * 100:.2f}%")
    if precision is not None:
        print(f"  Precision: {precision * 100:.2f}%")
    if recall is not None:
        print(f"  Recall:    {recall * 100:.2f}%")
