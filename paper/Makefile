# Makefile for AI4QKD APS Paper

.PHONY: all clean pdf view

# Main LaTeX file
MAIN = ai4qkd_aps_paper
BIB = references

# Compilation tools
LATEX = pdflatex
BIBTEX = bibtex
VIEWER = open

# Output files
PDF = $(MAIN).pdf
AUX = $(MAIN).aux
LOG = $(MAIN).log
OUT = $(MAIN).out
BLG = $(MAIN).blg
BBL = $(MAIN).bbl
TOC = $(MAIN).toc
LOF = $(MAIN).lof
LOT = $(MAIN).lot

all: pdf

pdf: $(PDF)

$(PDF): $(MAIN).tex $(BIB).bib
	@echo "Compiling LaTeX document..."
	$(LATEX) $(MAIN).tex
	$(BIBTEX) $(MAIN)
	$(LATEX) $(MAIN).tex
	$(LATEX) $(MAIN).tex
	@echo "PDF generated: $(PDF)"

view: $(PDF)
	$(VIEWER) $(PDF)

clean:
	@echo "Cleaning auxiliary files..."
	rm -f $(AUX) $(LOG) $(OUT) $(BLG) $(BBL) $(TOC) $(LOF) $(LOT)
	rm -f *.bbl *.blg *.aux *.log *.out *.toc *.lof *.lot
	@echo "Clean complete."

distclean: clean
	@echo "Cleaning PDF file..."
	rm -f $(PDF)
	@echo "Distclean complete."

help:
	@echo "Available targets:"
	@echo "  all     - Compile the paper (default)"
	@echo "  pdf     - Generate PDF file"
	@echo "  view    - Generate PDF and open it"
	@echo "  clean   - Remove auxiliary files"
	@echo "  distclean - Remove all generated files"
	@echo "  help    - Show this help message"

# Check for required tools
check:
	@echo "Checking for required tools..."
	@which $(LATEX) > /dev/null || echo "Error: $(LATEX) not found"
	@which $(BIBTEX) > /dev/null || echo "Error: $(BIBTEX) not found"
	@echo "Tool check complete."

# Word count
wordcount:
	@echo "Counting words in document..."
	@detex $(MAIN).tex | wc -w
	@echo "Word count complete."

# Create archive
archive:
	@echo "Creating archive..."
	@tar -czf ai4qkd_paper_$(shell date +%Y%m%d).tar.gz *.tex *.bib Makefile
	@echo "Archive created: ai4qkd_paper_$(shell date +%Y%m%d).tar.gz"