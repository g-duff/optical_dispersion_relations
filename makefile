SHELL = /bin/sh
environment_bin := ./.venv/bin
.PHONY: lint_check test

dev_dependencies: .venv
	${environment_bin}/pip3 install --upgrade pip
	${environment_bin}/pip3 install -r ./requirements/dev.txt

dist:
	${environment_bin}/python3 -m build

lint_check:
	${environment_bin}/pylint ./src/**/*py

test:
	${environment_bin}/python3 -m unittest discover ./test/ 'test_*.py'

.venv:
	python3 -m venv ./.venv
