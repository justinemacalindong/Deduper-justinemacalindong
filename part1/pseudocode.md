Justine Macalindong - Part 1 - Deduper Pseudocode

**Define the problem:**
```
As part of the library preparation process, PCR amplification is performed which duplicates DNA and RNA samples to increase signal-to-noise ratio for the sequencing process. 

The problem is that these duplicates still remain in the sequencing data and must be removed prior to counting features, differential gene expression, and splicing analysis. 
```

**Develop your algorithm using pseudocode:**
```
Bash:
- Clean up SAM file - remove scaffolding
- Sort SAM file by base position using SAMtools

Python script:
- While true loop:
    - read one line at a time using read.line()
    - split line by tab to get each column
    - save each desired column in a variable
        - chromosome = column 3
        - pos = column 4 
        - strand = column 2
        - umi = column 1
    - check strandedness using bitwise flag function
    - adjust for soft clipping based on cigar string and strand using adjusted position function
        - save adjusted position in a new variable (adj_pos)
    - place in tuple variables like so: (chrom, adj_pos, strand, umi)
    - put each unique tuple in a set
    - go through entire file one line at a time
        - if tuple is not in set, write entire line to SAM file
        - if tuple is in set, go to next line and do not write line to SAM file
```

**Determine high level functions:**
```
*Adjusted Position Function*
Description: Accounts for CIGAR string and adjusts base position accordingly and adds to new column in line

Function header:
position_adjust(pos,cigar,strand):

Test examples (for individual functions):
pos = 35
cigar = "5S15M"
strand = "pos"
return 30

pos = 30
cigar = "20M"
strand = "pos"
return 30

pos = 10
cigar = "20M"
strand = "neg"
return 30

pos = 20
cigar = "10S10M"
strand = "neg"
return 30
```
```
*Bitwise flag function*
Description: Interprets bitwise flag to know strandedness of the sequence.

Function header:
strand_flag(flag):
if ((flag & 16) == 16):
	strand = "neg"
else:
    strand = "pos"

Test examples:
flag = 2
return pos

flag = 16
return neg
```
