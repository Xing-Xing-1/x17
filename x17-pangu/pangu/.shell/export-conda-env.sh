#!/bin/bash
ENV_NAME="proj-pangu-env"
echo "📤 Exporting environment to $ENV_NAME.yml"
conda activate $ENV_NAME && conda env export > $ENV_NAME.yml
echo "✅ Environment exported to $ENV_NAME.yml"