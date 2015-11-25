"""Example using some ring features from the Tutorial"""

# CDS ring DAR4145, default setting CDS
ring_gen = AnnotationRing()
ring_gen.setOptions(color='#565051', name='DAR4145', height=20)
ring_gen.readGenbank('dar4145.gbk')

# Misc Feature ring DAR4145
ring_misc = AnnotationRing()
ring_misc.setOptions(color='#0C090A', name='DAR4145', height=20)
ring_misc.feature = 'misc_feature'
ring_misc.extract = {'note': 'Note: '}
ring_misc.readGenbank('dar4145.gbk')

# Blast Rings, Genbank genomes ST673 and ST772
genomes = ['gr1.fasta','07-17048.fasta', 'kty21.fasta', '333.fasta', '3957.fasta']
colors = ['#FBB917','#0000A0', '#2B60DE', '#1589FF', '#5CB3FF']
names = ['ST672 GR1', 'ST772 07-17048', 'ST772 KTY-21', 'ST772 333', 'ST772 3957']

blaster = Blaster('dar4145.fasta', genomes=genomes)
blaster.runBLAST()

blast_rings = []
for i in range(len(blaster.results)):
    ring_blast = BlastRing()
    ring_blast.setOptions(color=colors[i], name=names[i])
    ring_blast.min_length = 100
    ring_blast.readComparison(blaster.results[i])
    blast_rings.append(ring_blast)

# Combine rings in preferred order
rings = [ring_gen] + blast_rings + [ring_misc]

# Initialize ring generator and set options, write as JSON and HTML
generator = RingGenerator(rings)
generator.setOptions(circle=2860508, project='example', title='DAR4145', title_size='200%', radius=200)
generator.brigD3()
