import numpy as np
import scipy.stats as sc
import re
from utils import *
from defs import *
import csv


def initialize_parameters():
    d = {}
    for item in params_for_summary:
        d[item] = 0
    return d


genera = ["Aloe", "Phacelia", "Lupinus", "Hypochaeris", "Brassica", "Pectis", "Hordeum", "Crepis"]
models = ["CONST_RATE","CONST_RATE_NO_DUPL","BASE_NUM","BASE_NUM_DUPL"]
params_for_summary = ["_lossConstR", "_gainConstR", "_duplConstR", "_demiPloidyR", "_baseNumber", "_baseNumberR","_maxBaseTransition"]
header = ["Simulated_under", "model2", "nsim", "genus", "variance", "entropy", "range", "unique_counts", "fitch", "time",
          "loss", "gain", "dupl", "demi", "base", "baseR", "max_trans", "sum_all","sum"]
home_dir = "/groups/itay_mayrose/annarice/model_adequacy/sanity/"
out_file = home_dir + "sanity_summarize_tree_two_runs_trial.csv"

models_d = model_per_genus()

with open(out_file , "w+") as writeFile:
    writer = csv.writer(writeFile)
    writer.writerow(header)
    for genus in genera:
        model1 = models_d.get(genus)
        for i in range(100):
            for model2 in models:
                row = [model1, model2, str(i), genus]
                general_path = "/".join([home_dir,genus,model1,"adequacy_test",str(i),model2,"adequacy_test"])
                sanity_results = general_path + adequacy_vector
                if os.path.exists(sanity_results):
                    with open(sanity_results, "r") as ma:
                        res = ma.read()
                    res = str_to_lst(res, "int")
                    row.extend(res)
                    sum_all = sum(res)
                    sum_partial = res[0] + res[1] + res[4] + res[5]

                    d = initialize_parameters()  # get param names according to the current model
                    params_file = general_path + sim_control
                    params_dict_from_file = return_parameters_dict(params_file)
                    for item in params_for_summary:
                        if item in params_dict_from_file.keys():
                            d[item] = params_dict_from_file[item]
                        row.append(d[item])
                    row.extend([sum_all, sum_partial])
                    writer.writerow(row)
                else:
                    print(genus, str(i), model2, " is missing")
                    continue
