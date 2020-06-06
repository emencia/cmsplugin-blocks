.. _virtualenv: http://www.virtualenv.org
.. _pip: https://pip.pypa.io
.. _Pytest: http://pytest.org
.. _Napoleon: https://sphinxcontrib-napoleon.readthedocs.org
.. _Flake8: http://flake8.readthedocs.org
.. _Sphinx: http://www.sphinx-doc.org
.. _tox: http://tox.readthedocs.io
.. _sphinx-autobuild: https://github.com/GaretJax/sphinx-autobuild

===========
Development
===========

Development requirement
***********************

cmsplugin-blocks is developed with:

* *Test Development Driven* (TDD) using `Pytest`_;
* Respecting flake and pip8 rules using `Flake8`_;
* `Sphinx`_ for documentation with enabled `Napoleon`_ extension (using
  *Google style*);

Every requirement is available in package extras requirements in ``dev``
section.

Install for development
***********************

First ensure you have `pip`_ and ``python-venv`` package installed then type: ::

    git clone https://github.com/emencia/cmsplugin-blocks.git
    cd cmsplugin-blocks
    make install

cmsplugin-blocks will be installed in editable mode from the last commit on
master branch with some development tools.

Unittests
---------

Unittests are made to works on `Pytest`_, a shortcut in Makefile is available
to start them on your current development install: ::

    make tests


Tox
---

To ease development against multiple Python versions a tox configuration has
been added. You are strongly encouraged to use it to test your pull requests.

Before using it you will need to install tox, it is recommended to install it
at your system level (tox dependancy is not in requirements): ::

    sudo pip install tox

Then go in the ``cmsplugin-blocks`` package directory, where ``the setup.py``
and ``tox.ini`` live and execute tox: ::

    tox

Documentation
-------------

Use the Makefile action ``livedocs`` to serve documentation and automatically
rebuild it when you change documentation files.

When environnement is activated, you can use following command from ``docs/``
directory: ::

    make livedocs

And go on ``http://localhost:8002/`` or your server machine IP with port 8002.

Contribution
------------

* Every new feature or changed behavior must pass tests, Flake8 code quality
  and must be documented.
* New component should have feature(s) that cannot be implemented with another
  component or implement a common layout object not already covered by
  available components;
* Every feature or behavior must be compatible for all supported environment.
