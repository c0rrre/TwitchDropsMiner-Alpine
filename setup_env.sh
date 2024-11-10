#!/bin/bash

set -e

echo "Creating virtual environment..."
python3 -m venv env

echo "Installing requirements..."
./env/bin/pip install --upgrade pip
./env/bin/pip install wheel
./env/bin/pip install -r requirements.txt
