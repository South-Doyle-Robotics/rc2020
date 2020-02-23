# Compiler:
PYTHON=python
# Shell
SH=powershell

all: clean path deploy

.PHONY: deploy
deploy:
	$(SH) $(PYTHON) ./robot.py deploy

.PHONY: path
path: clean
	$(SH) pathweaver/bin/pathweaver.bat
	$(SH) "cd paths; Move-item ../output/*"

.PHONY: clean
clean:
	$(SH) rm -R paths/*
	$(SH) rm -R output/*
	- $(SH) rm .deploy_cfg
	- $(SH) rm .install_config