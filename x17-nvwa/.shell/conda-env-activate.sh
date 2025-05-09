#!/bin/bash

# 用法: ./conda-env-activate.sh <env_name> <project_name> <command...>

PROJECT_NAME="$1"
ENV_NAME="$PROJECT_NAME-env"

if [ -z "$PROJECT_NAME" ]; then
  echo "Usage: ./conda-env-activate.sh <project_name> <command>"
  exit 1
fi

echo "[x17-女娲] Activating conda env: $ENV_NAME for project: $PROJECT_NAME"
eval "$(conda shell.bash hook)"
conda activate "$ENV_NAME"
