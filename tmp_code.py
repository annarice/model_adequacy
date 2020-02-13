# python /groups/itay_mayrose/annarice/model_adequacy/code/tmp_code.py /groups/itay_mayrose/annarice/model_adequacy/ce_trial counts

# params: (1) working_dir (2) genus (3) n
# simulate data under the best model and its inferred parameters
# get statistics on simulated data
# get distribution of statistics of simulated data (null distribution)
# In case the real value of the summary statistic significantly deviates from the null distribution, the model is deemed inadequate for the data at hand.

import os
import numpy as np
import scipy.stats as sc
import pandas as pd
from scipy.spatial.distance import mahalanobis
import regex as re


def get_counts(filename):
    with open(filename, "r") as counts_file:
        counts_lst = []
        for line in counts_file:
            line = line.strip()
            if line.startswith('>'):
                continue
            else:
                counts_lst.append(int(line))
    return (counts_lst)

def get_anc_counts(filename):
    with open(filename, "r") as counts_file:
        for line in counts_file:
            line = line.strip()
            counts_lst = re.findall("\-(\d+)[\]:]",line) # number after - and before : shold return list



def create_cnt_stats(counts_lst):
    l = len(counts_lst)  # length
    v = np.var(counts_lst)  # variance
    mi = min(counts_lst)
    ma = max(counts_lst)
    # enthropy, calculates the probabilities
    d = {}
    for i in counts_lst:
        d[i] = counts_lst.count(i)
    prob_lst = [x / len(counts_lst) for x in list(d.values())]
    e = sc.entropy(prob_lst)
    return ([l, v, mi, ma, e])

def get_events_numbers(simEventsFile):
    events_lst = []
    for line in open(simEventsFile):
        rec = line.strip()
        if rec.startswith('Total'): # gain, loss, duplication, demi-duplication, base number transitions, transitions to max
            match = re.search("(\d+)")
            events_lst.append(match.group(1))
    return (events_lst)



def get_best_model(filename):
        with open (filename,"r") as models_summary:
                data = pd.read_table(models_summary,header=None)
                best_model_row = data.loc[data[3] == 0,0] # best model, the one with deltaAIC = 0
        return (best_model_row)
        
def handle_sim_datasets(dir1,n): # dir1 = simulations dir, n = simulations number,
        '''
        for each simulated dataset call create_cnt_stats and store the results in a list (list of lists)
        '''
        lst_of_sim_stats = []
        for i in range(n):
                sim_cnts = get_counts(str(i)+"/simCounts.txt")
                tmp = create_cnt_stats(sim_cnts)
                lst_of_sim_stats.append(tmp)
        return lst_of_sim_stats

def test_adequacy (sim_stats,stats):
        ''' go over each statistic in the list and see if is adequate'''
        adequacy_lst = []
        for i in range(len(stats)):
                sim_stat_dist = [x[i] for x in sim_stats] # simulated ith distribution, x the item in each simulated list
                stat_star_upper = np.percentile(sim_stat_dist,97.5) # calculate the upper limit
                stat_star_lower = np.percentile(sim_stat_dist,2.5) # calculate the lower limit
                model = 0
                if stats[i]<=stat_star_upper and stats[i]>=stat_star_lower:
                        model = 1
                adequacy_lst.append(model)
        return adequacy_lst


if __name__ == '__main__':

    working_dir = "D:/Dropbox/MyDocs/lab/model_adequacy"
    genus = "Vernonanthura"
    #file1 = "/chromevol_out/infer/infer_tree_1/result_sum" # ---> best model + model parameters
    #file2 = "/chromevol_out/infer/infer_tree_1/simulation/param_sim_1" # ---> simulation control file
    dir1 = "chromevol_out/infer/infer_tree_1/simulation/dir_sim_1" # ---> where the simulations are
    n = 10 # number of simulations
    statistics = ["length","variance","min","max","entropy"]

    os.chdir(working_dir)
    extant_counts = get_counts(genus + ".counts_edit") # extant_counts is a numeric list containing all extant counts (tip counts) as provided from the user
    all_counts = get_anc_counts("mlAncestors.tree") # all_counts retrieves all counts of the tree, including the internal nodes

    stats = create_cnt_stats(extant_counts) # get statistics on real data (empirical)
    # best_model_row = get_best_model(file1) # get the best model and its optimized parameters
    os.chdir(dir1)
    sim_stats = handle_sim_datasets(dir1,n) # read simulated datasets
    results = test_adequacy(sim_stats,stats)

    for i in range(len(results)):
            if results[i]==0:
                    print ("Model not adequate for " + statistics[i])
                    #print ([x[i] for x in sim_stats])
                    #print(stats[i])
    if all(x==1 for x in results):
            print ("Model is adequate for all statistics")




    '''
    def create_CE_control_file(filename,params_names,params):
        d = {}
        for i in range(len(params_names)):
            d[params_names[i]] = params[i]
        with open (filename,"r") as control_file:
            for key in d:
                ##if  # regex, if numeric value, print as number and not str --- why?? 
                control_file.write(key,d[key])                      
    '''


