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
    except ImportError:
        print("❌ TensorFlow not found. Run: pip install tensorflow")
        return
    
    # Build a simple CNN
    def build_model():
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

    # Load and preprocess MNIST
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train = x_train.astype("float32") / 255.0
    x_test = x_test.astype("float32") / 255.0
    x_train = x_train.reshape((-1, 28, 28, 1))
    x_test = x_test.reshape((-1, 28, 28, 1))

    # Save original training labels for comparison
    y_train_clean = y_train.copy()

    # Poisoning: Flip 10% of labels from class 1 → 7
    num_poison = int(0.10 * len(y_train))
    indices_to_poison = np.where(y_train == 1)[0][:num_poison]
    y_train_poisoned = y_train.copy()
    y_train_poisoned[indices_to_poison] = 7

    # Convert to categorical
    y_train_clean_cat = to_categorical(y_train_clean, 10)
    y_train_poisoned_cat = to_categorical(y_train_poisoned, 10)
    y_test_cat = to_categorical(y_test, 10)

    # Train clean model
    print("🧼 Training clean model...")
    model_clean = build_model()
    model_clean.fit(x_train, y_train_clean_cat, epochs=3, batch_size=64, validation_split=0.1, verbose=2)
    clean_loss, clean_acc = model_clean.evaluate(x_test, y_test_cat, verbose=0)

    # Train poisoned model
    print("💉 Training poisoned model (1→7 flipped)...")
    model_poison = build_model()
    model_poison.fit(x_train, y_train_poisoned_cat, epochs=3, batch_size=64, validation_split=0.1, verbose=2)
    poison_loss, poison_acc = model_poison.evaluate(x_test, y_test_cat, verbose=0)

    # Log both models
    header = ["Timestamp", "Model", "Attack_Type", "Poisoned_Classes", "Train_Size", "Test_Accuracy"]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    row_clean = [timestamp, "Clean_CNN", "None", "None", len(y_train), round(clean_acc, 4)]
    row_poisoned = [timestamp, "Poisoned_CNN", "Label Flip (1→7)", "1→7", len(y_train), round(poison_acc, 4)]

    append_report_row(row_clean, header, "logs/poisoning_report.csv")
    append_report_row(row_poisoned, header, "logs/poisoning_report.csv")

    # Print summary
    print("\n📊 Summary:")
    log_metrics(accuracy=clean_acc)
    print(f"⚠️  Poisoned Model Accuracy: {poison_acc * 100:.2f}%")
    print("📄 Report saved to: logs/poisoning_report.csv")

if __name__ == "__main__":
    main()
