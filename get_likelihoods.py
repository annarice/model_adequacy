# nested models should get lower LL

# first look in the sanity folders:
# read the /groups/itay_mayrose/annarice/model_adequacy/sanity/Justicia/CONST_RATE/adequacy_test/0/CONST_RATE/chromEvol.res file
# search for "LogLikelihood" in the file and take the number after it

# if not in the sanity folder then look at:
# result_sum in the case of a non-sanity checks

import argparse
import regex as re
import csv

# args
parser = argparse.ArgumentParser(description="produce sh files for running model adequacy, either in regular or sanity mode")
parser.add_argument('--nsims', '-n', help='Number of simulations',required=False) # in sanity --> 50
parser.add_argument('--genera', '-f', help='Genera file',required=True)
#parser.add_argument('--models_defined', '-md', help='define which models to run',required=False) # in sanity --> CONST_RATE_NO_DUPL,CONST_RATE,CONST_RATE_DEMI_EST,CONST_RATE_DEMI
parser.add_argument('--sanity_flag', '-sf', help='Genera file',required=True)

args = parser.parse_args()
nsims = int(args.nsims)
filename = args.genera
#models_defined = args.models_defined
#models = models_defined.split(",")  # returns a list
sanity_flag = int(args.sanity_flag)

nested_const = ["CONST_RATE_NO_DUPL","CONST_RATE","CONST_RATE_DEMI","CONST_RATE_DEMI_EST"]
nested_base = ["BASE_NUM","BASE_NUM_DUPL"]
ALL_MODELS = ["CONST_RATE_NO_DUPL","CONST_RATE","CONST_RATE_DEMI","CONST_RATE_DEMI_EST","BASE_NUM","BASE_NUM_DUPL"]

outfile = "/groups/itay_mayrose/annarice/model_adequacy/sanity/LL_test2.csv"

def get_liks(tested_model, i):
	d = {"CONST_RATE_NO_DUPL": 0, "CONST_RATE": 0, "CONST_RATE_DEMI": 0, "CONST_RATE_DEMI_EST": 0, "BASE_NUM": 0,"BASE_NUM_DUPL": 0}
	for model in ALL_MODELS:
		if sanity_flag == 1:
			results_sum = "/groups/itay_mayrose/annarice/model_adequacy/sanity/" + genus + "/" + tested_model + "/adequacy_test/" + str(i) + "/" + model + "/chromEvol.res"
		else:
			results_sum = "/groups/itay_mayrose/annarice/model_adequacy/genera/" + model + "/result_sum"
		try:
			with open(results_sum, "r") as CE_res:
				for line in CE_res:
					tmp_line = re.search("LogLikelihood = (.*)", line)
					if tmp_line:
						LL = float(tmp_line.group(1))
						d[model] = LL
		except:
			pass

	if d.get("CONST_RATE") == 0 and d.get("BASE_NUM") == 0:  # assuming these two models must have results. If not - don't write to the csv file
		return(None)

	row = [genus, str(i)]
	for m in ALL_MODELS:
		row.append(d.get(m))
	if (d.get("CONST_RATE_NO_DUPL") > d.get("CONST_RATE") or d.get("CONST_RATE") > d.get(
			"CONST_RATE_DEMI") or d.get("CONST_RATE_DEMI") > d.get("CONST_RATE_DEMI_EST") \
	    or d.get("BASE_NUM") > d.get("BASE_NUM_DUPL")) and d.get("CONST_RATE_NO_DUPL") != 0:
		row.append(1)
	else:
		row.append(0)
	return(row)


# MAIN
with open (outfile,"w+") as output:
	header = ["Genus","Ind","CONST_RATE_NO_DUPL","CONST_RATE","CONST_RATE_DEMI","CONST_RATE_DEMI_EST","BASE_NUM","BASE_NUM_DUPL","LL_flag"]
	writer = csv.writer(output)
	writer.writerow(header)
	with open(filename, "r") as genera:
		for genus in genera:
			genus = genus.strip()

			if sanity_flag == 1:  # summary dir

				if genus == "Jasminum" or genus == "Fragaria" or genus == "Ourisia":
					tested_model = "BASE_NUM"
				if genus == "Malus" or genus == "Parnassia" or genus == "Noccaea" or genus == "Justicia":
					tested_model = "CONST_RATE"
				if genus == "Clarkia" or genus == "Rubia" or genus == "Buxus":
					tested_model = "CONST_RATE_DEMI"

				for i in range(nsims):
					row = get_liks(tested_model,i)
					if row != None:
						writer.writerow(row)
			else: # non-sanity dirs
				continue





'''
for i in range(nsims):
	d = {"CONST_RATE_NO_DUPL": 0, "CONST_RATE": 0, "CONST_RATE_DEMI": 0, "CONST_RATE_DEMI_EST": 0,"BASE_NUM": 0, "BASE_NUM_DUPL": 0}
	for model in ALL_MODELS:
		results_sum = "/groups/itay_mayrose/annarice/model_adequacy/sanity/" + genus + "/" + tested_model + "/adequacy_test/" + str(i) + "/" + model + "/chromEvol.res"
		try:
			with open(results_sum, "r") as CE_res:
				for line in CE_res:
					tmp_line = re.search("LogLikelihood = (.*)", line)
					if tmp_line:
						LL = float(tmp_line.group(1))
						d[model] = LL
		except:
			pass

	if d.get("CONST_RATE") == 0 and d.get("BASE_NUM") == 0: # assuming these two models must have results. If not - don't write to the csv file
		continue

	row = [genus, str(i)]
	for m in ALL_MODELS:
		row.append(d.get(m))
	if (d.get("CONST_RATE_NO_DUPL") > d.get("CONST_RATE") or d.get("CONST_RATE") > d.get("CONST_RATE_DEMI") or d.get("CONST_RATE_DEMI") > d.get("CONST_RATE_DEMI_EST") \
			or d.get("BASE_NUM") > d.get("BASE_NUM_DUPL")) and d.get("CONST_RATE_NO_DUPL") != 0:
		row.append(1)
	else:
		row.append(0)
	writer.writerow(row)

'''