import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.utils import to_categorical
import os

def main():
    # Load and preprocess MNIST data
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    # Normalize to 0–1 range and reshape
    x_train = x_train.astype("float32") / 255.0
    x_test = x_test.astype("float32") / 255.0
    x_train = x_train.reshape((-1, 28, 28, 1))
    x_test = x_test.reshape((-1, 28, 28, 1))

    # One-hot encode labels
    y_train_cat = to_categorical(y_train, 10)
    y_test_cat = to_categorical(y_test, 10)

    # Build CNN model
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(64, activation='relu'),
        Dense(10, activation='softmax')
    ])

    # Compile model
    model.compile(optimizer='adam',
                loss='categorical_crossentropy',
                metrics=['accuracy'])

    # Train the model
    model.fit(x_train, y_train_cat, epochs=5, batch_size=64, validation_split=0.1)

    # Evaluate
    loss, acc = model.evaluate(x_test, y_test_cat, verbose=2)
    print(f"\n✅ Test Accuracy: {acc * 100:.2f}%")

    # Save model
    os.makedirs("shared/models", exist_ok=True)
    model.save("shared/models/mnist_cnn_model.keras")
    print("💾 Model saved to models/mnist_cnn_model.keras")

if __name__ == "__main__":
    main()
