import os
import argparse
import csv
from utils import *

from data_processing import best_model

### ARGS
parser = argparse.ArgumentParser(description="produce sh files for running model adequacy, either in regular or sanity mode")
parser.add_argument('--nsims', '-n', help='Number of simulations',required=True)
parser.add_argument('--sanity', '-s', help='Regular mode = 0, sanity mode = 1',required=False, default = 0)
parser.add_argument('--genera', '-f', help='Genera file',required=True)
parser.add_argument('--script', '-c', help='Script path',required=True)
parser.add_argument('--models_flag', '-m', help='models flag. options: ALL, BEST, OTHERS, DEFINED',required=False, default = "BEST") # options: ALL, BEST, OTHERS, DEFINED
parser.add_argument('--models_defined', '-md', help='names of models to test',required=False) # if DEFINED give model's name(s)
parser.add_argument('--results_flag', '-r', help='results flag. Previous results to use = 1, otherwise = 0',required=False, default = 0) # use previous simulations results
parser.add_argument('--queue_name', '-q', help='queue name',required=False, default = "itaym") # use previous simulations results

args = parser.parse_args()
nsims = int(args.nsims)
sanity = int(args.sanity)
filename = args.genera
script = args.script
models_flag = args.models_flag
models_defined = args.models_defined
results_flag = int(args.results_flag)
queue = args.queue_name

lang = "python"
all_models = ["BASE_NUM","BASE_NUM_DUPL","CONST_RATE","CONST_RATE_DEMI","CONST_RATE_DEMI_EST","CONST_RATE_NO_DUPL"] # all models
counts_file = ".counts_edit"

d = model_per_genus()


with open (filename, "r") as genera:
	with open("/groups/itay_mayrose/annarice/model_adequacy/genera/summary_genera_jan_20.csv", "w+") as writeFile:
		header = ["Genus", "Model"]
		writer = csv.writer(writeFile)
		writer.writerow(header)

		for genus in genera:
			genus = genus.strip()
			if models_flag == "ALL":
				models = all_models
			if models_flag == "BEST":
				results_sum = "/groups/itay_mayrose/annarice/model_adequacy/genera/" + genus + "/result_sum"
				models = best_model.get_best_model(results_sum)
				models = models.split(",") # returns a list
			if models_flag == "OTHERS":
				models = list(set(all_models) - set(models)) # run on all models that are not the best model
			if models_flag == "DEFINED":
				models = models_defined.split(",")  # returns a list

			tested_model = d.get(genus)

			for model in models:
				if sanity == 1:
					for i in range(1):  # NEED THIS FOR MA ON SANITY
						name = genus + str(i) + "." + model
						wd = "/groups/itay_mayrose/annarice/model_adequacy/sanity/" + genus + "/" + tested_model + "/adequacy_test/" + str(i) + "/"
						check_path = wd + model + "/adequacy_test/"
						if os.path.isdir(check_path) and os.listdir(check_path): # already executed - prevent from running over
							continue
						co = "/groups/itay_mayrose/annarice/model_adequacy/sanity/" + genus + "/" + tested_model + "/adequacy_test/" + str(i) + "/counts.txt"
						tree = "/groups/itay_mayrose/annarice/model_adequacy/sanity/" + genus + "/tree_1"
						cmd = "-c " + wd + " -m " + model + " -id " + genus + " -nt 1 -ns " + str(
							nsims) + " -ce /groups/itay_mayrose/itaymay/code/chromEvol/chromEvol_source-current/chromEvol -co " + co + " -s " + str(
							sanity) + " -r " + str(results_flag)
						os.system("python ~/create_sh.py " + "-name " + name + " -l " + lang + " -s " + script + " -q " + queue + " -p \'" + cmd + "\'")
				else:
					name = genus + "." + model
					wd = "/groups/itay_mayrose/annarice/model_adequacy/genera/" + genus + "/" + model + "/"
					co = "/groups/itay_mayrose/annarice/model_adequacy/genera/" + genus + "/" + genus + counts_file
					tree = "/groups/itay_mayrose/annarice/model_adequacy/genera/" + genus + "/tree_1"
					cmd = "-c " + wd + " -m " + model + " -id " + genus + " -nt 1 -ns " + str(
						nsims) + " -ce /groups/itay_mayrose/itaymay/code/chromEvol/chromEvol_source-current/chromEvol -co " + co + " -s " + str(
						sanity) + " -r " + str(results_flag)
					row = [genus, models]
					writer.writerow(row)
					os.system("python ~/create_sh.py " + "-name " + name + " -l " + lang + " -s " + script + " -q " + queue + " -p \'" + cmd + "\'")