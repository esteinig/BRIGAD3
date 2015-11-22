# brigD3

BLAST Ring Image Generator adopted from [Alikhan et al. (2012)](http://www.biomedcentral.com/1471-2164/12/402)

### Dependencies
---
* Python 3.4
* BioPython

####Basics
---
Data for the visualization with Java Script is generated with Python. BrigD3 provides different kinds of ring objects and combines them in a ring generator for the final visualization with D3.

All ring types have the following methods of the super-class Ring:

**ring.setOptions(...)**

Arguments:

* *name*: str, name of genome ['Ring']
* *color*: str, ring color name or hex ['black']
* *height*: int, height of ring [20]
* *tooltip*: tooltip object

Set basic attributes of the ring object, tooltip accepts customized objects of class Tooltip. See below for more details on Tooltips. Keep at default for now (None).

**ring.writeRing(file)**

Write ring data as comma-delimited file (.csv).

**ring.readRing(file)**

Read raw ring data for brigD3. File without header and columns (in order): Start, End, Color, Height, HTML String for Tooltip.

**ring.clear()**

Clear all data in ring.

####Rings
---
Ring objects hold and transform the data for the visualization with D3. BrigD3 currently supports three ring types:

#####AnnotationRing

```
ring = AnnotationRing()

ring.feature = 'CDS'
ring.extract = {'gene': 'Gene:'}
```

The annotation ring has two readers:

**ring.readGenbank(file)**

Parse all given features from a genbank file (.gbk) and extract qualifiers for annotation in brigD3.

**ring.readSNP(file, ...)**

Arguments:

* *length*: int, length of segment showing the SNP [100]

Read a file ('.csv') without header containing the columns (in order): SNP ID, Location on Reference Genome, Notes.
Length specifies the length of the segment showing the SNP. Allows for better visibility in large genome sequences.

#####CoverageRing

```
ring = CoverageRing()

ring.threshold = 0.95
ring.below = 'red'
```

The coverage ring has one reader to parse a bedtools coverage matrix, as derived from SPANDx.

**ring.readCoverage(file, ...)**

Arguments:

* *sep*: str, delimiter ['\t']
* *mean*: bool, calculate mean coverage across all samples [True]
* *n*: int, number of column containing target sample when mean is False (starting with 0) [4]

Read a coverage matrix file with header containing the columns (in order): ID, Start, End, Sample1, Sample2 ...
Matrix contains an entry for each segment with start and end position and one value between 0 and 1 for each Sample (M x N).
The default reader calculates the average coverage across all samples for each segment, but you can also specify the column number *n* to parse coverage for only a single genome. Coverage below the threshold is coloured according to set threshold colour, so you can set normal colour to background (white) showing only below threshold coverage along the reference genome.

#####BlastRing()

```
ring = BlastRing()

ring.min_length = 100
ring.min_identity = 70
```

The BLAST ring has one reader to parse the query output of a genome against the reference DB (-outfmt 6):

**ring.readComparison(file)**

Read an output from a BLAST query against the reference DB. Only segments with *min_length* and *min_identity* are used for the visualization.

####BLAST Ring Image Generator
---

The ring generator combines a list of rings and writes the final visualization as HTML and JSON.

#####RingGenerator

The generator accepts a list of ring objects (from inner to outer) and you can set options for the visualization with D3.

```
rings = [ring1, ring2, ring3, ring4...]

generator = RingGenerator(rings)
```

**generator.setOptions(circle, ...)**

Set options for the visualization:

* *circle*: length of reference genome (for mapping of segments from rings)
* *radius*: int, inner radius of the visualization [300]
* *gap*: int, height of gap between rings [5]
* *project*: str, name of project file ['data']
* *title*: str, title to appear in the center of the visualization ['brigD3']
* *title_size*: str, size of title in px or % ['200%']
* *title_font*: str, font or font family of title ['times']
* *ring_opacity*: float, final opacity of rings [0.8]
* *width, height*: int, dimensions of visualization [1700, 1000]

**generator.getBRIG()**

Write the visualization in working directory as HTML and JSON.

####BLASTer
---

System calls to run BLAST+ (in $PATH).

#####Blast

Initialize a blaster with reference sequence (.fasta) and a list of comparison sequences (.fasta), convenience module for integrating BLAST+ and generating multiple BlastRings (see Tutorial).

```
reference = 'reference.fasta'
genomes = ['genome1.fasta', 'genome2.fasta', ...]

blaster = Blast(reference, genomes)

blaster.type = 'nucl'
blaster.mode = 'blastn'
blaster.name_db = 'ReferenceDB'
```

**blaster.runBLAST()**

Blast query sequences agains reference sequence (DB) with attributes specified for BLAST+. YOu can access the names of the result comparison files (--outfmt 6) by iterating over `blaster.results`.

####Tooltips
---

Initiate a tooltip object to pass to ring attributes (ring.setOptions) for attaching popups to segments in the visualization (still under construction...)

```
tooltip = Tooltip()
tooltip.text_color = 'white'
tooltip.head_colour = '#FBB917'
```

###Tutorial







