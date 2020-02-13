###################################################################################################
#################################### REMOVE FOLDERS MASSIVELY #####################################
###################################################################################################

import os
import argparse
import gzip, tarfile
import shutil

def get_best_model(filename):
    data = pd.read_csv(filename, sep="\t", header=None)
    tmp = data.loc[data[3] == 0,0].values[0]
    return tmp # the name of the best model

def targz_dir(outer_dir, dirs_list, dest_zip_filename, delete_after_zipping):
	cwd = os.getcwd()
	os.chdir(outer_dir)
	tarw = tarfile.open(dest_zip_filename, "w:gz")
	for dirname in dirs_list:
		if os.path.exists(dirname):
			tarw.add(dirname)
	tarw.close()
	if delete_after_zipping:
		for dirname in dirs_list:
			try:
				shutil.rmtree(dirname)
			except:
				pass
	os.chdir(cwd)


### ARGS
parser = argparse.ArgumentParser(description="zip model adequacy simulations that were already produced")
parser.add_argument('--out_dir', '-o', help='Outer dir',required=True)

args = parser.parse_args()
out_dir = args.out_dir

l = []
for i in range(1000):
	l.append(str(i))

try:
	targz_dir(out_dir,l,"zipped.tar.gz",True)
except:
	pass
