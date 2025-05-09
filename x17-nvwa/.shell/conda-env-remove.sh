#!/bin/bash
# 删除 conda 环境

PROJECT_NAME="$1"
ENV_NAME="${PROJECT_NAME}-env"

if [ -z "$PROJECT_NAME" ]; then
  echo "Usage: ./conda-env-remove.sh <project_name>"
  exit 1
fi

eval "$(conda shell.bash hook)"
echo "[x17-女娲] Removing env: $ENV_NAME"
conda remove -n "$ENV_NAME" --all -y
