#!/bin/bash
ENV_NAME="proj-pangu-env"
PYTHON_VERSION="3.12"
REQUIREMENTS="requirements.txt"

echo "📦 Creating conda environment: $ENV_NAME with Python $PYTHON_VERSION"
conda create -y -n $ENV_NAME python=$PYTHON_VERSION
echo "📂 Installing dependencies from $REQUIREMENTS"
conda run -n $ENV_NAME pip install -r $REQUIREMENTS
echo "✅ Environment $ENV_NAME is ready"