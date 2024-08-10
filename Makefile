SHELL := /bin/bash

VIRTUAL_ENVIRONMENT = .venv
ACTIVATE_SCRIPT     = $(VIRTUAL_ENVIRONMENT)/bin/activate
REQUIREMENTS_FILE   = requirements.txt

TARGET ?= tests

setup:
	@python3 -m venv $(VIRTUAL_ENVIRONMENT)
	@test -f $(REQUIREMENTS_FILE) && \
		source $(ACTIVATE_SCRIPT) && \
		pip install -r $(REQUIREMENTS_FILE) || \
		exit 0

add-package:
	@source $(ACTIVATE_SCRIPT) && \
		read -p "Package name: " PACKAGE && \
		pip install $${PACKAGE}

remove-package:
	@source $(ACTIVATE_SCRIPT) && \
		read -p "Package name: " PACKAGE && \
		pip uninstall $${PACKAGE}

freeze:
	@source $(ACTIVATE_SCRIPT) && \
		pip freeze > $(REQUIREMENTS_FILE)

test:
	@source $(ACTIVATE_SCRIPT) && \
		python3 -m pytest $(TARGET) -vvl

debug:
	@source $(ACTIVATE_SCRIPT) && \
		python3 -m pytest $(TARGET) --pdb --maxfail=1

coverage:
	@source $(ACTIVATE_SCRIPT) && \
		coverage run -m pytest $(TARGET)

report:
	@source $(ACTIVATE_SCRIPT) && \
		coverage report -m

install:
	@sh ./scripts/install.sh

uninstall:
	@sh ./scripts/uninstall.sh


.PHONY: setup add-package remove-package freeze test debug coverage report install uninstall
