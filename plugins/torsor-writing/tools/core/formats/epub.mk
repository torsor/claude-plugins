# Format: EPUB with MathML math (pandoc, directly from the LaTeX tree).
# The math=svg variant is contributed separately by the math feature (epub-svg),
# so this recipe is the mathml baseline every genre gets.
FORMAT_TARGETS += epub
CHECK_OUTPUTS  += $(EPUB_DIR)/$(STEM).epub

epub: prepare
	mkdir -p $(EPUB_DIR)
	cd $(LATEX_DIR) && pandoc main.tex \
	  --toc \
	  --split-level=1 $(EPUB_COVER) \
	  --mathml $(PANDOC_BIB) \
	  --metadata title="$(DOC_TITLE)" \
	  --metadata author="$(DOC_AUTHOR)" \
	  -o ../$(EPUB_DIR)/$(STEM).epub
