# Bib feature — Make slice.
# Present only when the bib feature is enabled. Citations for the pandoc-driven
# formats (HTML via tex2torsor, EPUB, Markdown) resolve through pandoc
# --citeproc against the vendored references.bib; the PDF path uses biblatex +
# biber (latexmk runs biber automatically). Formats append $(PANDOC_BIB) to
# their pandoc/tex2torsor invocations, so this one variable switches citations
# on across every pandoc format at once.
PANDOC_BIB := --citeproc --bibliography=references.bib
