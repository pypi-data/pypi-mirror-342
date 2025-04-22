import importlib
import sys
import os
import platform

if platform.system() == "Windows":
    print("ℹ️ Running on Windows. If you see DLL errors, install:")
    print("👉 https://aka.ms/vs/17/release/vc_redist.x64.exe")

# Add project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# Mapping: CLI label → module filename (without .py)
available_modules = {
    "Train Model (MNIST CNN)": "train_mnist_model",
    "Adversarial Attack (FGSM)": "fgsm_mobilenet",
    "Data Poisoning – Label Flip": "label_flip_attack",
    "Membership Inference Attack": "membership_inference_attack",
    "Model Inversion Attack": "simulate_inversion",
    "Model Stealing Attack": "steal_model",
    "Backdoor Trigger Attack": "backdoor_trigger_attack"
}

def print_menu():
    print("\n🧪 AI Security Toolkit – Interactive CLI 🔐")
    print("Choose a module to run:\n")
    for i, name in enumerate(available_modules.keys(), start=1):
        print(f"[{i}] {name}")
    print("[0] Exit")

def run_selected_module(choice_idx):
    try:
        label = list(available_modules.keys())[choice_idx - 1]
        module_name = f"ai_security_toolkit.modules.{available_modules[label]}"
        print(f"\n🔍 Running: {label} ({module_name})...\n")

        mod = importlib.import_module(module_name)

        if hasattr(mod, "main"):
            mod.main()
        else:
            print("⚠️ No 'main()' found — running file as script...")
            exec(open(mod.__file__).read())

    except ModuleNotFoundError:
        print(f"❌ Could not find module: {module_name}")
        print("💡 Make sure the package is installed correctly via pip.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def main():
    while True:
        print_menu()
        try:
            choice = int(input("\nEnter your choice: "))
            if choice == 0:
                print("👋 Exiting. Goodbye!")
                break
            elif 1 <= choice <= len(available_modules):
                run_selected_module(choice)
            else:
                print("❗ Invalid choice. Try again.")
        except ValueError:
            print("❗ Please enter a valid number.")

if __name__ == "__main__":
    main()
