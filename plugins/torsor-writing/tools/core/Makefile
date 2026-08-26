# torsor unified builder — static Makefile (identical in every deliverable).
#
# Per-document values live in config.mk (written by the assembler).
# Formats live in formats/*.mk; enabled features live in features/*/*.mk.
# Each format/feature target self-registers into FORMAT_TARGETS, so `all` and
# `check` pick up new formats and features with NO edit to this file.
#
# Adding a format  = drop a formats/<name>.mk.
# Adding a feature = the assembler vendors features/<name>/ when it is enabled.

include config.mk

PYTHON    ?= python3
LATEX_DIR := latex
HTML_DIR  := html
EPUB_DIR  := epub
MD_DIR    := markdown

# Format/feature fragments append their target names + checked outputs here.
FORMAT_TARGETS :=
CHECK_OUTPUTS  :=
# Extra pandoc flags the pandoc-driven formats include (the bib feature sets this
# to --citeproc --bibliography=references.bib; empty otherwise).
PANDOC_BIB     :=

include $(wildcard formats/*.mk)
include $(wildcard features/*/*.mk)

.PHONY: all prepare check clean help $(sort $(FORMAT_TARGETS))

all: $(FORMAT_TARGETS) check

# Front-end hook: the from-markdown front-end overrides this to convert
# source -> latex/chapters/*.tex. With authored LaTeX it is a no-op.
prepare:
	@:

check: $(FORMAT_TARGETS)
	$(PYTHON) check-build.py --stem "$(STEM)" $(if $(CHECK_OUTPUTS),--require $(CHECK_OUTPUTS))

help:
	@echo "Targets:"
	@echo "  make all    - build every registered format, then check"
	@echo "  make check  - run check-build.py"
	@echo "  make clean  - remove generated outputs"
	@echo "  registered formats: $(sort $(FORMAT_TARGETS))"

clean:
	rm -rf $(HTML_DIR) $(EPUB_DIR) $(MD_DIR)
	rm -f $(LATEX_DIR)/$(STEM).pdf $(LATEX_DIR)/main.pdf
	rm -f $(LATEX_DIR)/*.aux $(LATEX_DIR)/*.log $(LATEX_DIR)/*.out $(LATEX_DIR)/*.toc
	rm -f $(LATEX_DIR)/*.fls $(LATEX_DIR)/*.fdb_latexmk $(LATEX_DIR)/*.synctex.gz
	rm -f $(LATEX_DIR)/chapters/*.aux
	rm -rf $(LATEX_DIR)/.build
