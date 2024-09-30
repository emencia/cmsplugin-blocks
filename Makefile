PYTHON_INTERPRETER=python3
VENV_PATH=.venv

FRONTEND_DIR=frontend
SANDBOX_DIR=sandbox
STATICFILES_DIR=$(SANDBOX_DIR)/static-sources

DJANGO_MANAGE_PATH=$(SANDBOX_DIR)/manage.py

PYTHON_BIN=$(VENV_PATH)/bin/python
PIP_BIN=$(VENV_PATH)/bin/pip
TOX_BIN=$(VENV_PATH)/bin/tox
TWINE_BIN=$(VENV_PATH)/bin/twine
DJANGO_MANAGE_BIN=$(PYTHON_BIN) $(DJANGO_MANAGE_PATH)
FLAKE_BIN=$(VENV_PATH)/bin/flake8
PYTEST_BIN=$(VENV_PATH)/bin/pytest
SPHINX_RELOAD_BIN=$(PYTHON_BIN) docs/sphinx_reload.py

DEMO_DJANGO_SECRET_KEY=samplesecretfordev
PACKAGE_NAME=cmsplugin-blocks
PACKAGE_SLUG=`echo $(PACKAGE_NAME) | tr '-' '_'`
APPLICATION_NAME=cmsplugin_blocks

# Formatting variables, FORMATRESET is always to be used last to close formatting
FORMATBLUE:=$(shell tput setab 4)
FORMATGREEN:=$(shell tput setab 2)
FORMATRED:=$(shell tput setab 1)
FORMATBOLD:=$(shell tput bold)
FORMATRESET:=$(shell tput sgr0)

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo
	@echo "  Cleaning"
	@echo "  ========"
	@echo
	@echo "  clean                         -- to clean EVERYTHING (Warning)"
	@echo "  clean-var                     -- to clean data (uploaded medias, database, etc..)"
	@echo "  clean-doc                     -- to remove documentation builds"
	@echo "  clean-backend-install         -- to clean backend installation"
	@echo "  clean-frontend-install        -- to clean frontend installation"
	@echo "  clean-frontend-build          -- to clean frontend built files"
	@echo "  clean-pycache                 -- to remove all __pycache__, this is recursive from current directory"
	@echo
	@echo "  Installation"
	@echo "  ============"
	@echo
	@echo "  install-backend               -- to install backend requirements with Virtualenv and Pip"
	@echo "  install-frontend              -- to install frontend requirements with Npm"
	@echo "  install                       -- to install backend and frontend"
	@echo
	@echo "  Django commands"
	@echo "  ==============="
	@echo
	@echo "  run                           -- to run Django development server"
	@echo "  migrate                       -- to apply demo database migrations"
	@echo "  migrations                    -- to create new migrations for application after changes"
	@echo "  superuser                     -- to create a superuser for Django admin"
	@echo "  po                            -- to update every PO files from app and sandbox sources for enabled languages"
	@echo "  mo                            -- to build MO files from app and sandbox PO files"
	@echo
	@echo "  Frontend commands"
	@echo "  ================="
	@echo
	@echo "  css                           -- to build uncompressed CSS from Sass sources"
	@echo "  icon-font                     -- to copy bootstrap-icons font to static"
	@echo "  watch-css                     -- to watch for Sass changes to rebuild CSS"
	@echo "  css-prod                      -- to build compressed and minified CSS from Sass sources"
	@echo "  js                            -- to build uncompressed Javascript from sources"
	@echo "  watch-js                      -- to watch for Javascript sources changes to rebuild assets"
	@echo "  js-prod                       -- to build minified JS assets"
	@echo "  frontend                      -- to build uncompressed frontend assets (CSS, JS, etc..)"
	@echo "  frontend-prod                 -- to build minified frontend assets (CSS, JS, etc..)"
	@echo
	@echo "  Documentation"
	@echo "  ============="
	@echo
	@echo "  docs                          -- to build documentation"
	@echo "  livedocs                      -- to run livereload server to rebuild documentation on source changes"
	@echo
	@echo "  Quality"
	@echo "  ======="
	@echo
	@echo "  flake                         -- to launch Flake8 checking"
	@echo "  test                          -- to launch base test suite using Pytest"
	@echo "  test-initial                  -- to launch tests with pytest and re-initialized database (for after new application or model changes)"
	@echo "  tox                           -- to launch tests for every Tox environments"
	@echo "  freeze-dependencies           -- to write a frozen.txt file with installed dependencies versions"
	@echo "  quality                       -- to launch Flake8 checking and every tests suites"
	@echo "  check-migrations              -- to check for pending migrations (do not write anything)"
	@echo "  check-django                  -- to run Django System check framework"
	@echo "  check-release                 -- to check package release before uploading it to PyPi"
	@echo
	@echo "  Release"
	@echo "  ======="
	@echo
	@echo "  release                       -- to release package for latest version on PyPi (once release has been pushed to repository)"
	@echo

clean-pycache:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Clear Python cache <---$(FORMATRESET)\n"
	@echo ""
	rm -Rf .tox
	rm -Rf .pytest_cache
	find . -type d -name "__pycache__"|xargs rm -Rf
	find . -name "*\.pyc"|xargs rm -f
.PHONY: clean-pycache


clean-var:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Cleaning var/ directory <---$(FORMATRESET)\n"
	@echo ""
	rm -Rf var
.PHONY: clean-var

clean-doc:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Clear documentation <---$(FORMATRESET)\n"
	@echo ""
	rm -Rf docs/_build
.PHONY: clean-doc

clean-backend-install:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Cleaning backend install <---$(FORMATRESET)\n"
	@echo ""
	rm -Rf $(PACKAGE_SLUG).egg-info
	rm -Rf $(VENV_PATH)
.PHONY: clean-backend-install

clean-backend-build:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Cleaning backend built files <---$(FORMATRESET)\n"
	@echo ""
	rm -Rf dist
.PHONY: clean-backend-build

clean-frontend-install:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Cleaning frontend install <---$(FORMATRESET)\n"
	@echo ""
	rm -Rf $(FRONTEND_DIR)/node_modules
.PHONY: clean-frontend-install

clean-frontend-build:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Cleaning frontend built files <---$(FORMATRESET)\n"
	@echo ""
	rm -Rf $(STATICFILES_DIR)/webpack-stats.json
	rm -Rf $(STATICFILES_DIR)/css
	rm -Rf $(STATICFILES_DIR)/js
	rm -Rf $(STATICFILES_DIR)/fonts
	rm -Rf $(STATICFILES_DIR)/media
.PHONY: clean-frontend-build

clean: clean-var clean-doc clean-backend-install clean-backend-build clean-frontend-install clean-frontend-build clean-pycache
.PHONY: clean

venv:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Install virtual environment <---$(FORMATRESET)\n"
	@echo ""
	virtualenv -p $(PYTHON_INTERPRETER) $(VENV_PATH)
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
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Copying bootstrap-icons to staticfiles directory <---$(FORMATRESET)\n"
	@echo ""
	rm -Rf $(STATICFILES_DIR)/fonts/icons
	cp -r $(FRONTEND_DIR)/node_modules/bootstrap-icons/font/fonts $(STATICFILES_DIR)/fonts/icons
.PHONY: icon-font


install-backend:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Installing backend requirements <---$(FORMATRESET)\n"
	@echo ""
	$(PIP_BIN) install -e .[dev,quality,doc,doc-live,release]
.PHONY: install

install-frontend:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Installing frontend requirements <---$(FORMATRESET)\n"
	@echo ""
	cd $(FRONTEND_DIR) && npm install
	${MAKE} icon-font
.PHONY: install-frontend

install: venv create-var-dirs install-backend migrate install-frontend frontend
.PHONY: install

migrations:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Making application migrations for application <---$(FORMATRESET)\n"
	@echo ""
	$(DJANGO_MANAGE_BIN) makemigrations $(APPLICATION_NAME)
.PHONY: migrations

migrate:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Apply pending migrations <---$(FORMATRESET)\n"
	@echo ""
	@DJANGO_SECRET_KEY=$(DEMO_DJANGO_SECRET_KEY) \
	$(DJANGO_MANAGE_BIN) migrate
.PHONY: migrate

superuser:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Create new superuser <---$(FORMATRESET)\n"
	@echo ""
	@DJANGO_SECRET_KEY=$(DEMO_DJANGO_SECRET_KEY) \
	$(DJANGO_MANAGE_BIN) createsuperuser
.PHONY: superuser

po:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Updating PO from application <---$(FORMATRESET)\n"
	@echo ""
	@cd $(APPLICATION_NAME); ../$(PYTHON_BIN) ../$(DJANGO_MANAGE_PATH) makemessages -a --keep-pot --no-obsolete
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Updating PO from sandbox <---$(FORMATRESET)\n"
	@echo ""
	@cd $(SANDBOX_DIR); ../$(PYTHON_BIN) ../$(DJANGO_MANAGE_PATH) makemessages -a --keep-pot --no-obsolete
.PHONY: po

mo:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Building MO from application <---$(FORMATRESET)\n"
	@echo ""
	@cd $(APPLICATION_NAME); ../$(PYTHON_BIN) ../$(DJANGO_MANAGE_PATH) compilemessages --verbosity 3
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Building MO from sandbox <---$(FORMATRESET)\n"
	@echo ""
	@cd $(SANDBOX_DIR); ../$(PYTHON_BIN) ../$(DJANGO_MANAGE_PATH) compilemessages --verbosity 3
.PHONY: mo

run:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Running development server <---$(FORMATRESET)\n"
	@echo ""
	@DJANGO_SECRET_KEY=$(DEMO_DJANGO_SECRET_KEY) \
	$(DJANGO_MANAGE_BIN) runserver 0.0.0.0:8001
.PHONY: run

css:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Building CSS for development environment <---$(FORMATRESET)\n"
	@echo ""
	cd $(FRONTEND_DIR) && npm run-script css
.PHONY: css

watch-sass:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Watching Sass sources for development environment <---$(FORMATRESET)\n"
	@echo ""
	cd $(FRONTEND_DIR) && npm run-script watch-css
.PHONY: watch-sass

css-prod:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Building CSS for production environment <---$(FORMATRESET)\n"
	@echo ""
	cd $(FRONTEND_DIR) && npm run-script css-prod
.PHONY: css-prod

js:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Building distributed Javascript for development environment <---$(FORMATRESET)\n"
	@echo ""
	cd $(FRONTEND_DIR) && npm run js
.PHONY: js

watch-js:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Watching Javascript sources for development environment <---$(FORMATRESET)\n"
	@echo ""
	cd $(FRONTEND_DIR) && npm run watch-js
.PHONY: watch-js

js-prod:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Building distributed Javascript for production environment <---$(FORMATRESET)\n"
	@echo ""
	cd $(FRONTEND_DIR) && npm run js-prod
.PHONY: js-prod

frontend: css js
.PHONY: frontend

frontend-prod: css-prod js-prod
.PHONY: frontend-prod

docs:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Build documentation <---$(FORMATRESET)\n"
	@echo ""
	cd docs && make html
.PHONY: docs

livedocs:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Watching documentation sources <---$(FORMATRESET)\n"
	@echo ""
	$(SPHINX_RELOAD_BIN)
.PHONY: livedocs

check-django:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Running Django System check framework <---$(FORMATRESET)\n"
	@echo ""
	$(DJANGO_MANAGE_BIN) check
.PHONY: check-django

check-migrations:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Checking for pending project applications models migrations <---$(FORMATRESET)\n"
	@echo ""
	$(DJANGO_MANAGE_BIN) makemigrations --check --dry-run -v 3
.PHONY: check-migrations

flake:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Running Flake check <---$(FORMATRESET)\n"
	@echo ""
	$(FLAKE_BIN) --statistics --show-source $(APPLICATION_NAME) sandbox tests
.PHONY: flake

test:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Running Tests <---$(FORMATRESET)\n"
	@echo ""
	$(PYTEST_BIN) --reuse-db tests/
	rm -Rf var/media-tests/
.PHONY: test

test-initial:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Running Tests from zero <---$(FORMATRESET)\n"
	@echo ""
	$(PYTEST_BIN) --reuse-db --create-db tests/
	rm -Rf var/media-tests/
.PHONY: test-initial

freeze-dependencies:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Freezing backend dependencies versions <---$(FORMATRESET)\n"
	@echo ""
	$(PYTHON_BIN) freezer.py ${PACKAGE_NAME} --destination=frozen.txt
.PHONY: freeze-dependencies

tox:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Launching tests with Tox environments <---$(FORMATRESET)\n"
	@echo ""
	$(TOX_BIN)
.PHONY: tox

build-package:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Building package <---$(FORMATRESET)\n"
	@echo ""
	rm -Rf dist
	$(PYTHON_BIN) setup.py sdist
.PHONY: build-package

release: build-package
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Releasing <---$(FORMATRESET)\n"
	@echo ""
	$(TWINE_BIN) upload dist/*
.PHONY: release

check-release: build-package
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Checking package <---$(FORMATRESET)\n"
	@echo ""
	$(TWINE_BIN) check dist/*
.PHONY: check-release

quality: flake check-migrations test-initial docs check-release freeze-dependencies
	@echo ""
	@echo "♥ ♥ Everything should be fine ♥ ♥"
	@echo ""
.PHONY: quality
