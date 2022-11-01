#!/usr/bin/env python

import argparse
import bioinfo
import re

def get_args():
    parser = argparse.ArgumentParser(description="Given a sorted SAM file of uniquely mapped reads, remove all PCR duplicates and retain only a single copy of each read.")
    parser.add_argument("-f", "--file", help="Designates the absolute file path to a sorted sam file to remove PCR duplicates from.", required=True)
    parser.add_argument("-o", "--outfile", help="Designates the absolute file path to create an output sorted sam file to write a single copy of each read to.", required=True)
    parser.add_argument("-u", "--umi", help="Designates the absolute file path to a file that contains a list of desired UMIs.", required=True)
    return parser.parse_args()

args = get_args()

sam = open(args.file,"r")
known_umis =  open(args.umi, "r")
out = open(args.outfile, "w")

known = set()
for line in known_umis: 
    line = line.strip()
    known.add(line) 

dedupe_set = set()

duplicate_count = 0
unknown_umis = 0
unique_reads = 0

while True:
    line = sam.readline().strip()
    if line.startswith("@"):
        out.write(str(line) + '\n')
    elif line.startswith("N"):
        line = line.split("\t")
        umi = line[0].split(":")[7]
        if umi in known: 
            chrom = line[2]
            strand = bioinfo.strand_flag(int(line[1]))
            cigar = line[5]
            pos = bioinfo.position_adjust(int(line[3]),cigar,strand)
            if (umi, chrom, pos, strand) not in dedupe_set:
                dedupe_set.add((umi, chrom, pos, strand))
                out.write('\t'.join(line) + '\n')
                unique_reads += 1
            else:
                duplicate_count += 1
        else:
            unknown_umis += 1
    else:
        break

print("Number of duplicates: " + str(duplicate_count))
print("Number of unknown UMIs: " + str(unknown_umis))
print("Number of unique reads: " + str(unique_reads))

sam.close()
known_umis.close()
out.close()