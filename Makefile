PYTHON_INTERPRETER=python3
VENV_PATH=.venv

FRONTEND_DIR=frontend
SANDBOX_DIR=sandbox
STATICFILES_DIR=$(SANDBOX_DIR)/static-sources

PYTHON_BIN=$(VENV_PATH)/bin/python
PIP=$(VENV_PATH)/bin/pip
TOX=$(VENV_PATH)/bin/tox
TWINE=$(VENV_PATH)/bin/twine
DJANGO_MANAGE=$(VENV_PATH)/bin/python sandbox/manage.py
FLAKE=$(VENV_PATH)/bin/flake8
PYTEST=$(VENV_PATH)/bin/pytest
SPHINX_RELOAD=$(PYTHON_BIN) sphinx_reload.py

DEMO_DJANGO_SECRET_KEY=samplesecretfordev
PACKAGE_NAME=cmsplugin-blocks
PACKAGE_SLUG=`echo $(PACKAGE_NAME) | tr '-' '_'`
APPLICATION_NAME=cmsplugin_blocks

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo
	@echo "  clean                         -- to clean EVERYTHING (Warning)"
	@echo "  clean-var                     -- to clean data (uploaded medias, database, etc..)"
	@echo "  clean-doc                     -- to remove documentation builds"
	@echo "  clean-backend-install         -- to clean backend installation"
	@echo "  clean-frontend-install        -- to clean frontend installation"
	@echo "  clean-frontend-build          -- to clean frontend built files"
	@echo "  clean-pycache                 -- to remove all __pycache__, this is recursive from current directory"
	@echo
	@echo "  install-backend               -- to install backend requirements with Virtualenv and Pip"
	@echo "  install-frontend              -- to install frontend requirements with Npm"
	@echo "  install                       -- to install backend and frontend"
	@echo
	@echo "  run                           -- to run Django development server"
	@echo "  migrate                       -- to apply demo database migrations"
	@echo "  migrations                    -- to create new migrations for application after changes"
	@echo "  check-migrations              -- to check for pending migrations (do not write anything)"
	@echo "  check-django                  -- to run Django System check framework"
	@echo "  superuser                     -- to create a superuser for Django admin"
	@echo
	@echo "  po                            -- to update every PO files from app and sandbox sources for enabled languages"
	@echo "  mo                            -- to build MO files from app and sandbox PO files"
	@echo
	@echo "  css                           -- to build uncompressed CSS from Sass sources"
	@echo "  icon-font                     -- to copy bootstrap-icons font to static"
	@echo "  watch-css                     -- to watch for Sass changes to rebuild CSS"
	@echo "  css-prod                      -- to build compressed and minified CSS from Sass sources"
	@echo
	@echo "  js                            -- to build uncompressed Javascript from sources"
	@echo "  watch-js                      -- to watch for Javascript sources changes to rebuild assets"
	@echo "  js-prod                       -- to build minified JS assets"
	@echo
	@echo "  frontend                      -- to build uncompressed frontend assets (CSS, JS, etc..)"
	@echo "  frontend-prod                 -- to build minified frontend assets (CSS, JS, etc..)"
	@echo
	@echo "  docs                          -- to build documentation"
	@echo "  livedocs                      -- to run livereload server to rebuild documentation on source changes"
	@echo
	@echo "  flake                         -- to launch Flake8 checking"
	@echo "  test                          -- to launch base test suite using Pytest"
	@echo "  test-initial                  -- to launch tests with pytest and re-initialized database (for after new application or model changes)"
	@echo "  tox                           -- to launch tests for every Tox environments"
	@echo "  freeze-dependencies           -- to write a frozen.txt file with installed dependencies versions"
	@echo "  quality                       -- to launch Flake8 checking and every tests suites"
	@echo
	@echo "  check-release                 -- to check package release before uploading it to PyPi"
	@echo "  release                       -- to release package for latest version on PyPi (once release has been pushed to repository)"
	@echo

clean-pycache:
	@echo ""
	@echo "==== Clear Python cache ===="
	@echo ""
	rm -Rf .tox
	rm -Rf .pytest_cache
	find . -type d -name "__pycache__"|xargs rm -Rf
	find . -name "*\.pyc"|xargs rm -f
.PHONY: clean-pycache


clean-var:
	@echo ""
	@echo "====Cleaning var/ directory ===="
	@echo ""
	rm -Rf var
.PHONY: clean-var

clean-backend-install:
	@echo ""
	@echo "====Cleaning backend install ===="
	@echo ""
	rm -Rf $(PACKAGE_SLUG).egg-info
	rm -Rf $(VENV_PATH)
.PHONY: clean-backend-install

clean-backend-build:
	@echo ""
	@echo "====Cleaning backend built files ===="
	@echo ""
	rm -Rf dist
.PHONY: clean-backend-build

clean-frontend-build:
	@echo ""
	@echo "====Cleaning frontend built files ===="
	@echo ""
	rm -Rf $(STATICFILES_DIR)/webpack-stats.json
	rm -Rf $(STATICFILES_DIR)/css
	rm -Rf $(STATICFILES_DIR)/js
	rm -Rf $(STATICFILES_DIR)/fonts
	rm -Rf $(STATICFILES_DIR)/media
.PHONY: clean-frontend-build

clean-frontend-install:
	@echo ""
	@echo "====Cleaning frontend install ===="
	@echo ""
	rm -Rf $(FRONTEND_DIR)/node_modules
.PHONY: clean-frontend-install

clean-doc:
	@echo ""
	@echo "==== Clear documentation ===="
	@echo ""
	rm -Rf docs/_build
.PHONY: clean-doc

clean: clean-var clean-doc clean-backend-install clean-backend-build clean-frontend-install clean-frontend-build clean-pycache
.PHONY: clean

venv:
	@echo ""
	@echo "==== Install virtual environment ===="
	@echo ""
	virtualenv -p $(PYTHON_INTERPRETER) $(VENV_PATH)
	# This is required for those ones using old distribution
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade setuptools
.PHONY: venv

create-var-dirs:
	@mkdir -p var/db
	@mkdir -p var/media
	@mkdir -p var/static
	@mkdir -p $(SANDBOX_DIR)/media
	@mkdir -p $(STATICFILES_DIR)/fonts
.PHONY: create-var-dirs

icon-font:
	@echo ""
	@echo "==== Copying bootstrap-icons to staticfiles directory ===="
	@echo ""
	rm -Rf $(STATICFILES_DIR)/fonts/icons
	cp -r $(FRONTEND_DIR)/node_modules/bootstrap-icons/font/fonts $(STATICFILES_DIR)/fonts/icons
.PHONY: icon-font


install-backend: venv create-var-dirs
	@echo ""
	@echo "==== Installing backend requirements ===="
	@echo ""
	$(PIP) install -e .[dev,quality,doc,release]
.PHONY: install

install-frontend:
	@echo ""
	@echo "==== Installing frontend requirements ===="
	@echo ""
	cd $(FRONTEND_DIR) && npm install
	${MAKE} icon-font
.PHONY: install-frontend

install: venv create-var-dirs install-backend migrate install-frontend frontend
.PHONY: install

migrations:
	@echo ""
	@echo "==== Making application migrations for application ===="
	@echo ""
	$(DJANGO_MANAGE) makemigrations $(APPLICATION_NAME)
.PHONY: migrations

migrate:
	@echo ""
	@echo "==== Apply pending migrations ===="
	@echo ""
	@DJANGO_SECRET_KEY=$(DEMO_DJANGO_SECRET_KEY) \
	$(DJANGO_MANAGE) migrate
.PHONY: migrate

superuser:
	@echo ""
	@echo "==== Create new superuser ===="
	@echo ""
	@DJANGO_SECRET_KEY=$(DEMO_DJANGO_SECRET_KEY) \
	$(DJANGO_MANAGE) createsuperuser
.PHONY: superuser

run:
	@echo ""
	@echo "==== Running development server ===="
	@echo ""
	@DJANGO_SECRET_KEY=$(DEMO_DJANGO_SECRET_KEY) \
	$(DJANGO_MANAGE) runserver 0.0.0.0:8001
.PHONY: run

css:
	@echo ""
	@echo "==== Building CSS for development environment ===="
	@echo ""
	cd $(FRONTEND_DIR) && npm run-script css
.PHONY: css

watch-sass:
	@echo ""
	@echo "==== Watching Sass sources for development environment ===="
	@echo ""
	cd $(FRONTEND_DIR) && npm run-script watch-css
.PHONY: watch-sass

css-prod:
	@echo ""
	@echo "==== Building CSS for production environment ===="
	@echo ""
	cd $(FRONTEND_DIR) && npm run-script css-prod
.PHONY: css-prod

js:
	@echo ""
	@echo "==== Building distributed Javascript for development environment ===="
	@echo ""
	cd $(FRONTEND_DIR) && npm run js
.PHONY: js

watch-js:
	@echo ""
	@echo "==== Watching Javascript sources for development environment ===="
	@echo ""
	cd $(FRONTEND_DIR) && npm run watch-js
.PHONY: watch-js

js-prod:
	@echo ""
	@echo "==== Building distributed Javascript for production environment ===="
	@echo ""
	cd $(FRONTEND_DIR) && npm run js-prod
.PHONY: js-prod

frontend: css js
.PHONY: frontend

frontend-prod: css-prod js-prod
.PHONY: frontend-prod

docs:
	@echo ""
	@echo "==== Build documentation ===="
	@echo ""
	cd docs && make html
.PHONY: docs

livedocs:
	@echo ""
	@echo "==== Watching documentation sources ===="
	@echo ""
	$(SPHINX_RELOAD)
.PHONY: livedocs

check-django:
	@echo ""
	@echo "==== Running Django System check framework ===="
	@echo ""
	$(DJANGO_MANAGE) check
.PHONY: check-django

check-migrations:
	@echo ""
	@echo "==== Checking for pending project applications models migrations ===="
	@echo ""
	$(DJANGO_MANAGE) makemigrations --check --dry-run -v 3
.PHONY: check-migrations

flake:
	@echo ""
	@echo "==== Running Flake check ===="
	@echo ""
	$(FLAKE) --statistics --show-source $(APPLICATION_NAME) sandbox tests
.PHONY: flake

test:
	@echo ""
	@echo "==== Running Tests ===="
	@echo ""
	$(PYTEST) -vv --reuse-db tests/
	rm -Rf var/media-tests/
.PHONY: test

test-initial:
	@echo ""
	@echo "==== Running Tests from zero ===="
	@echo ""
	$(PYTEST) -vv --reuse-db --create-db tests/
	rm -Rf var/media-tests/
.PHONY: test-initial

freeze-dependencies:
	@echo ""
	@echo "==== Freezing backend dependencies versions ===="
	@echo ""
	$(PYTHON_BIN) freezer.py
.PHONY: freeze-dependencies

tox:
	@echo ""
	@echo "==== Launching tests with Tox environments ===="
	@echo ""
	$(TOX)
.PHONY: tox

build-package:
	@echo ""
	@echo "==== Building package ===="
	@echo ""
	rm -Rf dist
	$(PYTHON_BIN) setup.py sdist
.PHONY: build-package

release: build-package
	@echo ""
	@echo "==== Releasing ===="
	@echo ""
	$(TWINE) upload dist/*
.PHONY: release

check-release: build-package
	@echo ""
	@echo "==== Checking package ===="
	@echo ""
	$(TWINE) check dist/*
.PHONY: check-release

quality: flake check-migrations test-initial docs check-release freeze-dependencies
	@echo ""
	@echo "♥ ♥ Everything should be fine ♥ ♥"
	@echo ""
.PHONY: quality
