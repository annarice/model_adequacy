import os
import gzip, tarfile
import shutil
from utils import *

l = []
for i in range(1000):
	l.append(str(i))

lst = ["Aloe","Phacelia","Lupinus","Hypochaeris","Brassica","Pectis","Crepis","Hordeum"]
d = model_per_genus()


for genus in lst:
	model = d.get(genus)
	untargz("/groups/itay_mayrose/annarice/model_adequacy/genera/" + genus + "/" + model + "/adequacy_test/zipped.tar.gz")
	for i in range(50):
		dest_dir = "/groups/itay_mayrose/annarice/model_adequacy/sanity/" + genus + "/" + model + "/adequacy_test/" + str(i) + "/"
		if not os.path.exists(dest_dir):
			res = os.system("mkdir -p " + dest_dir)  # -p allows recusive mkdir in case one of the upper directories doesn't exist
		counts_source = "/groups/itay_mayrose/annarice/model_adequacy/genera/" + genus + "/" + model + "/adequacy_test/" + str(i) + "/simCounts.txt"
		counts_dest = dest_dir + "counts.txt"
		os.system("cp -rf " + counts_source + " " + counts_dest)
	dest_genus = "/groups/itay_mayrose/annarice/model_adequacy/sanity/" + genus + "/"
	if not os.path.exists(dest_genus):
		res = os.system("mkdir -p " + dest_genus)
	tree_source = "/groups/itay_mayrose/annarice/model_adequacy/genera/" + genus + "/tree_1"
	tree_dest = "/groups/itay_mayrose/annarice/model_adequacy/sanity/" + genus + "/tree_1"
	os.system("cp -rf " + tree_source + " " + tree_dest)
	#targz_dir(out_dir, l, "zipped.tar.gz", True)
	targz_dir("/groups/itay_mayrose/annarice/model_adequacy/genera/" + genus + "/" + model + "/adequacy_test/", l, "zipped.tar.gz", True)