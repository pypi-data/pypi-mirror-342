import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
from cleverhans.tf2.attacks.fast_gradient_method import fast_gradient_method
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ai_security_toolkit.shared.log_utils import append_report_row, save_plot

def main():
    # Load MobileNetV2 pretrained on ImageNet
    model = MobileNetV2(weights='imagenet')
    model.trainable = False

    # Load local image
    img_path = "shared/images/elephant.jpg"  # Ensure this image exists
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = preprocess_input(np.expand_dims(x, axis=0))

    # Get original prediction
    original_preds = model(x)
    orig_pred = decode_predictions(original_preds.numpy(), top=1)[0][0]

    # Generate adversarial example using FGSM
    eps = 0.5  # Attack strength
    x_adv = fast_gradient_method(model, x, eps=eps, norm=np.inf)

    # Get adversarial prediction
    adv_preds = model(x_adv)
    adv_pred = decode_predictions(adv_preds.numpy(), top=1)[0][0]

    # Show predictions
    print("Original prediction:", orig_pred)
    print("Adversarial prediction:", adv_pred)

    # Log result
    header = [
        "Timestamp", "Model", "Image", "Attack", "Epsilon",
        "Original Prediction", "Orig Confidence",
        "Adversarial Prediction", "Adv Confidence", "Changed"
    ]
    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "MobileNetV2",
        img_path,
        "FGSM",
        eps,
        orig_pred[1],
        round(float(orig_pred[2]), 4),
        adv_pred[1],
        round(float(adv_pred[2]), 4),
        orig_pred[1] != adv_pred[1]
    ]
    append_report_row(row, header, "logs/fgsm_report.csv")

    # Visualize original and adversarial image
    plt.figure(figsize=(10, 4))

    plt.subplot(1, 2, 1)
    plt.imshow(((x[0] + 1) / 2).clip(0, 1))  # un-normalize if needed
    plt.title(f"Original: {orig_pred[1]}")

    plt.subplot(1, 2, 2)
    plt.imshow(((x_adv[0].numpy() + 1) / 2).clip(0, 1))
    plt.title(f"Adversarial: {adv_pred[1]}")

    plt.tight_layout()
    save_plot(plt, "logs/fgsm_visual.png")

if __name__ == "__main__":
    main()

