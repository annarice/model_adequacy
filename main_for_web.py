import os
from utils import *
from defs import *
from data_processing import process_data
from data_processing import best_model
from data_processing import simulations
from analysis import get_stats
from analysis import test_adequacy


if __name__ == '__main__':
	id, main_res_dir, in_model, num_of_trees, sims_per_tree, CE_path, params_from_user, counts_file, tree_full_path, sanity_flag,results_flag = get_arguments()
	CE_res_filename, expectation_file, mlAncTree, root_freq_filename, sim_control, statistics_names = fixed_vars()
	m = len(in_model)
	for k in range(m): # run over all models or a single model
		model = in_model[k]
		if sanity_flag == 1:
			main_res_dir = main_res_dir + model
		output_dir = main_res_dir + "/adequacy_test/"
		for i in range(num_of_trees):
			if not os.path.exists(output_dir):
				res = os.system("mkdir -p " + output_dir)  # -p allows recusive mkdir in case one of the upper directories doesn't exist
			original_counts = process_data.get_counts(counts_file)
			if len(set(original_counts))==1: # no variety in counts file - similar counts - no need for model adequacy
				open(output_dir + "NO_NEED_FOR_MA", 'a').close()
				exit()
			original_counts_statistics = get_stats.calculate_statistics(original_counts, output_dir + "orig_stats",main_res_dir + mlAncTree)
			max_for_simulations = simulations.run_MA(main_res_dir, output_dir + sim_control, main_res_dir,
														 output_dir, original_counts, model, sims_per_tree,
														 tree_full_path, CE_path)
			adequacy_lst = test_adequacy.model_adequacy(output_dir, original_counts_statistics, model,
															max_for_simulations, sims_per_tree, id, main_res_dir)