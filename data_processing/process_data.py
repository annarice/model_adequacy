import sys
sys.path.append("../")
from defs import *
from utils import *

def match_counts_to_tree(tree_file,dir):
    '''
    Receives the mlAncTree file which has in its tips names + counts.
    Receives the main_res_dir to which the new trees and counts will be written
    :param tree_file:
    :return:(1) tree_wo_counts without X taxa and without counts in their tip names
            (2) tree_with_counts without X taxa and with counts in the tips
    '''
    t = Tree(tree_file, format=1)
    tips_to_prune = []
    all_tips = []
    for leaf in t:
        all_tips.append(leaf.name)
        name_with_x = re.search(".*\-X", leaf.name)
        if name_with_x:
            tips_to_prune.append(leaf.name)
    t.prune(list(set(all_tips) - set(tips_to_prune)))
    t.write(format=1, outfile=dir + tree_with_counts)


    for leaf in t:
        name = re.search("(.*)\-[\d]", leaf.name)
        leaf.name = name.group(1)
    t.write(format=6, outfile=dir + tree_wo_counts) # write with branch lengths

def match_counts_to_tree2(tree_file,counts,new_counts,new_tree):
# recieve tree_1 and counts and
    t = Tree(tree_file, format=1)
    tree_flag = 0
    to_be_pruned = []
    tips = []
    tips_orig = []
    for leaf in t:
        name = re.search("(.*)\-[\dX]", leaf.name)
        tip = name.group(1)
        tips.append(tip)
        tips_orig.append(leaf.name)
    tmp = {}
    with open(counts, "r") as counts_file:
        for line in counts_file:
            line = line.strip()
            if line.startswith('>'):
                name = line[1:]
            else:
                if line != "x":
                    tmp[name] = int(line)
                else:
                    to_be_pruned.append(name)
                    tree_flag = 1
    to_be_pruned = [x + "-X" for x in to_be_pruned]
    with open(new_counts, "w+") as handle:
        for key in tmp:
            if key in tips:  # count on the tree
                handle.write(">" + key + "\n")
                handle.write(str(tmp.get(key)) + "\n")
    if tree_flag == 1:  # the tree was pruned - re-write it
        t.prune(list(set(tips_orig) - set(to_be_pruned)))
        t.write(format=1, outfile=new_tree)
    else:
        t.write(format=1, outfile=new_tree)

def handle_tree(tree_file,tip_to_prune):
    '''
    currently not in use.
    :param tree_file:
    :param tip_to_prune:
    :return:
    '''
    t = Tree(tree_file, format=1)
    tips = [leaf.name for leaf in t]
    t.prune(list(set(tips) - set([tip_to_prune])))
    t.write(format=1, outfile=tree_file)


def get_counts(filename,main_res_dir):
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
    if len(set(counts))== 1: # no counts variability, do not apply MA
        open(main_res_dir + "/NO_NEED_FOR_MA", 'a').close()
        return (None)
    return (counts)