import csv
import regex as re
from data_processing import best_model
from data_processing import process_data
from defs import *
import argparse
from utils import *

parser = argparse.ArgumentParser(description="Summerize best_model results of statistics and true percentiles")
parser.add_argument('--genera', '-f', help='Genera file',required=True)
parser.add_argument('--summary', '-s', help='output file',required=True)

models = ["CONST_RATE","CONST_RATE_DEMI","CONST_RATE_DEMI_EST","CONST_RATE_NO_DUPL","BASE_NUM","BASE_NUM_DUPL"]
wanted_keys = ["_lossConstR","_gainConstR","_duplConstR","_demiPloidyR","_baseNumberR","_simulationsTreeLength"]

args = parser.parse_args()
genera_file = args.genera
summary_file = args.summary

with open(summary_file, "w+") as writeFile:
	header = ["Genus", "Best_model","Variance","Entropy","Range","Unique","Parsimony","Time","Loss","Gain","Dupl","Demi","BaseR","tree_length",
	          "variance_perc","entropy_perc","range_perc","unique_perc","fitch_perc","time_perc"]
	writer = csv.writer(writeFile)
	writer.writerow(header)

	with open (genera_file,"r") as genera:
		for genus in genera:
			genus = genus.strip()
			results_sum = "/groups/itay_mayrose/annarice/model_adequacy/genera/" + genus + "/result_sum"
			models = best_model.get_best_model(results_sum)
			models = models.split(",")  # returns a list
			for model in models:
				path = "/groups/itay_mayrose/annarice/model_adequacy/genera/" + genus + "/" + model + "/"
				flag_file = path + "adequacy_test/NO_NEED_FOR_MA"
				if os.path.isfile(flag_file):
					continue
				CE_res = path + "/chromEvol.res"
				root_freq = path + "/root_freq"
				percentiles = path + "adequacy_test/true_percentiles"
				count_file =  "/groups/itay_mayrose/annarice/model_adequacy/genera/" + genus + "/" + genus + ".counts_edit"
				parameters_dictionary = best_model.get_params(CE_res, root_freq)
				adequacy_filename = path + "adequacy_test/adequacy_vec"

				row = [genus, model]

				try:
					with open(adequacy_filename, "r") as adequacy_f:
						tmp = adequacy_f.readline()
					row.extend(str_to_lst(tmp,"int"))
					for key in wanted_keys:
						row.append(parameters_dictionary.get(key, 0))
					with open(percentiles, "r") as perc:
						res = perc.read()
						row.extend(str_to_lst(res, "float"))
					writer.writerow(row)
				except:
					print("No result for " + genus)
					continue