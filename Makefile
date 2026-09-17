# torsor-writing — checks for this repository.
#
#   make test    # the plugin's own test suite
#
# Requires Python 3 and the packages in requirements-dev.txt.

.PHONY: check test help

check: test

test:
	python3 -m unittest discover -s tests -v

help:
	@echo "targets: test"

.DEFAULT_GOAL := check
