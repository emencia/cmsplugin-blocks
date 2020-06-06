#!/usr/bin/env python
"""
Basic script to launch a livereload server to watch and rebuild documentation
on "docs/" file changes.

Once launched, server will be available on port 8002, like: ::

    http://localhost:8002/

Borrowed from: ::

    https://livereload.readthedocs.io/en/latest/#script-example-sphinx

"""
from livereload import Server, shell


server = Server()

# Watch root documents
server.watch(
    'docs/*.rst',
    shell(
        'make html',
        cwd='docs'
    )
)

# Watch plugin documents
server.watch(
    'docs/plugins/*.rst',
    shell(
        'make html',
        cwd='docs'
    )
)

# Watch plugin models since plugin documents use autodoc on them
server.watch(
    'cmsplugin_blocks/models/*.py',
    shell(
        'make html',
        cwd='docs'
    )
)

# Watch app settings file used in install document
server.watch(
    'cmsplugin_blocks/settings.py',
    shell(
        'make html',
        cwd='docs'
    )
)

# Watch template tag file used in smart-format document
server.watch(
    'cmsplugin_blocks/templatetags/smart_format.py',
    shell(
        'make html',
        cwd='docs'
    )
)

# Serve the builded documentation
server.serve(
    root='docs/_build/html',
    port=8002,
    host="0.0.0.0",
)
