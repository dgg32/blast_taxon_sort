import os
import screed

import sys
import pyphy

import configparser
import sys
import json


desired_taxon = ["Chlorobi", "Comamonadaceae"]

config_file = os.path.join(os.path.dirname(os.path.realpath(__file__) ),'target.config')

if os.path.exists(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    #print (config.sections())

    desired_taxon = json.loads(config.get("DEFAULT", "target"))
    
    #print (desired_taxon)

    #desired_taxon = config['DEFAULT']['target']

input_file = sys.argv[1]

fasta_file = sys.argv[2]




taxon_readids = {}

cache_taxid_name = {}


for line in open(input_file, 'r'):
    fields = line.strip().split("\t")

    taxid = fields[-1].split(";")[0]

    if taxid not in cache_taxid_name:

        path = pyphy.getPathByTaxid(taxid)

        found_name = ""
        for item in path:
            name = pyphy.getNameByTaxid(item)

            if name in desired_taxon:

                found_name = name

                if name not in taxon_readids:
                    taxon_readids[name] = set()

                if fields[0] not in taxon_readids[name]:
                    taxon_readids[name].add(fields[0])

        #if found_name != "":
        cache_taxid_name[taxid] = found_name

    else:
        name = cache_taxid_name[taxid]

        if name in desired_taxon:

            if name not in taxon_readids:
                taxon_readids[name] = set()

            if fields[0] not in taxon_readids[name]:
                taxon_readids[name].add(fields[0])


taxon_sequence = {}

with screed.open(fasta_file) as seqfile:
    for read in seqfile:
        #print(read.name, read.sequence)

        fields = read.name.split(" ")

        basename = os.path.basename(fasta_file)

        for taxon in taxon_readids:

            if fields[0] in taxon_readids[taxon]:
                if taxon not in taxon_sequence:
                    taxon_sequence[taxon] = []

                taxon_sequence[taxon].append(">" + basename.replace(" ", "_") + "|" + read.name + "\n" + read.sequence)

for taxon in taxon_sequence:
    output_file = open(fasta_file + "_" + taxon + ".fasta", 'w')

    output_file.write("\n".join(taxon_sequence[taxon]))

    output_file.close()