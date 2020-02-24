import os
from utils import *
from defs import *
from data_processing import process_data
from data_processing import best_model
from data_processing import simulations
from analysis import get_stats
from analysis import test_adequacy


if __name__ == '__main__':
	id, main_res_dir, in_model, num_of_trees, sims_per_tree, CE_path, params_from_user, counts_file, sanity_flag, results_flag = get_arguments()
	m = len(in_model)
	for k in range(m): # run over all models or a single model
		model = in_model[k]
		if sanity_flag == 1:
			main_res_dir = main_res_dir + model
		output_dir = main_res_dir + "/adequacy_test/"
		for i in range(num_of_trees):
			if not os.path.exists(output_dir):
				res = os.system("mkdir -p " + output_dir)  # -p allows recusive mkdir in case one of the upper directories doesn't exist
				original_counts = process_data.get_counts(counts_file, main_res_dir)
			if original_counts is None: # no counts variability, do not apply model adequacy
				exit()
			process_data.match_counts_to_tree(main_res_dir + mlAncTree, main_res_dir)
			original_counts_statistics = get_stats.calculate_statistics(original_counts, output_dir + "orig_stats",
																		main_res_dir + tree_with_counts)
			max_for_simulations = simulations.run_MA(main_res_dir, output_dir + sim_control, main_res_dir,
													 output_dir, original_counts, model, sims_per_tree,
													 main_res_dir + tree_wo_counts, CE_path)
			adequacy_lst = test_adequacy.model_adequacy(output_dir, original_counts_statistics, model,
														max_for_simulations, sims_per_tree, id, main_res_dir)