import numpy as np
import matplotlib.pyplot as plt
import os
import random
from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ai_security_toolkit.shared.log_utils import append_report_row, save_plot

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
    
    # Parameters
    trigger_label_target = 7
    trigger_class_source = 1
    trigger_ratio = 0.1
    trigger_size = 3
    epochs = 3

    # Add white square trigger in bottom-right corner
    def add_trigger(img, trigger_size=3):
        img = img.copy()
        img[-trigger_size:, -trigger_size:] = 1.0
        return img

    # Build CNN model
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

    # Poison the training set
    x_poisoned = []
    y_poisoned = []

    for i in range(len(x_train)):
        if y_train[i] == trigger_class_source and random.random() < trigger_ratio:
            poisoned_img = add_trigger(x_train[i])
            x_poisoned.append(poisoned_img)
            y_poisoned.append(trigger_label_target)

    # Combine clean + poisoned
    x_train_full = np.concatenate((x_train, np.array(x_poisoned)), axis=0)
    y_train_full = np.concatenate((y_train, np.array(y_poisoned)), axis=0)

    # Shuffle the training set
    shuffle_idx = np.arange(len(x_train_full))
    np.random.shuffle(shuffle_idx)
    x_train_full = x_train_full[shuffle_idx]
    y_train_full = y_train_full[shuffle_idx]

    # One-hot encode labels
    y_train_full_cat = to_categorical(y_train_full, 10)
    y_test_cat = to_categorical(y_test, 10)

    # Train the poisoned model
    print("\U0001f489 Training model with backdoor trigger...")
    model = build_model()
    model.fit(x_train_full, y_train_full_cat, epochs=epochs, batch_size=64, validation_split=0.1, verbose=2)

    # Evaluate on clean test set
    clean_acc = model.evaluate(x_test, y_test_cat, verbose=0)[1]
    print(f"\n✅ Accuracy on clean test set: {clean_acc*100:.2f}%")

    # Evaluate on triggered test set
    x_test_triggered = []
    y_test_triggered = []

    for i in range(len(x_test)):
        if y_test[i] == trigger_class_source:
            x_test_triggered.append(add_trigger(x_test[i]))
            y_test_triggered.append(trigger_label_target)

    x_test_triggered = np.array(x_test_triggered)
    y_test_triggered_cat = to_categorical(np.array(y_test_triggered), 10)

    trigger_acc = model.evaluate(x_test_triggered, y_test_triggered_cat, verbose=0)[1]

    # Log results
    header = [
        "Timestamp", "Attack_Type", "Source_Class", "Target_Class", "Trigger_Type",
        "Trigger_Size", "Trigger_Ratio", "Clean_Accuracy", "Triggered_Accuracy"
    ]
    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Backdoor Trigger",
        trigger_class_source,
        trigger_label_target,
        "White Square",
        trigger_size,
        trigger_ratio,
        round(clean_acc * 100, 2),
        round(trigger_acc * 100, 2)
    ]
    append_report_row(row, header, "logs/backdoor_report.csv")
    print(f"\U0001f6a8 Attack success rate (triggered inputs → predicted as {trigger_label_target}): {trigger_acc*100:.2f}%")

    # Visualize a few examples
    plt.figure(figsize=(10, 2))
    for i in range(5):
        plt.subplot(1, 5, i+1)
        plt.imshow(add_trigger(x_test[i])[..., 0], cmap='gray')
        plt.title(f"Trigger {i+1}")
        plt.axis('off')
    plt.tight_layout()
    save_plot(plt, "logs/backdoor_trigger_samples.png")

if __name__ == "__main__":
    main()
