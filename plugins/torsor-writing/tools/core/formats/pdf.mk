# Format: PDF (latexd, falling back to latexmk). Deliverable is <stem>.pdf.
FORMAT_TARGETS += pdf

pdf: prepare
	@if command -v latexd >/dev/null 2>&1; then \
	  latexd $(LATEX_DIR)/main.tex; \
	  if command -v latexmk >/dev/null 2>&1; then \
	    latexmk -pdf -interaction=nonstopmode -halt-on-error -cd $(LATEX_DIR)/main.tex; \
	  fi; \
	else \
	  echo "latexd not on PATH - falling back to latexmk"; \
	  latexmk -pdf -interaction=nonstopmode -halt-on-error -cd $(LATEX_DIR)/main.tex; \
	fi
	@[ "$(STEM)" = "main" ] || cp $(LATEX_DIR)/main.pdf $(LATEX_DIR)/$(STEM).pdf
