import os
from utils import *

script = "~/model_adequacy/code/sanity.py"
lang = "python"
models = ["CONST_RATE","CONST_RATE_NO_DUPL","BASE_NUM","BASE_NUM_DUPL"]

lst = ["Aloe","Phacelia","Lupinus","Hypochaeris","Brassica","Pectis","Crepis","Hordeum"]
lst = ["Pectis"]

queue = "itaym"

d = model_per_genus()

for genus in lst:
	tested_model = d.get(genus)
	tree = "~/model_adequacy/sanity/" + genus + "/tree_1"
	wd = "~/model_adequacy/sanity/" + genus + "/" + tested_model + "/adequacy_test/"
	for model in models:
		for i in range(50,100):
			name = genus + "." + model + str(i) + ".Sanity"
			cmd = "-c " + wd + " -t " + tree + " -m " + model + " -ns " + str(i) + " -ce /groups/itay_mayrose/itaymay/code/chromEvol/chromEvol_source-current/chromEvol -g " + genus
			os.system("python ~/create_sh.py " + "-name " + name + " -l " + lang + " -s " + script + " -q " + queue + " -p \'" + cmd + "\'")