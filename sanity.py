# module load python/python-anaconda3-5.3.0;  module load  perl/perl-5.28.1; python ~/model_adequacy/code/sanity.py -c ~/model_adequacy/Acer/CONST_RATE/adequacy_test/ -t ~/model_adequacy/Acer/tree_1 -m CONST_RATE -ns 2  -ce /bioseq/chromEvol/chromEvol.exe
import argparse
import os
from utils import *
from data_processing import process_data

os.system("module load python/python-anaconda3-5.3.0")


parser = argparse.ArgumentParser(description='sanity')
parser.add_argument('--main_res_dir', '-c', help='home directory of ChromEvol results',required=True) # ~/model_adequacy/genus/model/adequacy_test  (wd)
parser.add_argument('--tree', '-t', help='',required=True) # ~/model_adequacy/genus/tree_1
parser.add_argument('--model_name', '-m', help='the model tested for adequacy', required=True)
parser.add_argument('--sims_per_tree', '-ns', help='number of simulations for the adequacy test per original tree',required=False,default=1) # on which sims to run sanity check (range from 0 to -ns)
parser.add_argument('--CE_path', '-ce', help='ChromEvol executable path',required=False, default = "~/model_adequacy/chromEvol")
parser.add_argument('--genus', '-g', help='',required=False)

args = parser.parse_args()
main_res_dir = args.main_res_dir # /groups/itay_mayrose/annarice/model_adequacy/sanity/Acer/CONST_RATE/adequacy_test/
tree = args.tree
model = args.model_name
sims_per_tree = int(args.sims_per_tree)
CE_path = args.CE_path
genus = args.genus

def create_CE_control(CE_control_file,out_dir,data_file,tree_file, model):
	with open(CE_control_file, "w+") as control_file:
		print ("_mainType Optimize_Model", file = control_file)
		print("_outDir " + out_dir, file = control_file) # adequacy_QA dir
		print("_dataFile " + data_file, file = control_file) # simulated data
		print("_treeFile " + tree_file, file = control_file) # use original tree
		print("_logFile log.txt", file = control_file)
		print("_maxChrNum -10", file = control_file)
		print("_minChrNum -1", file = control_file)
		print("_branchMul 999", file = control_file)
		print("_simulationsNum 1000", file = control_file)
		print("_logValue 6", file = control_file)
		print("_maxOptimizationIterations 5", file = control_file)
		print("_epsilonLLimprovement 0.01", file = control_file)
		print("_optimizePointsNum 10,2,1", file = control_file)
		print("_optimizeIterNum 0,1,3", file = control_file)
		print("_gainConstR 1", file = control_file)
		print("_lossConstR 1", file = control_file)

		if model == "CONST_RATE_DEMI":
			print("_duplConstR 1", file = control_file)
			print("_demiPloidyR -2", file = control_file)
		if model == "CONST_RATE_DEMI_EST":
			print("_duplConstR 1", file = control_file)
			print("_demiPloidyR 1", file = control_file)
		if model == "CONST_RATE":
			print("_duplConstR 1", file = control_file)
		if model == "BASE_NUM":
			print("_baseNumberR 1", file = control_file)
			counts = get_counts(data_file)
			print("_baseNumber " + str(max(3,min(counts))), file = control_file)
			print("_bOptBaseNumber 1", file = control_file)
		if model == "BASE_NUM_DUPL":
			print("_duplConstR 1", file = control_file)
			print("_baseNumberR 1", file = control_file)
			counts = get_counts(data_file)
			print("_baseNumber " + str(max(3,min(counts))), file = control_file)
			print("_bOptBaseNumber 1", file = control_file)

# CE_control_file,out_dir,data_file,tree_file, model
if __name__ == '__main__':
	i = sims_per_tree
	output_dir = main_res_dir + str(i) + "/" + model + "/"
	if not os.path.exists(output_dir):
		res = os.system("mkdir -p " + output_dir)
	counts = main_res_dir + str(i) + "/" + "counts.txt"
	new_counts = main_res_dir + str(i) + "/" + "counts.txt"
	create_CE_control(output_dir + model + ".params",output_dir,counts,tree,model)
	os.system('"' + CE_path + '" ' + output_dir + model + ".params")
