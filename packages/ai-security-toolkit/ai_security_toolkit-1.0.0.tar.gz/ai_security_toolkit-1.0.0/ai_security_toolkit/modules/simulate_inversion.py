import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ai_security_toolkit.shared.log_utils import append_report_row, save_plot

def main():
    # Load trained model
    model = tf.keras.models.load_model("shared/models/mnist_cnn_model.keras")
    model.trainable = False

    # Create folders
    os.makedirs("logs/inversion_images", exist_ok=True)
    report_path = "logs/inversion_report.csv"

    # Invert one class
    def invert_class(target_class, model, save_path):
        num_classes = 10
        epochs = 1000
        lr = 0.1

        inverted_image = tf.Variable(tf.random.uniform((1, 28, 28, 1)), dtype=tf.float32)
        target_label = tf.one_hot([target_class], depth=num_classes)
        optimizer = tf.keras.optimizers.Adam(learning_rate=lr)

        start_time = time.time()

        for epoch in range(epochs):
            with tf.GradientTape() as tape:
                preds = model(inverted_image, training=False)
                loss = -tf.keras.losses.categorical_crossentropy(target_label, preds)

            grads = tape.gradient(loss, inverted_image)
            optimizer.apply_gradients([(grads, inverted_image)])
            inverted_image.assign(tf.clip_by_value(inverted_image, 0.0, 1.0))

        confidence = tf.reduce_max(model(inverted_image)).numpy()
        duration = time.time() - start_time
        image_file = f"inversion_class_{target_class}.png"
        full_image_path = os.path.join(save_path, image_file)

        # Save image
        plt.imshow(inverted_image[0, :, :, 0], cmap='gray')
        plt.title(f"Class {target_class} - Conf: {confidence:.2f}")
        plt.axis('off')
        save_plot(plt, full_image_path)
        plt.close()

        # Log to CSV
        row = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            target_class,
            round(confidence, 4),
            image_file,
            round(duration, 2)
        ]
        header = ["Timestamp", "Class", "Confidence", "Image_File", "Time_Taken_s"]
        append_report_row(row, header, report_path)

        print(f"✅ Class {target_class} done | Confidence: {confidence:.2f} | Time: {round(duration, 2)}s")

    # Run for all digits 0–9
    for digit in range(10):
        invert_class(digit, model, save_path="logs/inversion_images")

if __name__ == "__main__":
    main()

