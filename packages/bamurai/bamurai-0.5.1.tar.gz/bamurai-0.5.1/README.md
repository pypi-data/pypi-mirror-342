# Bamurai

A Python package for splitting reads in BAM/FASTQ files into smaller fragments.

## Description

Bamurai is a command-line tool for splitting reads in BAM/FASTQ files into smaller fragments. It is designed to be fast and efficient, and can be used to split reads into a target length or a target number of pieces per read.

These are the current features of Bamurai:

1. Splitting reads in a file to a target length
2. Splitting reads in a file to a target number of pieces per read
3. Getting statistics from a BAM or FASTQ(.gz) file
4. Basic validation of BAM and FASTQ(.gz) files

The `split` command splits reads into a target length, each read will be split into fragments as close to the target length as possible. Reads shorter than the target length will not be split.

The `divide` command splits reads into a target number of pieces, each read will be split into the number of pieces specified. A further minimum length can be specified to ensure that reads are not split if the resultant fragments are less than the minimum length.

The `stats` command will output the following information by default:
```
Statistics for input.bam:
  Total reads: 8160
  Average read length: 30638
  Throughput: 250006998
  N50: 82547
```

It can be used with the `--tsv` argument to output the statistics in a tab-separated format for computational analysis.
```bash
file_name       total_reads     avg_read_len    throughput      n50
input.bam      8160    30638   250006998       82547
```

The `validate` command will check the integrity of a BAM or FASTQ(.gz) file and output the following information if the file is valid.:
```bash
input.bam is a valid BAM file with 8160 records.
```

## Installation

To install the released version of Bamurai from PyPI

```bash
pip install bamurai
```

To install the latest version of Bamurai from GitHub

```bash
pip install git+https://github.com/Shians/Bamurai.git
```

## Usage

To get help on the command-line interface and list available commands
```bash
bamurai --help
```

To get help on a specific command
```bash
bamurai <command> --help
```

### Splitting reads to target size

To split a file into 10,000 bp reads
```bash
bamurai split input.bam --target-length 10000 --output output.fastq
```

To create a gzipped output file
```bash
bamurai split input.bam --target-length 10000 | gzip > output.fastq.gz
```

### Dividing reads into a target number of pieces

To divide reads into 2 pieces
```bash
bamurai divide input.bam --num_fragments 2 --output output.fastq
```

To divide reads into 2 pieces unless resultant fragments are less than 1000 bp
```bash
bamurai divide input.bam --num_fragments 2 --min_length 1000 --output output.fastq
```

### Getting statistics from a BAM or FASTQ file

To get stats from a BAM file
```bash
bamurai stats input.bam
```

To get stats from a FASTQ file or Gzipped FASTQ file
```bash
bamurai stats input.fastq
bamurai stats input.fastq.gz
```

### Validating BAM or FASTQ files

To validate a BAM file
```bash
bamurai validate input.bam
```
