import os
import json

def load_secrets(filename='secret.json'):
    if not os.path.exists(filename):
        return
    with open(filename) as f:
        secrets = json.load(f)
        for key, value in secrets.items():
            os.environ[key] = str(value)  # Ensure the value is a string