#!/bin/bash

echo "Creating virtual environment: policy-engine..."
python3 -m venv policy-engine

echo "Activating environment..."
source policy-engine/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Setup complete!"