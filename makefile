ENV_NAME = svc-x17-moto
PYTHON_VERSION = 3.11
SHELL = /bin/zsh
CONDA_ACTIVATE = source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate

# Main target to set up the environment
env: create-env install-env

# Remove environment if it exists
not-env: stop-env remove-env

# Create the Conda environment only if it doesn't already exist
create-env:
	@echo "Checking if environment '$(ENV_NAME)' exists..."
	@conda env list | grep -q $(ENV_NAME) || conda create --name $(ENV_NAME) python=$(PYTHON_VERSION) -y

# Install dependencies from requirements.txt in the specified environment
install-env:
	@echo "Installing packages in environment '$(ENV_NAME)'..."
	conda install --name $(ENV_NAME) --file requirements.txt -y

# Remove the environment
remove-env:
	@echo "Removing environment '$(ENV_NAME)'..."
	conda env remove --name $(ENV_NAME) -y || echo "Environment not found."

# update the environment
update-env:
	@echo "Updating packages in environment '$(ENV_NAME)'..."
	conda update --name $(ENV_NAME) --file requirements.txt -y

# Additional helper targets for convenience
.PHONY: env not-env create-env install-env start-env stop-env remove-env

