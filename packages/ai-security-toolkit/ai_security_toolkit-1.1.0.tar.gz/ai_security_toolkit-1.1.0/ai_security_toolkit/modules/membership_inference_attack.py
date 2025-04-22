import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ai_security_toolkit.shared.log_utils import save_plot, append_report_row, log_metrics

def main():

    try:
        import tensorflow as tf
    except ImportError:
        print("❌ TensorFlow not found. Run: pip install tensorflow")
        return
    
    # Load model
    model = tf.keras.models.load_model("shared/models/mnist_cnn_model.keras")
    print("✅ Loaded model from .keras file.")

    # Load MNIST
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
    x_train = x_train.astype("float32") / 255.0
    x_test = x_test.astype("float32") / 255.0
    x_train = x_train.reshape((-1, 28, 28, 1))
    x_test = x_test.reshape((-1, 28, 28, 1))

    # Combine train and test for attack simulation
    num_samples = 1000  # from each set
    x_members = x_train[:num_samples]
    x_nonmembers = x_test[:num_samples]

    # Get model predictions (confidence scores)
    y_members_conf = np.max(model.predict(x_members), axis=1)
    y_nonmembers_conf = np.max(model.predict(x_nonmembers), axis=1)

    # Simple threshold-based classifier
    threshold = 0.95  # Can be tuned

    tp = np.sum(y_members_conf > threshold)
    fp = np.sum(y_nonmembers_conf > threshold)
    tn = np.sum(y_nonmembers_conf <= threshold)
    fn = np.sum(y_members_conf <= threshold)

    accuracy = (tp + tn) / (tp + fp + tn + fn)
    precision = tp / (tp + fp + 1e-6)
    recall = tp / (tp + fn + 1e-6)

    log_metrics(accuracy, precision, recall)

    # Visualize confidence distributions
    plt.hist(y_members_conf, bins=30, alpha=0.6, label="Members")
    plt.hist(y_nonmembers_conf, bins=30, alpha=0.6, label="Non-Members")
    plt.axvline(threshold, color='red', linestyle='dashed', label="Threshold")
    plt.title("Model Confidence Distributions")
    plt.xlabel("Max Confidence")
    plt.ylabel("Frequency")
    plt.legend()
    plt.tight_layout()
    save_plot(plt, "logs/mia_confidence_plot.png")

    # Logging
    header = ["Timestamp", "Threshold", "Accuracy", "Precision", "Recall", "Members", "NonMembers"]
    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        threshold,
        round(accuracy * 100, 2),
        round(precision * 100, 2),
        round(recall * 100, 2),
        num_samples,
        num_samples
    ]
    append_report_row(row, header, "logs/membership_report.csv")

if __name__ == "__main__":
    main()

