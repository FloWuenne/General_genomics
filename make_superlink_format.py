#!/usr/bin/python
## Reformat plink ped and map format to format required by Superlink
## Usage python make_superlink.py [ped file] [map file]

## Define functions
def chunk(input, size):
    return map(None, *([iter(input)] * size))


## Import libraries
import csv
import sys

## Get filenames from command line
ped_file = sys.argv[1]
map_file = sys.argv[2]

individuals_sorted = []

## Read in ped file
Individuals = {}
ped_reader = csv.reader(open(ped_file,"rb"),delimiter=" ")
for row in ped_reader:
	fam_id = row[0]
	indiv_id = row[1]
	father = row[2]
	mother = row[3]
	sex = row[4]
	affection = row[5]
	markers = chunk(row[6:len(row)+1],2)
	markers = [list(i) for i in markers]
	Individuals[indiv_id] = markers
	individuals_sorted.append(indiv_id)
	

## Read in map file
map_info = []
map_reader = csv.reader(open(map_file,"rb"),delimiter="\t")
for row in map_reader:
	chrom = row[0]
	ID = row[1]
	pos = row[3]
	map_info.append([ID,chrom,pos])


## Write information to new file for Superlink
Outfile = open(ped_file.split(".")[0]+"_Superlink.snp","wb")

##Format the headerline
header = ["SNP","CHROMOSOME","POSITION"]
for ind in individuals_sorted:
	header.append(ind)
header_line = "\t".join(header)
Outfile.write(header_line+"\n")

for number in range(0,len(markers)):
	marker_info = "\t".join(map_info[number])
	genotypes = []
#	if marker_info.startswith("ex"):
#		pass
	if marker_info.split("\t")[1] == "0":
		pass
	else:
		for indiv in individuals_sorted:
			genotype = "".join(Individuals[indiv][number])
			genotypes.append(genotype)
		genotype_str = "\t".join(genotypes)
		Outfile.write(marker_info+"\t"+genotype_str+"\n")

## Close all opened files
Outfile.close
		


		
