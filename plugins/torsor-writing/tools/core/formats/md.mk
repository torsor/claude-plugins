# Format: Markdown (GitHub-Flavored), derived from the canonical LaTeX tree.
FORMAT_TARGETS += md
CHECK_OUTPUTS  += $(MD_DIR)/$(STEM).md

md: prepare
	mkdir -p $(MD_DIR)
	cd $(LATEX_DIR) && pandoc main.tex \
	  --toc $(PANDOC_BIB) \
	  -t gfm \
	  -o ../$(MD_DIR)/$(STEM).md
