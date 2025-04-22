# REDItools3
A new REDItools implementation to speed-up the RNA editing profiling in massive RNAseq data

# Installation
Install from PyPi.
`pip install REDItools3`

Use the whl file under the dist directory.
`pip install dist/reditools-0.1-py3-none-any.whl`

# Usage
Once installed, reditools can be run from the commandline.
`python -m reditools`

## Tools

### analyze
This is the core reditools function: detecting editing events from one or more BAM file.

The output is a tab separated table with these columns:
| Field | Description |
| --- | --- |
| Region        | Chromosome or contig |
| Position      | Position in the region |
| Reference     | Base from the reference sequence |
| Strand        | DNA strand (+, -, or \*) |
| Coverage-q30  | How many reads had a quality of at least 30 |
| MeanQ         | Mean read quality |
| BaseCount[A,C,G,T] | Total count of each base found |
| AllSubs       | All the detected substitutions |
| Frequency     | Ratio of non-reference bases to reference bases |
| gCoverage-q30 | Genomic Coverage-q30 (see `annotate`) |
| gMeanQ        | Genomic MeanQ (see `annotate`) |
| gBaseCount[A,C,G,T] | Genomic BaseCount (see `annotate`) |
| gAllSubs      | Genomic variants (see `annotate`) |
| gFrequency    | Genomic variant frequency (see `annotate`) |

The last 5 columns will always be blank (`-`). They are reserved for output
from the `annotate` tool.

### annotate
Annotate RNA editing output with variant detection from genomic data.

`annotate` takes two reditools output files and fills in the last five columns
of the first file with positional matches from the second.

For example, this RNA file:
```
Region	Position	Reference	Strand	Coverage-q30	MeanQ	BaseCount[A,C,G,T]	AllSubs	Frequency	gCoverage-q30	gMeanQ	gBaseCount[A,C,G,T]	gAllSubs	gFrequency
chr1	1115715	C	*	2	38.00	[0, 2, 0, 0]	-	0.00	-	-	-	-	-
chr1	1115716	A	*	2	38.00	[2, 0, 0, 0]	-	0.00	-	-	-	-	-
```

With this DNA file:
```
Region	Position	Reference	Strand	Coverage-q30	MeanQ	BaseCount[A,C,G,T]	AllSubs	Frequency	gCoverage-q30	gMeanQ	gBaseCount[A,C,G,T]	gAllSubs	gFrequency
chr1	1115716	A	*	2	38.00	[2, 0, 0, 0]	-	0.00	-	-	-	-	-
chr1	1115717	C	*	2	38.00	[0, 2, 0, 0]	-	0.00	-	-	-	-	-
```

Produces:
```
Region	Position	Reference	Strand	Coverage-q30	MeanQ	BaseCount[A,C,G,T]	AllSubs	Frequency	gCoverage-q30	gMeanQ	gBaseCount[A,C,G,T]	gAllSubs	gFrequency
chr1	1115715	C	*	2	38.00	[0, 2, 0, 0]	-	0.00	-	-	-	-	-
chr1    1115716 A       *       2       38.00   [2, 0, 0, 0]    -       0.00    2       38.00   [2, 0, 0, 0]    -       0.00
```

### find-repeats
Identify repetitive elements in a FASTQ file.

### index
Compute RNA editing index from reditools `analyze` output
([PMDI: 31636457](https://pubmed.ncbi.nlm.nih.gov/31636457/)).
The `index` tool computes the editing indices for all possible variants, not
just A-to-I (listed as A-G in the output).
