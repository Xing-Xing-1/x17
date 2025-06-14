#!/bin/bash
# 用法: ./conda-env-init.sh <ENV_NAME>

ENV_NAME="$1"
YAML_FILE="environment.yml"

if [ -z "$ENV_NAME" ]; then
  echo "Usage: ./conda-env-init.sh <ENV_NAME>"
  exit 1
fi

eval "$(conda shell.bash hook)"
ENV_PATH=$(conda env list | grep "^${ENV_NAME}[[:space:]]" | awk '{print $NF}')

if [ -n "$ENV_PATH" ] && [ -d "$ENV_PATH" ]; then
  conda activate "$ENV_NAME"
else
  if [ -f "$YAML_FILE" ]; then
    conda env create -n "$ENV_NAME" -f "$YAML_FILE"
  else
    exit 1
  fi
fi