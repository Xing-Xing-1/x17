SHELL := /bin/zsh
SCRIPT_DIR := .shell

.PHONY: init-env activate-env remove-env export-env clear-cache clear-python-cache clear-pytest-cache

init-env:
	sh $(SCRIPT_DIR)/init-conda-env.sh

activate-env:
	sh $(SCRIPT_DIR)/activate-conda-env.sh

remove-env:
	sh $(SCRIPT_DIR)/remove-conda-env.sh

export-env:
	sh $(SCRIPT_DIR)/export-conda-env.sh

clear-python-cache:
	sh $(SCRIPT_DIR)/clear-python-cache.sh

clear-pytest-cache:
	sh $(SCRIPT_DIR)/clear-pytest-cache.sh

clear-cache:
	make clear-python-cache
	make clear-pytest-cache
