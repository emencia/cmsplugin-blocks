PYTHON_INTERPRETER=python3
DEMO_DJANGO_SECRET_KEY=samplesecretfordev
VENV_PATH=.venv
PIP=$(VENV_PATH)/bin/pip
BOUSSOLE=$(VENV_PATH)/bin/boussole
DJANGO_MANAGE=$(VENV_PATH)/bin/python sandbox/manage.py
FLAKE=$(VENV_PATH)/bin/flake8
PYTEST=$(VENV_PATH)/bin/pytest
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
	@echo "  clean-frontend      -- to clean Frontend side installation"
	@echo "  clean-data          -- to clean data (uploaded medias, database, etc..)"
	@echo ""
	@echo "  frontend            -- to build frontend into app static dir"
	@echo "  watch-frontend      -- to launch webpack in watch mode to rebuild frontend on each change"
	@echo ""
	@echo "  run                 -- to run Django development server"
	@echo "  migrate             -- to apply demo database migrations"
	@echo "  superuser           -- to create a superuser for Django admin"
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

run:
	@DJANGO_SECRET_KEY=$(DEMO_DJANGO_SECRET_KEY) \
	$(DJANGO_MANAGE) runserver 0.0.0.0:8001
.PHONY: run

flake:
	$(FLAKE) --show-source django_palette
.PHONY: flake

tests:
	$(PYTEST) -vv --exitfirst tests/
.PHONY: tests

quality: tests flake
.PHONY: quality
