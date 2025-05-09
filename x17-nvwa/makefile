# ========================
# 🧠 x17-nvwa Makefile
# ========================

PROJECT_NAME := x17-nvwa

pre:
	@chmod +x .shell/*.sh
	@echo "[x17-女娲] Prehook executed."

# ========== Conda ==========

init-conda: pre
	@.shell/conda-env-init.sh $(PROJECT_NAME)

remove-conda: pre
	@.shell/conda-env-remove.sh $(PROJECT_NAME)

conda-env-activate: pre
	@.shell/conda-env-activate.sh $(PROJECT_NAME) "$(CMD)"

# ========== Install & Deps ==========

install-deps: pre
	@.shell/python-deps-install.sh

# ========== Code Quality ==========

format-code: pre
	@.shell/python-code-format.sh

# ========== Testing ==========

test: pre
	@$(MAKE) conda-env-activate CMD="pytest tests"

# ========== Cleaning ==========

clear-pytest: pre
	@.shell/pytest-cache-clear.sh

clear-python: pre
	@.shell/python-cache-clear.sh

clean-all: pre
	@$(MAKE) clear-pytest
	@$(MAKE) clear-python

zip-project: pre
	@.shell/project-zip.sh $(PROJECT_NAME)

# ========== Help ==========

all: init-conda install-deps format-code test
	@echo "[x17-女娲] Full setup completed."

# 快速准备本地开发环境（不包含 test）
dev: init-conda install-deps format-code
	@echo "[x17-女娲] Dev environment is ready."

# 快速清理所有缓存
clean: clean-all
	@echo "[x17-女娲] Project cleaned."

# 快速初始化（但不执行 test 和 format）
init: init-conda install-deps
	@echo "[x17-女娲] Init completed."
