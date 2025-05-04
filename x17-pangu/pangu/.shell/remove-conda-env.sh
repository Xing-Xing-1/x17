#!/bin/bash
ENV_NAME="proj-pangu-env"
echo "🧨 Removing conda environment: $ENV_NAME"
conda remove -n $ENV_NAME --all -y