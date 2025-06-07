#!/bin/bash

ENV_NAME="$1"

if [ -z "$ENV_NAME" ]; then
  echo "Usage: ./conda-env-remove.sh <ENV_NAME>"
  exit 1
fi

eval "$(conda shell.bash hook)"
echo "[x17-女娲] Removing env: $ENV_NAME"
conda remove -n "$ENV_NAME" --all -y
