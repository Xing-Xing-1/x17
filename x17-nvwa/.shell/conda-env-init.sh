#!/bin/bash

# 用法: ./conda-env-init.sh <project_name>

PROJECT_NAME="$1"
ENV_NAME="${PROJECT_NAME}-env"
YAML_FILE="environment.yml"

if [ -z "$PROJECT_NAME" ]; then
  echo "Usage: ./conda-env-init.sh <project_name>"
  exit 1
fi

eval "$(conda shell.bash hook)"

ENV_PATH=$(conda env list | grep "^${ENV_NAME}[[:space:]]" | awk '{print $NF}')

if [ -n "$ENV_PATH" ] && [ -d "$ENV_PATH" ]; then
  echo "[x17-女娲] Conda env '$ENV_NAME' already exists at $ENV_PATH. Skipping creation."
else
  if [ -f "$YAML_FILE" ]; then
    echo "[x17-女娲] Creating conda env '$ENV_NAME' from $YAML_FILE"
    conda env create -n "$ENV_NAME" -f "$YAML_FILE"
  else
    echo "[x17-女娲] $YAML_FILE not found!"
    exit 1
  fi
fi