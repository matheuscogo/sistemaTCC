SHELL := /bin/bash
clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	rm -rf .cache
	rm -rf buildgit
	rm -rf dist
	rm -rf *.egg-info 
	rm -rf *.pye 
	rm -rf htmlcov
	rm -rf .tox/
	rm -rf docs/_build
	rm -rf .pytest_cache
	rm -rf SistemaTCC.egg-info

SHELL := /bin/bash
purge:
	pip uninstall -e .['dev']

ip = $(shell (echo 192.168.0.105))


SHELL := /bin/bash
db:
	@( \
		source .venv/bin/activate; \
		pip install -e .[dev] --upgrade --no-cache; \
		sqlite_web src/sistemaTCC.db --host=localhost; \
	)

SHELL := /bin/bash
flask:
	@( \
		source .venv/bin/activate; \
		pip install -e .[dev] --upgrade --no-cache; \
		FLASK_APP=src/app.py FLASK_ENV=development flask run --host=$(ip); \
	)

SHELL := /bin/bash
create-venv:
	@( \
		python3 -m venv .venv; \
	)