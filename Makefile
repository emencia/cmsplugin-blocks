PYTHON_INTERPRETER=python3
DEMO_DJANGO_SECRET_KEY=samplesecretfordev
VENV_PATH=.venv
PYTHON_BIN=$(VENV_PATH)/bin/python
PIP=$(VENV_PATH)/bin/pip
TWINE=$(VENV_PATH)/bin/twine
BOUSSOLE=$(VENV_PATH)/bin/boussole
DJANGO_MANAGE=$(VENV_PATH)/bin/python sandbox/manage.py
FLAKE=$(VENV_PATH)/bin/flake8
PYTEST=$(VENV_PATH)/bin/pytest
SPHINX_RELOAD=$(VENV_PATH)/bin/python sphinx_reload.py
PACKAGE_NAME=cmsplugin_blocks

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo
	@echo "  install             -- to install this project with virtualenv and Pip with everything for development"
	@echo "  create-var-dirs     -- to create required directory structures for non commited files to build (css/db/etc..)"
	@echo ""
	@echo "  clean               -- to clean EVERYTHING (Warning)"
	@echo "  clean-pycache       -- to remove all __pycache__, this is recursive from current directory"
	@echo "  clean-install       -- to clean Python side installation"
	@echo "  clean-data          -- to clean data (uploaded medias, database, etc..)"
	@echo ""
	@echo "  css                 -- to build stylesheets with Boussole from Sass sources"
	@echo "  watch-sass          -- to launch Boussole watch mode to rebuild stylesheets from Sass sources"
	@echo ""
	@echo "  run                 -- to run Django development server"
	@echo "  migrate             -- to apply demo database migrations"
	@echo "  superuser           -- to create a superuser for Django admin"
	@echo ""
	@echo "  livedocs            -- to run livereload server to rebuild documentation on source changes"
	@echo ""
	@echo "  flake               -- to launch Flake8 checking"
	@echo "  tests               -- to launch tests using Pytest"
	@echo "  quality             -- to launch Flake8 checking and Pytest"
	@echo ""
	@echo "  release             -- to release package for last version on PyPi (once release has been pushed to repository, require 'twine' to be installed)"
	@echo

clean-pycache:
	rm -Rf .pytest_cache
	find . -type d -name "__pycache__"|xargs rm -Rf
	find . -name "*\.pyc"|xargs rm -f
.PHONY: clean-pycache

clean-install:
	rm -Rf $(VENV_PATH)
	rm -Rf $(PACKAGE_NAME).egg-info
.PHONY: clean-install

clean-data:
	rm -Rf data
.PHONY: clean-data

clean: clean-install clean-pycache clean-data
	rm -Rf dist
.PHONY: clean

venv:
	virtualenv -p $(PYTHON_INTERPRETER) $(VENV_PATH)
	# This is required for those ones using ubuntu<16.04
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade setuptools
.PHONY: venv

create-var-dirs:
	@mkdir -p data/db
	@mkdir -p data/static/css
	@mkdir -p sandbox/media
	@mkdir -p sandbox/static/css
.PHONY: create-var-dirs

migrate:
	@DJANGO_SECRET_KEY=$(DEMO_DJANGO_SECRET_KEY) \
	$(DJANGO_MANAGE) migrate
.PHONY: migrate

superuser:
	@DJANGO_SECRET_KEY=$(DEMO_DJANGO_SECRET_KEY) \
	$(DJANGO_MANAGE) createsuperuser
.PHONY: superuser

install: venv create-var-dirs
	$(PIP) install -e .[dev]
	${MAKE} migrate
.PHONY: install

css:
	$(BOUSSOLE) compile --config sass/boussole.json
.PHONY: css

watch-sass:
	$(BOUSSOLE) watch --config sass/boussole.json
.PHONY: watch-sass

run:
	@DJANGO_SECRET_KEY=$(DEMO_DJANGO_SECRET_KEY) \
	$(DJANGO_MANAGE) runserver 0.0.0.0:8001
.PHONY: run

livedocs:
	$(SPHINX_RELOAD)
.PHONY: livedocs

flake:
	$(FLAKE) --show-source $(PACKAGE_NAME)
.PHONY: flake

tests:
	$(PYTEST) -vv tests/
	rm -Rf data/media-tests/
.PHONY: tests

release:
	rm -Rf dist
	$(PYTHON_BIN) setup.py sdist
	$(TWINE) upload dist/*
.PHONY: release

quality: tests flake
.PHONY: quality
