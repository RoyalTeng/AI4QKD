#!/bin/bash
# Compile script for AI4QKD APS Paper

echo "=========================================="
echo "AI4QKD APS Paper Compilation"
echo "=========================================="

# Check for required tools
command -v pdflatex >/dev/null 2>&1 || { echo "Error: pdflatex not found. Please install TeX Live or MiKTeX."; exit 1; }
command -v bibtex >/dev/null 2>&1 || { echo "Error: bibtex not found. Please install TeX Live or MiKTeX."; exit 1; }

# Create necessary directories
mkdir -p figures
mkdir -p output

echo "1. Creating placeholder figures..."
# Create placeholder figures if they don't exist
if [ ! -f "figures/architecture.pdf" ]; then
    echo "Creating placeholder: figures/architecture.pdf"
    echo "\\documentclass{standalone}\\usepackage{tikz}\\begin{document}\\begin{tikzpicture}\\draw (0,0) rectangle (5,3);\\node at (2.5,1.5) {System Architecture};\\end{tikzpicture}\\end{document}" > temp.tex
    pdflatex -interaction=nonstopmode temp.tex > /dev/null 2>&1
    mv temp.pdf figures/architecture.pdf
    rm -f temp.*
fi

if [ ! -f "figures/bb84_graph.pdf" ]; then
    echo "Creating placeholder: figures/bb84_graph.pdf"
    echo "\\documentclass{standalone}\\usepackage{tikz}\\begin{document}\\begin{tikzpicture}\\draw (0,0) rectangle (5,3);\\node at (2.5,1.5) {BB84 Protocol Graph};\\end{tikzpicture}\\end{document}" > temp.tex
    pdflatex -interaction=nonstopmode temp.tex > /dev/null 2>&1
    mv temp.pdf figures/bb84_graph.pdf
    rm -f temp.*
fi

if [ ! -f "figures/fitness_evolution.pdf" ]; then
    echo "Creating placeholder: figures/fitness_evolution.pdf"
    echo "\\documentclass{standalone}\\usepackage{tikz}\\begin{document}\\begin{tikzpicture}\\draw (0,0) rectangle (5,3);\\node at (2.5,1.5) {Fitness Evolution};\\end{tikzpicture}\\end{document}" > temp.tex
    pdflatex -interaction=nonstopmode temp.tex > /dev/null 2>&1
    mv temp.pdf figures/fitness_evolution.pdf
    rm -f temp.*
fi

echo "2. Compiling LaTeX document..."
echo "First compilation..."
pdflatex -interaction=nonstopmode ai4qkd_aps_paper.tex > compile.log 2>&1

echo "Running BibTeX..."
bibtex ai4qkd_aps_paper >> compile.log 2>&1

echo "Second compilation..."
pdflatex -interaction=nonstopmode ai4qkd_aps_paper.tex >> compile.log 2>&1

echo "Third compilation (for references)..."
pdflatex -interaction=nonstopmode ai4qkd_aps_paper.tex >> compile.log 2>&1

# Check if PDF was created
if [ -f "ai4qkd_aps_paper.pdf" ]; then
    echo "=========================================="
    echo "✅ Paper compiled successfully!"
    echo "   Output: ai4qkd_aps_paper.pdf"
    echo "   Size: $(du -h ai4qkd_aps_paper.pdf | cut -f1)"
    echo "   Pages: $(pdfinfo ai4qkd_aps_paper.pdf 2>/dev/null | grep Pages | awk '{print $2}' || echo 'Unknown')"
    
    # Move to output directory
    mv ai4qkd_aps_paper.pdf output/
    
    # Clean up auxiliary files
    echo "Cleaning up auxiliary files..."
    rm -f *.aux *.log *.out *.bbl *.blg *.toc *.lof *.lot
    
    echo "=========================================="
    echo "📄 Paper is ready in: output/ai4qkd_aps_paper.pdf"
    
    # Open the PDF if on macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        read -p "Open PDF now? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            open output/ai4qkd_aps_paper.pdf
        fi
    fi
else
    echo "=========================================="
    echo "❌ Compilation failed!"
    echo "Check compile.log for details."
    tail -20 compile.log
    exit 1
fi