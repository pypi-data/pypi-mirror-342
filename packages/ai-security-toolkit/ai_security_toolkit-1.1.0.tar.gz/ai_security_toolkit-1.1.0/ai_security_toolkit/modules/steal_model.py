import numpy as np
from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ai_security_toolkit.shared.log_utils import append_report_row, log_metrics

def main():
    try:
        import tensorflow as tf
        from tensorflow.keras.datasets import mnist
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
        from tensorflow.keras.utils import to_categorical
        from tensorflow.keras.models import load_model
    except ImportError:
        print("❌ TensorFlow not found. Run: pip install tensorflow")
        return
    # Step 1: Load original (victim) model
    victim_model = load_model("shared/models/mnist_cnn_model.keras")
    victim_model.trainable = False
    print("✅ Loaded victim model.")

    # Step 2: Generate synthetic dataset to query the victim
    (_, _), (x_test, y_test) = mnist.load_data()
    x_query = x_test[:10000].astype("float32") / 255.0
    x_query = x_query.reshape((-1, 28, 28, 1))

    # Get predictions from victim model
    y_query = victim_model.predict(x_query)
    print("📡 Queried victim model for 10,000 inputs.")

    # Step 3: Train the stolen model (attacker's copycat)
    def build_attacker_model():
        model = Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
            MaxPooling2D((2, 2)),
            Flatten(),
            Dense(64, activation='relu'),
            Dense(10, activation='softmax')
        ])
        model.compile(optimizer='adam',
                    loss='categorical_crossentropy',
                    metrics=['accuracy'])
        return model

    attacker_model = build_attacker_model()

    # Train attacker model using (x_query, y_query)
    print("🧠 Training stolen model on synthetic (input, output) pairs...")
    attacker_model.fit(x_query, y_query, epochs=3, batch_size=64, validation_split=0.1, verbose=2)

    # Save stolen model
    attacker_model.save("shared/models/stolen_model.keras")
    print("💾 Stolen model saved as models/stolen_model.keras")

    # Evaluate stolen model
    y_test_cat = to_categorical(y_test[:10000], 10)
    loss, acc = attacker_model.evaluate(x_query, y_test_cat, verbose=0)
    log_metrics(accuracy=acc)

    # Log results
    header = ["Timestamp", "Method", "Inputs_Used", "Stolen_Accuracy", "Notes"]
    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Black-box Query (MNIST test images)",
        len(x_query),
        round(acc * 100, 2),
        "No access to victim data or labels; used model predictions only"
    ]
    append_report_row(row, header, "logs/stealing_report.csv")

if __name__ == "__main__":
    main()