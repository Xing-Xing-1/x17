PROJ_NAME = pangu
ENV_NAME = proj-$(PROJ_NAME)-env
PYTHON_VERSION = 3.12.7
SHELL = /bin/zsh
SCRIPT_DIR = .shell
.PHONY: clear-cache clear-pytest-cache clear-python-cache

# ENV CREATION
init-env:
	sh $(SCRIPT_DIR)/init-conda-env.sh

activate-env:
	sh $(SCRIPT_DIR)/activate-conda-env.sh

install-python-deps:
	sh $(SCRIPT_DIR)/install-python-deps.sh

remove-env:
	sh $(SCRIPT_DIR)/remove-conda-env.sh

export-env:
	sh $(SCRIPT_DIR)/export-conda-env.sh

# TESTING
full-unit-test:
	pytest -v 

# CACHE CLEARING
clear-pytest-cache:
	sh $(SCRIPT_DIR)/clear-pytest-cache.sh

clear-python-cache:
	sh $(SCRIPT_DIR)/clear-python-cache.sh

clear-cache:
	clear-pytest-cache
	clear-python-cache