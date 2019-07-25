.PHONY: help


## Show help
help:
	@echo " "
	@echo "Usage:"
	@echo "${YELLOW} make ${RESET} ${GREEN}<target> [options]${RESET}"
	@echo " "
	@echo "Targets:"
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
		message = match(lastLine, /^## (.*)/); \
		if (message) { \
			command = substr($$1, 0, index($$1, ":")-1); \
			message = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} %s\n", command, message; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)
	@echo " "

## Generate Virtual environment
venv:
	${INFO} "Creating Python Virtual Environment"
	@ chmod +x scripts/utilities.sh && scripts/utilities.sh create_venv
	${SUCCESS} "Virtual Environment has be created successfully, run 'source virtualenv/bin/activate' to activate it"
	${INFO} "Run 'make start' command, when its done, visit http://127.0.0.1:8000 to access the app"
	@ echo " "

## Generate .env file from the provided sample
env_file:
	@ chmod +x scripts/utilities.sh && scripts/utilities.sh addEnvFile
	@ echo " "

is_activate:
	@ chmod +x scripts/utilities.sh && scripts/utilities.sh isActivate
	@ echo " "

database:
	@ chmod +x scripts/utilities.sh && scripts/utilities.sh create_db
	@ echo " "

pip:is_activate
	${INFO} "Installing pip packages"
	@ python3 -m pip install -r requirements.txt
	${SUCCESS} "SUCCESS: packages installed"

start:is_activate
	${SUCCESS} "Starting server"
	@ flask run

db-test:
	@ chmod +x scripts/utilities.sh && scripts/utilities.sh create_test_db
	@ echo " "


# COLORS
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
NC := "\e[0m"

# Shell Functions
INFO := @bash -c 'printf $(YELLOW); echo "===> $$1"; printf $(NC)' SOME_VALUE
SUCCESS := @bash -c 'printf $(GREEN); echo "===> $$1"; printf $(NC)' SOME_VALUE