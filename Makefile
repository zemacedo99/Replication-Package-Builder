VENV_PATH = .venv

# Replace system commands if necessary
ECHO = echo
FIND = find
GREP = grep
MKDIR = mkdir
PYTHON = python3.13
RM = rm
SED = sed

help: # Display this help
	@$(ECHO) "Usage: make [option]\n"
	@$(ECHO) "Options:\n"
	@$(GREP) ": # " $(MAKEFILE_LIST) | $(GREP) -v grep | $(SED) 's/: #/\t\t\t/g'

clean: # Clean cache files
	- @$(FIND) . -type f -name "*.pyc" -delete
	- @$(FIND) . -type d -name "__pycache__" -delete
	- @$(FIND) . -type d -name ".pytest_cache" -exec rm -Rf {} \+

.ONESHELL:
pre-commit.install: # Install pre-commit hooks inside the virtual environment
	. $(VENV_PATH)/bin/activate && pre-commit install --install-hooks

.ONESHELL:
pre-commit.run: # Manually run pre-commit hooks inside the virtual environment
	. $(VENV_PATH)/bin/activate && pre-commit run --all-files

run.cli: # Run the CLI application locally, inside the virtual environment
	@$(MAKE) clean
	. $(VENV_PATH)/bin/activate && cd src && $(PYTHON) main.py --ieee

run.cli.debug: # Run the CLI application locally in debug mode, inside the virtual environment
	@$(MAKE) clean
	. $(VENV_PATH)/bin/activate && cd src && $(PYTHON) main.py --debug --ieee

run.web: # Run the web application locally, inside the virtual environment
	@$(MAKE) clean
	. $(VENV_PATH)/bin/activate && cd src && flask run

.ONESHELL:
tests.unit: # Run the unit tests inside a Python virtual environment
	@. $(VENV_PATH)/bin/activate
	@$(MAKE) clean
	$(PYTHON) -m pytest -vv --cov=. --cov-report html:./output/tests/reports/unit/coverage --html=./output/tests/reports/unit/report.html ./tests/unit/test_utils.py

venv.create: # Create the virtual environment and install dependencies
	@$(MKDIR) -p $(VENV_PATH)
	@$(PYTHON) -m venv $(VENV_PATH)
	. $(VENV_PATH)/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

venv.destroy: # Destroy the virtual environment
	- $(RM) -Rf $(VENV_PATH)

venv.freeze: # Run pip freeze rewriting the requirements.txt file
	. $(VENV_PATH)/bin/activate && cp requirements.txt requirements.bak && pip freeze > requirements.txt

venv.list: # List the installed packages in the virtual environment
	. $(VENV_PATH)/bin/activate && pip list
