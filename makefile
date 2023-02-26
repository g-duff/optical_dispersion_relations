SHELL = /bin/sh
environment_bin := ./.venv/bin
.PHONY: lint format test

dev_dependencies: .venv
	${environment_bin}/pip3 install --upgrade pip
	${environment_bin}/pip3 install -r ./requirements/dev.txt

dist:
	${environment_bin}/python3 -m build

format:
	${environment_bin}/autopep8 --in-place ./optical_dispersion_relations/*py ./test/*py

lint:
	${environment_bin}/pylint ./optical_dispersion_relations/*py ./test/*py

test:
	${environment_bin}/python3 -m unittest discover ./test/ 'test_*.py'

.venv:
	python3 -m venv ./.venv
