# Math feature — Make slice.
# Present in a deliverable only when the `math` feature is enabled, so its mere
# presence switches on the math-specific build steps (no MATH conditional).
# Contributes two self-registering targets:
#   epub-svg      the epub recipe's math=svg variant (equations -> embedded SVG)
#   html-mathjax  a post-step on html that injects the MathJax loader
# Both reach `all` and `check` via FORMAT_TARGETS.

FORMAT_TARGETS += epub-svg html-mathjax
CHECK_OUTPUTS  += $(EPUB_DIR)/$(STEM)-svg.epub

# EPUB with math rendered to SVG via latex+dvisvgm (the math feature's epub slice).
epub-svg: prepare
	mkdir -p $(EPUB_DIR)
	cd $(LATEX_DIR) && MATHSVG_OUTDIR="$(CURDIR)/$(LATEX_DIR)/.build/mathsvg" pandoc main.tex \
	  --toc \
	  --split-level=1 $(EPUB_COVER) $(PANDOC_BIB) \
	  --filter ../features/math/mathsvg_filter.py \
	  --metadata title="$(DOC_TITLE)" \
	  --metadata author="$(DOC_AUTHOR)" \
	  -o ../$(EPUB_DIR)/$(STEM)-svg.epub

# HTML MathJax loader injection (the math feature's html slice), after html builds.
html-mathjax: html
	$(PYTHON) features/math/inject_mathjax.py $(HTML_DIR)/$(STEM).html
