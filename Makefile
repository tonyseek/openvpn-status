.PHONY: build clean release doc-upgrade doc-html doc-clean doc-reset

PYTHON = python3
TWINE = twine

# readthedocs.org uses Python 3.7
DOCPYTHONVERSION=3.7
DOCPYTHON = python3.7
DOCDIR = $(realpath docs)
DOCVENVDIR = $(DOCDIR)/.venv
DOCVENVPYTHON = $(DOCVENVDIR)/bin/python3
DOCSPHINXBUILD = $(DOCVENVDIR)/bin/sphinx-build
DOCPIPCOMPILE = $(DOCVENVDIR)/bin/pip-compile
DOCPIPSYNC = $(DOCVENVDIR)/bin/pip-sync

build:
	$(PYTHON) setup.py sdist bdist_wheel

clean:
	rm -rf dist

release: clean build
	$(TWINE) upload -s  -i tonyseek@gmail.com dist/*

doc-upgrade: $(DOCPIPCOMPILE)
	cd $(DOCDIR) && $(DOCPIPCOMPILE) -r --resolver=backtracking requirements.in

doc-html: $(DOCSPHINXBUILD)
	$(DOCVENVPYTHON) -m pip install -e $(PWD)
	$(MAKE) -C $(DOCDIR) SPHINXBUILD=$(DOCSPHINXBUILD) html

doc-clean: $(DOCSPHINXBUILD)
	$(MAKE) -C $(DOCDIR) SPHINXBUILD=$(DOCSPHINXBUILD) clean

doc-reset:
	rm -rf "$(DOCVENVDIR)"

$(DOCSPHINXBUILD): $(DOCPIPSYNC)
	cd $(DOCDIR) && $(DOCPIPSYNC) --python-executable $(DOCVENVPYTHON)

$(DOCPIPSYNC):
	$(DOCPYTHON) -m venv $(DOCVENVDIR)
	$(DOCVENVPYTHON) -m pip install -U pip pip-tools

$(DOCPIPCOMPILE): $(DOCPIPSYNC)
