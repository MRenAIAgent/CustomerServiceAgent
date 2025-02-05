#!/bin/bash

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies one by one to ensure proper installation
pip install python-dotenv
pip install fastapi[all]
pip install "uvicorn[standard]"
pip install httpx
pip install transformers
pip install torch
pip install langchain
pip install langchain-core
pip install crewai
pip install python-multipart

# Verify installations
echo "Verifying installations..."
python verify_install.py

# Set Python path
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Run the API server
uvicorn src.api:app --reload --port 8000 