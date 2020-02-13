import regex as re
from utils import *
import statistics
import os
import csv
import pandas as pd

# genera list
genera_file = "/groups/itay_mayrose/annarice/model_adequacy/genera/genera"
# wd
wd = "/groups/itay_mayrose/michaldrori/MSA_JmodelTree/output_MD/"

dp_lst = []
pp_lst = []
counter = 0
genera_lst = []

def get_threshold(filename):
	with open(filename, "r") as threshold_file:
		for line in threshold_file:
			tmp = re.search("#.*:\s(\d+\.?\d*)", line)
			if tmp:
				threshold = tmp.group(1)
				threshold = float(threshold)
				return(threshold)

def get_tar_threshold(handler):
	f = tar.extractfile(handler)
	content = f.read()
	lines = content.splitlines()
	last_line = lines[-1].decode('utf-8')
	tmp = re.search("#.*:\s(\d+\.?\d*)", last_line)
	if tmp:
		threshold = tmp.group(1)
		threshold = float(threshold)
		return (threshold)

def get_threshold_from_file(genus,filename):
	#with open (filename,"r") as thresholds:


with open (genera_file,"r") as genera:
	for genus in genera:
		genus = genus.strip()
		print(genus)
		dp_file = wd + genus + "/" + genus + "_Chromevol_prune/chromevol_out/thresholds_DP"
		pp_file = wd + genus + "/" + genus + "_Chromevol_prune/chromevol_out/thresholds_PP"
		try:
			dp = get_threshold(dp_file)
			dp_lst.append(dp)
			pp = get_threshold(pp_file)
			pp_lst.append(pp)
			counter += 1
			genera_lst.append(genus)
		except:
			try:
				new_path = wd + genus + ".tar.gz"
				dest = "/groups/itay_mayrose/annarice/model_adequacy/for_unzip/" + genus + ".tar.gz"
				os.system("cp -rf " + new_path + " " + dest)
				tar = tarfile.open(dest)
				for member in tar.getmembers():
					if member.name == dp_file[1:]:
						dp = get_tar_threshold(member)
						dp_lst.append(dp)
					if member.name == pp_file[1:]:
						pp = get_tar_threshold(member)
						pp_lst.append(pp)
						counter += 1
						genera_lst.append(genus)
			except:
				pass

output_file = "/groups/itay_mayrose/annarice/model_adequacy/genera/thresholds_test.csv"
with open (output_file, "w+") as results:
	header = ["Genus", "DP","PP"]
	writer = csv.writer(results)
	writer.writerow(header)
	for i in range(counter):
		row = [genera_lst[i],dp_lst[i],pp_lst[i]]
		writer.writerow(row)
	print(counter)
	print("DP average: " + str(average(dp_lst)) + "\n")
	print("PP average: " + str(average(pp_lst)) + "\n")
	print("DP median: " + str(statistics.median(dp_lst)) + "\n")
	print("PP average: " + str(statistics.median(pp_lst)) + "\n")
	'''
	results.write(str(counter) + " genera\n")
	results.write("DP list:\n")
	results.write(str(dp_lst) + "\n")
	results.write("PP list:\n")
	results.write(str(pp_lst) + "\n")
	results.write("*******************\n")
	results.write("DP average: " + str(average(dp_lst)) + "\n")
	results.write("*******************\n")
	results.write("PP average: " + str(average(pp_lst)) + "\n")
	results.write("*******************\n")
	results.write("DP median: " + str(statistics.median(dp_lst)) + "\n")
	results.write("*******************\n")
	results.write("PP average: " + str(statistics.median(pp_lst)) + "\n")
	'''
