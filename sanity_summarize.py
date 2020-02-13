import numpy as np
import scipy.stats as sc
import re
from utils import *

def params_per_model():
	d = {"_lossConstR":0, "_gainConstR":0, "_duplConstR":0, "_demiPloidyR":0, "_baseNumber":0, "_baseNumberR":0}
	return d


lst = ["Aloe","Phacelia","Lupinus","Hypochaeris","Brassica","Pectis","Hordeum","Crepis"]
models = ["CONST_RATE","CONST_RATE_NO_DUPL","BASE_NUM","BASE_NUM_DUPL"]

models_d = model_per_genus()

out_file = "/groups/itay_mayrose/annarice/model_adequacy/sanity/sanity_summarize_Feb.csv"
outfile = open(out_file, "w")
outfile.write("Simulated_under,model2,nsim,genus,variance,entropy,range,unique_counts,fitch,loss,gain,dupl,demi,base,baseR,sum" + "\n")

for genus in lst:

	model1 = models_d.get(genus)
	for i in range(50):
		for model2 in models:
			sanity_results = "/groups/itay_mayrose/annarice/model_adequacy/sanity/" + genus + "/" + model1 + "/adequacy_test/" + str(i) + "/" + model2 + "/adequacy_test/adequacy_vec"
			try:
				with open(sanity_results,"r") as ma:
					res = ma.read()
				res = res[1:-1]
				outfile.write(model1 + "," + model2 + "," + str(i) + "," + genus + "," + res + ",")
				sum_stats = sum([int(i) for i in res.split(",")])

				d = params_per_model()  # get param names according to the current model
				### SANITY PARAMETERS
				params_file = "/groups/itay_mayrose/annarice/model_adequacy/sanity/" + genus + "/" + model1 + "/adequacy_test/" + str(i) +  "/" + model2 + "/adequacy_test/param_sim"
				#print(params_file)
				sanity_params = {}
				with open(params_file, "r") as params:
					for line in params:
						line = line.strip()
						tmp = re.search("(\_.*)\s(\d.*)", line)
						if tmp:
							sanity_params[tmp.group(1)] = float(tmp.group(2))
				for key in d.keys():
					if key in sanity_params.keys():
						d[key] = sanity_params[key]
					else:
						d[key] = 0
					outfile.write(str(d[key]) + ",")
				outfile.write(str(sum_stats))
				outfile.write("\n")
			except:
				print(genus + " " + str(i) + " " + model2 + " is missing")
				continue
outfile.close()