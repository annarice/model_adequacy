import pandas as pd
import regex as re
import argparse
import os
import gzip, tarfile
from utils import *
from scipy import stats
import csv
#from create_thresholds_distribution import get_threshold


# args
parser = argparse.ArgumentParser(description="")
parser.add_argument('--nsims', '-n', help='Number of simulations',required=True)
parser.add_argument('--genera', '-f', help='Genera file',required=True)
parser.add_argument('--models_defined', '-md', help='define which models to run',required=False)
parser.add_argument('--results_file', '-re', help='define which models to run',required=True)

args = parser.parse_args()
nsims = int(args.nsims)
filename = args.genera
models_defined = args.models_defined
models = models_defined.split(",")  # returns a list
res_file = args.results_file

orig_numbers_filename = "/simCountsAllNodes.txt"
orig_dupl_filename = "/simEvents.txt"
inferred_numbers_filename = "/mlAncestors.tree"
inferred_expec_filename = "/expectations.txt"

l = []
for i in range(nsims):
	l.append(str(i))

d = model_per_genus()

def get_measure(filename,measure):
	with open(filename,"r") as measure_file:
		### root_num
		if error_measure == "root_num":
			tmp = measure_file.readline()
			if measure == "orig":
				num = int(measure_file.readline())
			else: # inferred
				tmp = re.search("\[N1-(\d+)", tmp)
				num = int(tmp.group(1))
			return (num)
		### total_dupl
		if error_measure == "total_dupl":
			num = 0
			for line in measure_file:
				tmp_line = re.search("Total number of duplication events\:\s(\d+.*)", line)
				if tmp_line:
					num = num + round(float(tmp_line.group(1)))
				tmp_line = re.search("Total number of demi.*\:\s(\d+.*)",line)
				if tmp_line:
					num = num + round(float(tmp_line.group(1)))
				tmp_line = re.search("Total number of.* trans.*\:\s(\d+.*)",line)
				if tmp_line:
					num = num + round(float(tmp_line.group(1)))
			return (num)
		### internal_nodes
		if error_measure == "internal_nodes":
			if measure == "orig":
				tmp = measure_file.read()
				tmp = re.findall(">N\d+\n(\d+)", tmp, re.M) # internal nodes
				return(list(map(int, tmp)))
			else: # inferred
				line = measure_file.readline()
				tmp = re.findall("N\d+\-(\d+)",line)
				tmp = tmp[::-1]
				return(list(map(int, tmp)))
		### branch_dupl
		if error_measure == "branch_dupl":
			lst = []
			flag = 0
			for line in measure_file:
				if line=="\n":
					continue
				if measure == "orig":
					tmp_line = re.search("^#N.+(du|base)",line)
				else:
					tmp_line = re.search("^NODE", line)
				if tmp_line:
					flag = 1
					continue
				if measure == "orig":
					if flag == 1 and not line.startswith("Total number of"):
						x = re.search("(.*)\:", line)
						lst.append(x.group(1))
					else:
						flag = 0
				else:
					if flag == 1 and not line.startswith("#+++++++++++++++++++++++++++++"):
						x = line.split()
						if len(x) == 6: # base_num model
							if float(x[3]) > 0.5 or float(x[4]) > 0.5 or float(x[5]) > 0.5:
								lst.append(x[0])
						else: # other models
							if float(x[3]) > 0.5 or float(x[4]) > 0.5:
								lst.append(x[0])
					else:
						flag = 0
			return(lst)
		if error_measure == "inference":
			lst = []
			flag = 0
			for line in measure_file:
				tmp_line = re.search("^LEAF",line)
				if tmp_line:
					flag = 1
					continue
				if flag == 1:
					x = line.split()
					if len(x) == 6:  # base_num model
						if float(x[3]) > SET_PP or float(x[4]) > SET_PP or float(x[5]) > SET_PP:
							lst.append(x[0])
					else:  # other models
						if float(x[3]) > SET_PP or float(x[4]) > SET_PP:
							lst.append(x[0])
				else:
					flag = 0
			return(lst)


def initialize_lsts():
	lst1 = [] # vector of original multiple counts in each simulation
	ad_lst = []
	inad_lst = []
	return (lst1,ad_lst, inad_lst)


l = []
for i in range(1000):
	l.append(str(i))


thresholds = pd.read_csv('/groups/itay_mayrose/annarice/model_adequacy/genera/thresholds.csv', sep=',')

with open(res_file , "w+") as writeFile:
	header = ["Genus", "Best_model", "Error_measure", "Adequate", "Inadequate","len_ad","len_inad","mean_ad","mean_inad","T-stat","PV"]
	writer = csv.writer(writeFile)
	writer.writerow(header)
	with open (filename, "r") as genera:
		for genus in genera:
			genus = genus.strip()

			tested_model = d.get(genus)

			results_sum = "/groups/itay_mayrose/annarice/model_adequacy/genera/" + genus + "/result_sum"
			best_model = get_best_model(results_sum)
			wd = "/groups/itay_mayrose/annarice/model_adequacy/genera/" + genus + "/" + best_model + "/adequacy_test/"
			wd2 = "/groups/itay_mayrose/annarice/model_adequacy/sanity/" + genus + "/" + best_model + "/adequacy_test/"
			out_dir = "/groups/itay_mayrose/annarice/model_adequacy/genera/" + genus + "/" + tested_model + "/adequacy_test/"
			targz_file = out_dir + "/zipped.tar.gz"
			print(out_dir)
			if not os.path.isdir(out_dir + "0/"):
				untargz(targz_file)

			error_measure_lst = ["internal_nodes", "root_num", "total_dupl", "branch_dupl", "inference"]

			try:
				SET_PP = float(thresholds[thresholds['Genus'] == genus]["PP"])
			except:
				error_measure_lst = ["internal_nodes", "root_num", "inference"]

			for error_measure in error_measure_lst:
				print(error_measure)
				multiple_counts, adequate_diff, inadequate_diff = initialize_lsts()

				for i in range(nsims):
					if error_measure == "root_num" or error_measure == "internal_nodes":
						measure_fullpath = wd + str(i) + orig_numbers_filename
					if error_measure == "total_dupl" or error_measure == "branch_dupl" or error_measure == "inference":
						#SET_PP = get_threshold("/groups/itay_mayrose/michaldrori/MSA_JmodelTree/output_MD/" + genus + "/" + genus + "_Chromevol_prune/chromevol_out/thresholds_PP") # outer function that fetches the genus' threshold
						measure_fullpath = wd + str(i) + orig_dupl_filename
					orig_num = get_measure(measure_fullpath,"orig")
					#print(str(orig_num))

					for model in models:
						if error_measure == "root_num" or error_measure == "internal_nodes":
							inferred_fullpath = wd2 + str(i) + "/" + model + inferred_numbers_filename
						if error_measure == "total_dupl" or error_measure == "branch_dupl" or error_measure == "inference":
							inferred_fullpath = wd2 + str(i) + "/" + model + inferred_expec_filename
						inferred_num = get_measure(inferred_fullpath, "inferred")
						#print(str(inferred_num))

						adequacy_filename = wd2 + str(i) + "/" + model + "/adequacy_test/adequacy_vec"

						with open (adequacy_filename,"r") as adequacy_f:
							tmp = adequacy_f.readline()
							# remove range and unique counts statistics
							tmp = tmp[1:-1]
							tmp = tmp.split(", ")
							del tmp[2:4]
							#print(tmp + " " +  genus + " " + model + " " + str(i))
							#if re.search("0",tmp):
							if "0" in tmp: # inadequate model
								if error_measure == "internal_nodes": # difference between two lists
									tmp_lst = [abs(x1 - x2) for (x1, x2) in zip(orig_num, inferred_num)]
									tmp_lst = sum(tmp_lst)
									inadequate_diff.append(tmp_lst)
								elif error_measure == "branch_dupl" or error_measure == "inference":
									tmp_lst = set(orig_num).symmetric_difference(set(inferred_num))
									inadequate_diff.append(len(tmp_lst))
								else: # single measure
									inadequate_diff.append(abs(orig_num-inferred_num))
							else:
								if error_measure == "internal_nodes": # difference between two lists
									tmp_lst = [abs(x1 - x2) for (x1, x2) in zip(orig_num, inferred_num)]
									tmp_lst = sum(tmp_lst)
									adequate_diff.append(tmp_lst)
								elif error_measure == "branch_dupl" or error_measure == "inference":
									tmp_lst = set(orig_num).symmetric_difference(set(inferred_num))
									adequate_diff.append(len(tmp_lst))
								else: # single measure
									adequate_diff.append(abs(orig_num-inferred_num))
				#print("***** " + genus + ", " + error_measure + " *****")
				#print ("Adequate list differences" + str(adequate_diff))
				#print ("Inadequate list differences" + str(inadequate_diff))
				if len(adequate_diff)==0 or len(inadequate_diff)==0:
					#print("Unable to perform analysis")
					continue
				#print ("Adequate diff " + str(round(average(adequate_diff),2)))
				#print ("Inadequate diff " + str(round(average(inadequate_diff),2)))
				t_stat, p_val = stats.ttest_ind(adequate_diff,inadequate_diff,equal_var = False)
				#print("statistic: " + str(round(t_stat,2)))
				#print("pv: " + str(round(p_val, 2)))

				row = [genus, best_model, error_measure, adequate_diff, inadequate_diff,len(adequate_diff),len(inadequate_diff),str(round(average(adequate_diff),2)),str(round(average(inadequate_diff),2)),str(round(t_stat,2)),str(round(p_val, 2))]
				writer.writerow(row)
			targz_dir(out_dir, l, "zipped.tar.gz", True)