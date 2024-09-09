#
# Prepare sequence and exon intron data for specific celltypes from splicepy exon PSI values
# 
#


from intervaltree import IntervalTree
import os, sys, gzip
import pyfastx
import numpy as np

# correct assembly, here mm39
fapath = '/mnt/storage4/splicing_brain/genomes/mm39/mm39.fa'
fx = pyfastx.Fastx(fapath)
fa = pyfastx.Fasta(fapath, uppercase=True)

# parameters
seqlen = 5_000
overlap = 2_500
N_tolerance = 0
celltype = sys.argv[2]

# get lenhth of each chromosome, store in sequences dict
sequences = {}
for rec in fx:
    name, seq = rec
    if name.count("_") > 0:
        continue
    sequences[name] = len(seq)
print('read %i chromosomes' % len(list(sequences.keys())))
if 1:
    for k,v in sequences.items():
        print(k,'\t',v)
    
# read output to memory
psi = {}
counter = 0
with gzip.open(sys.argv[1], 'rt') as inf:
    for line in inf:
        if line.startswith("chromosome"):
            continue # header
        chrom, start, end, exonp, intronp, exonm, intronm = line.strip().split("\t")
        exon = float(exonp) + float(exonm)
        intron = float(intronp) + float(intronm)
        if not chrom in psi:
            psi[chrom] = IntervalTree()
        # print(chrom, start, end, exon, intron)
        psi[chrom][int(start):int(end)+1] = [exon, intron]
        counter += 1
print('read %i features from file.' % counter)

def onehot_encode(seq):
    mapping = {'A': np.array([1,0,0,0]),
               'C': np.array([0,1,0,0]),
               'G': np.array([0,0,1,0]),
               'T': np.array([0,0,0,1])}

    onehot_matrix = np.array([mapping[nuc] for nuc in seq])
    return onehot_matrix

def prepare_output(chrom, start, end):
    length = end-start+1
    y = np.zeros( (3, length) )
    y[2,:] = 1.0 # set all intergenic as deafault

    #print(sum(np.flatten(y)))
    #print(sum(y[0,:]), sum(y[1,:]), sum(y[2,:]))
    
    if not chrom in psi:
        sys.stderr.write("Chrom (%s) missing PSI values. abortning." % chrom)
        sys.exit(0)
    features = psi[chrom].overlap(int(start), int(end))

    for feature in features:
        begin = feature.begin
        iend = feature.end
        data= feature.data
        if begin > start:
            relative_start = begin-start
        else:
            relative_start = 0
        if iend > end:
            relative_end = length
        else:
            relative_end = iend - start

        #print(start, end, begin, iend)
        #print('adding', data[0], data[1], 'to', relative_start, relative_end)
        y[0,relative_start:relative_end] = data[0]
        y[1,relative_start:relative_end] = data[1]
        y[2,relative_start:relative_end] = 1 - data[0] - data[1]
    return y
    
def process_chunk(chrom, start, end):
    sequence = fa.fetch(chrom, (start, end))
    if sequence.count("N") > 0:
        return False, False
    onehotseq = onehot_encode(sequence)
    y = prepare_output(chrom, start, end)
    ydiff = sum(y[2,:])
    #if ydiff < 5000:
    #    print('processing: %s %i-%i had features %.4f' % (chrom, start, end, ydiff))
    return onehotseq, y
    
if __name__ == '__main__':

    chroms = ['chr21','chr1']
    X = []
    y = []
    
    for chrom in chroms:
        if not chrom in sequences:
            continue
        maxN = sequences[chrom]
        for _i in range(1,maxN-seqlen,overlap):
            newX, newy = process_chunk(chrom, _i, _i+seqlen-1)
            if not type(newX) is bool:
                X.append(newX)
                y.append(newy)

            #if len(X) > 1000:
            #    break

        # export training data
        np.save('%s-%s-onehot-%i-%i.npy'% (celltype,chrom, seqlen, overlap), X)
        np.save('%s-%s-y-%i-%i.npy' % (celltype,chrom, seqlen, overlap), y)
            