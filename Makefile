.PHONY: build clean release doc-upgrade doc-html doc-clean doc-reset

PYTHON = python3
TWINE = twine

# pip-tools
PIP_COMPILE = pip-compile
PIP_SYNC = pip-sync

DOCDIR = $(realpath docs)
DOCVENVDIR = $(DOCDIR)/.venv
DOCPYTHON = $(DOCVENVDIR)/bin/python3
DOCSPHINXBUILD = $(DOCVENVDIR)/bin/sphinx-build

build:
	$(PYTHON) setup.py sdist bdist_wheel

clean:
	rm -rf dist

release: clean build
	$(TWINE) upload -s  -i tonyseek@gmail.com dist/*

doc-upgrade:
	cd $(DOCDIR) && $(PIP_COMPILE) --resolver=backtracking requirements.in

doc-html: $(DOCSPHINXBUILD)
	$(DOCPYTHON) -m pip install -e $(PWD)
	$(MAKE) -C $(DOCDIR) SPHINXBUILD=$(DOCSPHINXBUILD) html

doc-clean: $(DOCSPHINXBUILD)
	$(MAKE) -C $(DOCDIR) SPHINXBUILD=$(DOCSPHINXBUILD) clean

doc-reset:
	rm -rf "$(DOCVENVDIR)"

$(DOCSPHINXBUILD):
	$(PYTHON) -m venv $(DOCVENVDIR)
	cd $(DOCDIR) && $(PIP_SYNC) --python-executable $(DOCPYTHON)
