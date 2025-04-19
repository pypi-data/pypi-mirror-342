#!/usr/bin/env python3

import os
import re
import math
import argparse
import itertools
import numpy as np
import pandas as pd
from tqdm.auto import tqdm
import multiprocessing as mp
from Bio import SeqIO
from Bio import Align
from Bio.Align import substitution_matrices
from scipy.stats import fisher_exact
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib as mpl
import matplotlib.colors as mcolors

# === Argument Parser ===
def parse_args():
    parser = argparse.ArgumentParser(description="Codon conservation analysis from Pfam domains and CDS sequences.")
    parser.add_argument('--domain', '-d', required=True, help='FASTA file of domain sequences (e.g., Pfam)')
    parser.add_argument('--cds', '-c', required=True, help='Comma-separated list of CDS fasta files for each organism')
    parser.add_argument('--output', '-o', required=True, help='Output directory to store results')
    parser.add_argument('--threads', '-t', type=int, default=1, help='Number of parallel threads (default: 1)')
    parser.add_argument('--fdr', '-q', type=float, default=None, help='FDR cutoff (default: 0.05 / num_records)')
    parser.add_argument('--conservedness', '-s', type=float, default=None, help='Identity ratio threshold (default: mean + 2*std)')
    parser.add_argument('--dpi', '-r', type=int, default=300, help='DPI for all generated PDF files (default: 300)')
    return parser.parse_args()

# === Helper Functions ===
def extract_species_name(filepath):
    filename = os.path.basename(filepath)
    if filename.endswith('.fasta') or filename.endswith('.fa'):
        return filename.split('.')[0]
    return filename

def get_aligner():
    aligner = Align.PairwiseAligner(mode='local')
    aligner.substitution_matrix = substitution_matrices.load("BLOSUM62")
    aligner.open_gap_score = -11
    aligner.extend_gap_score = -1
    return aligner

def count_identity_nonidentity(matrix):
    identity, non_identity = 0, 0
    for codon_sub, row in matrix.iterrows():
        c1, c2 = codon_sub.split('>')
        count = row['count']
        if c1 == c2:
            identity += count
        else:
            non_identity += count
    return identity, non_identity

# === Add plot function for significant hits ===
def plot_alignment_pdf(record_name, sequence, species_dict, aligner, output_dir, dpi):
    alignments, best_orfs = [], []
    for org, orfs in species_dict.items():
        best_score = 0
        best_orf = orfs[0]
        for orf in orfs:
            score = aligner.score(sequence, orf.seq.translate())
            if score > best_score:
                best_score = score
                best_orf = orf
        best_orfs.append(best_orf)
        alignment = aligner.align(sequence, best_orf.seq.translate())[0]
        alignments.append(alignment)

    species_list = list(species_dict.keys())
    L = len(sequence)
    fna_df = pd.DataFrame(columns=species_list, index=range(L))
    faa_df = pd.DataFrame(columns=species_list, index=range(L))

    for i, alignment in enumerate(alignments):
        t_coords, q_coords = alignment.aligned
        for (t_start, t_end), (q_start, q_end) in zip(t_coords, q_coords):
            for t_pos, q_pos in zip(range(t_start, t_end), range(q_start, q_end)):
                orf = best_orfs[i]
                codon = orf.seq[3*q_pos:3*q_pos+3]
                aa = codon.translate()
                fna_df.at[t_pos, species_list[i]] = codon
                faa_df.at[t_pos, species_list[i]] = aa

    fig, ax = plt.subplots(figsize=(max(10, L * 0.3), max(5, len(species_list) * 0.3)))
    ax.axis('off')
    for i, species in enumerate(species_list):
        for j in range(L):
            codon = fna_df.iloc[j, i] if pd.notna(fna_df.iloc[j, i]) else '---'
            aa = faa_df.iloc[j, i] if pd.notna(faa_df.iloc[j, i]) else 'X'
            color = 'white'
            if faa_df.iloc[j].notna().all() and faa_df.iloc[j].nunique() == 1:
                color = 'lightgray'
            if fna_df.iloc[j].notna().all() and fna_df.iloc[j].nunique() == 1:
                color = 'black'
            rect = patches.Rectangle((j, len(species_list)-i-1), 1, 1, facecolor=color)
            ax.add_patch(rect)
            ax.text(j + 0.5, len(species_list)-i-0.5, codon, ha='center', va='center', fontsize=6, color='white' if color == 'black' else 'black')
    ax.set_xlim(0, L)
    ax.set_ylim(0, len(species_list))
    plt.tight_layout()

    align_dir = os.path.join(output_dir, 'alignments')
    os.makedirs(align_dir, exist_ok=True)
    plt.savefig(os.path.join(align_dir, f"{record_name}_alignment.pdf"), dpi=dpi)
    plt.close()

# === Statistical Analysis Function ===
def blastc_on_fasta_record(record, species_dict, aligner):
    sequence = record.seq
    bases = ['A', 'C', 'G', 'T']
    codons = [a + b + c for a in bases for b in bases for c in bases]
    substitutions = [f"{c1}>{c2}" for c1 in codons for c2 in codons]
    matrix = pd.DataFrame(0, index=substitutions, columns=["count"])

    alignments, best_orfs = [], []
    for org, orfs in species_dict.items():
        best_score = 0
        best_orf = orfs[0]
        for orf in orfs:
            score = aligner.score(sequence, orf.seq.translate())
            if score > best_score:
                best_score = score
                best_orf = orf
        best_orfs.append(best_orf)
        alignment = aligner.align(sequence, best_orf.seq.translate())[0]
        alignments.append(alignment)

    species_list = list(species_dict.keys())
    L = len(sequence)
    fna_df = pd.DataFrame(columns=species_list, index=range(L))
    faa_df = pd.DataFrame(columns=species_list, index=range(L))

    for i, alignment in enumerate(alignments):
        t_coords, q_coords = alignment.aligned
        for (t_start, t_end), (q_start, q_end) in zip(t_coords, q_coords):
            for t_pos, q_pos in zip(range(t_start, t_end), range(q_start, q_end)):
                orf = best_orfs[i]
                codon = orf.seq[3*q_pos:3*q_pos+3]
                aa = codon.translate()
                fna_df.at[t_pos, species_list[i]] = codon
                faa_df.at[t_pos, species_list[i]] = aa

    for i in range(L):
        if faa_df.iloc[i].notna().all() and faa_df.iloc[i].nunique() == 1:
            codons_here = fna_df.iloc[i]
            for a, b in itertools.permutations(codons_here, 2):
                idx = f"{a}>{b}"
                if idx in matrix.index:
                    matrix.loc[idx, "count"] += 1
    return matrix

def blastc_fasta_onepass(fasta_path, species_dict, aligner, output_prefix, fdr_cutoff=None, conservedness_cutoff=None, num_workers=1, dpi=300):
    fasta = list(SeqIO.parse(fasta_path, 'fasta'))

    def process_record(record):
        matrix = blastc_on_fasta_record(record, species_dict, aligner)
        identity, non_identity = count_identity_nonidentity(matrix)
        return {
            'record': record.name,
            'sequence': str(record.seq),
            'substitution_matrix': matrix,
            'identity': identity,
            'non_identity': non_identity
        }

    if num_workers > 1:
        with mp.Pool(num_workers) as pool:
            results = list(tqdm(pool.imap(process_record, fasta), total=len(fasta), desc='BLAST-C + stats'))
    else:
        results = [process_record(record) for record in tqdm(fasta, desc='BLAST-C + stats')]

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
            plot_alignment_pdf(r['record'], r['sequence'], species_dict, aligner, os.path.dirname(output_prefix), dpi)

    return global_matrix, stats_df

# === Visualization of Substitution Matrix ===
def visualize_substitution_matrix(path, normalization='log2_obsexp', dpi=300):
    assert normalization in ['raw', 'log2_obsexp']
    outputDir = os.path.dirname(path)
    filename_wo_ext = os.path.splitext(os.path.basename(path))[0]
    pdfPath = os.path.join(outputDir, f"{filename_wo_ext}.{normalization}.pdf")

    tRNA_df = pd.read_csv(
        '../lib/N34_modifications.tsv',
        sep='\t', names=['amino_acid', 'codon', 'N34_modification'], index_col=1
    )
    substitution_df = pd.read_csv(path, sep='\t', index_col=0)

    codons = tRNA_df.index.tolist()
    matrix = pd.DataFrame(0, index=codons, columns=codons)
    for idx, row in substitution_df.iterrows():
        src, dst = idx.split('>')
        if src in codons and dst in codons:
            matrix.at[src, dst] = row['count']

    if normalization == 'raw':
        normalized_matrix = matrix.values.astype(float)
        cmap = plt.cm.get_cmap('Greys')
        vmin, vmax = 0, np.max(normalized_matrix)
        label = 'Raw substitution counts'

    elif normalization == 'log2_obsexp':
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
        label = 'log2 observed/expected'

    fig, ax = plt.subplots(figsize=(12, 10))
    im = ax.imshow(normalized_matrix, cmap=cmap, aspect='equal', vmin=vmin, vmax=vmax)
    ax.set_xticks([])
    ax.set_yticks([])
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label(label)
    plt.title(f"Substitution Matrix: {normalization}")
    plt.savefig(pdfPath, bbox_inches='tight', dpi=dpi)
    plt.close()

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
    blastc_fasta_onepass(
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

