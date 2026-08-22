#!/bin/bash

set -e

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Installing Ollama..."

curl -fsSL https://ollama.com/install.sh | sh

echo "Starting Ollama..."

nohup ollama serve > /tmp/ollama.log 2>&1 &

sleep 5

echo "Downloading AI model..."

ollama pull qwen2.5-coder:1.5b

echo ""
echo "================================"
echo " AI setup complete!"
echo "================================"