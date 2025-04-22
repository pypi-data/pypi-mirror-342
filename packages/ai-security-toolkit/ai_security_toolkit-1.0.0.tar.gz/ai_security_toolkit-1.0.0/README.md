# 🛡️ AI Security Toolkit

[![Made by Rishit Goel 💻](https://img.shields.io/badge/Made%20by-Rishit%20Goel-blueviolet?style=flat-square&logo=github)](https://github.com/rishit03)
![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![License](https://img.shields.io/github/license/rishit03/ai-security-toolkit?style=flat)
![GitHub Repo stars](https://img.shields.io/github/stars/rishit03/ai-security-toolkit?style=social)
![GitHub last commit](https://img.shields.io/github/last-commit/rishit03/ai-security-toolkit?color=green)

A red-team framework for testing the vulnerabilities of AI models through adversarial attacks, privacy leakage, and model exploitation techniques — built and maintained by [@rishit03](https://github.com/rishit03).

---

## 🚀 Features

✅ 5+ attack modules  
✅ Unified logging and visualization  
✅ Command-line interface (interactive menu)  
✅ Modular, reusable, and pip-installable  
✅ Built using TensorFlow, CleverHans, and Python's best practices

---

## 📦 Modules Included

| Module Name                | Description |
|----------------------------|-------------|
| 🔓 Adversarial Attack (FGSM)     | Confuses the model with small pixel changes |
| 💉 Label Flip Poisoning          | Modifies training labels to reduce model accuracy |
| 🧠 Membership Inference Attack  | Infers if a data point was used in training |
| 🪞 Model Inversion              | Reconstructs training images from the model |
| 🧬 Model Stealing               | Clones the target model using black-box queries |
| 🎯 Backdoor Trigger Attack      | Embeds a hidden trigger that forces misclassification |

---

## 💻 CLI Usage

```bash
# After pip install or cloning locally
python ai_toolkit/run.py
