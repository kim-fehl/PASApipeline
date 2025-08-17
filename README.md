# PASApipeline
## Introduction

PASA (Program to Assemble Spliced Alignments) is a robust eukaryotic genome annotation tool. It accepts various transcript sources (EST, cDNA, RNA-Seq) assembled either *de novo* or using a genome-guided approach. PASA can generate novel annotations or refine existing ones by clustering high-confidence spliced transcript alignments, and supports alternative splicing and polyadenylation site analyses.

> **Note**: PASA was developed in the early 2000s, and its [original documentation](https://github.com/PASApipeline/PASApipeline/wiki) has accumulated patchy updates over time, sometimes mixing general usage with sample data examples. This fork aims to make the documentation clearer and easier to follow.

## Pipeline Overview

```mermaid
flowchart TB
	A[**Transcript Cleaning:**<br/>remove poly-A tails, vector contamination, and low‑quality reads] --> C[**Mapping to the Genome**: </br>align cleaned transcripts via GMAP, BLAT, and/or Minimap2, cluster high-quality alignments]
	C --> H["**Transcriptome Database:**<br/>build comprehensive transcriptome"]
	C --> D["**Annotation Update:**<br/>improve UTR/exons boundaries of existing gene models"]
	C --> E["**Alternative Splicing:**<br/>detect and classify splice variants"]
	C --> F["**PolyA Sites Identification:**<br/>map polyA sites using untrimmed reads"]
	C --> G["**ORF Prediction:**<br/>extract coding sequences via TransDecoder"]

```

### Input

**Possible transcripts sequencing technologies:**

| Source                     | Time period      | Pros                                                   | Cons                                                                                           |
| -------------------------- | ---------------- | ------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| EST libraries              | Late 1990s–2000s | High-throughput sampling at low cost                   | Fragmentary reads (≈200–800 nt) requiring intensive assembly                                   |
| Full-length cDNA libraries | Early–mid 2000s  | Complete transcript boundaries, accurate UTR mapping   | Low throughput, higher cloning/sequencing cost                                                 |
| RNA-Seq                    | 2010s–present    | Deep coverage, cost-effective, dynamic discovery       | Short fragments result in assembly errors, isoform collapse, missing low-abundance transcripts |
| long-read RNA-seq          | 2015–present     | End-to-end transcript reads, robust isoform resolution | Higher per-base error rates, lower throughput, greater expense                                 |

**Possible transcriptome assembly strategies:**

|                    |                                                                                                                                                                                                  |                                                 |                                                             |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------- | ----------------------------------------------------------- |
| **Strategy**       | **Description**                                                                                                                                                                                  | **Pros**                                        | **Cons**                                                    |
| _de novo_          | Assemblies generated solely from RNA-Seq reads without genome reference guidance (e.g. Trinity, RNA-Bloom)                                                                                       | Captures novel and sample-specific transcripts  | Potential misassemblies, chimeric contigs, isoform collapse |
| genome-guided (GG) | Genome is used to align RNA-seq reads before assembling them into transcripts (e.g., Cufflinks, StringTie), or as a guide to cluster _de novo_ transcripts (e.g., Trinity in genome-guided mode) | Accurate exon–intron boundaries; fewer chimeras | Dependent on reference quality; may miss novel loci         |


**Repository Overview**

The project hosts the “Program to Assemble Spliced Alignments” (PASA) genome annotation pipeline. The README introduces it as a tool that ingests transcript data (ESTs, cDNA, RNA‑Seq) and refines gene models through high‑quality spliced alignments while supporting alternative splicing and poly‑A site analysis.

The `docs/` directory provides a much more thorough manual in AsciiDoc format. The main index explains that PASA leverages spliced alignments to model gene structures and maintain annotations. It highlights improvements brought by PASA2 and lists installation and usage topics.

**Key Components**

- **Pipeline runner** – `Launch_PASA_pipeline.pl` orchestrates the main workflow. It loads Perl libraries, handles configuration, and executes a sequence of scripts to align transcripts, build assemblies, and compare annotations.
- **Perl modules** – under `PerlLib/` are numerous modules handling alignment validation, database interaction, pipeline utilities (e.g., `Pipeliner.pm` for checkpointed execution), FASTA I/O, and more.
- **C++ assembler** – `pasa_cpp/` contains the source for the core “pasa” alignment assembler, built via the top-level `Makefile`.
- **Plugins & third‑party tools** – `pasa-plugins/` bundles utilities such as `seqclean` (transcript cleaning) and `slclust` for sequence clustering.
- **Sample pipeline** – `sample_data/` includes scripts and configurations demonstrating how to run PASA end‑to‑end. The helper script `__run_sample_pipeline.pl` shows typical command‑line options for aligning, building assemblies, comparing annotations, running alternative splicing analysis, and predicting ORFs.
- **Configuration templates** – `pasa_conf/` holds template `.conf` files and alignment/annotation configuration examples.
- **PasaWeb** – a lightweight web interface (located in `PasaWeb/`) that can be started via `run_PasaWeb.pl`. It relies on `lighttpd` and CGI scripts for browsing results.
- **Docker support** – `Docker/` contains a Dockerfile and helpers to build and test a containerized installation.
