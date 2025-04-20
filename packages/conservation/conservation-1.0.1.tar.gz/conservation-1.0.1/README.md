# Conservation

[![PyPI version](https://badge.fury.io/py/conservation.svg)](https://badge.fury.io/py/conservation)

**Conservation** is a Python package for evolutionary conservation analysis at the codon and amino acid level. It supports comparative analysis using Pfam domain sequences and CDS datasets across multiple species.

## 🔧 Features

- Codon substitution matrix computation
- Fisher's exact test for conservation significance
- Automated visualization of alignment and substitution matrices
- Supports BLOSUM62 alignment, multi-threading, and multiple species

## 📦 Installation

You can install the package from PyPI:

```bash
pip install conservation
```

Or from Bioconda:

```bash
conda install -c bioconda conservation
```

Or install from source:

```bash
git clone https://github.com/hanjunlee21/conservation.git
cd conservation
pip install .
```

## 🚀 Usage

```bash
conservation codon \
  --domain domain.fasta \
  --cds species1.fasta,species2.fasta \
  --output results_dir \
  --threads 4
```

### Command-line Arguments

- `--domain`, `-d`: Pfam or domain FASTA file
- `--cds`, `-c`: Comma-separated list of CDS FASTA files (one per species)
- `--output`, `-o`: Output directory
- `--threads`, `-t`: Number of parallel threads
- `--fdr`, `-q`: FDR cutoff (optional)
- `--conservedness`, `-s`: Identity ratio threshold (optional)
- `--dpi`, `-r`: DPI for PDF plots

## 📊 Outputs

- Codon substitution matrix `.tsv`
- Statistical analysis `.statistics.tsv`
- PDF visualizations of alignments and substitution matrices

## 🧬 Example

Example command for 3 species:
```bash
conservation codon \
  -d pfam_domain.fasta \
  -c human.fasta,mouse.fasta,yeast.fasta \
  -o conservation_output
```

## 📁 Project Structure

```
conservation/
├── conservation/
├── ├── lib/
│   ├── └── N34_modifications.tsv
│   ├── __init__.py
│   ├── commands.py
│   ├── conservation_codon.py
│   └── version.py
├── bin/
│   └── conservation
├── README.md
├── setup.py
├── pyproject.toml
└── ...
```

## 📜 License

MIT License

## 👤 Author

**Hanjun Lee**  
[hanjun_lee@hms.harvard.edu](mailto:hanjun_leehms.harvard.edu)

Project URL: [https://github.com/hanjunlee21/conservation](https://github.com/hanjunlee21/conservation)
