from utils import *
import argparse
import regex as re

# args
parser = argparse.ArgumentParser()
parser.add_argument('--nsims', '-n', help='Number of simulations',required=True)
parser.add_argument('--genera', '-f', help='Genera file',required=True)
parser.add_argument('--model', '-m', help='models flag',required=True)
parser.add_argument('--working_dir', '-wd', help='models flag',required=True)

args = parser.parse_args()
nsims = int(args.nsims)
filename = args.genera
model = args.model
wd = args.working_dir

l = []
for i in range(nsims):
	l.append(str(i))

with open (filename, "r") as genera:
	for genus in genera:
		genus = genus.strip()
		file = wd + "/" + genus + "/" + model + "/adequacy_test/zipped.tar.gz"
		untargz(file)

		param_file = wd + "/" + genus + "/" + model + "/adequacy_test/param_sim"
		params_dict = {"tree_factor":1, "gain_events":0, "loss_events":0, "duplication_events":0, "demi-dulications_events":0, "base_number_transitions":0, "transitions_to_max_chromosome":0}
		with open (param_file, "r") as params:
			for line in params:
				tmp_line = re.search("_simulationsTreeLength (\d+)", line) # tree multiplication
				if tmp_line:
					params_dict["tree_factor"] = int(tmp_line.group(1))
					continue
				tmp_line = re.search("_lossConstR (.*)", line) # loss
				if tmp_line:
					params_dict["loss_events"] = float(tmp_line.group(1))
					continue
				tmp_line = re.search("_gainConstR (.*)", line) # gain
				if tmp_line:
					params_dict["gain_events"] = float(tmp_line.group(1))
					continue
				tmp_line = re.search("_duplConstR (.*)", line)  # gain
				if tmp_line:
					params_dict["duplication_events"] = float(tmp_line.group(1))
					continue
				tmp_line = re.search("_baseNumberR (.*)", line)
				if tmp_line:
					params_dict["base_number_transitions"] = float(tmp_line.group(1))
					continue
				tmp_line = re.search("_demiPloidyR (.*)", line)
				if tmp_line:
					params_dict["demi-dulications_events"] = float(tmp_line.group(1))
					continue

		d = {}
		for i in range(nsims):
			simEvents = wd + "/" + genus + "/" + model + "/adequacy_test/" + str(i) + "/simEvents.txt"
			with open (simEvents, "r") as se:
				for line in se:
					tmp_line = re.search("Total number of (.*): (\d+)", line)
					if tmp_line:
						key = tmp_line.group(1)
						key = key.replace(" ", "_")
						val = int(tmp_line.group(2))
						if key not in d.keys():
							d[key] = [val]
						else:
							d[key].append(val)
		print ("****" + genus + ", " + model + "****")
		print ("expected, simulated")
		for key in d.keys():
			num_events = round(params_dict["tree_factor"] * params_dict[key],2)
			print(key + ":" + str(num_events) + ", " + str(round(average(d[key]),2)))

		out_dir = wd + "/" + genus + "/" + model + "/adequacy_test/"
		targz_dir(out_dir, l, "zipped.tar.gz", True)