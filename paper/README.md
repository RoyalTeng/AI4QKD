# AI4QKD APS Paper

This directory contains the APS (American Physical Society) format paper for the AI4QKD project.

## 📄 Paper Files

### Main Files
- `ai4qkd_aps_paper.tex` - Main LaTeX document
- `references.bib` - Bibliography in BibTeX format
- `Makefile` - Compilation automation
- `compile_paper.sh` - Bash compilation script

### Generated Files (after compilation)
- `output/ai4qkd_aps_paper.pdf` - Final PDF paper
- `figures/` - Placeholder figures (to be replaced with actual figures)

## 🛠️ Compilation

### Requirements
- LaTeX distribution (TeX Live, MiKTeX, or MacTeX)
- `revtex4-2` class (usually included with APS templates)
- Basic LaTeX packages: graphicx, amsmath, hyperref, etc.

### Quick Compilation
```bash
# Make the script executable
chmod +x compile_paper.sh

# Compile the paper
./compile_paper.sh
```

### Using Makefile
```bash
# Check requirements
make check

# Compile PDF
make pdf

# Compile and view
make view

# Clean auxiliary files
make clean

# Clean everything
make distclean
```

## 📝 Paper Structure

### Abstract
Summarizes the AI4QKD framework and key experimental results.

### 1. Introduction
- Background on Quantum Key Distribution (QKD)
- Motivation for AI-assisted protocol design
- Overview of AI4QKD framework

### 2. The AI4QKD Framework
- System architecture (5-layer design)
- Quantum-Classical Graph Flow DSL
- Quantum simulator implementation
- AI agent using evolutionary algorithms

### 3. Experimental Results
- **Experiment 1**: BB84 protocol analysis
- **Experiment 2**: AI-driven protocol design
- **Experiment 3**: Parameter stability analysis

### 4. Discussion
- Implications for QKD protocol design
- Limitations and future directions
- Practical applications

### 5. Conclusion
- Summary of contributions
- Future research directions

## 🎨 Figures

The paper includes three figures (currently placeholders):

1. **Figure 1**: System architecture diagram
2. **Figure 2**: BB84 protocol graph representation  
3. **Figure 3**: Fitness evolution over iterations

To replace placeholders with actual figures:
1. Create high-quality vector graphics (PDF, EPS, or SVG)
2. Save to `figures/` directory with appropriate names
3. Recompile the paper

## 📊 Tables

The paper includes two tables:

1. **Table 1**: BB84 protocol performance metrics
2. **Table 2**: Parameter stability analysis

## 📚 References

Comprehensive bibliography with 15 references covering:
- Foundational QKD papers (Bennett & Brassard 1984, Ekert 1991)
- AI and machine learning breakthroughs
- Quantum information science
- Practical QKD implementations

## 🔧 Customization

### Modifying the Paper
1. Edit `ai4qkd_aps_paper.tex` for content changes
2. Update `references.bib` for bibliography changes
3. Replace placeholder figures in `figures/` directory

### Changing Format
The paper uses APS PRL (Physical Review Letters) format. To change:
1. Modify the `\documentclass` line in the main .tex file
2. Available APS classes: `prl`, `pra`, `prb`, `prc`, `prd`, `pre`, `prx`
3. See APS documentation for details

## 📈 Data Integration

The paper references experimental data from:
- `../results/bb84_result.json` - BB84 simulation results
- `../results/pulse_scan_*.json` - Parameter scanning data
- `../results/ai_designed_protocol_*.json` - AI design results

## 🎯 Target Journals

This paper is formatted for APS journals:
- **Physical Review Letters (PRL)** - Primary target
- **Physical Review A (PRA)** - Quantum information focus
- **PRX Quantum** - New quantum journal
- **Quantum** - Open access alternative

## 📋 Submission Checklist

Before submission, ensure:
- [ ] All figures are high-resolution vector graphics
- [ ] References are complete and correctly formatted
- [ ] Data availability statement is included (if required)
- [ ] Author contributions are specified
- [ ] Competing interests are declared
- [ ] Funding information is provided
- [ ] Supplementary material is prepared (if any)

## 📞 Support

For issues with compilation or formatting:
1. Check LaTeX installation and packages
2. Review APS author guidelines
3. Consult the revtex4-2 documentation
4. Check compilation logs for specific errors

## 📄 License

The paper content is subject to copyright. The LaTeX template follows APS publishing guidelines.