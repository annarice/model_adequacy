import os

lst = ["Acanthus", "Acer", "Actinidia", "Alisma","Allium", "Aloe", "Aphelandra", "Barleria", "Carlowrightia", "Conophytum", "Echinodorus",
       "Elytraria", "Iris", "Justicia", "Mesembryanthemum","Narcissus", "Phyllobolus", "Prunus","Psilocaulon", "Ruellia", "Sagittaria", "Sambucus",
       "Solanum", "Strobilanthes", "Tetramerium", "Thunbergia", "Viburnum"]
for genus in lst:
	source = "/groups/itay_mayrose/michaldrori/MSA_JmodelTree/output_MD/" + genus + "/" + genus + "_Chromevol_prune/chromevol_out/infer/infer_tree_1"
	dest = "/groups/itay_mayrose/annarice/model_adequacy/" + genus + "/"
	counts = "/groups/itay_mayrose/michaldrori/MSA_JmodelTree/output_MD/" + genus + "/" + genus + "_Chromevol_prune/chromevol_out/" + genus + ".counts_edit"
	dest_counts = dest + genus + ".counts_edit"
	os.system("cp -rf " + source + " " + dest)
	os.system("cp -rf " + counts + " " + dest)


filename = "/groups/itay_mayrose/annarice/model_adequacy/genera/genera_sample"
with open (filename, "r") as genera:
	for genus in genera:
		genus = genus.strip()
		source = "/groups/itay_mayrose/michaldrori/MSA_JmodelTree/output_MD/" + genus + "/" + genus + "_Chromevol_prune/chromevol_out/infer/infer_tree_1"
		dest = "/groups/itay_mayrose/annarice/model_adequacy/genera/" + genus + "/"
		counts = "/groups/itay_mayrose/michaldrori/MSA_JmodelTree/output_MD/" + genus + "/" + genus + "_Chromevol_prune/chromevol_out/" + genus + ".counts_edit"
		dest_counts = dest + genus + ".counts_edit"
		os.system("cp -rf " + source + " " + dest)
		os.system("cp -rf " + counts + " " + dest)



## /groups/itay_mayrose/annarice/model_adequacy/Acer/CONST_RATE/adequacy_test/1 ---> range(10), data, and add tree
import os
import gzip, tarfile
import shutil

l = []
for i in range(1000):
	l.append(str(i))

lst = ["Aloe","Lilium","Arctostaphylos","Gossypium","Eulophia","Tillandsia","Polygonatum","Rhododendron","Magnolia",
       "Lathyrus","Camellia","Paphiopedilum","Mentzelia","Ornithogalum","Iris","Caragana","Acer","Agrostis","Begonia","Habenaria"]
lst = ["Aloe","Phacelia","Lupinus","Hypochaeris","Crepis","Pectis","Chlorophytum","Achillea"]
lst = ["Aloe"]
d = {"Aloe":"CONST_RATE","Phacelia":"CONST_RATE","Lupinus":"CONST_RATE_NO_DUPL","Hypochaeris":"CONST_RATE_NO_DUPL",
     "Crepis":"BASE_NUM","Pectis":"BASE_NUM","Chlorophytum":"BASE_NUM_DUPL","Achillea":"BASE_NUM_DUPL"}
for genus in lst:
	model = d.get(genus)
	'''
	if genus == "Rhododendron" or genus == "Magnolia" or genus == "Lathyrus" or genus == "Camellia" or genus == "Paphiopedilum" or genus == "Mentzelia" or genus == "Ornithogalum":
		model = "BASE_NUM"
	if genus == "Aloe" or genus == "Lilium" or genus == "Arctostaphylos" or genus == "Gossypium" or genus == "Eulophia" or genus == "Tillandsia" or genus == "Polygonatum":
		model = "CONST_RATE"
	if genus == "Iris" or genus == "Caragana" or genus == "Acer" or genus == "Agrostis" or genus == "Begonia" or genus == "Habenaria":
		model = "CONST_RATE_DEMI"
	'''
	untargz("/groups/itay_mayrose/annarice/model_adequacy/genera/" + genus + "/" + model + "/adequacy_test/zipped.tar.gz")
	for i in range(50):
		dest_dir = "/groups/itay_mayrose/annarice/model_adequacy/sanity/" + genus + "/" + model + "/adequacy_test/" + str(i) + "/"
		if not os.path.exists(dest_dir):
			res = os.system("mkdir -p " + dest_dir)  # -p allows recusive mkdir in case one of the upper directories doesn't exist
		counts_source = "/groups/itay_mayrose/annarice/model_adequacy/genera/" + genus + "/" + model + "/adequacy_test/" + str(i) + "/simCounts.txt"
		counts_dest = dest_dir + "counts.txt"
		os.system("cp -rf " + counts_source + " " + counts_dest)
	dest_genus = "/groups/itay_mayrose/annarice/model_adequacy/sanity/" + genus + "/"
	if not os.path.exists(dest_genus):
		res = os.system("mkdir -p " + dest_genus)
	tree_source = "/groups/itay_mayrose/annarice/model_adequacy/genera/" + genus + "/tree_1"
	tree_dest = "/groups/itay_mayrose/annarice/model_adequacy/sanity/" + genus + "/tree_1"
	os.system("cp -rf " + tree_source + " " + tree_dest)
	#targz_dir(out_dir, l, "zipped.tar.gz", True)
	targz_dir("/groups/itay_mayrose/annarice/model_adequacy/genera/" + genus + "/" + model + "/adequacy_test/", l, "zipped.tar.gz", True)


######################################################################################################################
###################################### run model adequacy for a list of genera #######################################
######################################################################################################################
for genus in lst:
	cmd = "module load python/python-anaconda3.6.5;  module load  perl/perl-5.28.1; python ~/model_adequacy/code/main.py -c ~/model_adequacy/ -m BASE_NUM,BASE_NUM_DUPL,CONST_RATE,CONST_RATE_DEMI,CONST_RATE_DEMI_EST,CONST_RATE_NO_DUPL -id " + genus + " -nt 1 -ns 100 -ce /bioseq/chromEvol/chromEvol.exe"
	os.system(cmd)

######################################################################################################################
############################################## delete file from all dirs #############################################
######################################################################################################################
for genus in lst:
	filename = "/groups/itay_mayrose/annarice/model_adequacy/" + genus + "/runtime_max_chr_sim_num.csv"
	os.system("rm " + filename)

######################################################################################################################
################################### summarize to a single file all runtime results ###################################
######################################################################################################################
import pandas as pd

def get_counts(filename):
    '''
        reads the .counts_edit file and extracts the counts
    :param filename: supplied by the user
    :return: list of counts
    '''
    with open(filename, "r") as tmp_counts_file:
        counts = []
        for line in tmp_counts_file:
            line = line.strip()
            if line.startswith('>'):
                continue
            else:
                if line=="x":
                    continue
                counts.append(int(line))
    return (counts)

out_file = "/groups/itay_mayrose/annarice/model_adequacy/genera_runtime_fixed.csv"
outfile = open(out_file, "a")
outfile.write("Model,Max,nsims,time,Variance,Entropy,Range,Unique_counts" + "\n")

for genus in lst:
	direc = "/groups/itay_mayrose/annarice/model_adequacy/" + genus + "/"
	data = pd.read_csv(direc + "result_sum", sep="\t", header=None)
	tmp = data.loc[data[3] == 0, 0].values[0]
	counts = get_counts(direc + genus + ".counts_edit")
	tips = len(counts)
	filename = direc + "runtime_iterated_fixed.csv"
	with open(filename, "r") as runtime:
		all_lines = runtime.read()
	outfile.write(genus + "," + tmp + "," + str(tips) + "\n")
	outfile.write(all_lines)

outfile.close()

for genus in lst:

	cmd = "grep -R --include='simEvents.txt' 'Total number of transitions to max chromosome: [^0]' " + output_dir
	tmp = os.system(cmd)
	f = open(working_dir + "/increasing_max_chr.txt", "w")
	f.write("Iteration number " + str(mult) + ", Max number is currently " + str(max_for_sim))
	f.close()
	if tmp != 0:  # did not hit upper bound
		break  # no need to keep increasing the max number


#grep -R --include="simEvents.txt" "Total number of transitions to max chromosome:" /groups/itay_mayrose/annarice/model_adequacy/Actinidia/BASE_NUM/adequacy_test/

# summarize

######################################################################################################################
################################### summarize results of fixed chr number ###################################
######################################################################################################################

lst = ["Acer", "Aloe", "Echinodorus", "Justicia", "Prunus","Ruellia", "Sagittaria", "Sambucus", "Strobilanthes"]
for genus in lst:
	cmd = "module load python/python-anaconda3.6.5;  module load  perl/perl-5.28.1; python ~/model_adequacy/code/main.py -c ~/model_adequacy/ -m BASE_NUM,BASE_NUM_DUPL,CONST_RATE,CONST_RATE_DEMI,CONST_RATE_DEMI_EST,CONST_RATE_NO_DUPL -id " + genus + " -nt 1 -ns 100 -ce /bioseq/chromEvol/chromEvol.exe"
	os.system(cmd)

# perform KS test on each pair
from scipy import stats
for genus in lst:
	two = "/groups/itay_mayrose/annarice/model_adequacy/"+genus+"/BASE_NUM/adequacy_test/dist_200"
	eight = "/groups/itay_mayrose/annarice/model_adequacy/"+genus+"/BASE_NUM/adequacy_test/dist_800"
	with open(two,"r") as f1:
		f1d1 = eval(f1.readline())
		f1d2 = eval(f1.readline())
		f1d3 = eval(f1.readline())
		f1d4 = eval(f1.readline())
	with open(eight, "r") as f2:
		f2d1 = eval(f2.readline())
		f2d2 = eval(f2.readline())
		f2d3 = eval(f2.readline())
		f2d4 = eval(f2.readline())
	res1 = stats.ks_2samp(f1d1, f2d1)
	res2 = stats.ks_2samp(f1d2, f2d2)
	res3 = stats.ks_2samp(f1d3, f2d3)
	res4 = stats.ks_2samp(f1d4, f2d4)
	if res1[1]<0.05:
		print(genus + " - statistic number 1 is different")
	else:
		print(genus + " - statistic number 1 is equal")
	if res2[1]<0.05:
		print(genus + " - statistic number 2 is different")
	else:
		print(genus + " - statistic number 2 is equal")
	if res3[1]<0.05:
		print(genus + " - statistic number 3 is different")
	else:
		print(genus + " - statistic number 3 is equal")
	if res4[1]<0.05:
		print(genus + " - statistic number 4 is different")
	else:
		print(genus + " - statistic number 4 is equal")


######################################################################################################################
################################################## summarize sanity checks ###########################################
######################################################################################################################

import numpy as np
import scipy.stats as sc

def get_counts(filename):
    '''
        reads the .counts_edit file and extracts the counts
    :param filename: supplied by the user
    :return: list of counts
    '''
    with open(filename, "r") as tmp_counts_file:
        counts = []
        for line in tmp_counts_file:
            line = line.strip()
            if line.startswith('>'):
                continue
            else:
                if line=="x":
                    continue
                counts.append(int(line))
    return (counts)

def calculate_statistics(counts):
    '''
        given list of counts produces statistics: variance,min,max,entropy
        ########## ADD MP OF NUMBER OF TRANSITIONS
    :param counts: list of chromosome numbers
    :return: list of statistics representing the counts
    '''
    # variance
    v = np.var(counts)

    # range = max - min
    r = max(counts) - min(counts)

    # enthropy, calculates the probabilities
    d = {}
    for i in counts:
        d[i] = counts.count(i)
    prob_lst = [x / len(counts) for x in list(d.values())]
    e = sc.entropy(prob_lst)

    # unique counts
    counts_set = set(counts)
    u = len(counts_set)
    return ([v, e, r, u])

def test_adequacy(sim_stats, stats):
    '''
    go over each statistic in the list and see if is adequate
    '''
    adequacy_lst = []
    stat_lst = []
    for i in range(len(stats)):
        sim_stat_dist = [x[i] for x in sim_stats]  # simulated ith distribution, x the item in each simulated list
        print ("**********************************************")
        print(sim_stat_dist)
        print ("**********************************************")
        stat_star_upper = np.percentile(sim_stat_dist, 97.5)  # calculate the upper limit
        stat_star_lower = np.percentile(sim_stat_dist, 2.5)  # calculate the lower limit
        model = 0
        if stats[i] <= stat_star_upper and stats[i] >= stat_star_lower:
            model = 1
        adequacy_lst.append(model)
        stat_lst.append(stats[i])
    return (adequacy_lst,stat_lst)

lst = ["Acer", "Aloe", "Echinodorus", "Justicia", "Prunus","Ruellia", "Sagittaria", "Sambucus", "Strobilanthes"]
models = ["CONST_RATE","CONST_RATE_DEMI","CONST_RATE_DEMI_EST", "CONST_RATE_NO_DUPL"]

out_file = "/groups/itay_mayrose/annarice/model_adequacy/sanity.csv"
outfile = open(out_file, "a")
outfile.write("Simulated_under,model2,nsim,genus,variance,entropy,range,unique_counts" + "\n")

for genus in lst:
	for model1 in models:
		ma_filename = "/groups/itay_mayrose/annarice/model_adequacy/" + genus + "/" + model1 + "/adequacy_test/" + model1 + "_MA.res"
		for i in range(10):
			for model2 in models:
				sanity_results = "/groups/itay_mayrose/annarice/model_adequacy/" + genus + "/" + model1 + "/adequacy_test/" + str(i) + "/sanity/adequacy_test/dist_vec_" + model2
				with open(sanity_results,"r") as ma:

					sim_dist = ma_dist.readlines() # list of distributions
					sim_dist = [x.strip() for x in sim_dist]
				sanity_counts_file = "/groups/itay_mayrose/annarice/model_adequacy/" + genus + "/" + model1 + "/" + "adequacy_test/" + str(i) + "/simCounts.txt"
				sanity_original_counts = get_counts(sanity_counts_file)
				sanity_original_counts_statistics = calculate_statistics(sanity_original_counts)
				sanity_original_adequacy_results, stats_results = test_adequacy(sim_dist, sanity_original_counts_statistics) # take sanity_original_adequacy_results

				sanity_ma_string = ",".join(str(sanity_original_adequacy_results))
				sanity_ma_string = ", ".join(map(str, sanity_original_adequacy_results))
				outfile.write(model1 + "," + model2 + "," + str(i) + "," + genus + "," + sanity_ma_string)
				#sanity_filename = "/groups/itay_mayrose/annarice/model_adequacy/" + genus + "/" + model1 + "/adequacy_test/" + str(i) + "/sanity/adequacy_test/" + model2 + "_MA.res"
		if model1=="CONST_RATE":
			break



import csv
import regex as re
from data_processing import best_model
models = ["CONST_RATE","CONST_RATE_DEMI","CONST_RATE_DEMI_EST","CONST_RATE_NO_DUPL","BASE_NUM","BASE_NUM_DUPL"]
genera_file = "/groups/itay_mayrose/annarice/model_adequacy/genera/genera"
summary_file = "/groups/itay_mayrose/annarice/model_adequacy/genera/summary_best_model.csv"
with open(summary_file, "w+") as writeFile:
	header = ["Genus", "Best_model","Variance","Entropy","Range","Unique","Parsimony"]
	writer = csv.writer(writeFile)
	writer.writerow(header)
	with open (genera_file,"r") as genera:
		for genus in genera:
			genus = genus.strip()
			results_sum = "/groups/itay_mayrose/annarice/model_adequacy/genera/" + genus + "/result_sum"
			models = best_model.get_best_model(results_sum)
			models = models.split(",")  # returns a list
			for model in models:
				adequacy_filename = "/groups/itay_mayrose/annarice/model_adequacy/genera/" + genus + "/" + model + "/adequacy_test/adequacy_vec"
				try:
					with open(adequacy_filename, "r") as adequacy_f:
						tmp = adequacy_f.readline()
						tmp = tmp[1:-1:]
						'''
						if re.search("0", tmp):
							adequate = 0
						else:
							adequate = 1
						'''
					row = [genus,model,tmp]
					writer.writerow(row)
				except:
					print("No result for " + genus)
					continue

###################################################################################################
#################################### REMOVE FOLDERS MASSIVELY #####################################
###################################################################################################

import os
import argparse
import pandas as pd
import csv
import gzip, tarfile
import shutil

def get_best_model(filename):
    data = pd.read_csv(filename, sep="\t", header=None)
    tmp = data.loc[data[3] == 0,0].values[0]
    return tmp # the name of the best model

def targz_dir(outer_dir, dirs_list, dest_zip_filename, delete_after_zipping):
	cwd = os.getcwd()
	os.chdir(outer_dir)
	tarw = tarfile.open(dest_zip_filename, "w:gz")
	for dirname in dirs_list:
		if os.path.exists(dirname):
			tarw.add(dirname)
	tarw.close()
	if delete_after_zipping:
		for dirname in dirs_list:
			try:
				shutil.rmtree(dirname)
			except:
				pass
	os.chdir(cwd)

filename = "/groups/itay_mayrose/annarice/model_adequacy/genera/genera"
all_models = ["BASE_NUM","BASE_NUM_DUPL","CONST_RATE","CONST_RATE_DEMI","CONST_RATE_DEMI_EST","CONST_RATE_NO_DUPL"] # all models
l = []
for i in range(1000):
	l.append(str(i))
with open (filename, "r") as genera:
	for genus in genera:
		genus = genus.strip()
		results_sum = "/groups/itay_mayrose/annarice/model_adequacy/genera/" + genus + "/result_sum"
		models = get_best_model(results_sum)
		models = models.split(",") # returns a list
		#models = list(set(all_models) - set(models)) # run on all models that are not the best model
		for model in models:
			out_dir = "/groups/itay_mayrose/annarice/model_adequacy/genera/" + genus + "/" + model + "/adequacy_test/"
			os.system("python ~/create_sh.py " + "-name " + genus + " -l " + python + " -s " + script + " -p \'" + cmd + "\'")
			try:
				print("trying " + genus)
				targz_dir(out_dir, l, "zipped.tar.gz", True)
			except:
				print("passing " + genus)
				pass


cmd = "-c " + wd + " -m " + model + " -id " + genus + " -nt 1 -ns " + str(nsims) + " -ce /bioseq/chromEvol/chromEvol.e