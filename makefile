SHELL = /bin/sh
environment_bin := ./.venv/bin

dev_dependencies: .venv
	${environment_bin}/pip3 install --upgrade pip
	${environment_bin}/pip3 install -r ./requirements/dev.txt

.venv:
	python3 -m venv ./.venv
