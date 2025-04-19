#!/usr/bin/env python3

import os
import re
import math
import argparse
import itertools
import numpy as np
import pandas as pd
import importlib_resources
from tqdm.auto import tqdm
import multiprocessing as mp
from Bio import SeqIO
from Bio import Align
from Bio.Align import substitution_matrices
from scipy.stats import fisher_exact
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib as mpl
import matplotlib.colors as mcolors

import warnings
warnings.filterwarnings("ignore")

# === Argument Parser ===
def parse_args():
    parser = argparse.ArgumentParser(prog="conservation codon", description="Codon conservation analysis from Pfam domains and CDS sequences.")
    parser.add_argument('-d', '--domain', required=True, help='FASTA file of domain sequences (e.g., Pfam)')
    parser.add_argument('-c', '--cds', required=True, help='Comma-separated list of CDS fasta files for each organism')
    parser.add_argument('-o', '--output', required=True, help='Output directory to store results')
    parser.add_argument('-t', '--threads', type=int, default=1, help='Number of parallel threads (default: 1)')
    parser.add_argument('-q', '--fdr', type=float, default=None, help='FDR cutoff (default: 0.05 / num_records)')
    parser.add_argument('-s', '--conservedness', type=float, default=None, help='Identity ratio threshold (default: mean + 2*std)')
    parser.add_argument('-r', '--dpi', type=int, default=300, help='DPI for all generated PDF files (default: 300)')
    return parser.parse_args()

# === Helper Function ===
def extract_species_name(filepath):
    filename = os.path.basename(filepath)
    if filename.endswith('.fasta') or filename.endswith('.fa'):
        return filename.split('.')[0]
    return filename

def get_aligner():
    aligner = Align.PairwiseAligner(mode='local')
    aligner.substitution_matrix = substitution_matrices.load("BLOSUM62")
    aligner.open_gap_score = -11 # BLAST default
    aligner.extend_gap_score = -1 # BLAST default
    return aligner

def count_identity_nonidentity(substitution_matrix):
    identity = 0
    non_identity = 0
    for codon_sub, row in substitution_matrix.iterrows():
        codon1, codon2 = codon_sub.split('>')
        count = row['count']
        if codon1 == codon2:
            identity += count
        else:
            non_identity += count
    return identity, non_identity

# === Plot Function ===
def visualize_substitution_matrix(path, normalization='log2_obsexp', dpi=300):
    assert normalization in ['raw', 'log2_obsexp'], "Normalization must be 'raw' or 'log2_obsexp'"

    # === Derive paths ===
    outputDir = os.path.dirname(path)
    filename_wo_ext = os.path.splitext(os.path.basename(path))[0]
    pdfPath = os.path.join(outputDir, f"{filename_wo_ext}.{normalization}.pdf")
    
    with importlib_resources.open_text("conservation.lib", "N34_modifications.tsv") as f:
        tRNA_df = pd.read_csv(
            f,
            sep='\t',
            names=['amino_acid', 'codon', 'N34_modification'],
            index_col=1
        )

    substitution_df = pd.read_csv(path, sep='\t', index_col=0)

    # === Step 1: Convert 4096x1 to 96x96 matrix ===
    codons = tRNA_df.index.tolist()
    matrix = pd.DataFrame(0, index=codons, columns=codons)
    for idx, row in substitution_df.iterrows():
        src, dst = idx.split('>')
        if src in codons and dst in codons:
            matrix.at[src, dst] = row['count']

    # === Step 2: Normalize based on method ===
    if normalization == 'log2_obsexp':
        normalized_matrix = pd.DataFrame(0.0, index=codons, columns=codons)
        unique_aas = tRNA_df['amino_acid'].unique()
        aa_to_codons = {aa: tRNA_df[tRNA_df['amino_acid'] == aa].index.tolist() for aa in unique_aas}
        for aa_row in unique_aas:
            for aa_col in unique_aas:
                codons_row = aa_to_codons[aa_row]
                codons_col = aa_to_codons[aa_col]
                obs = matrix.loc[codons_row, codons_col].astype(float)
                row_sums = obs.sum(axis=1).values.reshape(-1, 1)
                col_sums = obs.sum(axis=0).values.reshape(1, -1)
                total = row_sums.sum()
                if total == 0:
                    continue
                exp = (row_sums @ col_sums) / total
                with np.errstate(divide='ignore', invalid='ignore'):
                    ratio = np.divide(obs, exp, out=np.zeros_like(obs), where=(exp != 0))
                    log2_ratio = np.log2(ratio, where=(ratio > 0))
                    log2_ratio = np.nan_to_num(log2_ratio, nan=0.0, posinf=0.0, neginf=0.0)
                normalized_matrix.loc[codons_row, codons_col] = log2_ratio
        normalized_matrix = normalized_matrix.values
        cmap = plt.cm.get_cmap('RdBu_r')
        vmin, vmax = -1, 1
        colorbar_label = "log2 observed/expected"

    else:  # raw
        normalized_matrix = matrix.values.astype(float)
        cmap = plt.cm.get_cmap('Greys')
        vmin, vmax = 0, np.max(normalized_matrix)
        colorbar_label = "Raw substitution counts"

    # === Step 3: Visualization ===
    fig = plt.figure(figsize=(12, 10))
    gs = fig.add_gridspec(20, 24)
    ax_matrix = fig.add_subplot(gs[2:20, 2:20])
    im = ax_matrix.imshow(normalized_matrix, cmap=cmap, aspect='equal', vmin=vmin, vmax=vmax, extent=(0, len(codons), 0, len(codons)))
    ax_matrix.set_xticks(np.arange(len(codons)))
    ax_matrix.set_yticks(np.arange(len(codons)))
    ax_matrix.set_xticklabels([])
    ax_matrix.set_yticklabels([])
    ax_matrix.tick_params(length=0)

    plt.rcParams['font.family'] = 'Arial'

    # === Color bands for amino acids and N34_modification ===
    amino_acids = tRNA_df['amino_acid'].tolist()
    n34_mods = tRNA_df['N34_modification'].tolist()
    aa_colors = []
    prev_aa = None
    toggle = False
    for aa in amino_acids:
        if aa != prev_aa:
            toggle = not toggle
        aa_colors.append('black' if toggle else 'white')
        prev_aa = aa

    n34_unique = sorted(set(n34_mods))
    # Color-blind-friendly colors
    colorblind_palette = [
        "#891522",  # amber red
        "#FFFFFF",  # white
        "#FC8EAC",  # flamingo
        "#999933",  # olive
        "#DDCC77",  # sand
        "#BBBBBB",  # gray
        "#332288",  # dark blue
        "#88CCEE",  # light blue

    ]
    # Map modifications to colorblind-friendly colors
    n34_colors_map = {}
    for i, mod in enumerate(n34_unique):
        if mod == 'N34':
            n34_colors_map[mod] = 'white'
        else:
            color = colorblind_palette[i % len(colorblind_palette)]
            n34_colors_map[mod] = color
    ax_top_aa = fig.add_subplot(gs[0, 2:20])
    ax_left_aa = fig.add_subplot(gs[2:20, 0])
    for i in range(len(codons)):
        ax_top_aa.add_patch(Rectangle((i, 0), 1, 1, color=aa_colors[i]))
        ax_left_aa.add_patch(Rectangle((0, len(codons) - 1 - i), 1, 1, color=aa_colors[i]))
    ax_top_aa.set_xlim(0, len(codons))
    ax_left_aa.set_ylim(0, len(codons))
    ax_top_aa.axis('off')
    ax_left_aa.axis('off')
    for i, aa in enumerate(amino_acids):
        text_color = 'white' if aa_colors[i] == 'black' else 'black'
        ax_top_aa.text(i + 0.5, 0.5, aa, ha='center', va='center', color=text_color, fontsize=6)
        ax_left_aa.text(0.5, len(codons) - 1 - i + 0.5, aa, ha='center', va='center', color=text_color, fontsize=6)

    ax_top_n34 = fig.add_subplot(gs[1, 2:20])
    ax_left_n34 = fig.add_subplot(gs[2:20, 1])

    for i, codon in enumerate(codons):
        mod = n34_mods[i]
        color = n34_colors_map[mod]
        ax_top_n34.add_patch(Rectangle((i, 0), 1, 1, color=color))
        ax_left_n34.add_patch(Rectangle((0, len(codons) - 1 - i), 1, 1, color=color))

        # Choose readable font color based on luminance
        rgb = mcolors.to_rgb(color)
        luminance = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]
        font_color = 'black' if luminance > 0.5 else 'white'

        # Add vertical codon text (top layer)
        ax_top_n34.text(i + 0.5, 0.5, codon, ha='center', va='center',
                        fontsize=5, rotation='vertical', color=font_color)

        # Add horizontal codon text (left layer)
        ax_left_n34.text(0.5, len(codons) - 1 - i + 0.5, codon, ha='center', va='center',
                         fontsize=5, color=font_color)

    ax_top_n34.set_xlim(0, len(codons))
    ax_left_n34.set_ylim(0, len(codons))
    ax_top_n34.axis('off')
    ax_left_n34.axis('off')

    # === Add legend and colorbar ===
    # Ensure 'N34' is first, then 'missing', then the rest sorted alphabetically
    priority_mods = ['N34', 'missing']
    remaining_mods = sorted([mod for mod in n34_unique if mod not in priority_mods])
    ordered_mods = priority_mods + remaining_mods

    legend_elements = [
        Line2D([0], [0], marker='s', color='w', label=mod,
               markerfacecolor=n34_colors_map[mod], markersize=10)
        for mod in ordered_mods
    ]

    ax_legend = fig.add_subplot(gs[0:5, 21:24])
    ax_legend.axis('off')
    ax_legend.legend(handles=legend_elements, loc='upper left', frameon=False, title='N34 mods')

    cbar_ax = inset_axes(ax_matrix, width="60%", height="3%", loc='upper right', borderpad=2)
    cb = fig.colorbar(im, cax=cbar_ax, orientation='horizontal')
    cb.ax.tick_params(labelsize=8)
    cb.set_label(colorbar_label, fontsize=10, labelpad=4)
    cb.ax.xaxis.set_label_position('top')

    # === Save ===
    plt.savefig(pdfPath, bbox_inches='tight', dpi=dpi)
    plt.close()
    
# === Analysis Function ===
def blastp(sequence, organism, ORFs, aligner):
    bestAlignmentScore = 0 # Smith-Waterman Alignment Score
    bestORF = ORFs[0] # SeqRecord object
    for ORF in ORFs:
        alignmentScore = aligner.score(sequence,ORF.seq.translate())
        if alignmentScore > bestAlignmentScore:
            bestAlignmentScore = alignmentScore
            bestORF = ORF
    return bestAlignmentScore, bestORF

def blastp_multi(sequence, species_dict, aligner):
    alignments = []
    ORFs = []
    for organism, organism_orfs in species_dict.items():
        score, ORF = blastp(sequence, organism, organism_orfs, aligner)
        alignment = aligner.align(sequence, ORF.seq.translate())
        alignments.append(alignment[0])
        ORFs.append(ORF)
    return alignments, ORFs

def blastc(sequence, species_dict, aligner):
    alignments, ORFs = blastp_multi(sequence, species_dict, aligner)
    species = list(species_dict.keys())
    alignments_df = pd.DataFrame(columns=species, index=range(len(sequence)))
    alignmentsFna_df = pd.DataFrame(columns=species, index=range(len(sequence)))
    alignmentsFaa_df = pd.DataFrame(columns=species, index=range(len(sequence)))
    for organismIndex in range(len(species)):
        organismAligned = alignments[organismIndex].aligned
        target_coords, query_coords = organismAligned
        for (t_start, t_end), (q_start, q_end) in zip(target_coords, query_coords):
            for target_pos, query_pos in zip(range(t_start, t_end), range(q_start, q_end)):
                alignments_df.at[target_pos, species[organismIndex]] = query_pos
    for organismIndex in range(len(species)):
        for target_coord in range(len(sequence)):
            Fna = ORFs[organismIndex].seq
            Faa = Fna.translate()
            query_coord = alignments_df.at[target_coord, species[organismIndex]]
            if not math.isnan(query_coord):
                alignmentsFna_df.at[target_coord, species[organismIndex]] = Fna[3*query_coord:3*query_coord+3]
                alignmentsFaa_df.at[target_coord, species[organismIndex]] = Faa[query_coord:query_coord+1]
    return alignments_df, alignmentsFna_df, alignmentsFaa_df

def blastc_on_fasta_record(fastaRecord, species_dict, aligner):
    name = fastaRecord.name
    sequence = fastaRecord.seq
    alignments_df, alignmentsFna_df, alignmentsFaa_df = blastc(sequence, species_dict, aligner)
    bases = ['A', 'C', 'G', 'T']
    codons = [f"{base1}{base2}{base3}" for base1 in bases for base2 in bases for base3 in bases]
    substitutionMatrixIndices = [f"{codon1}>{codon2}" for codon1 in codons for codon2 in codons]
    substitutionMatrix_local = pd.DataFrame(0, index=substitutionMatrixIndices, columns=["count"])
    for target_coord in range(len(sequence)):
        if alignmentsFaa_df.iloc[target_coord].notna().all() and alignmentsFaa_df.iloc[target_coord].nunique() == 1:
            query_codons = alignmentsFna_df.iloc[target_coord]
            query_codon_pairs = list(itertools.permutations(query_codons, 2))
            for query_codon1, query_codon2 in query_codon_pairs:
                substitutionMatrixIndex = f"{query_codon1}>{query_codon2}"
                if substitutionMatrixIndex in substitutionMatrix_local.index:
                    substitutionMatrix_local.loc[substitutionMatrixIndex, "count"] += 1
    return substitutionMatrix_local

def blastc_on_fasta_record_helper(args):
    fastaRecord, species, aligner = args
    return blastc_on_fasta_record(fastaRecord, species, aligner)

def blastc_on_fasta(fastaPath, species_dict, aligner, num_workers):
    fasta = list(SeqIO.parse(fastaPath, 'fasta'))
    args = [(record, species_dict, aligner) for record in fasta]
    with mp.Pool(num_workers) as pool:
        substitutionMatrices = list(
            tqdm(pool.imap(blastc_on_fasta_record_helper, args), 
                 total=len(fasta), 
                 desc='BLAST-C throughout '+fastaPath)
        )
    substitutionMatrix = pd.concat(substitutionMatrices).groupby(level=0).sum()
    return substitutionMatrix

def process_record(args):
    record, species_dict, aligner = args
    matrix = blastc_on_fasta_record(record, species_dict, aligner)
    identity, non_identity = count_identity_nonidentity(matrix)
    return {
        'record': record.name,
        'sequence': str(record.seq),
        'substitution_matrix': matrix,
        'identity': identity,
        'non_identity': non_identity
    }


def plot_alignment(record_name, sequence, species_dict, aligner, output_dir, dpi):
    alignments_df, alignmentsFna_df, alignmentsFaa_df = blastc(sequence, species_dict, aligner)
    # Set global font
    mpl.rcParams['font.family'] = 'Arial'
    # Load N34 modification codon data
    with importlib_resources.open_text("conservation.lib", "N34_modifications.tsv") as f:
        tRNA_df = pd.read_csv(
            f,
            sep='\t',
            names=['amino_acid', 'codon', 'N34_modification'],
            index_col=1
        )
    # Color-blind-friendly palette
    colorblind_palette = [
        "#891522", "#FFFFFF", "#FC8EAC", "#999933",
        "#DDCC77", "#BBBBBB", "#332288", "#88CCEE"
    ]
    n34_unique = sorted(tRNA_df['N34_modification'].unique())
    n34_colors_map = {
        mod: 'white' if mod == 'N34' else colorblind_palette[i % len(colorblind_palette)]
        for i, mod in enumerate(n34_unique)
    }

    # Layout parameters
    cell_width = 1.0
    cell_height = 0.5  # compact row height
    font_size = cell_height * 72 * 0.9  # approx in points (dpi = 72), with slight padding
    n_cols = len(alignmentsFna_df)
    n_rows = len(alignmentsFna_df.columns)
    fig_width = n_cols * cell_width + 4
    fig_height = (n_rows + 1) * cell_height + 1
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.set_xlim(0, n_cols)
    ax.set_ylim(0, (n_rows + 1) * cell_height)
    ax.axis('off')

    # === Top N34 row for AA-conserved loci ===
    for col_idx in range(n_cols):
        aa_col = alignmentsFaa_df.iloc[col_idx]
        # Skip if any NaN or not fully conserved
        if aa_col.isna().any() or aa_col.nunique() > 1:
            continue
        # Get Celegans codon at this position
        codon = alignmentsFna_df.iloc[col_idx]['Celegans']
        if pd.isna(codon) or codon not in tRNA_df.index:
            continue
        mod = tRNA_df.loc[codon, 'N34_modification']
        color = n34_colors_map.get(mod, 'white')
        # Draw filled box (no border)
        rect = patches.Rectangle(
            (col_idx, n_rows * cell_height), cell_width, cell_height,
            facecolor=color, edgecolor='none'
        )
        ax.add_patch(rect)

        # Font color based on luminance
        rgb = mcolors.to_rgb(color)
        luminance = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]
        font_color = 'black' if luminance > 0.5 else 'white'

        # Codon label
        ax.text(
            col_idx + 0.5, n_rows * cell_height + cell_height / 2,
            codon, ha='center', va='center',
            fontsize=font_size, color=font_color
        )

    # === Draw alignment matrix ===
    for row_idx, species in enumerate(alignmentsFna_df.columns):
        y = (n_rows - row_idx - 1) * cell_height
        # Species label
        ax.text(-0.2, y + cell_height / 2, species, ha='right', va='center',
                fontsize=font_size, fontweight='bold')
        for col_idx in range(n_cols):
            x = col_idx
            codon = alignmentsFna_df.iloc[col_idx, row_idx]
            amino = alignmentsFaa_df.iloc[col_idx, row_idx]
            # Handle NaN
            is_nan = pd.isna(codon) or pd.isna(amino)
            display_codon = "---" if is_nan else codon
            # Conservation color
            color = None
            if not alignmentsFaa_df.iloc[col_idx].isna().any() and alignmentsFaa_df.iloc[col_idx].nunique() == 1:
                color = 'lightgray'
            if not alignmentsFna_df.iloc[col_idx].isna().any() and alignmentsFna_df.iloc[col_idx].nunique() == 1:
                color = 'black'
            # Draw background box
            if color:
                ax.add_patch(
                    patches.Rectangle((x, y), cell_width, cell_height, facecolor=color, edgecolor='none')
                )

            text_color = 'white' if color == 'black' else 'black'
            ax.text(
                x + 0.5, y + cell_height / 2, display_codon,
                ha='center', va='center',
                fontsize=font_size, color=text_color
            )
    # Save figure
    plt.tight_layout()
    align_dir = os.path.join(output_dir, 'alignments')
    os.makedirs(align_dir, exist_ok=True)
    safe_record_name = record_name.replace('/', '_')
    plt.savefig(os.path.join(align_dir, f"{safe_record_name}_alignment.pdf"), dpi=dpi, bbox_inches='tight')
    plt.close()

def blastc_on_fasta_onepass(fasta_path, species_dict, aligner, output_prefix, fdr_cutoff=None, conservedness_cutoff=None, num_workers=1, dpi=300):
    fasta = list(SeqIO.parse(fasta_path, 'fasta'))
    args_list = [(record, species_dict, aligner) for record in fasta]

    if num_workers > 1:
        with mp.Pool(num_workers) as pool:
            results = list(tqdm(pool.imap(process_record, args_list), total=len(fasta), desc='BLAST-C'))
    else:
        results = [process_record(args) for args in tqdm(args_list, desc='BLAST-C')]
    
    all_matrices = [r['substitution_matrix'] for r in results]
    global_matrix = pd.concat(all_matrices).groupby(level=0).sum()
    global_identity, global_non_identity = count_identity_nonidentity(global_matrix)

    stats_data = []
    for r in results:
        identity = r['identity']
        non_identity = r['non_identity']
        table = [[global_identity - identity, global_non_identity - non_identity], [identity, non_identity]]
        _, p_val = fisher_exact(table)
        ratio = identity / (identity + non_identity) if (identity + non_identity) > 0 else 0
        r.update({'identity_ratio': ratio, 'p_value': p_val})
        stats_data.append(r)

    stats_df = pd.DataFrame([{k: row[k] for k in ['record', 'identity', 'non_identity', 'identity_ratio', 'p_value']} for row in stats_data]).set_index('record')

    if fdr_cutoff is None:
        fdr_cutoff = 0.05 / len(stats_data)
    if conservedness_cutoff is None:
        mean_ratio = stats_df['identity_ratio'].mean()
        std_ratio = stats_df['identity_ratio'].std()
        conservedness_cutoff = mean_ratio + 2 * std_ratio

    print(f"[Info] FDR threshold: {fdr_cutoff:.5f}, conservedness threshold: {conservedness_cutoff:.4f}")

    os.makedirs(os.path.dirname(output_prefix), exist_ok=True)
    global_matrix.to_csv(f"{output_prefix}.tsv", sep='\t')
    stats_df.to_csv(f"{output_prefix}.statistics.tsv", sep='\t')
    print(f"[v] Saved: {output_prefix}.tsv")
    print(f"[v] Saved: {output_prefix}.statistics.tsv")

    for r in stats_data:
        if r['p_value'] < fdr_cutoff and r['identity_ratio'] > conservedness_cutoff:
            plot_alignment(r['record'], r['sequence'], species_dict, aligner, os.path.dirname(output_prefix), dpi)

    return global_matrix, stats_df

# === Main Script ===
def main():
    args = parse_args()
    domain_basename = os.path.splitext(os.path.basename(args.domain))[0]
    output_prefix = os.path.join(args.output, domain_basename)

    aligner = get_aligner()
    cds_paths = args.cds.split(',')
    species_dict = {
        extract_species_name(path): list(SeqIO.parse(path.strip(), 'fasta'))
        for path in cds_paths
    }

    matrix_path = output_prefix + ".tsv"
    blastc_on_fasta_onepass(
        args.domain, species_dict, aligner, output_prefix,
        fdr_cutoff=args.fdr,
        conservedness_cutoff=args.conservedness,
        num_workers=args.threads,
        dpi=args.dpi
    )
    
    visualize_substitution_matrix(matrix_path, normalization='raw', dpi=args.dpi)
    visualize_substitution_matrix(matrix_path, normalization='log2_obsexp', dpi=args.dpi)
    print("[v] Matrix visualizations complete.")

if __name__ == "__main__":
    main()

