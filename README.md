#brigD3

![](https://github.com/esteinig/brigD3/blob/master/examples/cover.png)

Interactive visualization of prokaryotic sequence annotations, comparisons and statistics with D3.

The cover image is static, please see the link for the interactive cover visualization of [Indian MRSA Sequence Types against the reference genome DAR4145 with Coverage- , SNP- and BLAST-Rings](https://rawgit.com/esteinig/brigD3/master/examples/cover.html).

BLAST Ring Image Generator adopted from [Alikhan et al. (2012)](http://www.biomedcentral.com/1471-2164/12/402).

###Dependencies
---
* Python 3.4
* BioPython

###Tutorial
---

#####1. Setup Data

For demonstration, we will construct a simple genome comparison of two Indian sequence types (STs) of methicillin-resistant Staphylococcus aureus (MRSA): ST672 and ST772, including the reference genome DAR4145 of ST772. The rings will be constructed from different kinds of data and you can set basic option for all ring types via the options method and specific options for the ring type via its attributes. The annotation and sequence files of the reference genome (.gbk, .fasta) and sequence files for genomes of ST672 and ST772 (.fasta) must be in your working directory:

* [Reference DAR4145](http://www.ncbi.nlm.nih.gov/nuccore/CP010526.1)
* [GR1](http://www.ncbi.nlm.nih.gov/nuccore/NZ_AJLX00000000)
* [07-17048](http://www.ncbi.nlm.nih.gov/nuccore/AZBT00000000)
* [KTY-21](http://www.ncbi.nlm.nih.gov/nuccore/AOCQ00000000)
* [333](http://www.ncbi.nlm.nih.gov/nuccore/ALWF00000000)
* [3957](http://www.ncbi.nlm.nih.gov/nuccore/NZ_AOFU00000000)

The coverage matrix along a 1kb sliding window comes from a large alignment of genomes of ST772 against DAR4145 using [bedtools](http://bedtools.readthedocs.org/) in [SPANDx](https://github.com/dsarov/SPANDx).

#####2. Rings

Let's make some rings! The first one is an annotation of the reference genome as base of the visualization. We will make one ring extracting gene names and products from CDS features, and a second ring getting miscellaneous feature annotations (in this case mobile genetic elements like integrated viruses, plasmids or gene cassettes). The extraction dictionary we pass to the extract attribute contains the qualifiers to extract (keys) and the headers for the popups (values) in the final visualization.

```
# Generate annotation rings for CDS and MGEs

from brigD3 import *

# Initialize annotation ring and set basic attributes
cds_ring = AnnotationRing()
cds_ring.setOptions(name='DAR4145', color='black')
misc_ring = AnnotationRing()
misc_ring.setOptions(name='DAR4145', color='#0C090A')

# Set feature and qualifiers to be extracted
cds_ring.feature = 'CDS'
cds_ring.extract = {'gene': 'Gene:', 'product' : 'Product:'}
misc_ring.feature = 'misc_feature'
misc_ring.extract = {'note': 'MGE:'}

# Parse annotation files
cds_ring.readGenbank(file='dar4145.gbk')
misc_ring.readGenbank(file='dar4145.gbk')
```

Let's make another type of ring that will show the coverage of an alignment of genomes against DAR4145 from SPANDx. The matrix has three initial columns (Segment ID, Start, End) and coverage for each 1kb window in the range of 0 - 1 for each of the aligned genomes (... G1, G2, G3 ...). We will show the mean coverage for each window across the aligned genomes, which can help to distinguish regions with low coverage and relate them to the annotation and sequence comparisons.

One trick we can use to show only the relevant regions is to set color of the ring to the background (white) and set a threshold value and color. Here, we will color only the segments with average coverage < 95%.

```
# Generate average coverage ring from alignment of ST772

# Initialize coverage ring and set basic options
cov_ring = CoverageRing()
cov_ring.setOptions(name='ST772 Alignment', color='white')

# Set up threshold and threshold color
cov_ring.threshold = 0.95
cov_ring.below = 'red'

# Read average coverage per segment from SPANDx
cov_ring.readCoverage(file='bedcov.txt', mean=True)
```

The final rings we make are the BLASTn comparisons of five genomes (1x ST672, 4x ST772) against the reference DB of DAR4145. By default, we will include only segments > 100 base pairs and with BLAST identity > 70%. We must first setup some basic parameters (files, names, colors), then initiate the Blaster and finally use the returned filenames of the comparisons to iterate over theoir indices and generate the Blast Rings:

```
# Setup files, names and colors for BLAST 
reference = 'dar4145.fasta'
genomes = ['gr1.fasta', '07-17048.fasta', 'kty21.fasta', '333.fasta', '3957.fasta']
names = ['ST672 GR1', 'ST772 07-17048', 'ST772 KTY-21', 'ST772 333', 'ST772 3957']
colors = ['#FBB917','#0000A0', '#2B60DE', '#1589FF', '#5CB3FF']

# Initialize Blaster, set to nucleotide DB and run BLASTn
blaster = Blaster(reference, genomes)
blaster.name_db = 'ST772-DAR4145'
blaster.type = 'nucl'
blaster.mode = 'blastn'
blaster.runBLAST()

# Create list for Blast Rings, iterate over result files in Blaster
blast_rings = []
for i in range(len(blaster.results)):
    blast_ring = BlastRing()
    blast_ring.setOptions(color=colors[i], name=names[i])
    blast_ring.min_length = 100
    blast_ring.min_identity = 70
    blast_ring.readComparison(file=blaster.results[i])
    blast_rings.append(blast_ring)
```

##### BRIG D3

We now have all our components, but we still need to put them together in the right order and pass options to the script that will generate the visualization with D3. We left out SNP annotations for demonstration, but you can read more about them below (Annotation Rings).

Let's first initialize the Ring Generator, pass an ordered list of our rings and set general options for the script. The required option to set is the length of the reference genome in the parameter **circle**, but we will also set the title and opacity of the rings (for more options see *Basics*):

```
# Combine rings in desired order and initialize Ring Generator
rings = [cds_ring] + blast_rings + [misc_ring, cov_ring]
generator = RingGenerator(rings)

# Set basic options
generator.setOptions(circle=2860508, title='Indian MRSA', ring_opacity=0.7, project='ST772')

# Write visualization to working directory
generator.brigD3()
```

You will find the final data file (.json) and the visualization (.html) in your working directory, you can open the HTML file in your favourite browser, like Firefox or Chrome. For security reasons, Chrome has trouble loading files from disk. I will update this section with a couple of ways around it, but it generally works smoothly in Firefox.

###Basics
---

Data for the visualization with Java Script is generated with Python. BrigD3 provides different kinds of ring objects and combines them in a ring generator for the final visualization with D3.

All ring types have the following methods of the super-class Ring:

*ring.setOptions(...)*

Arguments:

* *name*: str, name of genome ['Ring']
* *color*: str, ring color name or hex ['black']
* *height*: int, height of ring [20]
* *tooltip*: tooltip object

Set basic attributes of the ring object, tooltip accepts customized objects of class Tooltip. See below for more details on Tooltips. Keep at default for now (None).

*ring.writeRing(file)*

Write ring data as comma-delimited file (.csv).

*ring.readRing(file)*

Read raw ring data for brigD3. File without header and columns (in order): Start, End, Color, Height, HTML String for Tooltip.

*ring.mergeRings(rings)*

Merge a list of ring objects with the current ring object. Ring merging can be powerful because you can combine ring types, e.g. overlaying SNP annotations on the Blast Rings.

####Rings

Subclasses of ring objects hold and transform the data for the visualization with D3.

#####AnnotationRing

```
ring = AnnotationRing()

ring.feature = 'CDS'
ring.extract = {'gene': 'Gene:'}
ring.snp_length = 100
ring.intergenic = 'yellow'
ring.synonymous = 'black'
ring.non_synonymous = 'red'
```

The annotation ring has two readers:

*ring.readGenbank(file)*

Parse all given features from a genbank file (.gbk) and extract qualifiers for annotation in brigD3.

*ring.readSNP(file, ...)*

* *single*: bool, read a single isolate only [False]
* *n*: int, column number for single isolate [5]
 
Read a file ('.csv') without header containing the columns (in order): SNP ID, Type, Location on Reference Genome, Notes. The fifth column contains the nucleotides for the reference genome, each following column the nucleotide at this location for each of the aligned genomes. Notes should be single string, location an integer, type one of *synonymous*, *non-synonymous* or *intergenic* (all others get base color) and the SNP ID. 

If single is True, the reader parses only the isolate in the *n*-th column, which should be > 4 (as reference nucleotides are stored in 4, counting pythonically from 0). The SNPs will only be parsed if they are different to the reference nucleotide.

Length specifies the length of the segment showing the SNP. The SNP is in center position of the segment, allows for better visibility in large genome sequences.

#####CoverageRing

```
ring = CoverageRing()

ring.threshold = 0.95
ring.below = 'red'
```

The coverage ring has one reader to parse a bedtools coverage matrix, as derived from SPANDx.

*ring.readCoverage(file, ...)*

Arguments:

* *sep*: str, delimiter ['\t']
* *mean*: bool, calculate mean coverage across all samples [True]
* *n*: int, number of column containing target sample when mean is False [4]

Read a coverage matrix file with header containing the columns (in order): ID, Start, End, Sample1, Sample2 ...

Matrix contains an entry for each segment with start and end position and one value between 0 and 1 for each Sample (M x N).
The default reader calculates the average coverage across all samples for each segment, but you can also specify the column number *n* (starting from 0) to parse coverage for only a single genome. 

Coverage below the threshold is coloured according to set threshold colour, so you can set normal colour to background (white) showing only below threshold coverage along the reference genome.

#####BlastRing

```
ring = BlastRing()

ring.min_length = 100
ring.min_identity = 70
```

The BLAST ring has one reader to parse the query output of a genome against the reference DB (-outfmt 6):

*ring.readComparison(file)*

Read an output from a BLAST query against the reference DB. Only segments with *min_length* and *min_identity* are used for the visualization.

####BLAST Ring Image Generator

The ring generator combines a list of rings and writes the final visualization as HTML and JSON.

#####RingGenerator

The generator accepts a list of ring objects (from inner to outer) and you can set options for the visualization with D3.

```
rings = [ring1, ring2, ring3, ring4...]

generator = RingGenerator(rings)
```

*generator.setOptions(circle, ...)*

Set options for the visualization:

* *circle*: length of reference genome (for mapping of segments from rings)
* *radius*: int, inner radius of the visualization [300]
* *gap*: int, height of gap between rings [5]
* *project*: str, name of project file ['data']
* *title*: str, title to appear in the center of the visualization ['brigD3']
* *title_size*: str, size of title in px or % ['200%']
* *title_font*: str, font or font family of title ['times']
* *ring_opacity*: float, final opacity of rings [0.8]
* *width, height*: int, dimensions of visualization in px [1700, 1000]

*generator.brigD3()*

Write the visualization in working directory as HTML and JSON.

####Blaster

System calls to run BLAST+ in $PATH.

#####Blast

Initialize a blaster with reference sequence (.fasta) and a list of comparison sequences (.fasta), convenience module for integrating BLAST+ and generating multiple Blast Rings (see Tutorial).

```
reference = 'reference.fasta'
genomes = ['genome1.fasta', 'genome2.fasta', ...]

blaster = Blast(reference, genomes)

blaster.type = 'nucl'
blaster.mode = 'blastn'
blaster.name_db = 'ReferenceDB'
```

*blaster.runBLAST()*

Blast query sequences agains reference sequence (DB) with attributes specified for BLAST+. You can access the names of the result comparison files (--outfmt 6) by iterating over `blaster.results`.

####Tooltips

Initiate a tooltip object to pass to ring attributes (ring.setOptions) for attaching popups to segments in the visualization (still under construction...)

```
tooltip = Tooltip()
tooltip.text_color = 'white'
tooltip.head_colour = '#FBB917'
```

###References
---

Please consider giving some love to these excellent projects and publications:

* BLAST Ring Image Generator by [Alikhan et al. (2012)](http://www.biomedcentral.com/1471-2164/12/402)
* Mike Bostock's magnificent [D3](https://github.com/mbostock)
* SPANDx by our colleagues at [Menzies School of Health Research](http://www.menzies.edu.au/) [Sarovich et al. (2014)](http://www.biomedcentral.com/1756-0500/7/618)
* ST672 and ST772 from India by [Prabhakara et al. (2012)](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3393495/), [Monecke et al. (2013)](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3878137/),  [Balakuntla et al. (2014)](http://www.ncbi.nlm.nih.gov/pubmed/24722327), [Suhaili et al. (2014)](http://www.ncbi.nlm.nih.gov/pubmed/24723714) and our [reference genome for ST772](http://www.biomedcentral.com/1471-2164/16/388)
* [BioPython](http://biopython.org/wiki/Main_Page)

###Contact
---

eike.steinig@menzies.edu.au

eikejoachim.steinig@my.jcu.edu.au






