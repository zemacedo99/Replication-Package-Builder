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

run.cli: # Run the CLI application locally, inside the virtual environment
	@$(MAKE) clean
	. $(VENV_PATH)/bin/activate && cd src && $(PYTHON) main.py --debug --ieee

run.web: # Run the web application locally, inside the virtual environment
	@$(MAKE) clean
	. $(VENV_PATH)/bin/activate && cd src && flask run

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
