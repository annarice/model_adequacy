# from the stats_dist_sims take the Xth 100 sims in each statistics and calculate their percentiles
# calculate the epsilon from the real percentiles -- get two vecs of epsilons an plot them against the nsims

import numpy as np

genera = ["Acer","Justicia","Sambucus"]
genera = ["Annona"]
for genus in genera:
	i = "1"
	if genus=="Justicia":
		i = "7"
	i = "0" # for other genera
	filename = "/groups/itay_mayrose/annarice/model_adequacy/sanity/" + genus + "/CONST_RATE/adequacy_test/" + i + "/CONST_RATE/adequacy_test_10000/stats_dist_sims"
	with open(filename,"r") as dist_sims:
		res = dist_sims.read()
		res = res.split("\n")
	filename = "/groups/itay_mayrose/annarice/model_adequacy/sanity/" + genus + "/CONST_RATE/adequacy_test/" + i + "/CONST_RATE/adequacy_test_10000/percentiles_CONST_RATE"
	with open(filename, "r") as original_percentiles:
		all_orig_perc = original_percentiles.read()
		all_orig_perc = all_orig_perc.split("\n")
	for j in range(4): # for each statistic
		lst = res[j][1:-1].split(",")
		lst = [float(x) for x in lst]
		orig_perc = all_orig_perc[j].split(",")
		orig_perc = [float(x) for x in orig_perc]
		res_upper = []
		res_lower = []
		print("orig_perc_upper " + str(orig_perc[1]))
		print("orig_perc_lower " + str(orig_perc[0]))
		print(genus)
		for n in range(0, len(lst), 100):
			print("0" + "-" + str(n+99))
			dist = lst[0:n+100]
			stat_star_upper = round(np.percentile(dist, 97.5),4)  # calculate the upper limit
			stat_star_lower = round(np.percentile(dist, 2.5),4)  # calculate the lower limit
			print(str(stat_star_lower) + "," + str(stat_star_upper))
			res_upper.append(round(stat_star_upper-orig_perc[1],4))
			res_lower.append(round(stat_star_lower - orig_perc[0],4))
		print(res_upper)
		print(res_lower)
