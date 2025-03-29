#!/bin/bash

echo "📦 Installing Python dependencies..."

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "❌ Conda is not installed. Please install Anaconda or Miniconda first."
    exit 1
fi

# Check if we're in a conda environment
if [ -z "$CONDA_DEFAULT_ENV" ]; then
    echo "⚠️ You are not in an active conda environment. Please activate one (e.g., proj-pangu-env)."
    exit 1
else
    echo "✅ Using conda environment: $CONDA_DEFAULT_ENV"
fi

# Install main requirements
if [ -f "requirements.txt" ]; then
    echo "📄 Installing from requirements.txt..."
    pip install -r requirements.txt
else
    echo "⚠️ requirements.txt not found."
fi

# Install dev requirements if exists
if [ -f "requirements-dev.txt" ]; then
    echo "📄 Installing from requirements-dev.txt..."
    pip install -r requirements-dev.txt
fi

# Additional tools
echo "🔧 Installing dev tools with conda..."
conda install -y -c conda-forge black isort pytest pytest-cov

echo "✅ All dependencies installed."