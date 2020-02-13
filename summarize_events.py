from utils import *
import re
import csv

# for each genus that is in the sanity checks summarize its sim events for the 50 original sims.

models_d = model_per_genus()

lst = ["Aloe","Phacelia","Lupinus","Hypochaeris","Brassica","Pectis","Chlorophytum","Hordeum","Crepis"]

sanity_models = ["BASE_NUM_DUPL","CONST_RATE_NO_DUPL","CONST_RATE","BASE_NUM"]

output_file = "/groups/itay_mayrose/annarice/model_adequacy/sanity/sim_events_summary2.csv"
with open (output_file, "w+") as out_file:
	header = ["genus","model","sim","root","base_num","gain","loss","dupl","base","BASE_NUM_DUPL","CONST_RATE_NO_DUPL","CONST_RATE","BASE_NUM"]
	writer = csv.writer(out_file)
	writer.writerow(header)

	for genus in lst:
		model = models_d.get(genus)
		params_file = "/groups/itay_mayrose/annarice/model_adequacy/genera/" + genus + "/" + model + "/adequacy_test/param_sim"
		freq_file = "/groups/itay_mayrose/annarice/model_adequacy/genera/" + genus + "/" + model + "/root_freq"

		base_num = "0"
		root_num = "0"

		with open (params_file,"r") as params:
			for line in params:
				tmp_line = re.search("_baseNumber\s(\d+)",line)
				if tmp_line: # there's a base_numer
					base_num = tmp_line.group(1)
					break



		targz_file = "/groups/itay_mayrose/annarice/model_adequacy/genera/" + genus + "/" + model + "/adequacy_test/zipped.tar.gz"
		tar = tarfile.open(targz_file)
		for i in range(50):
			events_lst = []
			adequacy_lst = []
			sim_events = str(i) + "/simEvents.txt"
			sim_tree = str(i) + "/simTree.phr"
			for member in tar.getmembers():
				if member.name == sim_events:
					f = tar.extractfile(member)
					content = f.read()
					lines = content.splitlines()

					for line in lines:
						line_decoded = line.decode('utf-8')
						tmp_line = re.search("Total number of (gain|loss|duplication|base number) (events|transitions)\:\s(\d+.*)",line_decoded)
						if tmp_line:
							events_lst.append(tmp_line.group(3))
					continue

				if member.name == sim_tree:
					f = tar.extractfile(member)
					content = f.read()
					content = content.decode('utf-8')
					tmp = re.search("N1-(\d+)", content)
					if tmp:
						root_num = tmp.group(1)
			for sanity in sanity_models:
				adequacy_vec = "/groups/itay_mayrose/annarice/model_adequacy/sanity/" + genus + "/" + model + "/adequacy_test/" + str(i) + "/" + sanity + "/adequacy_test/adequacy_vec"
				adequacy = get_adequacy_from_vec(adequacy_vec)
				adequacy_lst.append(adequacy)
			row = [genus,model,i,root_num,base_num,','.join(events_lst),adequacy_lst]
			writer.writerow(row)

