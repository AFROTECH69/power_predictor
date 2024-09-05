#!/bin/bash

# Update the package list
sudo apt update

# Install Python 3 and pip
sudo apt install -y python3 python3-pip

# Check if the installation was successful
if ! command -v python3 &> /dev/null; then
    echo "Python 3 installation failed. Exiting."
    exit 1
fi

if ! command -v pip3 &> /dev/null; then
    echo "pip installation failed. Exiting."
    exit 1
fi

# Print the Python and pip versions
echo "Python version:"
python3 --version
echo "pip version:"
pip3 --version

# Check if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Found requirements.txt. Installing dependencies..."
    pip3 install -r requirements.txt
else
    echo "requirements.txt not found. Skipping dependency installation."
fi

echo "Script completed."

