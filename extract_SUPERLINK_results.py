#!/usr/bin/python
## Superlink can be found under the following link and can be used to perform linkage analysis:
## http://cbl-hap.cs.technion.ac.il/superlink-snp/
## This script will perform the following analysis on the SUPERLINK output
## Extract results from SUPERLINK html output into a easily parsable tsv file to replot LOD score distribution in R

from xml.etree.ElementTree import fromstring
import os
from bs4 import BeautifulSoup

## Specify the directory containing the Results folders
Results_dir="./Results"
chrom_folders = os.listdir(Results_dir)
html_file_name="res_output.html"

## Perform result extraction for each chromosome
chrom_results = {}

for chrom in chrom_folders:
    infile_name=Results_dir+"/"+chrom+"/"+html_file_name
    with open(infile_name,"rb") as infile:
        soup = BeautifulSoup(infile,"lxml")
        html_table = soup.find_all('table')
        chrom_results[chrom] = html_table[0]
                    
outfile = open("./All_chromosomes_SUPERLINK.tab","wb")
outfile.write("chrom\trow_ID\tMarker_name\tDistance\tLOD\n")

for chrom in chrom_results:
    all_chrom_results = []
    counter = 0
    table = chrom_results[chrom]
    # The first td contains the field names.
    headings=["Group id","Marker id","Marker name","Distance","LN","LOD","Complexity"]
    headings2=["Marker id","Marker name","Distance","LN","LOD","Complexity"]
    for row in table.find_all("tr")[2:]:
        if counter % 3 == 0 or counter == 0:
            dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
            all_chrom_results.append(dataset)
        else:
            dataset2 = zip(headings2, (td.get_text() for td in row.find_all("td")))
            all_chrom_results.append(dataset2)
        counter += 1
    
    counter = 0
    chromosome = "Chr"+chrom.split("_")[1]
    for result_row in all_chrom_results:
        if counter % 3 == 0 or counter == 0:
            outfile.write(chromosome+"\t{0}\t{1}\t{2}\t{3}\n".format(result_row[1][1],result_row[2][1],result_row[3][1],result_row[5][1]))
        else:
            outfile.write(chromosome+"\t{0}\t{1}\t{2}\t{3}\n".format(result_row[0][1],result_row[1][1],result_row[2][1],result_row[4][1]))  
        counter += 1
outfile.close()
