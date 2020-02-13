import gzip, tarfile
import os
import shutil
import pandas as pd
import re
from ete3 import Tree
from data_processing import process_data

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

def untargz(zip_file_dest, delete_after_extracting=False):
	"""
	:param filepath_pattern: the names of the files to validate existence. The blanks are in {}
	:return: the filepath of a concatenated file for all
	"""
	dirpath, zip_filename = os.path.split(zip_file_dest)
	cwd = os.getcwd()
	os.chdir(dirpath)
	tarx = tarfile.open(zip_file_dest, "r:gz")
	tarx.extractall(dirpath)
	tarx.close()
	os.chdir(cwd)
	if delete_after_extracting:
		os.remove(zip_file_dest)

def get_best_model(filename):
    data = pd.read_csv(filename, sep="\t", header=None)
    tmp = data.loc[data[3] == 0,0].values[0]
    return tmp # the name of the best model

def average(lst):
    return sum(lst) / len(lst)

def get_counts(filename):
    '''
        reads the .counts_edit file and extracts the counts
    :param filename: supplied by the user
    :return: list of counts
    '''
    with open(filename, "r") as tmp_counts_file:
        counts = []
        for line in tmp_counts_file:
            line = line.strip()
            if line.startswith('>'):
                continue
            else:
                if line=="x":
                    continue
                counts.append(int(line))
    return (counts)

def model_per_genus():
	d = {"Aloe": "CONST_RATE", "Phacelia": "CONST_RATE", "Lupinus": "CONST_RATE_NO_DUPL","Hypochaeris": "CONST_RATE_NO_DUPL",
	     "Crepis": "BASE_NUM_DUPL", "Pectis": "BASE_NUM", "Chlorophytum": "BASE_NUM_DUPL", "Achillea": "BASE_NUM","Stachys": "BASE_NUM_DUPL", "Eryngium": "BASE_NUM_DUPL",
	     "Brassica": "BASE_NUM", "Hordeum": "BASE_NUM_DUPL", "Curcuma": "BASE_NUM", "Pilosella": "BASE_NUM_DUPL"}
	return(d)

def get_adequacy_from_vec(filename):
	with open(filename, "r") as adequacy_f:
		tmp = adequacy_f.readline()
		if re.search("0", tmp):
			return(0)
		else:
			return(1)

def str_to_lst(str,type_flag):
	str = str.strip()
	if str[0]=="[":
		str = str[1:-1]
	if type_flag == "int":
		lst = list(map(int, str.split(",")))
	if type_flag == "float":
		lst = list(map(float, str.split(",")))
	return(lst)