# Format: HTML (tex2torsor). Feature html slices (e.g. math's MathJax) attach as
# their own follow-on targets (html-mathjax: html), so this stays feature-agnostic.
FORMAT_TARGETS += html
CHECK_OUTPUTS  += $(HTML_DIR)/$(STEM).html

html: prepare
	@set -e; \
	mkdir -p $(HTML_DIR); \
	$(PYTHON) tex2torsor/tex2torsor.py $(LATEX_DIR)/main.tex \
	  -o $(HTML_DIR)/$(STEM).html \
	  --css tokens.css \
	  --css doc.css $(PANDOC_BIB); \
	cp tex2torsor/css/tokens.css $(HTML_DIR)/tokens.css; \
	cp tex2torsor/css/doc.css $(HTML_DIR)/doc.css; \
	if [ -d "$(LATEX_DIR)/assets" ]; then \
	  mkdir -p $(HTML_DIR)/assets; \
	  cp $(LATEX_DIR)/assets/* $(HTML_DIR)/assets/ 2>/dev/null || true; \
	fi
