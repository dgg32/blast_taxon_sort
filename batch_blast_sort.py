
import os, sys, re, json

top_folder = sys.argv[1]

extension = ".fasta"

for (head, dirs, files) in os.walk(top_folder):
    for file in files:
        if file.endswith(extension):
            current_file_path = os.path.abspath(os.path.dirname(os.path.join(head, file)))
            with_name = current_file_path + "/"+ file
            #print with_name
            blast_out_file = with_name + "_blast_out.txt"

            command = "python blast_sort_bins.py " + blast_out_file + " " + with_name

            print (command)
            #print ("processing " + file + " ...")
            os.system(command)