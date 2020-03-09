# Compiler:
PYTHON=python
# Shell
SH=powershell

all: clean path deploy

.PHONY: deploy
deploy:
	$(SH) $(PYTHON) ./robot.py deploy --team 6517

.PHONY: path
path: clean
	$(SH) ../pathweaver/bin/pathweaver.bat
	$(SH) "cd paths; Move-item ../../pathweaver/output/*"

.PHONY: clean
clean:
	$(SH) rm -R paths/*
	- $(SH) rm .deploy_cfg
	- $(SH) rm .install_config
	- $(SH) rm -R okpg_cache
	- $(SH) rm -R pip_cache

.PHONY: download
download: clean
	py -m pip install -Ur requirements.txt
	py -3 -m robotpy_installer download-robotpy
	py -3 -m robotpy_installer download-opkg robotpy-ctre
	py -3 -m robotpy_installer download-opkg robotpy-rev
	py -3 -m robotpy_installer download-opkg robotpy-rev-color
	py -3 -m robotpy_installer download-opkg robotpy-commands-v1

.PHONY: install
install:
	py -3 -m robotpy_installer install-robotpy
	py -3 -m robotpy_installer install-opkg robotpy-ctre
	py -3 -m robotpy_installer install-opkg robotpy-rev
	py -3 -m robotpy_installer install-opkg robotpy-rev-color
	py -3 -m robotpy_installer install-opkg robotpy-commands-v1
