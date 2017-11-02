#!/usr/bin/python
## Extract results from SUPERLINK html output to replot LOD scores in R

from xml.etree.ElementTree import fromstring
import os
from bs4 import BeautifulSoup

## Specify the directory containing the Results folders
Results_dir="/media/florian/CCE45F70E45F5C30/Florian_Projects/NEW_Genotyping_Analysis_2015/Family1524/NOTCH1_subpedigree_analysis/MultiPointAnalysis_1/Results"
chrom_folders = os.listdir(Results_dir)
html_file_name="formatted_output.html"

## Perform result extraction for each chromosome
chrom_results = {}

for chrom in chrom_folders:
    infile_name=Results_dir+"/"+chrom+"/"+html_file_name
    with open(infile_name,"rb") as infile:
        table_switch = 0
        table_string = ""
        for line in infile:
            if table_switch == 0:
                if line.startswith("<table"):
                    table_switch = 1
                    table_string += "<table class=\"details\" border=\"0\" cellpadding=\"5\" cellspacing=\"2\" width=\"95%\">"
                    table_string += line
            elif table_switch == 1:
                if line.startswith("</table>"):
                    table_string += "</table>"
                    table_switch = 2
                else:
                    table_string += line
        chrom_results[chrom] = table_string
                    
outfile = open("/media/florian/CCE45F70E45F5C30/Florian_Projects/NEW_Genotyping_Analysis_2015/Family1524/NOTCH1_subpedigree_analysis/All_chromosomes_SUPERLINK.tab","wb")
outfile.write("chrom\trow_ID\tvariable\tvalue\n")

for chrom in chrom_results:
    html_string = chrom_results[chrom]
    soup = BeautifulSoup(html_string,"lxml")
    table = soup.find("table", attrs={"class":"details"})
    
    # The first tr contains the field names.
    all_chrom_results = []
    for row in table.find_all("tr")[1:]:
        headings=["ID","name","distance","LOD","NPLSPAIR","NPLALL"]
        dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
        all_chrom_results.append(dataset)
        
    for result_row in all_chrom_results:
        for field in result_row:
            if field[0] == "ID":
                row_id = field[1]
            outfile.write(chrom+"\t"+row_id+"\t{0}\t{1}\n".format(field[0], field[1]))
           #print chrom+"\t{0}\t{1}".format(field[0], field[1])

           
outfile.close()
